
# Document Processing with Google Cloud Document AI

## 1. Introduction

This Python script automates the processing of documents using Google Cloud's Document AI service. It extracts relevant data from these documents and uploads the extracted information to BigQuery for subsequent analysis.

### Key Components

- **Document Processing**: Leverages Google Cloud Document AI to analyze and extract structured data from documents stored in Google Cloud Storage. This involves using a pre-configured Document AI processor capable of handling various document types and formats.

- **Data Extraction**: Retrieves field names and values from the processed document, along with their confidence scores, to evaluate the accuracy of the extracted data.

- **Data Handling**: Converts the extracted data into a Pandas DataFrame, which is ideal for data manipulation and analysis in Python.

- **Data Ingestion**: Uploads the DataFrame to BigQuery, facilitating integration with other analytics tools and providing a platform for complex queries and data visualization.

### Workflow

1. **Download Document**: Retrieves a PDF file from Google Cloud Storage.
2. **Process Document**: Sends the document to Document AI for processing.
3. **Extract Data**: Extracts key fields and their confidence scores from the processed document.
4. **Create DataFrame**: Organizes the extracted data into a Pandas DataFrame.
5. **Upload Data**: Ingests the DataFrame into a BigQuery table for further analysis.

This script efficiently automates document processing, ensuring that data from scanned or digitized documents is accurately captured and readily accessible for business intelligence and analytics.

## 2. Setup and Requirements

Before running the script, ensure that you have completed the Document AI setup steps outlined in the Document AI OCR Codelab.

Please follow these steps:

1. **Start Cloud Shell**.
2. **Enable the Document AI API**.
3. **Install the Python Client Library**.
4. **Install Pandas**: Use the following command to install the Pandas library, a powerful tool for data analysis in Python:

    ```bash
    pip3 install --upgrade pandas
    ```

## 3. Create a Form Parser Processor

To use Document AI for this tutorial, you need to create a Form Parser processor instance:

1. Navigate to the Document AI Platform Overview in the Google Cloud Console.
2. Click **Create Processor** and select **Form Parser** from the available options.
3. Enter a processor name and select your region.
4. Click **Create** to set up the processor.
5. Copy the Processor ID, as you will need it in your code.

## 4. Extract Form Key/Value Pairs

In this step, you will use the online processing API to call the Form Parser processor you created. This will allow you to extract key-value pairs from the document.

- **Online Processing**: Suitable for processing a single document and receiving a response. For batch processing multiple files or handling large files, refer to the OCR Codelab for detailed instructions.

The process request code is the same across different processor types, differing only by Processor ID.

The Document AI response object provides a list of pages from the input document, with each page containing a list of form fields and their text locations.

The following code snippet demonstrates how to iterate through each page, extract key fields and values, and their confidence scores, structuring the data for storage in databases or other applications.

Create a file named `form_parser.py` and include the provided code.
