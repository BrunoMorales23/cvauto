import pdfplumber
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os, time

texto = ""
load_dotenv()
api_key = os.getenv("API_KEY")


input_value = input("Como proceder. 1 PUSH | 2 Modify ...  ")

if input_value == "1":

    root_path = Path("C:/Users/bmorales/OneDrive - rmrconsultores.com/Escritorio/cv")
    pdf_paths = list(root_path.glob('*.pdf'))


    for path in pdf_paths:
        with pdfplumber.open(path) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text()
        print("Success")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/learnlm-2.0-flash-experimental')

    prompt = f"""Filtra los nombres de las personas, a quienes estos curriculums vitae pertenece. Posicionalos junto a su correo electrónico. Ten en cuenta la separación de guiones, que define distintos contextos." \
    lo que debes analizar, es el siguiente texto: {texto}
    Evita generar oraciones tal como 'De acuerdo, aquí están los nombres y correos electrónicos filtrados de los currículums', '¡Entendido! Aquí está la lista filtrada con el cambio solicitado:', 'Okay, I have the following two email addresses:' y enfocate en solo devolver el resultado
    Corta la primer oración generada y solo devuelve los resultados 'Nombre' | 'Correo'
    Extrae únicamente la información de nombres y correos electrónicos tal como aparece en el texto. No agregues ninguna explicación, conclusión ni interpretación adicional. El formato de salida debe ser exactamente este:
INSTRUCCIONES ESTRICTAS:

Extrae solamente líneas que contengan nombres completos seguidos de su correo electrónico, exactamente en este formato:

* Nombre Apellido - correo@ejemplo.com

NO agregues:
- Frases como “okay”, “here is”, “I have extracted”, etc.
- Títulos, encabezados o frases de cierre.
- Ninguna palabra fuera del formato indicado.

🔴 Si escribes **algo fuera del formato exacto**, se considerará un ERROR.

Si no hay coincidencias, tu respuesta debe estar completamente vacía.


    """

    response = model.generate_content(prompt)
    print(response.text)

elif input_value == "2":
    order_value = input("Como proceder. 1 Pisar Prompt | 2 Complementar Prompt")
    if order_value == "1":
        prompt = input("Deposite el nuevo prompt: ")
    elif order_value == "2":
        new_prompt = input("Deposite la nueva instrucción para el prompt: ")

        root_path = Path("C:/Users/bmorales/OneDrive - rmrconsultores.com/Escritorio/cv")
        pdf_paths = list(root_path.glob('*.pdf'))


        for path in pdf_paths:
            with pdfplumber.open(path) as pdf:
                for pagina in pdf.pages:
                    texto += pagina.extract_text()

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/learnlm-2.0-flash-experimental')

        prompt = f"""Filtra los nombres de las personas, a quienes estos curriculums vitae pertenece. Posicionalos junto a su correo electrónico. Ten en cuenta la separación de guiones, que define distintos contextos." \
        lo que debes analizar, es el siguiente texto: {texto} PORFAVOR, DEVUELVE SOLAMENTE LO SOLICITADO, NO REQUIERO DE NINGUN SCRIPT, NINGUNA EXPLICACION NI NINGUNA DEFINICION, SOLAMENTE SE REQUIERE OBTENER LO CONSULTADO EN EL PROMPT
        """

        prompt_instruction = f"Teniendo en cuenta el prompt inicial, osea: {prompt}, y el nuevo prompt recibido: {new_prompt}. Es necesario que fusiones ambas instrucciones, en un solo prompt, optimizandolo lo más posible a fin de utilizar la menor cantidad de tokens posibles. PORFAVOR, DEVUELVE SOLAMENTE LO SOLICITADO, NO REQUIERO DE NINGUN SCRIPT, NINGUNA EXPLICACION NI NINGUNA DEFINICION, SOLAMENTE SE REQUIERE OBTENER LO CONSULTADO EN EL PROMPT. CUT ANY SENTENCE THAT IS NOT REFERED TO THE REQUERIMENT ITSELF"

        new_prompt = prompt_instruction

        response = model.generate_content(new_prompt)
        prompt = response.text
        time.sleep(5)
        response = model.generate_content(prompt)
        print(response.text)

    