import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")

st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")
st.write("Generador de presets con cadena de bloques estricta (100% Gratis con Gemini).")

SYSTEM_PROMPT = """
Eres un ingeniero de sonido y firmware especializado en la Mooer GE150 Max Li. Tu única tarea es recibir un artista, canción o estilo musical y generar un preset detallado con los 9 bloques exactos en orden estricto:
1. FX/COMP 2. DS/OD 3. AMP 4. CAB 5. NS 6. EQ 7. MOD 8. DELAY 9. REVERB.
"""

# Obtener clave desde Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    api_key = ""

query = st.text_input("¿Qué tono necesitas?", placeholder="Ej: Killswitch Engage - My Curse")

if st.button("🚀 Generar Preset y Archivo"):
    if not api_key:
        st.warning("Falta configurar la GEMINI_API_KEY en los Secrets de Streamlit Cloud.")
    elif not query:
        st.warning("Escribe qué sonido quieres modelar.")
    else:
        try:
            with st.spinner("Procesando tono con el SDK oficial de Gemini..."):
                # Inicializa el cliente oficial con la clave proporcionada
                client = genai.Client(api_key=api_key)
                
                # Petición oficial usando el modelo recomendado gemini-2.5-flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=query,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                    ),
                )
                
                preset_text = response.text
                
                st.success("¡Preset generado con éxito!")
                st.markdown(preset_text)
                
                st.download_button(
                    label="📥 Descargar archivo (.txt)",
                    data=preset_text,
                    file_name=f"preset_ge150_{query.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
