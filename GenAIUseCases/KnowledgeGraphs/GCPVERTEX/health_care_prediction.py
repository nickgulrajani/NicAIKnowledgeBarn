from google.cloud import aiplatform
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from py2neo import Graph
from sklearn.impute import SimpleImputer
import joblib
import os

# Project and location setup
PROJECT_ID = 'aivertex-421013'
REGION = 'us-central1'
BUCKET_NAME = 'model_bucket_storage'  # Your bucket name
MODEL_DIRECTORY = 'logistic_regression/'  # The directory in your bucket for the model
MODEL_FILENAME = 'model.pkl'  # or 'model.joblib', depending on the format you choose

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=REGION)

# Connect to Neo4j (update with your credentials)
graph = Graph("bolt://localhost:7687", auth=("neo4j", ""))

# Query to extract features for model training
query = """
MATCH (p:Patient)-[:HAS_EPISODE]->(e:EpisodeOfCare)-[:INCLUDES]->(v:Visit)
OPTIONAL MATCH (v)-[:INCLUDES]->(proc:Procedure)
OPTIONAL MATCH (v)-[:PRESCRIBES]->(med:Medication)
OPTIONAL MATCH (d:Doctor)-[:ATTENDS]->(v)
OPTIONAL MATCH (n:Nurse)-[:ASSISTS]->(v)
WITH p, e, 
     count(v) AS visit_count,
     size(collect(DISTINCT proc.name)) AS num_procedures,
     size(collect(DISTINCT med.name)) AS num_medications,
     size(collect(DISTINCT d.name)) AS num_doctors,
     size(collect(DISTINCT n.name)) AS num_nurses,
     duration.between(date(e.start_date), date(e.end_date)).days AS episode_duration
RETURN 
    p.name AS patient_name,
    coalesce(p.age, 0) AS patient_age,
    visit_count,
    num_procedures,
    num_medications,
    num_doctors,
    num_nurses,
    episode_duration
"""

# Fetch and convert to DataFrame
result = graph.run(query)
data = pd.DataFrame(result.data())

# Preprocessing
data['readmitted'] = data['episode_duration'].apply(lambda x: 1 if x > 20 else 0)  # Example logic

# Features and target
X = data[['patient_age', 'visit_count', 'num_procedures', 'num_medications', 'num_doctors', 'num_nurses', 'episode_duration']]
y = data['readmitted']

# Impute missing values (if any)
imputer = SimpleImputer(strategy='median')
X = imputer.fit_transform(X)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# Save the model locally with the correct filename ('model.pkl' or 'model.joblib')
joblib.dump(model, MODEL_FILENAME)

# Upload the model to Google Cloud Storage in the specified directory
artifact_uri = f"gs://{BUCKET_NAME}/{MODEL_DIRECTORY}"
os.system(f"gsutil cp {MODEL_FILENAME} {artifact_uri}")

# Upload the model to Vertex AI Model Registry using the directory
model = aiplatform.Model.upload(
    display_name="my-readmission-prediction-model",
    artifact_uri=artifact_uri,  # Pointing to the directory
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest",
)

# Create an endpoint for model deployment
endpoint = aiplatform.Endpoint.create(display_name="my-readmission-prediction-endpoint")

# Deploy the model to the endpoint
model.deploy(
    endpoint=endpoint,
    deployed_model_display_name='my-deployed-readmission-model',
    machine_type='n1-standard-4',
    min_replica_count=1,
    max_replica_count=1,
)

# Making predictions (example new data)
new_data = pd.DataFrame({
    'patient_age': [45, 60, 30],
    'visit_count': [3, 1, 5],
    'num_procedures': [2, 0, 4],
    'num_medications': [3, 1, 2],
    'num_doctors': [1, 2, 1],
    'num_nurses': [2, 3, 2],
    'episode_duration': [15, 25, 10]
})

predictions = endpoint.predict(instances=new_data.to_dict(orient='records'))
print(predictions)

# Cleanup: Remove the local model file if not needed anymore
if os.path.exists(MODEL_FILENAME):
    os.remove(MODEL_FILENAME)
