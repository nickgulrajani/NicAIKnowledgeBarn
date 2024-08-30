import vertexai
from vertexai.language_models import TextGenerationModel

def initialize_vertexai(project_id: str, location: str):
    vertexai.init(project=project_id, location=location)

def generate_treatment_plan(patient_history: str, similar_cases: str, model_name: str = "text-bison@002") -> str:
    model = TextGenerationModel.from_pretrained(model_name)
    
    prompt = f"""
    Given the following patient history and information about similar cases, 
    generate a personalized treatment plan suggestion. Be specific and consider 
    all relevant factors.

    Patient History:
    {patient_history}

    Similar Cases and Outcomes:
    {similar_cases}

    Suggested Treatment Plan:
    """

    response = model.predict(
        prompt,
        max_output_tokens=1024,
        temperature=0.2,
        top_k=40,
        top_p=0.8,
    )

    return response.text
