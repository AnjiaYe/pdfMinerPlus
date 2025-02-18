from toolbox import update_ui, promote_file_to_downloadzone, gen_time_str 
from toolbox import CatchException, report_exception
from toolbox import write_history_to_file, promote_file_to_downloadzone
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from .crazy_utils import read_and_clean_pdf_text
from .crazy_utils import input_clipping

import re  # Import regex module
import json  # Import JSON module
import fitz  # Import PyMuPDF to read PDF metadata


def extract_pdf_metadata(file_name):
    """Extract Title and Author metadata from the PDF file."""
    try:
        with fitz.open(file_name) as doc:
            metadata = doc.metadata
            pdf_title = metadata.get('title', 'NA')
            pdf_author = metadata.get('author', 'NA')
            # Handle empty strings
            if not pdf_title:
                pdf_title = 'NA'
            if not pdf_author:
                pdf_author = 'NA'
            return pdf_title, pdf_author
    except Exception as e:
        print(f"Error extracting metadata from {file_name}: {e}")
        return 'NA', 'NA'


def pdfAnalyst(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    file_write_buffer = []
    for file_name in file_manifest:
        print('Begin analysis on:', file_name)
        
        try:
            # Extract PDF metadata
            pdf_title, pdf_author = extract_pdf_metadata(file_name)

            # Add error handling for PDF text extraction
            try:
                file_content, page_one = read_and_clean_pdf_text(file_name)
                if not file_content or not page_one:
                    raise ValueError(f"No content could be extracted from {file_name}")
                    
                file_content = file_content.encode('utf-8', 'ignore').decode()   
                page_one = str(page_one).encode('utf-8', 'ignore').decode()
                
            except Exception as e:
                error_msg = f"Error processing PDF {file_name}: {str(e)}"
                print(error_msg)
                chatbot.append((file_name, f"⚠️ {error_msg}"))
                yield from update_ui(chatbot=chatbot, history=history)
                continue

            # Process the content
            final_results = []
            iteration_results = [file_content]
            final_results.extend(iteration_results)
            final_results.append('Please respond with content above')

            # Handle advanced arguments
            if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""):
                plugin_kwargs.pop("advanced_arg")
                
            i_say = "Extract the following information from a research article above. Structure the extracted information as a JSON. Use NA if information is not found. JSON Fields:" + plugin_kwargs.get("advanced_arg", "")
            i_say, final_results = input_clipping(i_say, final_results, max_token_limit=32000)
            
            # Request GPT analysis with error handling
            try:
                gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                    inputs=i_say, 
                    inputs_show_user=file_name, 
                    llm_kwargs=llm_kwargs, 
                    chatbot=chatbot, 
                    history=final_results, 
                    sys_prompt="[Important]You need to respond in JSON format. Use NA if information is not found."
                )
                
                # Process GPT response
                if gpt_say and gpt_say.strip():
                    json_match = re.search(r'{.*}', gpt_say.strip(), re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        try:
                            # Step 3: Parse the existing JSON string
                            json_data = json.loads(json_str)
                            # Step 4: Add file_name and metadata fields to the JSON object
                            # Create a new ordered dictionary to maintain field order
                            from collections import OrderedDict
                            new_json_data = OrderedDict()
                            new_json_data['file_name'] = file_name
                            new_json_data['pdf_title'] = pdf_title
                            new_json_data['pdf_author'] = pdf_author
                            # Include the rest of the json_data fields
                            for key, value in json_data.items():
                                new_json_data[key] = value
                            # Step 5: Convert back to string format
                            gpt_say_modified = json.dumps(new_json_data, ensure_ascii=False, indent=2)
                            # Update gpt_say with the new JSON string
                            gpt_say = gpt_say_modified
                        except json.JSONDecodeError as e:
                            # If JSON parsing fails, log an error message
                            print(f"JSON decoding failed: {e}")
                    else:
                        print("No JSON object found in gpt_say.")
                else:
                    print("gpt_say is empty or whitespace only.")
                    
            except Exception as e:
                error_msg = f"Error analyzing PDF content {file_name}: {str(e)}"
                print(error_msg)
                chatbot.append((file_name, f"⚠️ {error_msg}"))
                yield from update_ui(chatbot=chatbot, history=history)
                continue
                
        except Exception as e:
            error_msg = f"Failed to process {file_name}: {str(e)}"
            print(error_msg)
            chatbot.append((file_name, f"⚠️ {error_msg}"))
            yield from update_ui(chatbot=chatbot, history=history)
            continue

        # Append the modified gpt_say to final_results and file_write_buffer
        final_results.append(gpt_say)
        file_write_buffer.append(gpt_say)

        _, final_results = input_clipping("", final_results, max_token_limit=32000)
        yield from update_ui(chatbot=chatbot, history=final_results)
    res = write_history_to_file(file_write_buffer)
    promote_file_to_downloadzone(res, chatbot=chatbot)


@CatchException
def pdfMinerPlus(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # Basic information: Functionality and contributor
    chatbot.append([
        "Instruction 3 citation",
        "https://doi.org/10.3390/fi16050167"])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh UI

    # Attempt to import dependencies; if missing, provide installation suggestion
    try:
        import fitz
    except:
        report_exception(chatbot, history, 
            a = f"Parsing project: {txt}", 
            b = f"Failed to import software dependencies. Using this module requires additional dependencies.")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh UI
        return

    # Clear history to prevent input overflow
    history = []

    # Check input parameters; exit if none provided
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "":
            txt = 'Empty input field'
        report_exception(chatbot, history,
                         a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh UI
        return

    # Search for files to process
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)] 
        
    # If no files found
    if len(file_manifest) == 0:
        report_exception(chatbot, history,
                         a=f"Parsing project: {txt}", b=f"Cannot find any .tex or .pdf files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh UI
        return

    # Begin processing
    yield from pdfAnalyst(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)