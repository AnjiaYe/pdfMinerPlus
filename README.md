# pdfMinerPlus 

Welcome to the pdfMinerPlus repository! This project focuses on developing an application for a Hybrid Semi-Automated Workflow for Systematic and Literature Review Processes with Large Language Model Analysis.

"Prompting is an art. You will likely need to try a few different approaches for your prompt if you don’t get your desired outcome the first time."
by [gemini-for-google-workspace-prompting-guide-101](https://inthecloud.withgoogle.com/gemini-for-google-workspace-prompt-guide/dl-cd.html)


## Citation

Please cite our [paper](https://www.mdpi.com/1999-5903/16/5/167)


## Use Cases

Test your prompts with articles today:

- [Microsoft Edge with built-in PDF reader and Copilot](https://microsoft.com/edge): This tool will help you get started by testing your prompt and easy to make changes. Utilize our identifier, verifier, and data field prompts to extract structured information from PDFs.
  Use instruction: "Act as a researcher, answer from this page. Structure the extracted information as a JSON. Use "NA" if information is not found. JSON Fields:"

 https://github.com/AnjiaYe/pdfMinerPlus/assets/162682573/f369a671-df0a-408c-b69b-ae582296b26f


- [AI Research Assistant](https://github.com/lifan0127/ai-research-assistant): Explore automated tools for literature review and analysis. 
  1. Install Zotero: [Zotero Download](https://www.zotero.org/download/). For a detailed walkthrough of the installation process, please check out: [Twitter Thread](https://twitter.com/MushtaqBilalPhD/status/1735221900584865904) (credit: Mushtaq Bilal, PhD - Syddansk Universitet).
  2. Download the latest release (.xpi file) from GitHub: [Latest Release](https://github.com/lifan0127/ai-research-assistant/releases/latest).
  3. In Zotero, select Tools from the top menu bar, and then click on Add-ons.
  4. On the Add-ons Manager panel, click the gear icon at the top right corner and select Install Add-on From File.
  5. Select the .xpi file you just downloaded and click Open, which will start the installation process.
  6. Quickstart
By default, Aria can be activated by clicking the button on Zoterol toolbar or through the "Shift + R" shortcut.
Before using Aria, you need to provide an OpenAI API Key. Follow the in-app instruction to add a key and restart Zotero. (screenshots)
After restart, you should see the activated Aria window (as shown above) and can start using it through conversations. 
Drag items to the conversation with your prompts to extract information. 
you can paste outputs to json editor https://jsoneditoronline.org/
You can save it to notes and export references to any other formats


- [Google AI Studio](https://aistudio.google.com): Use Gemini Pro 1.5 models within Google AI Studio for title/abstract screening.
  1. Retrieve title and abstract: For example, Endnote 21: Select reference - File - Export. Make sure you select following output style:
     
     ![image](https://github.com/AnjiaYe/pdfMinerPlus/assets/162682573/f3b0ac45-3faa-4617-b6c3-228f41e1e23c)
     
  2. Use Gemini Pro to extract data from abstracts: Create a new chat in [Google AI Studio](https://aistudio.google.com/app/prompts/new_chat). Use instruction:"Act as a researcher, extract the following information from context consist of titles and abstracts. Structure the extracted information as a JSON. Use "NA" if information is not found. JSON Fields:". Copy/Upload your txt file to the chat. You also need to use following settings for the LLM.
     
     ![image](https://github.com/AnjiaYe/pdfMinerPlus/assets/162682573/b5c57c87-fd31-4dd6-b4e9-2d1f03b4accd)
     
  3. Convert to CSV: Copy outputs to a [JSON editor](https://jsoneditoronline.org/). Save - Export to CSV - Save to disk.
     
  4. Use MS Excel to process data as described in our paper.
 

## Collaboration Opportunities

We are open to collaboration and welcome researchers interested in testing the prototype application. If you are interested in participating, please contact us directly at [anjia.ye@utas.edu.au](mailto:anjia.ye@utas.edu.au).

https://github.com/AnjiaYe/pdfMinerPlus/assets/162682573/3696b6c6-5d5e-449c-b361-7c593706d953


## What's Next 

We are actively working on developing a more user-friendly version for self hosting and public release. Stay tuned for updates! 

