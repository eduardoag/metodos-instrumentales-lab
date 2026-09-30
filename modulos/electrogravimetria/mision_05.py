"""Electrogravimetría · Misión 05: campaña simulada de un efluente industrial.

Modelo didáctico con concentraciones ocultas, réplicas, blanco y adición conocida.
No sustituye el muestreo, la validación ni las normas ambientales aplicables.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

FARADAY = 96485.33212  # C/mol de electrones
M_CU = 63.546  # g/mol
ELECTRONES_CU = 2
MASA_CATODO = 25.4320  # g; electrodo limpio y seco
MASA_ADICION = 0.0200  # g de Cu añadidos a la alícuota de control
BLANCO_REAL = 0.0004  # g de residuo aparente por determinación
SIGMA_PESAJE = 0.00015  # g por lectura individual de balanza

# Valores internos del caso: no se muestran hasta el cierre docente opcional.
MUESTRAS = {
    "E1 · Efluente antes del tratamiento": 1.35,
    "E2 · Efluente después del tratamiento": 0.32,
    "E3 · Agua receptora, aguas abajo": 0.12,
}


def simular_deposito(masa_cu_g, corriente_a, tiempo_min, eficiencia, transporte):
    """Depósito limitado por la carga útil y el analito disponible."""
    carga_c = corriente_a * tiempo_min * 60.0
    capacidad_g = carga_c * (eficiencia / 100.0) * M_CU / (ELECTRONES_CU * FARADAY)
    masa_depositada = min(masa_cu_g, capacidad_g) * transporte
    return masa_depositada, carga_c, capacidad_g


def crear_campana(muestra, volumen_ml, corriente_a, tiempo_min, eficiencia,
                   agitacion, secado, replicas, usar_blanco, semilla):
    """Devuelve resultados reproducibles de la campaña y del control de calidad."""
    rng = np.random.default_rng(semilla)
    volumen_l = volumen_ml / 1000.0
    masa_original = MUESTRAS[muestra] * volumen_l
    transporte = {"Insuficiente": 0.84, "Moderada": 0.95, "Adecuada": 0.995}[agitacion]
    humedad_g = 0.0 if secado else 0.0020

    deposito, carga, capacidad = simular_deposito(
        masa_original, corriente_a, tiempo_min, eficiencia, transporte
    )
    deposito_adicionado, _, _ = simular_deposito(
        masa_original + MASA_ADICION, corriente_a, tiempo_min, eficiencia, transporte
    )

    # Cada pesaje inicial y final tiene su propio error aleatorio.
    inicial = MASA_CATODO + rng.normal(0, SIGMA_PESAJE, replicas)
    final = (MASA_CATODO + deposito + BLANCO_REAL + humedad_g
             + rng.normal(0, SIGMA_PESAJE, replicas))
    diferencia = final - inicial

    # Blanco independiente: reproduce residuo y humedad del procedimiento.
    blanco_inicial = MASA_CATODO + rng.normal(0, SIGMA_PESAJE)
    blanco_final = (MASA_CATODO + BLANCO_REAL + humedad_g
                    + rng.normal(0, SIGMA_PESAJE))
    blanco_medido = blanco_final - blanco_inicial
    correccion = blanco_medido if usar_blanco else 0.0

    concentraciones = (diferencia - correccion) / volumen_l
    resultados = pd.DataFrame({
        "Réplica": np.arange(1, replicas + 1),
        "Cátodo inicial (g)": inicial,
        "Cátodo final (g)": final,
        "Δm aparente (g)": diferencia,
        "Cu calculado (g/L)": concentraciones,
    })

    # Una alícuota separada de la misma muestra recibe una adición conocida.
    adicionado_inicial = MASA_CATODO + rng.normal(0, SIGMA_PESAJE)
    adicionado_final = (MASA_CATODO + deposito_adicionado + BLANCO_REAL + humedad_g
                       + rng.normal(0, SIGMA_PESAJE))
    delta_adicionado = adicionado_final - adicionado_inicial - correccion
    # La recuperación por adición se estima por diferencia de masas; los sesgos
    # comunes pueden cancelarse, por lo que NO reemplaza el balance del analito.
    delta_muestra_promedio = float(np.mean(diferencia - correccion))
    recuperacion_adicion = 100 * (delta_adicionado - delta_muestra_promedio) / MASA_ADICION

    return {
        "muestra": muestra,
        "volumen_ml": volumen_ml,
        "corriente_a": corriente_a,
        "tiempo_min": tiempo_min,
        "eficiencia": eficiencia,
        "agitacion": agitacion,
        "secado": secado,
        "replicas": replicas,
        "usar_blanco": usar_blanco,
        "resultados": resultados,
        "carga_c": carga,
        "capacidad_g": capacidad,
        "masa_original_g": masa_original,
        "deposito_g": deposito,
        "blanco_medido_g": blanco_medido,
        "concentracion_media": float(np.mean(concentraciones)),
        "desviacion": float(np.std(concentraciones, ddof=1)) if replicas > 1 else None,
        "recuperacion_adicion": recuperacion_adicion,
        "capacidad_insuficiente": capacidad < masa_original + MASA_ADICION,
    }


st.title("⚖️ Electrogravimetría · Misión 05")
st.subheader("🏭 Investigá un efluente industrial")
st.markdown(
    "**Situación:** un establecimiento industrial solicita una evaluación exploratoria "
    "del cobre en tres puntos de su sistema de tratamiento. La concentración de "
    "cada muestra es desconocida para el equipo de estudiantes. Tu tarea consiste "
    "en diseñar una determinación electrogravimétrica, comprobar la calidad de "
    "los datos y redactar un informe técnico."
)

with st.expander("📚 Protocolo y límites del modelo", expanded=True):
    st.markdown(
        "1. Seleccioná un punto de muestreo y una alícuota.\n"
        "2. Elegí corriente, tiempo, eficiencia de corriente y agitación.\n"
        "3. Realizá determinaciones independientes y, si corresponde, corregí con un blanco.\n"
        "4. Evaluá una adición conocida de **20,0 mg de Cu**.\n"
        "5. Informá la concentración estimada, la dispersión y las limitaciones.\n\n"
        "**Supuestos:** matriz simplificada, un único metal depositable, cátodo "
        "colector y ánodo inerte. La eficiencia de corriente se fija como parámetro "
        "didáctico; la agitación modifica la fracción recuperada. El modelo no "
        "representa cinética de electrodo ni interferencias específicas."
    )
    st.latex(r"Cu^{2+}+2e^-\longrightarrow Cu(s)")
    st.latex(r"m_{\mathrm{Cu,teórica}}=\frac{M_{\mathrm{Cu}}\,I\,t\,\eta}{2F}")
    st.caption(
        "El valor teórico está limitado por el cobre presente en la alícuota. "
        "La masa del depósito y la concentración calculada pueden diferir por "
        "recuperación incompleta, blanco, humedad y errores de pesaje."
    )

st.header("1️⃣ Diseñá la campaña")
with st.form("eg5_campana"):
    a, b = st.columns(2)
    with a:
        muestra = st.selectbox("Punto de muestreo", list(MUESTRAS), key="eg5_muestra")
        volumen_ml = st.select_slider(
            "Alícuota de muestra (mL)", options=[50, 100, 150, 200], value=100
        )
        corriente_a = st.slider("Corriente aplicada (A)", 0.1, 1.5, 0.8, 0.1)
        tiempo_min = st.slider("Duración de la electrólisis (min)", 5, 60, 25, 5)
    with b:
        eficiencia = st.slider("Eficiencia de corriente (%)", 60, 100, 98, 1)
        agitacion = st.selectbox("Agitación", ["Insuficiente", "Moderada", "Adecuada"], index=2)
        replicas = st.slider("Determinaciones independientes", 2, 6, 3)
        secado = st.checkbox("Lavar y secar correctamente el cátodo", value=True)
        usar_blanco = st.checkbox("Medir y descontar un blanco de procedimiento", value=True)
    ejecutar = st.form_submit_button("🧪 Ejecutar campaña", type="primary")

if ejecutar:
    st.session_state.eg5_semilla = st.session_state.get("eg5_semilla", 2026) + 1
    st.session_state.eg5_campana = crear_campana(
        muestra, volumen_ml, corriente_a, tiempo_min, eficiencia,
        agitacion, secado, replicas, usar_blanco, st.session_state.eg5_semilla
    )
    st.session_state.eg5_informe_enviado = False

if "eg5_campana" not in st.session_state:
    st.info("Configurá las condiciones y presioná **Ejecutar campaña** para obtener los datos.")
    st.stop()

camp = st.session_state.eg5_campana
datos = camp["resultados"]

st.header("2️⃣ Analizá los resultados")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Carga total", f"{camp['carga_c']:.0f} C")
c2.metric("Masa aparente media", f"{datos['Δm aparente (g)'].mean() * 1000:.2f} mg")
c3.metric("Cu estimado", f"{camp['concentracion_media']:.4f} g/L")
c4.metric("Blanco medido", f"{camp['blanco_medido_g'] * 1000:.2f} mg")

st.dataframe(
    datos.style.format({
        "Cátodo inicial (g)": "{:.5f}",
        "Cátodo final (g)": "{:.5f}",
        "Δm aparente (g)": "{:.5f}",
        "Cu calculado (g/L)": "{:.4f}",
    }),
    hide_index=True,
    use_container_width=True,
)
st.write(f"**Concentración media:** {camp['concentracion_media']:.4f} g/L")
st.write(f"**Desviación estándar entre determinaciones:** {camp['desviacion']:.4f} g/L")
st.caption("La desviación estándar describe la dispersión de las réplicas; no es la incertidumbre total del método.")

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.scatter(datos["Réplica"], datos["Cu calculado (g/L)"], s=70, label="Determinaciones")
ax.axhline(camp["concentracion_media"], linestyle="--", label="Promedio")
ax.set(xlabel="Determinación", ylabel="Cu calculado (g/L)", title="Resultados de la muestra")
ax.set_xticks(datos["Réplica"])
ax.grid(alpha=0.2)
ax.legend()
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.header("3️⃣ Comprobá la calidad analítica")
q1, q2 = st.columns(2)
q1.metric("Recuperación de adición de 20,0 mg", f"{camp['recuperacion_adicion']:.1f} %")
q2.metric("Capacidad faradaica útil", f"{camp['capacidad_g'] * 1000:.1f} mg")
if camp["capacidad_insuficiente"]:
    st.warning(
        "La carga útil no alcanza para recuperar completamente la muestra adicionada. "
        "Aumentá el tiempo o la corriente y repetí la campaña."
    )
if not camp["secado"]:
    st.warning("El cátodo conserva humedad simulada. El blanco puede corregir parte del sesgo, pero no reemplaza el secado.")
if not camp["usar_blanco"]:
    st.warning("No se descontó el blanco. El depósito aparente puede incluir masa que no corresponde al cobre.")
if not 90 <= camp["recuperacion_adicion"] <= 110:
    st.warning(
        "La recuperación de la adición está fuera del intervalo didáctico de 90–110 %. "
        "Revisá las condiciones antes de emitir un resultado definitivo."
    )
else:
    st.success("La recuperación de la adición está dentro del intervalo didáctico de 90–110 %.")
st.caption(
    "El intervalo 90–110 % es un criterio pedagógico de esta misión, no un límite "
    "reglamentario ni un criterio universal de validación. Una recuperación aceptable "
    "de la adición no demuestra por sí sola la recuperación total del analito original."
)

st.download_button(
    "⬇️ Descargar datos de la campaña (CSV)",
    data=datos.to_csv(index=False).encode("utf-8-sig"),
    file_name="electrogravimetria_mision_05_resultados.csv",
    mime="text/csv",
)

st.header("4️⃣ Elaborá tu informe ambiental")
with st.form("eg5_informe"):
    interpretacion = st.text_area(
        "Interpretación del resultado: ¿qué concentración estimaste y qué tan reproducible fue?",
        placeholder="Incluí concentración media, unidades y dispersión...",
    )
    calidad = st.text_area(
        "Control de calidad: ¿qué indican el blanco y la recuperación de la adición?",
        placeholder="Explicá si repetirías o aceptarías la determinación...",
    )
    limitaciones = st.text_area(
        "Limitaciones: ¿qué información falta antes de concluir si el efluente cumple una norma?",
        placeholder="Considerá jurisdicción, tipo de vertido, muestreo, especiación y validación...",
    )
    enviar = st.form_submit_button("📋 Presentar informe")

if enviar:
    if not all(texto.strip() for texto in (interpretacion, calidad, limitaciones)):
        st.warning("Completá las tres partes del informe antes de presentarlo.")
    else:
        st.session_state.eg5_informe_enviado = True
        st.success("¡Misión completada! Presentaste un informe técnico basado en datos experimentales simulados.")
        st.info(
            "La comparación entre E1, E2 y E3 requiere analizar las tres muestras "
            "con condiciones verificadas. No atribuyas causalidad ni cumplimiento "
            "normativo únicamente a partir de esta simulación."
        )

st.divider()
st.caption(
    "Misión 05 · Simulación educativa de electrogravimetría aplicada a un efluente. "
    "El resultado no es un ensayo de laboratorio real ni un dictamen regulatorio."
)
