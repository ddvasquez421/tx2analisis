import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from PIL import Image
import nltk
from wordcloud import WordCloud
from collections import Counter

# Descargar recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Multimodal",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("📝 Analizador de Texto Multimodal con TextBlob")
st.markdown("""
Esta aplicación utiliza TextBlob para analizar texto en diferentes modalidades:
- Análisis de sentimiento y subjetividad
- Extracción de frases y palabras clave
- Visualización de frecuencia de palabras
- Análisis de archivos de texto
""")

# Barra lateral
st.sidebar.title("Opciones")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto", "Imagen con texto (OCR)"]
)

# Función para procesar el texto con TextBlob
def procesar_texto(texto):
    blob = TextBlob(texto)
    
    # Análisis de sentimiento
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    # Extraer frases
    frases = list(blob.sentences)
    
    # Palabras más comunes (excluyendo stopwords)
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('spanish') + stopwords.words('english'))
    palabras = [word.lower() for word in blob.words if word.lower() not in stop_words and len(word) > 2]
    contador_palabras = Counter(palabras)
    
    # Reconocimiento de entidades (como sustituto de NER)
    #
