import os
from google.cloud import aiplatform
from treatment_plan_generator import initialize_vertexai, generate_treatment_plan

# Set your Google Cloud project ID and region
os.environ["GOOGLE_CLOUD_PROJECT"] = "aivertex-421013"  # Replace with your actual project ID
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nichgul/GENAI/KNOWLEDGEGRAPHS/USECASES/FRAUD_DETECTION/aivertex-421013-e00abc7415f6.json"  # Replace with your actual credentials file

def test_treatment_plan_generator():
    # Initialize Vertex AI
    initialize_vertexai(project_id=os.environ["GOOGLE_CLOUD_PROJECT"], location="us-central1")

    # Test cases
    test_cases = [
        {
            "patient_history": """
            Patient is a 35-year-old male with a recent diagnosis of type 1 diabetes. 
            No other significant medical history. Currently not on any medication.
            """,
            "similar_cases": """
            In similar cases of newly diagnosed type 1 diabetes in adults:
            - 90% were started on a basal-bolus insulin regimen
            - 10% were enrolled in clinical trials for immunotherapy
            All cases emphasized the importance of diabetes education and regular monitoring.
            """
        },
        {
            "patient_history": """
            Patient is a 60-year-old female with a history of hypertension and 
            osteoarthritis. Recent blood tests show elevated LDL cholesterol levels.
            Current medications include lisinopril and acetaminophen as needed.
            """,
            "similar_cases": """
            In similar cases of patients with hypertension and high cholesterol:
            - 70% responded well to a combination of statins and lifestyle changes
            - 20% required additional medication for blood pressure control
            - 10% were referred to a lipid specialist for advanced management
            Regular follow-ups and dietary counseling were crucial in all cases.
            """
        }
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("Patient History:", case["patient_history"])
        print("Similar Cases:", case["similar_cases"])
        
        treatment_plan = generate_treatment_plan(case["patient_history"], case["similar_cases"])
        
        print("\nGenerated Treatment Plan:")
        print(treatment_plan)
        print("\n" + "="*50)

if __name__ == "__main__":
    test_treatment_plan_generator()