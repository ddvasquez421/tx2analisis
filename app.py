import streamlit as st
from textblob import TextBlob
from googletrans import Translator

translator = Translator()

# 🎨 Estética lovecraftiana
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: #d6d3c4;
        font-family: 'Georgia', serif;
    }
    h1, h2, h3 {
        color: #c7a96c;
        text-shadow: 0 0 10px #3e3b32;
    }
    .stTextArea textarea {
        background-color: #1b1b1b;
        color: #e5e3dc;
        border: 1px solid #5c5345;
    }
    .stSidebar {
        background-color: #151515;
    }
    .stButton>button {
        background-color: #312b23;
        color: #f5f1e6;
        border: 1px solid #6b5e4b;
    }
    .stExpanderHeader {
        color: #e2d2a2 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Grimorio de la Mente: Análisis Emocional Inhumano")

st.subheader("☠️ Escribe una frase para revelar su verdadera esencia emocional")

with st.sidebar:
    st.subheader("📊 Sobre las Energías Detectadas")
    st.markdown("""
    **Polaridad**: Mide el eco emocional de la frase, desde -1 (oscuridad absoluta) hasta 1 (luz cegadora).

    **Subjetividad**: Revela si el texto contiene hechos o delirios personales (de 0 a 1). 
    ¡Cuidado! Las entidades se alimentan de emociones intensas...
    """)

with st.expander("🔍 Invocar a los Antiguos para Analizar"):
    texto = st.text_area("💬 Ingresa tu oración maldita aquí:")

    if texto:
        traduccion = translator.translate(texto, src="es", dest="en")
        trans_text = traduccion.text
        blob = TextBlob(trans_text)

        polaridad = round(blob.sentiment.polarity, 2)
        subjetividad = round(blob.sentiment.subjectivity, 2)

        st.write("🩸 **Polaridad detectada**:", polaridad)
        st.write("🕯️ **Subjetividad liberada**:", subjetividad)

        if polaridad >= 0.5:
            st.markdown("🔮 *La frase evoca esperanza... una emoción rara en estas tierras.*")
        elif polaridad <= -0.5:
            st.markdown("🕳️ *La oscuridad habita en estas palabras. Has invocado algo...*")
        else:
            st.markdown("🌫️ *Ni luz ni sombra. Un eco neutral resuena entre dimensiones.*")

with st.expander("📚 Purificación del Lenguaje (Corrección en inglés)"):
    texto2 = st.text_area("🖋️ Transcribe el texto corrupto:", key='4')
    if texto2:
        blob2 = TextBlob(texto2)
        corregido = blob2.correct()
        st.write("✨ *Versión purificada por entidades del conocimiento:*")
        st.code(corregido)
