# DFLER: Drone Flight Log Entity Extractor

DFLER is an automation tool to perform named entity recognition in drone flight log files, specifically flight logs that are acquired from controller devices which contain human-readable messages. We use our own annotated dataset to fine-tune a BERT-base model to build a NER model to support this tool.

DFLER has three core features i.e., forensic timeline construction, entity recognition and forensic report generation. The needed input are flight log files that can be acquired from controller devices such as Android-based or iOS-based smartphone.

## Files Structure

Here is the folder structure of DFLER. There will be more files in `flight_logs` and `sample_output` folder, as we prepared a number of decrypted flight log files for input.

```
.
├── flight_logs                 # Source evidence for input
│   ├── android                 # Compiled files (alternatively `dist`)
│   ├── ios                     # Compiled files (alternatively `dist`)
├── model                       # To store the NER model
├── outputs
│   ├── 20221128_201545         # Generated folder to store output files
├── sample_output               # Sample output of a successful execution.
│   ├── parsed                  # Parsed message found in flight log
├── .gitignore
├── config.json                 # Some configuration parameter
├── dfler.py                    # Main file to run
├── generate_report.py          # Function to generate the forensic report
├── LICENSE
├── parse.py                    # Function to parse the flight log message
├── README.md
└── requirements.txt            # List of dependency packages
```

## How to run

Before starting the tool, make sure all the dependencies listed in **requirements.txt** are installed. To convert the generated HTML report file into PDF, we use the [`wkhtmltopdf`](https://wkhtmltopdf.org/downloads.html/) engine. Therefore, make sure to install the engine first, and set the executable path in the `config.json` file accordingly. Usually, the executable path is in `C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe` path. While for a Linux-based system like Ubuntu, it is stored in `/usr/bin/wkhtmltopdf` folder by default.

We have provided several flight log files that we extracted from Android- and iOS-based controller devices of VTO Labs drone forensic image [dataset](https://www.vtolabs.com/drone-forensics/) for samples. To perform named entity recognition, we need the fine-tuned BERT model. The mode is hosted on a public Huggingface repository. Clone the repository by issuing the command:

> git lfs install
> git clone https://huggingface.co/swardiantara/droner

After finish downloading the model, copy the model file (`pytorch_model.bin`) to the **`model`** folder.
Having all the dependency packages, engine, model and input files prepared, simply run the command `python dfler.py` to run the tools. The results of every step will be saved into **`/outputs/yyyymmdd_HHMMSS`** folder.

> **Note:** Run the step sequentially to avoid error, because every step is depending on the previous step.

## Sample Output

We provide a sample of output if all steps are running successfully. There will be several files resulted as listed in `sample_output` folder. The final output report file contains a forensic report along with an attached highlighted forensic timeline that is constructed from several flight log files. The highlighted timeline is expected to be able to support the forensic investigator in pinpointing mentioned entities.
We have tested the tool both on Windows and Ubuntu Operating System. The tool is running smoothly, except for the generated PDF file, which resulting in a slightly different file.
