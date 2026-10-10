import time
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
default_model = st.secrets.get("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    st.warning("Falta GEMINI_API_KEY en los Secrets.")
    st.stop()

client = genai.Client(
    api_key=api_key, http_options=types.HttpOptions(timeout=90000)
)

with st.expander("⚙️ Modelo"):
    if st.button("Ver modelos disponibles"):
        try:
            st.session_state["modelos"] = sorted(
                m.name.replace("models/", "")
                for m in client.models.list()
                if "generateContent" in (m.supported_actions or [])
            )
        except Exception as e:
            st.error(f"No pude listar modelos: {e}")
    opciones = st.session_state.get("modelos", [default_model])
    idx = opciones.index(default_model) if default_model in opciones else 0
    model = st.selectbox("Modelo", opciones, index=idx)
    sin_pensar = st.checkbox("Desactivar thinking (más rápido)", value=True)

query = st.text_input("¿Qué tono necesitas?")

if st.button("🚀 Generar Preset"):
    if not query.strip():
        st.warning("Escribe qué sonido quieres.")
    else:
        t = {"inicio": time.time(), "primera": None}
        extra = {}
        if sin_pensar:
            extra["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT, max_output_tokens=2000, **extra
        )

        def gen():
            for c in client.models.generate_content_stream(
                model=model, contents=query, config=config
            ):
                if c.text:
                    if t["primera"] is None:
                        t["primera"] = time.time() - t["inicio"]
                    yield c.text

        try:
            with st.spinner("Esperando al modelo..."):
                text = st.write_stream(gen())
            total = time.time() - t["inicio"]
            st.caption(
                f"⏱ Primera palabra: {t['primera'] or 0:.1f}s · Total: {total:.1f}s"
            )
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
