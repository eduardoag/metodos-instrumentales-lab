import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Misión 02 - Ecuación de Nernst",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ MISIÓN 02 — La ecuación de Nernst")

st.markdown(
    """
    En la Misión 01 modificábamos manualmente el potencial
    del electrodo indicador.

    Ahora vamos a dar un paso fundamental:

    **modificaremos la química y observaremos cómo cambia
    el potencial eléctrico.**
    """
)

st.divider()

# --------------------------------------------------
# CONSTANTES
# --------------------------------------------------

R = 8.314462618       # J / (mol K)
F = 96485.33212       # C / mol

# --------------------------------------------------
# CONTROLES
# --------------------------------------------------

st.subheader("🧪 Sistema electroquímico")

col1, col2, col3 = st.columns(3)

with col1:
    temperatura_c = st.slider(
        "Temperatura (°C)",
        min_value=0.0,
        max_value=60.0,
        value=25.0,
        step=1.0
    )

with col2:
    n = st.selectbox(
        "Número de electrones (n)",
        options=[1, 2, 3],
        index=0
    )

with col3:
    e0_mv = st.number_input(
        "Potencial estándar E° (mV)",
        value=0.0,
        step=10.0
    )

st.markdown("### Actividad química")

log_actividad = st.slider(
    "log₁₀(a)",
    min_value=-6.0,
    max_value=0.0,
    value=-2.0,
    step=0.1
)

actividad = 10 ** log_actividad

# --------------------------------------------------
# CÁLCULOS
# --------------------------------------------------

temperatura_k = temperatura_c + 273.15
e0_v = e0_mv / 1000

# Semirreacción conceptual:
# M^n+ + n e- <-> M(s)
#
# E = E° + RT/(nF) ln(a)

e_v = (
    e0_v
    + (R * temperatura_k / (n * F))
    * np.log(actividad)
)

e_mv = e_v * 1000

pendiente_mv = (
    2.303
    * R
    * temperatura_k
    / (n * F)
    * 1000
)

# --------------------------------------------------
# RESULTADOS
# --------------------------------------------------

st.subheader("📟 Resultado")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Actividad",
    f"{actividad:.2e}"
)

m2.metric(
    "Temperatura",
    f"{temperatura_k:.2f} K"
)

m3.metric(
    "Pendiente",
    f"{pendiente_mv:.2f} mV/década"
)

m4.metric(
    "Potencial E",
    f"{e_mv:.2f} mV"
)

st.latex(
    r"E = E^\circ + \frac{RT}{nF}\ln(a)"
)

st.markdown(
    f"""
    Para las condiciones seleccionadas:

    - **a = {actividad:.3e}**
    - **T = {temperatura_k:.2f} K**
    - **n = {n}**
    - **E° = {e0_mv:.2f} mV**

    El potencial calculado es:

    **E = {e_mv:.2f} mV**
    """
)

st.divider()

# --------------------------------------------------
# GENERACIÓN DE DATOS
# --------------------------------------------------

st.subheader("📊 ¿Qué ocurre al cambiar la actividad?")

actividades = np.logspace(-6, 0, 100)

potenciales_v = (
    e0_v
    + (R * temperatura_k / (n * F))
    * np.log(actividades)
)

potenciales_mv = potenciales_v * 1000

df = pd.DataFrame(
    {
        "Actividad": actividades,
        "log10_actividad": np.log10(actividades),
        "Potencial_mV": potenciales_mv
    }
)

# --------------------------------------------------
# GRÁFICO
# --------------------------------------------------

fig, ax = plt.subplots()

ax.plot(
    df["log10_actividad"],
    df["Potencial_mV"]
)

ax.scatter(
    [log_actividad],
    [e_mv]
)

ax.set_xlabel("log₁₀(actividad)")
ax.set_ylabel("Potencial (mV)")
ax.set_title("Respuesta potenciométrica ideal")

ax.grid(True)

st.pyplot(fig)

# --------------------------------------------------
# DATOS
# --------------------------------------------------

with st.expander("🔎 Ver datos generados con pandas"):
    st.dataframe(df, use_container_width=True)

st.divider()

# --------------------------------------------------
# DESAFÍO
# --------------------------------------------------

st.subheader("🎯 Experimento")

st.markdown(
    """
    Configurá:

    **Temperatura = 25 °C**

    **n = 1**

    **E° = 0 mV**

    y probá sucesivamente:

    - a = 1
    - a = 0.1
    - a = 0.01
    - a = 0.001

    Observá cuánto cambia el potencial cada vez que
    la actividad disminuye diez veces.
    """
)

st.success(
    """
    IDEA CLAVE

    Una modificación química de la muestra puede producir
    una modificación medible del potencial eléctrico.

    Esa relación está descrita por la ecuación de Nernst.
    """
)
