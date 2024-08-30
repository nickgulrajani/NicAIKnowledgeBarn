import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import vertexai
from vertexai.language_models import TextGenerationModel

def initialize_vertexai(project_id: str, location: str):
    vertexai.init(project=project_id, location=location)

def generate_treatment_plan(prompt: str, model_name: str = "text-bison@002") -> str:
    model = TextGenerationModel.from_pretrained(model_name)
    
    response = model.predict(
        prompt,
        max_output_tokens=1024,
        temperature=0.2,
        top_k=40,
        top_p=0.8,
    )

    return response.text

class TreatmentPlanGeneratorUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Treatment Plan Generator")

        self.load_template_button = ttk.Button(master, text="Load Prompt Template", command=self.load_template)
        self.load_template_button.pack()

        self.prompt_label = ttk.Label(master, text="Edit the prompt below:")
        self.prompt_label.pack()

        self.prompt_entry = scrolledtext.ScrolledText(master, height=20)
        self.prompt_entry.pack()

        self.generate_button = ttk.Button(master, text="Generate Treatment Plan", command=self.generate_plan)
        self.generate_button.pack()

        self.result_label = ttk.Label(master, text="Generated Treatment Plan:")
        self.result_label.pack()

        self.result_text = scrolledtext.ScrolledText(master, height=20)
        self.result_text.pack()

    def load_template(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                template_content = file.read()
                self.prompt_entry.delete("1.0", tk.END)
                self.prompt_entry.insert(tk.END, template_content)

    def generate_plan(self):
        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if prompt:
            treatment_plan = generate_treatment_plan(prompt)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, treatment_plan)
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Please enter a prompt.")

if __name__ == "__main__":
    # Initialize Vertex AI (replace with your project ID and location)
    initialize_vertexai("aivertex-421013", "us-central1")

    root = tk.Tk()
    app = TreatmentPlanGeneratorUI(root)
    root.mainloop()
