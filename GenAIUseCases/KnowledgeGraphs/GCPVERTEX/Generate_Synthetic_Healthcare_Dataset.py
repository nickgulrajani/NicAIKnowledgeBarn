import random
from datetime import datetime, timedelta
import pandas as pd
import os

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Sample data generation for healthcare records, modeled similarly to the bank.csv structure
# We will generate 1000 rows of sample patient healthcare data

# Define sample data categories
genders = ['male', 'female']
marital_statuses = ['single', 'married', 'divorced', 'widowed']
education_levels = ['primary', 'secondary', 'tertiary']
chronic_conditions_list = ['none', 'diabetes', 'hypertension', 'asthma', 'heart disease']
allergies_list = ['none', 'penicillin', 'pollen', 'peanuts', 'dust']
facilities = ["Emergency Room", "Inpatient Ward", "Outpatient Clinic", "Radiology", "Laboratory"]
procedures = ["Blood Test", "X-Ray", "MRI", "CT Scan", "Ultrasound", "Surgery"]
diagnoses = ["healthy", "mild condition", "moderate condition", "severe condition"]
outcomes = ["improved", "stable", "worsened"]

# Generate 1000 rows of sample data
healthcare_data = []

for i in range(1000):
    age = random.randint(18, 85)
    gender = random.choice(genders)
    marital_status = random.choice(marital_statuses)
    education_level = random.choice(education_levels)
    chronic_conditions = random.choice(chronic_conditions_list)
    allergies = random.choice(allergies_list)
    current_medications = random.choice(["none", "aspirin", "insulin", "blood pressure medication", "antidepressants"])
    visit_date = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31)).strftime("%Y-%m-%d")
    facility = random.choice(facilities)
    procedure = random.choice(procedures)
    diagnosis = random.choice(diagnoses)
    medication_prescribed = random.choice(["none", "antibiotic", "pain reliever", "antihypertensive"])
    number_of_visits = random.randint(1, 10)
    readmission = random.randint(0, 1)
    outcome = random.choice(outcomes)
    
    # Add generated record to the list
    healthcare_data.append({
        "age": age,
        "gender": gender,
        "marital_status": marital_status,
        "education_level": education_level,
        "chronic_conditions": chronic_conditions,
        "allergies": allergies,
        "current_medications": current_medications,
        "visit_date": visit_date,
        "facility": facility,
        "procedure": procedure,
        "diagnosis": diagnosis,
        "medication_prescribed": medication_prescribed,
        "number_of_visits": number_of_visits,
        "readmission": readmission,
        "outcome": outcome
    })

# Convert to DataFrame
healthcare_df = pd.DataFrame(healthcare_data)

# Specify the file path to a valid directory on your machine
cleaned_csv_file_path = "/Users/nichgul/Downloads/cleaned_healthcare_data.csv"

# Check if the directory exists
directory = os.path.dirname(cleaned_csv_file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
else:
    print(f"Directory exists. Saving data to {cleaned_csv_file_path}...")

    # Attempt to save the file
    try:
        healthcare_df.to_csv(cleaned_csv_file_path, index=False)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Display the first few rows of the generated data for validation
print(healthcare_df.head())
