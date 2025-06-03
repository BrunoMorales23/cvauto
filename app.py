import pdfplumber

with pdfplumber.open("C:/Users/MarsuDIOS666/Desktop/CV Bruno Morales 2025.pdf") as pdf:
    texto = ""
    for pagina in pdf.pages:
        texto += pagina.extract_text()
print(texto)