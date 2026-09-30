"""Electrogravimetría · Misión 02: ley de Faraday (modelo didáctico)."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

F = 96485.33212  # C/mol de electrones
N_A = 6.02214076e23  # entidades/mol
M_CU = 63.546  # g/mol
ELECTRONES_POR_CU = 2

st.title("⚖️ Electrogravimetría · Misión 02")
st.subheader("🧮 Dominá la ley de Faraday")
st.markdown(
    "**Desafío:** predecí cuánta masa de cobre se deposita sobre el cátodo "
    "y comprobá qué sucede cuando la corriente no se aprovecha por completo "
    "o cuando se agota el Cu²⁺ disponible."
)
st.latex(r"Cu^{2+}_{(ac)}+2e^-\longrightarrow Cu_{(s)}")

with st.expander("📚 Fundamentos y supuestos del modelo", expanded=True):
    st.latex(r"Q=I\,t\qquad n_{e^-}=\frac{Q}{F}\qquad m_{\mathrm{ideal}}=\frac{M_{Cu}\,I\,t}{2F}")
    st.latex(r"m_{\mathrm{dep}}=\min\!\left(\eta\,\frac{M_{Cu}\,I\,t}{2F},\;C_0\,V\,M_{Cu}\right)")
    st.markdown(
        "La **eficiencia de corriente** (η) es la fracción de la carga destinada "
        "a depositar cobre. El modelo supone corriente constante, eficiencia constante "
        "y depósito selectivo; detiene la deposición cuando se agota el cobre inicial. "
        "Si la muestra se agota, la carga adicional no deposita más cobre. "
        "En una celda real intervienen el transporte de materia, el potencial, "
        "las reacciones secundarias y la calidad del depósito."
    )

st.header("1️⃣ Configurá tu experimento")
col_i, col_t, col_eta = st.columns(3)
with col_i:
    corriente = st.slider("Corriente aplicada (A)", 0.1, 5.0, 1.0, 0.1, key="eg2_i")
with col_t:
    minutos = st.slider("Duración (min)", 1, 180, 30, 1, key="eg2_t")
with col_eta:
    eficiencia_pct = st.slider("Eficiencia de corriente (%)", 10, 100, 90, 5, key="eg2_eta")

col_c, col_v = st.columns(2)
with col_c:
    concentracion = st.slider("Concentración inicial de Cu²⁺ (mol/L)", 0.01, 0.50, 0.10, 0.01, key="eg2_c")
with col_v:
    volumen_ml = st.slider("Volumen de muestra (mL)", 50, 1000, 250, 50, key="eg2_v")

segundos = minutos * 60.0
eta = eficiencia_pct / 100.0
moles_iniciales = concentracion * volumen_ml / 1000.0
masa_disponible = moles_iniciales * M_CU
carga = corriente * segundos
moles_electrones = carga / F
numero_electrones = moles_electrones * N_A
masa_ideal_sin_limite = M_CU * carga / (ELECTRONES_POR_CU * F)
masa_eficiente_sin_limite = eta * masa_ideal_sin_limite
masa_depositada = min(masa_eficiente_sin_limite, masa_disponible)
masa_restante = max(0.0, masa_disponible - masa_depositada)
fraccion_recuperada = masa_depositada / masa_disponible
carga_util_cobre = masa_depositada / M_CU * ELECTRONES_POR_CU * F
carga_otros_procesos = max(0.0, carga - carga_util_cobre)
tiempo_agotamiento = (
    masa_disponible * ELECTRONES_POR_CU * F / (eta * M_CU * corriente)
)
agotamiento = segundos >= tiempo_agotamiento - 1e-9

st.header("2️⃣ Observá los resultados")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Carga total", f"{carga:,.1f} C")
k2.metric("Electrones transferidos", f"{numero_electrones:.3e}")
k3.metric("Cobre depositado", f"{masa_depositada:.5f} g")
k4.metric("Recuperación del cobre", f"{fraccion_recuperada * 100:.1f} %")

st.progress(fraccion_recuperada, text=f"Cu depositado: {masa_depositada:.5f} g / {masa_disponible:.5f} g disponibles")
if agotamiento:
    st.warning(
        "La muestra alcanzó el límite de cobre disponible. "
        f"En este modelo se agotó aproximadamente a los {tiempo_agotamiento / 60:.1f} minutos. "
        "La carga posterior no puede aumentar la masa de Cu depositado."
    )
else:
    st.info("Todavía queda cobre disuelto: modificá el tiempo o la corriente y observá qué sucede.")

st.header("3️⃣ Compará teoría, eficiencia y disponibilidad")
fig, ax = plt.subplots(figsize=(9, 4.5))
tiempo_min = np.linspace(0.0, float(minutos), 250)
q_t = corriente * tiempo_min * 60.0
masa_ideal_t = M_CU * q_t / (ELECTRONES_POR_CU * F)
masa_eficiente_t = eta * masa_ideal_t
masa_real_t = np.minimum(masa_eficiente_t, masa_disponible)
ax.plot(tiempo_min, masa_ideal_t, "--", linewidth=2, label="Ideal: η = 100 %, sin límite de muestra")
ax.plot(tiempo_min, masa_eficiente_t, ":", linewidth=2, label=f"η = {eficiencia_pct} %, sin límite de muestra")
ax.plot(tiempo_min, masa_real_t, linewidth=3, label="Depósito con límite de Cu²⁺")
ax.axhline(masa_disponible, color="gray", linewidth=1.5, alpha=0.8, label="Cu disponible en la muestra")
if agotamiento:
    ax.axvline(tiempo_agotamiento / 60, color="gray", linestyle="-.", alpha=0.7)
ax.set(xlabel="Tiempo (min)", ylabel="Masa de cobre (g)", title="Evolución de la deposición")
ax.set_xlim(0, max(1.0, float(minutos)))
ax.set_ylim(bottom=0)
ax.grid(alpha=0.2)
ax.legend(fontsize=8, loc="best")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

resumen = pd.DataFrame(
    [
        ("Carga total", carga, "C"),
        ("Electrones transferidos", numero_electrones, "electrones"),
        ("Masa ideal sin límite", masa_ideal_sin_limite, "g"),
        ("Masa con eficiencia, sin límite", masa_eficiente_sin_limite, "g"),
        ("Masa disponible inicialmente", masa_disponible, "g"),
        ("Masa realmente depositada (modelo)", masa_depositada, "g"),
        ("Masa de cobre restante", masa_restante, "g"),
        ("Carga destinada a depositar Cu", carga_util_cobre, "C"),
        ("Carga no destinada a depositar Cu", carga_otros_procesos, "C"),
    ],
    columns=["Magnitud", "Valor", "Unidad"],
)
st.dataframe(resumen, hide_index=True, use_container_width=True)
st.caption(
    "La carga no destinada a depositar Cu incluye las pérdidas por eficiencia y, "
    "si la muestra se agota, la carga que continúa circulando después del agotamiento."
)

st.header("4️⃣ Investigá como ingeniera/o")
st.markdown(
    "**Experimento A.** Duplicá la corriente sin cambiar el tiempo. "
    "¿Se duplica siempre la masa depositada? Explicá qué ocurre si se agota la muestra.\n\n"
    "**Experimento B.** Compará eficiencias de 100 % y 50 % con el mismo tiempo. "
    "¿Qué sucede con la masa antes de alcanzar el límite de cobre?\n\n"
    "**Experimento C.** Duplicá el volumen manteniendo la concentración. "
    "¿Qué cambia: la masa disponible, la carga transferida o ambas?"
)
with st.form("eg2_desafio"):
    respuesta = st.radio(
        "Si la muestra no se agota y la eficiencia es constante, al duplicar la corriente y mantener el tiempo…",
        [
            "La masa depositada se reduce a la mitad.",
            "La masa depositada se duplica.",
            "La masa depositada no cambia.",
        ],
        index=None,
    )
    comprobar = st.form_submit_button("Comprobar respuesta")
if comprobar:
    if respuesta is None:
        st.info("Seleccioná una respuesta antes de comprobar.")
    elif respuesta == "La masa depositada se duplica.":
        st.success("¡Correcto! Q = I·t y, antes del agotamiento, la masa es proporcional a la carga útil.")
    else:
        st.warning("Revisá la relación Q = I·t y la proporcionalidad entre carga útil y masa.")

st.divider()
st.caption(
    "Misión 02 · Modelo didáctico. La eficiencia de corriente no equivale "
    "necesariamente a la recuperación analítica. En la próxima misión estudiaremos "
    "cómo las condiciones electroquímicas y el transporte de materia afectan el proceso."
)
