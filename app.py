import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")
st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")

SYSTEM_PROMPT = """
Eres un ingeniero de sonido especializado en la Mooer GE150 Max Li.
Recibes un artista, canción o estilo y generas un preset con los 9 bloques
exactos, en este orden: 1. FX/COMP 2. DS/OD 3. AMP 4. CAB 5. NS 6. EQ
7. MOD 8. DELAY 9. REVERB. Para cada bloque indica modelo y parámetros
con valores concretos. Sé conciso: una lista corta por bloque y como
máximo una línea de explicación.
"""

api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
model = st.secrets.get("GEMINI_MODEL", "gemini-3.8-flash")
query = st.text_input("¿Qué tono necesitas?")


def stream_preset(client, query):
    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    for chunk in client.models.generate_content_stream(
        model=model, contents=query, config=config
    ):
        if chunk.text:
            yield chunk.text


if st.button("🚀 Generar Preset"):
    if not api_key:
        st.warning("Falta GEMINI_API_KEY en los Secrets.")
    elif not query.strip():
        st.warning("Escribe qué sonido quieres.")
    else:
        client = genai.Client(api_key=api_key)
        try:
            text = st.write_stream(stream_preset(client, query))
            st.session_state["preset"] = text
            st.session_state["shown"] = True
        except Exception as e:
            st.error(f"Error de la API: {e}")

if st.session_state.get("preset"):
    if not st.session_state.pop("shown", False):
        st.markdown(st.session_state["preset"])
    st.download_button(
        "📥 Descargar .txt",
        st.session_state["preset"],
        file_name="preset_ge150.txt",
        mime="text/plain",
    )
