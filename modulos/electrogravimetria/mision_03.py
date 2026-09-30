"""Electrogravimetría · Misión 03: control y transporte de materia.

Modelo didáctico, no una predicción de potenciales ni de cinética industrial.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

F = 96485.33212  # C/mol de electrones
M_CU = 63.546  # g/mol
N = 2  # Cu2+ + 2e- -> Cu(s)
E_MEDIO = -0.10  # V respecto de una referencia didáctica
ANCHO = 0.06  # V; transición fenomenológica, no ecuación de Butler-Volmer

st.title("⚖️ Electrogravimetría · Misión 03")
st.subheader("🎛️ Controlá el proceso")
st.markdown(
    "**Desafío:** elegí cómo controlar la celda y descubrí por qué la deposición "
    "de cobre depende tanto de la electricidad como del transporte de iones "
    "hacia el cátodo."
)
st.latex(r"Cu^{2+}_{(ac)}+2e^-\longrightarrow Cu_{(s)}")

with st.expander("📚 Fundamentos y límites de la simulación", expanded=True):
    st.markdown(
        "- **Corriente controlada:** solicitamos una corriente a la fuente. Si el "
        "transporte de Cu²⁺ es insuficiente, la corriente *parcial* que deposita "
        "cobre queda limitada; en una celda real pueden aparecer otras reacciones.\n"
        "- **Potencial controlado:** fijamos un potencial del cátodo respecto de "
        "una referencia didáctica. El modelo usa una transición suave para "
        "representar qué fracción de la corriente límite se utiliza.\n"
        "- **Transporte de materia:** representamos agitación y difusión mediante "
        "un coeficiente efectivo de transferencia de materia, k.\n"
        "- **Supuestos:** muestra bien mezclada, volumen constante, superficie "
        "constante, depósito selectivo de Cu y ausencia de redisolución. "
        "No calculamos sobrepotenciales, pH, potencial real de electrodo "
        "ni corrientes de reacciones secundarias."
    )
    st.latex(r"I_{\mathrm{lim},Cu}=n F k A C(t)")
    st.caption("En esta ecuación, A está en m², k en m/s y C en mol/m³; el resultado se expresa en amperios.")

st.header("1️⃣ Configurá la celda")
modo = st.radio(
    "Modalidad de control",
    ["Corriente controlada", "Potencial controlado"],
    horizontal=True,
    key="eg3_modo",
)
col1, col2, col3 = st.columns(3)
with col1:
    concentracion = st.slider("[Cu²⁺] inicial (mol/L)", 0.01, 0.50, 0.10, 0.01, key="eg3_c")
    volumen_ml = st.slider("Volumen de muestra (mL)", 50, 1000, 250, 50, key="eg3_v")
with col2:
    area_cm2 = st.slider("Área del cátodo (cm²)", 20, 200, 100, 10, key="eg3_a")
    agitacion = st.slider("Transporte efectivo k (×10⁻⁵ m/s)", 1, 50, 20, 1, key="eg3_k")
with col3:
    duracion_min = st.slider("Duración (min)", 5, 180, 60, 5, key="eg3_t")
    if modo == "Corriente controlada":
        corriente_objetivo = st.slider("Corriente solicitada (mA)", 5, 200, 50, 5, key="eg3_i") / 1000.0
        potencial = None
    else:
        potencial = st.slider("Potencial aplicado (V, referencia didáctica)", -0.50, 0.20, -0.25, 0.01, key="eg3_e")
        corriente_objetivo = None

k = agitacion * 1e-5  # m/s
area_m2 = area_cm2 * 1e-4
volumen_l = volumen_ml / 1000.0
moles_iniciales = concentracion * volumen_l
masa_inicial = moles_iniciales * M_CU
limite_inicial = N * F * k * area_m2 * concentracion * 1000.0
if potencial is not None:
    fraccion_potencial = 1.0 / (1.0 + np.exp((potencial - E_MEDIO) / ANCHO))
else:
    fraccion_potencial = None

# Integración explícita con pasos cortos y balance de materia estricto.
numero_pasos = max(400, duracion_min * 20)
tiempos_s = np.linspace(0.0, duracion_min * 60.0, numero_pasos + 1)
dt = float(tiempos_s[1] - tiempos_s[0])
moles = moles_iniciales
carga_cobre = 0.0
historial = [(0.0, concentracion, 0.0, 0.0, limite_inicial)]
for t in tiempos_s[1:]:
    c_actual = max(0.0, moles / volumen_l)
    i_lim = N * F * k * area_m2 * c_actual * 1000.0
    if corriente_objetivo is not None:
        i_cu = min(corriente_objetivo, i_lim)
    else:
        i_cu = fraccion_potencial * i_lim
    # No se puede depositar más cobre del que queda en la solución.
    dq = min(i_cu * dt, moles * N * F)
    moles -= dq / (N * F)
    carga_cobre += dq
    c_nueva = max(0.0, moles / volumen_l)
    historial.append((t / 60.0, c_nueva, dq / dt, (moles_iniciales - moles) * M_CU, i_lim))

df = pd.DataFrame(
    historial,
    columns=["Tiempo (min)", "Cu²⁺ (mol/L)", "Corriente Cu (A)", "Masa Cu (g)", "Corriente límite (A)"],
)
masa_final = (moles_iniciales - moles) * M_CU
recuperacion = 100.0 * (moles_iniciales - moles) / moles_iniciales

st.header("2️⃣ Observá el experimento")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Corriente límite inicial", f"{limite_inicial * 1000:.2f} mA")
c2.metric("Carga útil para Cu", f"{carga_cobre:.1f} C")
c3.metric("Cobre depositado", f"{masa_final:.5f} g")
c4.metric("Recuperación", f"{recuperacion:.1f} %")
st.progress(min(1.0, max(0.0, recuperacion / 100.0)), text=f"{masa_final:.5f} g depositados / {masa_inicial:.5f} g disponibles")

if corriente_objetivo is not None and corriente_objetivo > limite_inicial:
    st.warning(
        "La corriente solicitada supera la corriente límite inicial de Cu²⁺. "
        "En este modelo, la deposición de cobre queda limitada por el transporte. "
        "En una celda real, la fuente podría sostener la corriente total mediante "
        "reacciones secundarias o un cambio de potencial."
    )
elif corriente_objetivo is not None:
    st.info(
        "Al principio hay suficiente transporte para la corriente solicitada. "
        "Observá si el descenso de concentración hace que aparezca una limitación después."
    )
else:
    st.info(
        "El potencial determina qué fracción de la corriente límite se utiliza "
        "en este modelo. A medida que disminuye Cu²⁺, también disminuye la corriente."
    )

st.header("3️⃣ Interpretá las curvas")
fig1, ax1 = plt.subplots(figsize=(9, 3.5))
ax1.plot(df["Tiempo (min)"], df["Corriente Cu (A)"] * 1000, label="Corriente parcial de Cu")
ax1.plot(df["Tiempo (min)"], df["Corriente límite (A)"] * 1000, "--", label="Límite por transporte")
if corriente_objetivo is not None:
    ax1.axhline(corriente_objetivo * 1000, linestyle=":", color="gray", label="Corriente solicitada")
ax1.set(xlabel="Tiempo (min)", ylabel="Corriente (mA)", title="Corriente y transporte de materia")
ax1.grid(alpha=0.2)
ax1.legend(fontsize=8)
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

fig2, ax2 = plt.subplots(figsize=(9, 3.5))
ax2.plot(df["Tiempo (min)"], df["Masa Cu (g)"], label="Cobre depositado")
ax2.axhline(masa_inicial, linestyle="--", color="gray", label="Cobre disponible inicialmente")
ax2.set(xlabel="Tiempo (min)", ylabel="Masa (g)", title="Acumulación de cobre en el cátodo")
ax2.grid(alpha=0.2)
ax2.legend(fontsize=8)
fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

fig3, ax3 = plt.subplots(figsize=(9, 3.2))
ax3.plot(df["Tiempo (min)"], df["Cu²⁺ (mol/L)"])
ax3.set(xlabel="Tiempo (min)", ylabel="[Cu²⁺] (mol/L)", title="Agotamiento del cobre disuelto")
ax3.grid(alpha=0.2)
fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

st.header("4️⃣ Revisá los datos")
indices = np.unique(np.linspace(0, len(df) - 1, 11, dtype=int))
st.dataframe(df.iloc[indices].round(6), hide_index=True, use_container_width=True)
st.caption("Los datos son resultados del modelo didáctico; no corresponden a mediciones experimentales.")

st.header("5️⃣ Desafíos de ingeniería")
st.markdown(
    "**Experimento A:** mantené la corriente solicitada y aumentá el transporte efectivo. "
    "¿En qué momento deja de limitar la deposición?\n\n"
    "**Experimento B:** seleccioná potencial controlado y hacé el potencial más negativo. "
    "¿Por qué la corriente deja de aumentar indefinidamente?\n\n"
    "**Experimento C:** duplicá el área del cátodo. ¿Cómo cambian la corriente límite "
    "y la recuperación durante el mismo intervalo?"
)
with st.form("eg3_pregunta"):
    respuesta = st.radio(
        "Si la corriente solicitada supera la corriente límite de Cu²⁺, ¿qué afirmación es correcta?",
        [
            "La masa de cobre necesariamente aumenta en proporción a toda la corriente solicitada.",
            "La deposición de cobre queda limitada por su transporte hacia el cátodo.",
            "La concentración de Cu²⁺ aumenta espontáneamente.",
        ],
        index=None,
    )
    verificar = st.form_submit_button("Comprobar")
if verificar:
    if respuesta is None:
        st.info("Elegí una respuesta antes de comprobar.")
    elif respuesta.startswith("La deposición de cobre queda limitada"):
        st.success("¡Correcto! La corriente total de la celda y la corriente parcial de cobre no siempre coinciden.")
    else:
        st.warning("Revisá la diferencia entre corriente solicitada y corriente parcial de deposición de Cu.")

st.divider()
st.caption(
    "Misión 03 · Modelo conceptual de transporte de materia y control electroquímico. "
    "En la Misión 04 trabajaremos con el pesaje, la recuperación y las fuentes de error."
)
