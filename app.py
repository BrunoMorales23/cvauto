import pdfplumber
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os

texto = ""

load_dotenv()
api_key = os.getenv("API_KEY")

root_path = Path("C:/Users/bmorales/OneDrive - rmrconsultores.com/Escritorio/cv")
pdf_paths = list(root_path.glob('*.pdf'))


for path in pdf_paths:
    with pdfplumber.open(path) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    print(texto)
    print("------------------------------------------------------------------------------")

input("Continue?")


genai.configure(api_key=api_key)

model = genai.GenerativeModel('models/learnlm-2.0-flash-experimental')

prompt = f"""Filtra los nombres de las personas, a quienes estos curriculums vitae pertenece. Posicionalos junto a su correo electrónico. Ten en cuenta la separación de guiones, que define distintos contextos." \
lo que debes analizar, es el siguiente texto: {texto}
"""
response = model.generate_content(prompt)
print(response.text)


#for m in genai.list_models():
#    print(f"{m.name} - {m.supported_generation_methods}")