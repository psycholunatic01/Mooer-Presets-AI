import streamlit as st
import openai

st.set_page_config(page_title="Mooer GE150 AI Presets", page_icon="🎸")

st.title("🎸 Mooer GE150 Max Li - Preset Creator")
st.write("Genera presets exactos para tu pedalera usando Inteligencia Artificial.")

# PROMPT DEL SISTEMA - CONFIGURACIÓN TÉCNICA DEL PEDAL
SYSTEM_PROMPT = """
Eres un ingeniero de sonido profesional y especialista técnico en la multiefectos Mooer GE150 Max Li. Tu objetivo es recibir peticiones de guitarristas y devolver la configuración exacta de bloques y parámetros para replicar ese sonido en la Mooer GE150 Max Li.

REGLAS TÉCNICAS STRICTAS DEL PEDAL MOOER GE150 MAX LI:
1. BLOQUES DISPONIBLES: FX/COMP, DS/OD, AMP, CAB, NS, EQ, MOD, DELAY, REVERB.
2. RANGOS Y LIMITACIONES: Todos los parámetros deben expresarse numéricamente de 0 a 100. Usa solo modelos compatibles con la GE150.

FORMATO DE RESPUESTA OBLIGATORIO:
- CONCEPTO DEL TONO
- CONFIGURACIÓN DE CADENA (Paso a paso bloque por bloque con valores 0-100)
- CONSEJO DE EJECUCIÓN O PASTILLA (Micrófono recomendado: Humbucker puente, Single Coil mástil, etc.)
"""

api_key = st.sidebar.text_input("Ingresa tu OpenAI API Key:", type="password")
prompt_usuario = st.text_input("¿Qué tono o artista buscas hoy?", placeholder="Ej: Eddie Van Halen 'Unchained'")

if st.button("🎛️ Generar Preset"):
    if not api_key:
        st.warning("Por favor, ingresa tu API Key de OpenAI en la barra lateral.")
    elif not prompt_usuario:
        st.warning("Escribe qué sonido necesitas antes de generar.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Diseñando tu preset para la GE150 Max Li..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt_usuario}
                    ]
                )
                st.success("¡Preset listo!")
                st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error al conectar: {e}")
