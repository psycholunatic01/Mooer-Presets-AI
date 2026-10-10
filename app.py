import streamlit as st
import requests
import json

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")

st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")
st.write("Generador de presets con cadena de bloques estricta (100% Gratis con Gemini).")

SYSTEM_PROMPT = """
Eres un ingeniero de sonido y firmware especializado en la Mooer GE150 Max Li. Tu única tarea es recibir un artista, canción o estilo musical y generar un preset detallado con los 9 bloques exactos en orden estricto:
1. FX/COMP 2. DS/OD 3. AMP 4. CAB 5. NS 6. EQ 7. MOD 8. DELAY 9. REVERB.
"""

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
            with st.spinner("Procesando tono con la API..."):
                # Endpoint oficial v1
                url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
                
                full_prompt = f"{SYSTEM_PROMPT}\n\nSolicitud del usuario: {query}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": full_prompt}]
                    }]
                }
                
                # Encabezado estándar compatible con el formato nuevo AQ. y el clásico AIza
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": api_key
                }
                
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    res_json = response.json()
                    preset_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    
                    st.success("¡Preset generado con éxito!")
                    st.markdown(preset_text)
                    
                    st.download_button(
                        label="📥 Descargar archivo (.txt)",
                        data=preset_text,
                        file_name=f"preset_ge150_{query.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Error de la API ({response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"Error técnico: {e}")
