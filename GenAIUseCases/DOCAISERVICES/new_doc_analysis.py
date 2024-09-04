#Author: Nicholas Gulrajani

import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound
from google.oauth2 import service_account
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_processor(client, name):
    try:
        processor = client.get_processor(name=name)
        logging.info(f"Processor exists: {processor.name}")
        return True
    except NotFound:
        logging.error(f"Processor not found: {name}")
        return False
    except Exception as e:
        logging.error(f"Error verifying processor: {str(e)}")
        raise

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    logging.info(f"Processing document: {file_path}")
    logging.info(f"Project ID: {project_id}, Location: {location}, Processor ID: {processor_id}")

    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    logging.info(f"Loaded credentials for: {credentials.service_account_email}")

    # Instantiate a client
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(credentials=credentials, client_options=opts)

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)
    logging.info(f"Processor path: {name}")

    # Verify processor exists
    if not verify_processor(client, name):
        raise ValueError(f"Processor {processor_id} not found")

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Document AI raw document
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    try:
        result = client.process_document(request=request)
        return result.document
    except Exception as e:
        logging.error(f"Error processing document: {str(e)}")
        raise

def main():
    # Check if GOOGLE_APPLICATION_CREDENTIALS is set
    if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
        logging.error("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
        return

    project_id = ''
    location = 'us'
    processor_id = ''
    file_path = './medical_notes.pdf'
    mime_type = 'application/pdf'

    try:
        document = process_document(project_id, location, processor_id, file_path, mime_type)

        print("\nExtracted text:")
        print("=" * 50)
        print(document.text)
        print("=" * 50)

        print("\nDetailed document analysis:")
        print("=" * 50)
        for page_num, page in enumerate(document.pages, start=1):
            print(f"\nPage {page_num}:")
            print("-" * 30)
            
            print("Text Blocks:")
            for block_num, block in enumerate(page.blocks, start=1):
                print(f"Block {block_num}:")
                print(f"Text: {block.layout.text_anchor.content.strip()}")
                print(f"Confidence: {block.layout.confidence:.2f}")
                print(f"Bounding box: {block.layout.bounding_poly.normalized_vertices}")
                print("-" * 20)
            
            print("\nParagraphs:")
            for para_num, paragraph in enumerate(page.paragraphs, start=1):
                text = paragraph.layout.text_anchor.content.strip()
                confidence = paragraph.layout.confidence
                print(f"Paragraph {para_num}:")
                print(f"Text: {text}")
                print(f"Confidence: {confidence:.2f}")
                print("-" * 20)
            
            print("\nLines:")
            for line_num, line in enumerate(page.lines, start=1):
                text = line.layout.text_anchor.content.strip()
                confidence = line.layout.confidence
                print(f"Line {line_num}:")
                print(f"Text: {text}")
                print(f"Confidence: {confidence:.2f}")
                print("-" * 20)

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
