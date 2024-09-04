Document AI Processing Solution
This project implements a document processing solution using Google Cloud's Document AI service. 

It's designed to digitize batch records and efficiently convert scanned PDFs into structured, analyzable data.
Features

Automated processing of PDF documents
Extraction of text content with confidence scores
Detailed breakdown of document structure (pages, blocks, paragraphs, lines)
Secure authentication using Google Cloud credentials
Logging for process monitoring and debugging

Prerequisites

Python 3.7 or higher
Google Cloud account with Document AI API enabled
Service account key with necessary permissions

Installation

Clone this repository:
git clone [repository-url]
cd [repository-name]

Install required packages:
pip install google-cloud-documentai google-auth

Set up Google Cloud credentials:

Download your service account key JSON file
Set the environment variable:
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"


Configuration
Update the following variables in the main() function:

project_id: Your Google Cloud project ID
location: The location of your Document AI processor (e.g., 'us')
processor_id: Your Document AI processor ID
file_path: Path to the PDF file you want to process
mime_type: MIME type of the file (default is 'application/pdf')

Usage
Run the script with:
Copypython document_processor.py
The script will process the specified document and output:

Extracted text from the entire document
Detailed analysis including text blocks, paragraphs, and lines with their confidence scores

Output
The script provides two levels of output:

Extracted text: The full text content extracted from the document.
Detailed document analysis: Breakdown of the document into:

Text Blocks: With text content, confidence score, and bounding box coordinates
Paragraphs: With text content and confidence score
Lines: With text content and confidence score



Logging
The script uses Python's logging module to provide informational and error messages. Logs are printed to the console with timestamps.
Error Handling
The script includes error handling for common issues such as:

Missing Google Cloud credentials
Non-existent Document AI processor
File reading errors
Document processing errors

Contributing
[Include instructions for how others can contribute to your project]
License
[Specify the license under which this project is released]
