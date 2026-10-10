import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")

st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")
st.write("Generador de presets con cadena de bloques estricta (100% Gratis con Gemini).")

SYSTEM_PROMPT = """
Eres un ingeniero de sonido y firmware especializado en la Mooer GE150 Max Li. Tu única tarea es recibir un artista, canción o estilo musical y generar un preset detallado con los 9 bloques exactos en orden estricto:
1. FX/COMP 2. DS/OD 3. AMP 4. CAB 5. NS 6. EQ 7. MOD 8. DELAY 9. REVERB.
"""

api_key = st.sidebar.text_input("Gemini API Key (Gratis):", type="password")
query = st.text_input("¿Qué tono necesitas?", placeholder="Ej: Killswitch Engage - My Curse")

if st.button("🚀 Generar Preset y Archivo"):
    if not api_key:
        st.warning("Ingresa tu Gemini API Key de Google Studio.")
    elif not query:
        st.warning("Escribe qué sonido quieres modelar.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Busca automáticamente el primer modelo disponible que genere contenido
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not available_models:
                st.error("No se encontraron modelos disponibles para esta API Key.")
            else:
                # Elige el primer modelo válido automáticamente
                selected_model = available_models[0]
                model = genai.GenerativeModel(selected_model, system_instruction=SYSTEM_PROMPT)
                
                with st.spinner(f"Procesando con {selected_model}..."):
                    response = model.generate_content(query)
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
            st.error(f"Error: {e}")
