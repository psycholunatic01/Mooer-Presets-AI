import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")
st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")
st.write("Generador de presets con cadena de bloques estricta.")

SYSTEM_PROMPT = """
Eres un ingeniero de sonido y firmware especializado en la Mooer GE150 Max Li.
Tu única tarea es recibir un artista, canción o estilo musical y generar un preset
detallado con los 9 bloques exactos, en este orden estricto:
1. FX/COMP  2. DS/OD  3. AMP  4. CAB  5. NS  6. EQ  7. MOD  8. DELAY  9. REVERB.
Para cada bloque indica el modelo/tipo y los parámetros relevantes con valores concretos.
"""

MODEL = st.secrets.get("GEMINI_MODEL", "gemini-2.5-flash")


@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
query = st.text_input("¿Qué tono necesitas?", placeholder="Ej: Killswitch Engage - My Curse")

if st.button("🚀 Generar Preset y Archivo"):
    if not api_key:
        st.warning("Falta configurar GEMINI_API_KEY en los Secrets de Streamlit Cloud.")
    elif not query.strip():
        st.warning("Escribe qué sonido quieres modelar.")
    else:
        try:
            with st.spinner("Procesando tono..."):
                client = get_client(api_key)
