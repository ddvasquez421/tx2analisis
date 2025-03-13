# Analizador de Texto Multimodal con TextBlob

Esta aplicación, desarrollada con Streamlit y TextBlob, permite realizar análisis de sentimiento y procesamiento de texto con soporte para la traducción automática español-inglés mediante Google Translate.

## Características

- **Análisis de sentimiento y subjetividad** - Obtén evaluaciones cuantitativas del tono emocional y la objetividad del texto.
- **Traducción automática** - Traduce automáticamente textos del español al inglés para un análisis más preciso.
- **Análisis de frecuencia de palabras** - Identifica las palabras más utilizadas en el texto.
- **Análisis por frases** - Examina el sentimiento de cada frase individualmente.
- **Interfaz multimodal** - Acepta entrada de texto directamente o a través de archivos.

## Requisitos

```
streamlit>=1.22.0
textblob>=0.15.3
pandas>=1.5.0
googletrans==4.0.0-rc1
```

## Instalación

1. Clona este repositorio o descarga los archivos fuente.
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:

```bash
streamlit run app.py
```

2. Accede a la interfaz web que se abrirá automáticamente en tu navegador (normalmente en http://localhost:8501).

3. Elige el modo de entrada de datos:
   - **Texto directo**: Escribe o pega el texto a analizar
   - **Archivo de texto**: Sube un archivo TXT, CSV o MD para su análisis

4. Haz clic en "Analizar texto" y observa los resultados.

## Cómo funciona

1. **Traducción**: El texto en español se traduce automáticamente al inglés utilizando Google Translate.
2. **Análisis de sentimiento**: TextBlob analiza el texto traducido para determinar su polaridad (positiva/negativa) y subjetividad.
3. **Procesamiento de palabras**: La aplicación cuenta y clasifica las palabras más frecuentes, excluyendo palabras comunes sin significado relevante.
4. **Visualización**: Los resultados se presentan en gráficos y tablas interactivas para facilitar su interpretación.

## Nota técnica

La aplicación utiliza:
- `googletrans 4.0.0-rc1` para la traducción (esta versión específica es importante para la estabilidad)
- Procesamiento de texto nativo para evitar dependencias externas
- Componentes de visualización integrados en Streamlit

## Limitaciones

- La precisión del análisis de sentimiento depende de la calidad de la traducción
- La API gratuita de Google Translate tiene límites de uso
- El análisis está optimizado para textos en español que se traducen al inglés

## Autor

[CC]

## Licencia

Este proyecto está licenciado bajo [MIT] - consulta el archivo LICENSE para más detalles.
