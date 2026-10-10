import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")

st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")
st.write("Generador de presets con cadena de bloques estricta (100% Gratis con Gemini).")

SYSTEM_PROMPT = """
Eres un ingeniero de sonido y firmware especializado en la Mooer GE150 Max Li. Tu única tarea es recibir un artista, canción o estilo, y devolver un preset técnico con valores exactos (0 a 100) respetando el orden físico de la cadena de bloques del pedal:
1. FX/COMP 2. DS/OD 3. AMP 4. CAB 5. NS 6. EQ 7. MOD 8. DELAY 9. REVERB.
"""

api_key = st.sidebar.text_input("Gemini API Key (Gratis):", type="password")
query = st.text_input("¿Qué tono necesitas?", placeholder="Ej: Van Halen - Brown Sound")

if st.button("🚀 Generar Preset y Archivo"):
    if not api_key:
        st.warning("Ingresa tu Gemini API Key de Google Studio.")
    elif not query:
        st.warning("Escribe qué sonido quieres modelar.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro", system_instruction=SYSTEM_PROMPT)


            with st.spinner("Procesando tono gratis..."):
                response = model.generate_content(query)
                preset_text = response.text
                
                st.success("¡Preset generado!")
                st.markdown(preset_text)
                
                st.download_button(
                    label="📥 Descargar archivo (.txt)",
                    data=preset_text,
                    file_name=f"preset_ge150_{query.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error: {e}")
