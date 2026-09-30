"""Electrogravimetría · Misión 04: pesaje, recuperación y fuentes de error.

Simulación educativa; no sustituye una validación de método experimental.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

M_CU = 63.546  # g/mol

st.title("⚖️ Electrogravimetría · Misión 04")
st.subheader("⚗️ Pesá el depósito y evaluá el error")
st.markdown(
    "**Desafío:** determiná la concentración de cobre de una muestra a partir "
    "del cambio de masa del cátodo. Investigá qué errores alteran el resultado "
    "y cómo mejorarlo mediante un procedimiento analítico adecuado."
)
st.latex(r"m_{\mathrm{depósito}}=m_{\mathrm{final}}-m_{\mathrm{inicial}}")
st.latex(r"C_{\mathrm{Cu}}\;(\mathrm{g/L})=\frac{m_{\mathrm{Cu}}\;(\mathrm{g})}{V_{\mathrm{muestra}}\;(\mathrm{L})}")

with st.expander("📚 Fundamentos y supuestos", expanded=True):
    st.markdown(
        "- **Recuperación de deposición:** fracción del cobre inicial que llega al cátodo. "
        "Si es menor al 100 %, el resultado tiende a subestimar la concentración.\n"
        "- **Pérdida del depósito:** cobre desprendido durante la manipulación o el lavado.\n"
        "- **Humedad y residuos:** aumentan la masa aparente si el electrodo no se lava "
        "o seca correctamente.\n"
        "- **Precisión de la balanza:** introduce dispersión en los pesajes; "
        "no corrige errores sistemáticos.\n"
        "- **Modelo:** muestra homogénea, un solo analito depositable y errores "
        "independientes. No simula reacciones secundarias ni cambios de composición."
    )

st.header("1️⃣ Prepará la muestra y el electrodo")
a, b, c = st.columns(3)
with a:
    volumen_ml = st.slider("Volumen de muestra (mL)", 50, 500, 100, 50, key="eg4_vol")
    concentracion_real = st.slider("Concentración real de Cu (g/L)", 0.10, 5.00, 1.00, 0.05, key="eg4_conc")
with b:
    masa_catodo = st.number_input(
        "Masa inicial nominal del cátodo (g)", 10.0, 100.0, 25.4320,
        step=0.0001, format="%.4f", key="eg4_catodo"
    )
    recuperacion = st.slider("Deposición recuperada (%)", 50, 100, 98, 1, key="eg4_rec")
with c:
    perdida = st.slider("Pérdida del depósito durante el manejo (%)", 0, 20, 2, 1, key="eg4_perd")
    humedad_mg = st.slider("Humedad o residuo adherido (mg)", 0, 100, 10, 1, key="eg4_hum")

st.header("2️⃣ Elegí la calidad del pesaje")
x, y = st.columns(2)
with x:
    desviacion_mg = st.select_slider(
        "Desviación estándar de cada lectura de balanza",
        options=[0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0],
        value=0.2, format_func=lambda z: f"{z:.1f} mg", key="eg4_sd"
    )
with y:
    replicas = st.slider("Número de determinaciones independientes", 1, 10, 3, key="eg4_n")

if "eg4_semilla" not in st.session_state:
    st.session_state.eg4_semilla = 2026
if st.button("🎲 Realizar nuevas mediciones", key="eg4_nueva"):
    st.session_state.eg4_semilla += 1

rng = np.random.default_rng(st.session_state.eg4_semilla)
volumen_l = volumen_ml / 1000.0
masa_disponible = concentracion_real * volumen_l
masa_depositada = masa_disponible * recuperacion / 100.0
masa_cobre_final = masa_depositada * (1.0 - perdida / 100.0)
masa_residuo = humedad_mg / 1000.0
sigma_g = desviacion_mg / 1000.0

# Dos lecturas independientes por determinación; el error en la diferencia
# tiene desviación estándar sqrt(2) * sigma_g.
ruido_inicial = rng.normal(0.0, sigma_g, replicas)
ruido_final = rng.normal(0.0, sigma_g, replicas)
masa_inicial_medida = masa_catodo + ruido_inicial
masa_final_medida = masa_catodo + masa_cobre_final + masa_residuo + ruido_final
masa_aparente = masa_final_medida - masa_inicial_medida
concentracion_medida = masa_aparente / volumen_l

resultados = pd.DataFrame({
    "Réplica": np.arange(1, replicas + 1),
    "Cátodo inicial (g)": masa_inicial_medida,
    "Cátodo final (g)": masa_final_medida,
    "Diferencia (g)": masa_aparente,
    "Cu aparente (g/L)": concentracion_medida,
})
promedio = float(np.mean(concentracion_medida))
sd = float(np.std(concentracion_medida, ddof=1)) if replicas > 1 else None
error_relativo = (promedio - concentracion_real) / concentracion_real * 100.0
recuperacion_aparente = promedio / concentracion_real * 100.0

st.header("3️⃣ Leé los resultados")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cu inicial", f"{masa_disponible:.5f} g")
col2.metric("Cu retenido", f"{masa_cobre_final:.5f} g")
col3.metric("Concentración calculada", f"{promedio:.4f} g/L")
col4.metric("Error relativo", f"{error_relativo:+.2f} %")
st.dataframe(
    resultados.style.format({
        "Cátodo inicial (g)": "{:.5f}",
        "Cátodo final (g)": "{:.5f}",
        "Diferencia (g)": "{:.5f}",
        "Cu aparente (g/L)": "{:.4f}",
    }),
    hide_index=True, use_container_width=True,
)
if sd is not None:
    st.write(f"**Desviación estándar entre determinaciones:** {sd:.4f} g/L")
else:
    st.info("Con una sola determinación no es posible estimar la desviación estándar muestral.")
st.write(f"**Recuperación aparente respecto del valor conocido:** {recuperacion_aparente:.2f} %")
st.caption(
    "La recuperación aparente se calcula usando el valor real conocido de esta "
    "simulación; en una muestra desconocida se necesita un patrón o una adición conocida."
)

fig, ax = plt.subplots(figsize=(9, 3.7))
ax.axhline(concentracion_real, linestyle="--", color="gray", label="Valor real (simulado)")
ax.scatter(resultados["Réplica"], concentracion_medida, s=70, label="Determinaciones")
ax.axhline(promedio, linestyle=":", label="Promedio calculado")
ax.set(xlabel="Determinación", ylabel="Cu (g/L)", title="Precisión y sesgo del resultado")
ax.set_xticks(resultados["Réplica"])
ax.grid(alpha=0.2)
ax.legend(fontsize=8)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.header("4️⃣ Diagnosticá el experimento")
if recuperacion < 100 or perdida > 0:
    st.warning(
        "La deposición incompleta o la pérdida del depósito producen un sesgo "
        "negativo: parte del cobre original no aparece en la masa final."
    )
if humedad_mg > 0:
    st.warning(
        "La humedad o los residuos agregan masa ajena al cobre y producen "
        "un sesgo positivo. Ambos efectos pueden compensarse accidentalmente."
    )
if desviacion_mg > 0:
    st.info(
        "La dispersión de la balanza afecta la precisión. Aumentar las réplicas "
        "puede estabilizar el promedio, pero no elimina los sesgos del procedimiento."
    )
if recuperacion == 100 and perdida == 0 and humedad_mg == 0 and desviacion_mg == 0:
    st.success("Caso ideal: toda la masa recuperada corresponde al cobre inicial.")

st.header("5️⃣ Experimentos guiados")
st.markdown(
    "**A. Recuperación:** fijá humedad y pérdida en cero. Compará una deposición "
    "del 100 % con una del 80 %. ¿Cómo cambia el error relativo?\n\n"
    "**B. Secado:** dejá la deposición al 100 % y variá sólo los miligramos "
    "de humedad. ¿Por qué el resultado aumenta?\n\n"
    "**C. Precisión:** eliminá los sesgos y aumentá la desviación de la balanza. "
    "Repetí la medición y compará los resultados.\n\n"
    "**D. Compensación:** combiná una deposición incompleta con humedad. "
    "¿Un resultado cercano al valor real demuestra que el procedimiento fue correcto?"
)
with st.form("eg4_desafio"):
    eleccion = st.radio(
        "Si un cátodo conserva humedad después del lavado, ¿qué ocurre con la concentración calculada?",
        [
            "Disminuye necesariamente.",
            "Aumenta por la masa adicional que no corresponde al analito.",
            "No cambia porque la balanza distingue el cobre del agua.",
        ],
        index=None,
    )
    comprobar = st.form_submit_button("Comprobar")
if comprobar:
    if eleccion is None:
        st.info("Elegí una respuesta.")
    elif eleccion.startswith("Aumenta por la masa"):
        st.success("¡Correcto! El secado adecuado es esencial para evitar un sesgo positivo.")
    else:
        st.warning("Recordá que la balanza mide toda la masa del electrodo, no sólo la del cobre.")

st.divider()
st.caption(
    "Misión 04 · Modelo didáctico de pesaje y control de calidad. "
    "La Misión 05 integrará estas decisiones en una muestra ambiental desconocida."
)
