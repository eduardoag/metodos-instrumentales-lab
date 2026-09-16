import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Misión 04 - Calibrá tu instrumento",
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# CONSTANTES
# ============================================================

R = 8.314462618
F = 96485.33212

st.title("🎯 MISIÓN 04 — Calibrá tu instrumento")

st.markdown("""
Hasta ahora trabajamos con un **pH-metro ideal**.

Pero un instrumento real puede perder sensibilidad,
desplazarse y producir mediciones variables.

### Pregunta de la misión

> **Si el pH-metro muestra un número, ¿cómo sabemos que podemos confiar en él?**
""")

st.divider()


# ============================================================
# 1. INSTRUMENTO IDEAL
# ============================================================

st.header("1️⃣ Recordemos nuestro instrumento ideal")

temperatura_c = st.slider(
    "Temperatura de trabajo (°C)",
    5.0, 45.0, 25.0, 1.0
)

temperatura_k = temperatura_c + 273.15

pendiente_ideal = (
    -2.303 * R * temperatura_k / F * 1000
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Pendiente ideal",
    f"{pendiente_ideal:.2f} mV/pH"
)

c2.metric(
    "Potencial ideal en pH 7",
    "0.00 mV"
)

c3.metric(
    "Respuesta",
    "100 %"
)

st.latex(
    r"E_{\mathrm{ideal}} = S(T)(pH-7)"
)

st.info("""
💡 **Éste será nuestro patrón mental.**

Un electrodo ideal tiene:

- pendiente nernstiana;
- 0 mV en pH 7 en nuestro modelo didáctico;
- respuesta lineal;
- ausencia de ruido.
""")


# ============================================================
# 2. DETERIORAR EL INSTRUMENTO
# ============================================================

st.divider()

st.header("2️⃣ Ahora descalibrá el instrumento")

st.markdown("""
Mové **una sola variable por vez**.

Observá qué cambia en la gráfica antes de modificar
la siguiente.
""")

col1, col2, col3 = st.columns(3)

with col1:
    eficiencia = st.slider(
        "Sensibilidad / pendiente (%)",
        80.0, 105.0, 100.0, 0.5
    )

with col2:
    offset = st.slider(
        "Offset en pH 7 (mV)",
        -25.0, 25.0, 0.0, 0.5
    )

with col3:
    ruido = st.slider(
        "Ruido instrumental (mV)",
        0.0, 8.0, 0.0, 0.1
    )

pendiente_real = (
    pendiente_ideal * eficiencia / 100
)


# ============================================================
# RUIDO CONTROLADO
# ============================================================

if "semilla_mision4" not in st.session_state:
    st.session_state.semilla_mision4 = 1

if st.button("🎲 Realizar una nueva medición"):
    st.session_state.semilla_mision4 += 1

rng = np.random.default_rng(
    st.session_state.semilla_mision4
)


# ============================================================
# 3. LOS TRES BUFFERS
# ============================================================

st.divider()

st.header("3️⃣ Tres soluciones conocidas interrogan al instrumento")

col4, col7, col10 = st.columns(3)

with col4:
    st.subheader("🧪 Buffer pH 4")
    st.markdown("""
    **Región ácida**

    Pregunta:

    **¿Responde correctamente por debajo de pH 7?**

    Junto con el buffer 7 nos ayuda a estudiar
    la **pendiente**.
    """)

with col7:
    st.subheader("🎯 Buffer pH 7")
    st.markdown("""
    **Punto central**

    En nuestro modelo ideal:

    **pH 7 → 0 mV**

    Es especialmente útil para visualizar
    el **offset**.
    """)

with col10:
    st.subheader("🧪 Buffer pH 10")
    st.markdown("""
    **Región alcalina**

    Pregunta:

    **¿La respuesta continúa correctamente
    por encima de pH 7?**

    Ayuda a comprobar pendiente y linealidad.
    """)


# ============================================================
# CALCULAR BUFFERS
# ============================================================

buffers = np.array([4.0, 7.0, 10.0])

e_buffers_ideal = (
    pendiente_ideal * (buffers - 7)
)

ruido_buffers = rng.normal(
    0,
    ruido,
    len(buffers)
)

e_buffers_actual = (
    offset
    + pendiente_real * (buffers - 7)
    + ruido_buffers
)

df_buffers = pd.DataFrame({
    "Buffer": ["pH 4", "pH 7", "pH 10"],
    "pH": buffers,
    "Ideal_mV": e_buffers_ideal,
    "Medido_mV": e_buffers_actual
})

df_buffers["Diferencia_mV"] = (
    df_buffers["Medido_mV"]
    - df_buffers["Ideal_mV"]
)

st.dataframe(
    df_buffers,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 4. GRÁFICO COMPARATIVO
# ============================================================

st.divider()

st.header("4️⃣ Mirá qué le ocurrió al instrumento")

ph_linea = np.linspace(3, 11, 200)

e_ideal_linea = (
    pendiente_ideal * (ph_linea - 7)
)

e_actual_linea = (
    offset
    + pendiente_real * (ph_linea - 7)
)

fig, ax = plt.subplots(figsize=(10, 6))

# Respuesta ideal
ax.plot(
    ph_linea,
    e_ideal_linea,
    linestyle="--",
    linewidth=2,
    label="Instrumento ideal"
)

# Respuesta actual
ax.plot(
    ph_linea,
    e_actual_linea,
    linewidth=3,
    label="Instrumento actual"
)

# Buffers ideales
ax.scatter(
    buffers,
    e_buffers_ideal,
    marker="o",
    s=90,
    label="Valor ideal de buffers"
)

# Buffers medidos
ax.scatter(
    buffers,
    e_buffers_actual,
    marker="X",
    s=160,
    label="Buffer medido"
)

# Unir ideal con medido
for x, ideal, actual in zip(
    buffers,
    e_buffers_ideal,
    e_buffers_actual
):
    ax.plot(
        [x, x],
        [ideal, actual],
        linestyle=":",
        linewidth=2
    )

ax.axhline(
    0,
    linewidth=1
)

ax.axvline(
    7,
    linewidth=1,
    linestyle=":"
)

ax.set_xlabel("pH")

ax.set_ylabel(
    "Potencial del electrodo (mV)"
)

ax.set_title(
    "Instrumento ideal vs. instrumento actual"
)

ax.grid(True)

ax.legend()

st.pyplot(fig)


# ============================================================
# 5. DIAGNÓSTICO VISUAL
# ============================================================

st.subheader("🔎 ¿Qué deberías mirar?")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    ### ↕ OFFSET

    Si la recta se desplaza hacia arriba o abajo
    pero conserva aproximadamente su inclinación:

    **cambió el punto cero.**
    """)

with c2:
    st.markdown("""
    ### 📐 PENDIENTE

    Si la recta se vuelve más horizontal o más inclinada:

    **cambió la sensibilidad del electrodo.**
    """)

with c3:
    st.markdown("""
    ### 🎲 RUIDO

    Si las mediciones fluctúan alrededor de la respuesta:

    **disminuyó la precisión de la señal.**
    """)


# ============================================================
# 6. CALIBRACIÓN
# ============================================================

st.divider()

st.header("5️⃣ Ahora sí: calibrá")

st.markdown("""
Conocemos el **pH verdadero de los buffers** y hemos
medido su potencial.

Por lo tanto podemos preguntarle a los datos:

> **¿Cuál es realmente la respuesta de este electrodo?**
""")

m, b = np.polyfit(
    df_buffers["pH"],
    df_buffers["Medido_mV"],
    1
)

pred = (
    m * df_buffers["pH"] + b
)

ss_res = np.sum(
    (df_buffers["Medido_mV"] - pred) ** 2
)

ss_tot = np.sum(
    (
        df_buffers["Medido_mV"]
        - df_buffers["Medido_mV"].mean()
    ) ** 2
)

if ss_tot > 0:
    r2 = 1 - ss_res / ss_tot
else:
    r2 = 1.0

eficiencia_calculada = (
    abs(m)
    / abs(pendiente_ideal)
    * 100
)

potencial_ph7_calculado = (
    m * 7 + b
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Pendiente encontrada",
    f"{m:.2f} mV/pH"
)

c2.metric(
    "Respuesta",
    f"{eficiencia_calculada:.1f} %"
)

c3.metric(
    "Offset estimado",
    f"{potencial_ph7_calculado:.2f} mV"
)

c4.metric(
    "R²",
    f"{r2:.5f}"
)


# ============================================================
# GRÁFICO DE CALIBRACIÓN
# ============================================================

st.subheader("📈 La recta que describe a TU instrumento")

e_calibracion = (
    m * ph_linea + b
)

fig2, ax2 = plt.subplots(figsize=(10, 6))

ax2.scatter(
    buffers,
    e_buffers_actual,
    s=150,
    marker="X",
    label="Buffers medidos"
)

ax2.plot(
    ph_linea,
    e_calibracion,
    linewidth=3,
    label="Recta de calibración"
)

ax2.plot(
    ph_linea,
    e_ideal_linea,
    linestyle="--",
    linewidth=2,
    label="Respuesta ideal"
)

ax2.set_xlabel("pH")

ax2.set_ylabel("Potencial (mV)")

ax2.set_title(
    "Calibrar = descubrir cómo responde realmente el instrumento"
)

ax2.grid(True)

ax2.legend()

st.pyplot(fig2)


# ============================================================
# ECUACIÓN
# ============================================================

st.latex(
    rf"E = ({m:.2f})\,pH + ({b:.2f})"
)

st.latex(
    r"pH=\frac{E-b}{m}"
)


# ============================================================
# 7. EXPERIMENTOS GUIADOS
# ============================================================

st.divider()

st.header("🧠 Experimentos para investigar")

st.markdown("""
### Experimento A — Sólo offset

Configurá:

- sensibilidad = **100 %**
- ruido = **0 mV**

Ahora mové solamente el **offset**.

**¿Qué le ocurre a toda la recta?**

---

### Experimento B — Sólo pendiente

Configurá:

- offset = **0 mV**
- ruido = **0 mV**

Reducí la sensibilidad:

**100 % → 95 % → 90 % → 85 %**

**¿Qué ocurre con la inclinación?**

---

### Experimento C — Sólo ruido

Configurá:

- sensibilidad = **100 %**
- offset = **0 mV**

Aumentá el ruido y presioná varias veces:

**🎲 Realizar una nueva medición**

**¿La recta teórica cambió o cambiaron las mediciones?**
""")


# ============================================================
# IDEA FINAL
# ============================================================

st.success("""
### 🎯 IDEA CLAVE

Los buffers no existen para que el instrumento
«vea números conocidos».

Nos permiten **interrogar su comportamiento**.

**pH 4 → región ácida**

**pH 7 → punto central / offset**

**pH 10 → región alcalina**

Juntos nos permiten evaluar la respuesta del electrodo
y construir una relación entre:

**pH conocido → potencial medido**

Esa relación es la que después utilizaremos para
interpretar una muestra desconocida.
""")
