import streamlit as st
import openai

st.set_page_config(page_title="Mooer GE150 AI Engine", page_icon="🎸")

st.title("🎸 Mooer GE150 Max Li - AI Tone Engine")
st.write("Generador de presets con cadena de bloques estricta y exportación de archivos.")

# MOTOR DE IA Y REGLAS DE HARDWARE GE150
SYSTEM_PROMPT = """
Eres un ingeniero de sonido y firmware especializado en la Mooer GE150 Max Li. Tu única tarea es recibir un artista, canción o estilo, y devolver un preset técnico con valores exactos (0 a 100) respetando implícitamente el orden físico de la cadena de bloques del pedal.

ORDEN OBLIGATORIO DE LA CADENA DE BLOQUES:
1. FX / COMP (Compresor, Boost, Pitch)
2. DS / OD (Distorsión / Overdrive)
3. AMP (Modelo de Amplificador de los 55 reales de la GE150)
4. CAB (Simulación de Gabinete / IR)
5. NS (Noise Suppressor / Puerta de ruido)
6. EQ (Ecualizador)
7. MOD (Modulación: Chorus, Flanger, Phaser)
8. DELAY (Tipo de eco y tiempo)
9. REVERB (Tipo de ambiente y decadencia)

FORMATO DE SALIDA ESTRICTO:
- 🎯 TÍTULO Y PASTILLA RECOMENDADA (Ej: Humbucker de puente)
- 🎛️ VALORES TÉCNICOS EXACTOS POR BLOQUE (Escala 0 a 100)
- 💾 RESUMEN DE CONFIGURACIÓN PARA ARCHIVO
"""

api_key = st.sidebar.text_input("OpenAI API Key:", type="password")
query = st.text_input("¿Qué tono necesitas?", placeholder="Ej: Van Halen - Brown Sound")

if st.button("🚀 Generar Preset y Archivo"):
    if not api_key:
        st.warning("Ingresa tu API Key de OpenAI en la barra lateral.")
    elif not query:
        st.warning("Escribe qué sonido quieres modelar.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Procesando arquitectura de audio..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": query}
                    ]
                )
                preset_text = response.choices[0].message.content
                
                st.success("¡Preset generado con éxito!")
                st.markdown(preset_text)
                
                # BOTÓN DE DESCARGA DIRECTA DE ARCHIVO
                st.download_button(
                    label="📥 Descargar archivo de configuración (.txt)",
                    data=preset_text,
                    file_name=f"preset_ge150_{query.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"Error de conexión: {e}")
