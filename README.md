# Data Engineering for Health Tech Startup

## Keywords
- Data Engineering
- Data Pipeline
- Document AI
- Data Transformation
- MongoDB to BigQuery
- Business Analytics

## Abstract
This project was part of an engagement with a health tech startup that needed to digitize a large volume of handwritten forms and migrate their MongoDB data to Google Cloud for analytics. The project used Google Cloud Document AI to parse handwritten medical forms, Python scripts for data ingestion into BigQuery, and a data pipeline leveraging Pub/Sub to transfer MongoDB data to BigQuery. Visualizations were created in Looker to assist in making data-driven decisions.

## Table of Contents
- [Introduction](#introduction)
- [Data Engineering](#data-engineering)
  - [Document Parsing](#document-parsing)
  - [MongoDB to BigQuery Pipeline](#mongodb-to-bigquery-pipeline)
  - [Data Collection Strategy](#data-collection-strategy)
  - [Data Transformation](#data-transformation)
  - [Data Loading](#data-loading)
  - [Data Quality](#data-quality)
- [Data Visualization](#data-visualization)
- [Site Reliability Engineering](#site-reliability-engineering)
  - [Code Integration](#code-integration)
  - [Deployment Procedures](#deployment-procedures)
  - [Operations Team Training and Adoption](#operations-team-training-and-adoption)
  - [Monitoring and Observability](#monitoring-and-observability)
- [Conclusion](#conclusion)

## Introduction
The health tech startup handles sensitive medical data through handwritten forms, making it difficult to process and analyze efficiently. In addition, they use MongoDB to manage data, but needed to migrate this to Google Cloud's BigQuery to integrate it into their analytics workflow. This project involved two main tasks: parsing handwritten forms with Document AI and building a real-time pipeline for MongoDB data ingestion into BigQuery.


![alt text](https://raw.githubusercontent.com/sumit6037/ride-service-gcp-pipeline/main/arch.png)

## Data Engineering

### Document Parsing
The startup had a significant backlog of handwritten forms that needed to be digitized. We used Google Cloud Document AI Form Parser to extract structured data from these forms. A Python script was developed to automate the parsing process, extracting key information like patient names, symptoms, and medical history. The parsed data was ingested into BigQuery for further processing and analysis.

### MongoDB to BigQuery Pipeline
To move data from MongoDB to BigQuery, we implemented a native Pub/Sub capability. Pub/Sub captured data changes from the MongoDB cluster, and a BigQuery subscription wrote the messages to a pre-configured table in real time. This pipeline ensured seamless data migration and integration for business analytics.

### Data Collection Strategy
For document parsing, the Python script automated form uploads to Document AI, processed the output, and stored structured data in BigQuery. The MongoDB data pipeline relied on Pub/Sub to ensure real-time data synchronization between the startup's on-prem MongoDB and BigQuery.

### Data Transformation
SQL transformations were applied in BigQuery to clean and structure the parsed data and MongoDB records, ensuring consistency in schema and format.

### Data Loading
Data was loaded into BigQuery via batch processes for handwritten forms, while MongoDB data was ingested continuously through Pub/Sub in near real-time.

### Data Quality
Data validation checks were applied to the parsed document data and the MongoDB pipeline. This included handling missing values, duplicates, and format discrepancies to ensure high-quality analytics.

## Data Visualization
Visualizations were created in Looker based on the data in BigQuery. These included dashboards showing trends in patient information, medical history patterns, and other critical metrics needed for business decisions.

## Site Reliability Engineering

### Code Integration
GitHub was used for version control and collaboration, with separate repositories for data processing scripts and LookML code.

### Deployment Procedures
The data pipelines and scripts were deployed using Cloud Scheduler and Pub/Sub. GitHub Actions automated code deployments and testing, ensuring continuous integration and delivery.

### Operations Team Training and Adoption
The operations team was provided with comprehensive documentation, including data model explanations and dashboard usage guides, to ensure they could leverage the system effectively.

### Monitoring and Observability
Google Cloud’s Monitoring and Logging services were set up to track the performance of the data pipelines, monitor Pub/Sub message delivery, and ensure smooth operations.

## Conclusion
This project empowered the startup to digitize handwritten forms and migrate their MongoDB data to BigQuery, providing an integrated view of their data. With real-time data access and insightful visualizations, the operations team could make timely, informed decisions, improving both efficiency and customer satisfaction.
