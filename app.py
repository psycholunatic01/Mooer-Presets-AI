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
    if api_key.startswith("AQ."):
        # Clave de Vertex AI (modo Express)
        return genai.Client(vertexai=True, api_key=api_key)
    # Clave estándar de Gemini Developer API (AIzaSy...)
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
                response = client.models.generate_content(
                    model=MODEL,
                    contents=f"Solicitud del usuario: {query}",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    ),
                )
                preset_text = response.text

            st.success("¡Preset generado con éxito!")
            st.markdown(preset_text)

            safe_name = "".join(c if c.isalnum() else "_" for c in query)[:60]
            st.download_button(
                label="📥 Descargar archivo (.txt)",
                data=preset_text,
                file_name=f"preset_ge150_{safe_name}.txt",
                mime="text/plain",
            )
        except Exception as e:
            st.error(f"Error de la API: {e}")
