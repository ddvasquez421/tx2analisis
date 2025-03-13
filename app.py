import streamlit as st
import pandas as pd
from textblob import TextBlob
from PIL import Image
import nltk
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
- Análisis de frecuencia de palabras 
- Soporte para diferentes fuentes de entrada
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
    
    # Reconocimiento de entidades (usando frases nominales como aproximación)
    frases_nominales = list(blob.noun_phrases)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases,
        "contador_palabras": contador_palabras,
        "frases_nominales": frases_nominales,
        "palabras": palabras
    }

# Función para crear visualizaciones usando componentes nativos de Streamlit
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    
    # Visualización de sentimiento y subjetividad con barras de progreso de Streamlit
    with col1:
        st.subheader("Análisis de Sentimiento y Subjetividad")
        
        # Normalizar valores para mostrarlos en barras de progreso
        # Sentimiento va de -1 a 1, lo normalizamos a 0-1 para la barra
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        
        st.write("**Sentimiento:**")
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
        
        # Subjetividad ya está en el rango 0-1
        st.write("**Subjetividad:**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    # Palabras más frecuentes usando chart de Streamlit
    with col2:
        st.subheader("Palabras más frecuentes")
        if resultados["contador_palabras"]:
            palabras_comunes = dict(resultados["contador_palabras"].most_common(10))
            st.bar_chart(palabras_comunes)
    
    # Frases nominales detectadas
    st.subheader("Frases nominales detectadas")
    if resultados["frases_nominales"]:
        st.write(", ".join(resultados["frases_nominales"]))
    else:
        st.write("No se detectaron frases nominales significativas.")
    
    # Análisis de frases
    st.subheader("Análisis por frases")
    if resultados["frases"]:
        datos_frases = []
        for i, frase in enumerate(resultados["frases"]):
            sentimiento = frase.sentiment.polarity
            subjetividad = frase.sentiment.subjectivity
            datos_frases.append({
                "Frase": str(frase),
                "Sentimiento": sentimiento,
                "Subjetividad": subjetividad
            })
        
        df_frases = pd.DataFrame(datos_frases)
        
        # Visualización de datos de frases con una tabla de Streamlit y código de colores
        st.dataframe(
            df_frases.style.background_gradient(
                subset=["Sentimiento"], 
                cmap="RdYlGn", 
                vmin=-1, 
                vmax=1
            ).background_gradient(
                subset=["Subjetividad"], 
                cmap="Blues", 
                vmin=0, 
                vmax=1
            )
        )

# Lógica principal según el modo seleccionado
if modo == "Texto directo":
    st.subheader("Ingresa tu texto para analizar")
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar...")
    
    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando texto..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Por favor, ingresa algún texto para analizar.")

elif modo == "Archivo de texto":
    st.subheader("Carga un archivo de texto")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    
    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("Ver contenido del archivo"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            
            if st.button("Analizar archivo"):
                with st.spinner("Analizando archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

elif modo == "Imagen con texto (OCR)":
    st.subheader("Carga una imagen con texto")
    st.warning("Nota: Para esta funcionalidad se requiere tener instalado pytesseract y Tesseract OCR.")
    
    try:
        import pytesseract
        from PIL import Image
        
        imagen = st.file_uploader("", type=["jpg", "jpeg", "png"])
        
        if imagen is not None:
            img = Image.open(imagen)
            st.image(img, width=400, caption="Imagen cargada")
            
            if st.button("Extraer y analizar texto"):
                with st.spinner("Extrayendo texto de la imagen..."):
                    try:
                        texto = pytesseract.image_to_string(img)
                        if texto.strip():
                            st.subheader("Texto extraído:")
                            st.text_area("", texto, height=150)
                            
                            resultados = procesar_texto(texto)
                            crear_visualizaciones(resultados)
                        else:
                            st.warning("No se pudo extraer texto de la imagen.")
                    except Exception as e:
                        st.error(f"Error en el OCR: {e}")
                        st.info("Asegúrate de tener instalado Tesseract OCR en tu sistema y la biblioteca pytesseract en Python.")
    except ImportError:
        st.error("No se pudo importar pytesseract. Instálalo con: pip install pytesseract")
        st.info("También necesitas instalar Tesseract OCR en tu sistema.")

# Información adicional
with st.expander("📚 Información sobre el análisis"):
    st.markdown("""
    ### Sobre el análisis de texto
    
    - **Sentimiento**: Varía de -1 (muy negativo) a 1 (muy positivo)
    - **Subjetividad**: Varía de 0 (muy objetivo) a 1 (muy subjetivo)
    - **Frases nominales**: Grupos de palabras que funcionan como sustantivos
    
    ### Requisitos
    
    Para utilizar todas las funcionalidades:
    ```
    pip install streamlit textblob pandas nltk
    ```
    
    Para OCR (opcional):
    ```
    pip install pytesseract pillow
    ```
    Y descargar [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
    """)

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️ usando Streamlit y TextBlob")
