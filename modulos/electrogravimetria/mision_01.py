"""Misión 01: celda electrolítica virtual. Streamlit >= 1.37."""
import time
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import Rectangle, FancyArrowPatch

F = 96485.33212       # C/mol de electrones
M_CU = 63.546         # g/mol
N = 2                 # Cu2+ + 2e- -> Cu(s)

st.title("⚖️ Electrogravimetría · Misión 01")
st.subheader("⚡ Construí tu celda electrolítica")
st.markdown("**Desafío:** conectá la fuente, identificá los electrodos y observá cómo Cu²⁺ se convierte en cobre metálico. En esta primera misión suponemos una eficiencia de corriente del 100 % y un ánodo inerte.")
st.latex(r"Cu^{2+}_{(ac)}+2e^-\longrightarrow Cu_{(s)}")

with st.expander("🔎 Antes de comenzar: ¿qué representa el modelo?", expanded=False):
    st.markdown("""- **Cátodo (−):** recibe electrones de la fuente; allí se reduce Cu²⁺ y aumenta la masa del electrodo.\n- **Ánodo (+):** ocurre una oxidación. En el modelo usamos un ánodo inerte; la reacción anódica no se cuantifica.\n- **Corriente:** fija el ritmo ideal de transferencia de carga.\n- **Puntos azules:** representan una muestra visual de los iones, **no** cada ion individual.\n- **Límite del modelo:** no contempla sobrepotenciales, transporte de masa, reacciones secundarias ni cambios de pH. La fuente se considera capaz de sostener la corriente elegida hasta agotar el Cu²⁺.""")

st.header("1️⃣ Prepará el experimento")
a, b, c, d = st.columns(4)
with a:
    corriente = st.slider("Corriente (A)", 0.1, 3.0, 1.0, 0.1)
with b:
    concentracion = st.slider("[Cu²⁺] inicial (mol/L)", 0.01, 0.20, 0.05, 0.01)
with c:
    volumen_ml = st.slider("Volumen (mL)", 50, 500, 100, 50)
with d:
    velocidad = st.select_slider("Velocidad virtual", options=[1, 10, 60, 300], value=60, format_func=lambda x: f"×{x}")

moles_iniciales = concentracion * volumen_ml / 1000
carga_maxima = moles_iniciales * N * F
masa_maxima = moles_iniciales * M_CU
firma = (corriente, concentracion, volumen_ml)

if "eg1_firma" not in st.session_state or st.session_state.eg1_firma != firma:
    st.session_state.eg1_firma = firma
    st.session_state.eg1_carga = 0.0
    st.session_state.eg1_tiempo = 0.0
    st.session_state.eg1_activo = False
    st.session_state.eg1_ultimo = time.monotonic()

st.caption("Si cambiás la corriente, la concentración o el volumen, el experimento se reinicia para que los resultados sean consistentes.")

x, y, z = st.columns(3)
with x:
    if st.button("▶️ Iniciar / reanudar", use_container_width=True):
        st.session_state.eg1_ultimo = time.monotonic()
        st.session_state.eg1_activo = True
with y:
    if st.button("⏸️ Pausar", use_container_width=True):
        st.session_state.eg1_activo = False
with z:
    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state.eg1_activo = False
        st.session_state.eg1_carga = 0.0
        st.session_state.eg1_tiempo = 0.0
        st.session_state.eg1_ultimo = time.monotonic()

@st.fragment(run_every="1s")
def simulacion():
    ahora = time.monotonic()
    anterior = st.session_state.eg1_ultimo
    st.session_state.eg1_ultimo = ahora
    if st.session_state.eg1_activo:
        dt_virtual = min(ahora - anterior, 5.0) * velocidad
        restante = max(0.0, carga_maxima - st.session_state.eg1_carga)
        dt_util = min(dt_virtual, restante / corriente)
        st.session_state.eg1_tiempo += dt_util
        st.session_state.eg1_carga += corriente * dt_util
        if st.session_state.eg1_carga >= carga_maxima - 1e-8:
            st.session_state.eg1_carga = carga_maxima
            st.session_state.eg1_activo = False

    q = st.session_state.eg1_carga
    moles_cu = q / (N * F)
    masa = moles_cu * M_CU
    fraccion = min(1.0, q / carga_maxima)
    moles_restantes = max(0.0, moles_iniciales - moles_cu)
    numero_electrones = (q / F) * 6.02214076e23

    st.header("2️⃣ Observá la celda en funcionamiento")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Tiempo virtual", f"{st.session_state.eg1_tiempo:,.1f} s")
    k2.metric("Carga transferida", f"{q:,.2f} C")
    k3.metric("Electrones transferidos", f"{numero_electrones:.3e}")
    k4.metric("Cobre depositado", f"{masa:.5f} g")

    fig, ax = plt.subplots(figsize=(10, 4.8))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    # Fuente y cables
    ax.add_patch(Rectangle((4.15, 5.15), 1.7, 0.65, facecolor="#34445c", edgecolor="none"))
    ax.text(5, 5.48, "FUENTE CC", color="white", ha="center", va="center", fontsize=10, weight="bold")
    ax.plot([4.4, 2.3, 2.3], [5.15, 5.15, 4.5], color="#64748b", lw=2)
    ax.plot([5.6, 7.7, 7.7], [5.15, 5.15, 4.5], color="#64748b", lw=2)
    ax.text(4.4, 5.0, "−", ha="center", fontsize=13)
    ax.text(5.6, 5.0, "+", ha="center", fontsize=13)
    # Vaso y solución
    ax.add_patch(Rectangle((1.4, 0.8), 7.2, 3.7, facecolor="none", edgecolor="#64748b", lw=2))
    ax.add_patch(Rectangle((1.45, 0.85), 7.1, 2.8, facecolor="#d9eef9", edgecolor="none"))
    # Electrodos
    ax.add_patch(Rectangle((2.08, 1.2), 0.44, 3.3, facecolor="#aab8c6", edgecolor="#65758b"))
    ax.add_patch(Rectangle((2.08, 1.2), 0.44, 3.3 * fraccion, facecolor="#b86b42", edgecolor="none"))
    ax.add_patch(Rectangle((7.48, 1.2), 0.44, 3.3, facecolor="#8999a8", edgecolor="#65758b"))
    ax.text(2.3, 4.72, "CÁTODO (−)", ha="center", fontsize=10, weight="bold")
    ax.text(7.7, 4.72, "ÁNODO (+)", ha="center", fontsize=10, weight="bold")
    # Los puntos son partículas representativas, no iones individuales.
    cantidad = round(48 * (1 - fraccion))
    rng = np.random.default_rng(123)
    puntos = rng.uniform([2.9, 1.15], [7.0, 3.45], size=(48, 2))
    if cantidad:
        ax.scatter(puntos[:cantidad, 0], puntos[:cantidad, 1], s=100, c="#67a5ce", edgecolors="#37759c", alpha=0.9)
    if fraccion > 0:
        ax.annotate("Cu²⁺ + 2e⁻ → Cu(s)", xy=(2.6, 2.2), xytext=(3.25, 4.0),
                    arrowprops={"arrowstyle": "->", "color": "#a45e39", "lw": 2},
                    fontsize=11, color="#8a4b2c", weight="bold")
    ax.text(5, 0.35, f"Cu²⁺ restante: {moles_restantes:.5f} mol", ha="center", fontsize=11)
    st.pyplot(fig, clear_figure=True)
    st.progress(fraccion, text=f"Cobre recuperado: {fraccion * 100:.1f} % · máximo teórico: {masa_maxima:.5f} g")
    if fraccion >= 1:
        st.success("🏁 Se agotó el Cu²⁺ disponible en este modelo. No puede depositarse más cobre de esta muestra.")
    elif st.session_state.eg1_activo:
        st.info("⚡ Celda conectada: la fuente suministra corriente y el cobre se deposita sobre el cátodo.")
    else:
        st.info("⏸️ Celda detenida. Podés reanudar el experimento o cambiar sus condiciones.")

simulacion()

st.divider()
st.header("3️⃣ Investigá como ingeniera/o")
st.markdown("""**Experimento A.** Mantené fija la concentración y duplicá la corriente. ¿Qué sucede con el tiempo necesario para depositar la misma masa?\n\n**Experimento B.** Mantené fija la corriente y duplicá la concentración inicial. ¿Qué sucede con la masa máxima disponible?\n\n**Experimento C.** ¿Por qué la masa deja de aumentar cuando se agota el Cu²⁺, aunque la fuente siga siendo capaz de entregar corriente?""")
st.latex(r"Q=I\,t\qquad n_{e^-}=\frac{Q}{F}\qquad m_{Cu}=\frac{M_{Cu}\,Q}{2F}")
st.caption("Modelo ideal para aprendizaje: en una celda real, la corriente puede desviarse hacia otras reacciones y el transporte de materia puede limitar la deposición. La próxima misión profundizará en la ley de Faraday.")
