## Author

This project was developed by Nicholas Gulrajani
 
# Healthcare Readmission Prediction Using Neo4j and Vertex AI

This project implements a predictive model to identify patients at risk of hospital readmission. The solution leverages data stored in a Neo4j knowledge graph and builds a predictive model using `scikit-learn`. The trained model is deployed on Google Cloud Vertex AI for scalable inference.

## Overview

Hospital readmissions can be costly and negatively impact patient outcomes. This project uses historical patient data, including information about visits, procedures, medications, and healthcare professionals, to predict whether a patient will be readmitted to the hospital. 

The pipeline includes:
1. Data extraction from a Neo4j knowledge graph.
2. Feature engineering and preprocessing.
3. Model training and evaluation using Logistic Regression.
4. Deployment of the trained model on Google Vertex AI for real-time predictions.
5. Model inference and proactive interventions based on predictions.

## Prerequisites

Before running the code, ensure that the following are set up:

1. **Google Cloud Project**:
   - Enable the Vertex AI API.
   - Set up Google Cloud SDK and authenticate with your GCP account.
   - Ensure you have a Google Cloud Storage bucket for storing the model.

2. **Neo4j Database**:
   - Ensure a Neo4j instance is running, and you have loaded patient data into it.
   - Update the connection credentials in the code to connect to your Neo4j instance.

3. **Python Environment**:
   - Install the required Python packages:
     ```bash
     pip install google-cloud-aiplatform py2neo pandas scikit-learn joblib
     ```

4. **Service Account Permissions**:
   - The service account running this script should have the following roles:
     - `Vertex AI Admin`
     - `Storage Object Viewer`
     - `Storage Admin`

## Project Setup

### 1. Environment Variables
Set the following environment variables in your Python environment:

- `PROJECT_ID`: Your Google Cloud project ID.
- `REGION`: The region where Vertex AI and other resources are located (e.g., `us-central1`).
- `BUCKET_NAME`: The Google Cloud Storage bucket name where the model will be stored.
- `MODEL_DIRECTORY`: The directory path in the GCS bucket where the model will be uploaded.

### 2. Neo4j Database Connection
Update the following line in the code with your Neo4j database credentials:

```python
graph = Graph("bolt://localhost:7687", auth=("neo4j", "<your-password>"))

