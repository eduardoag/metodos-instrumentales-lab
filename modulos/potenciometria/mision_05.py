import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Misión 05 - Investigá el río",
    page_icon="🌊",
    layout="wide"
)


# ============================================================
# CONSTANTES
# ============================================================

R = 8.314462618
F = 96485.33212

TEMPERATURA_C = 25.0
TEMPERATURA_K = TEMPERATURA_C + 273.15

PENDIENTE_IDEAL = (
    -2.303 * R * TEMPERATURA_K / F * 1000
)


# ============================================================
# ESTADO DE LA MISIÓN
# ============================================================

if "m5_calibrado" not in st.session_state:
    st.session_state.m5_calibrado = False

if "m5_resultados" not in st.session_state:
    st.session_state.m5_resultados = None

if "m5_semilla" not in st.session_state:
    st.session_state.m5_semilla = 42


# ============================================================
# VERDAD OCULTA DEL RÍO
# ============================================================

# IMPORTANTE:
# estos valores existen en la simulación,
# pero NO se muestran al estudiante.

rio = pd.DataFrame({
    "Estacion": [
        "P1 - Aguas arriba",
        "P2 - Antes de la descarga",
        "P3 - Zona de descarga",
        "P4 - 500 m aguas abajo",
        "P5 - 2 km aguas abajo"
    ],

    "Distancia_km": [
        0.0,
        1.0,
        2.0,
        2.5,
        4.0
    ],

    "pH_real": [
        7.25,
        7.18,
        5.35,
        6.15,
        6.90
    ]
})


# ============================================================
# INSTRUMENTO OCULTO
# ============================================================

# Nuestro instrumento no es perfecto.

EFICIENCIA_REAL = 95.0
OFFSET_REAL = 5.0
RUIDO_REAL = 1.2

PENDIENTE_REAL = (
    PENDIENTE_IDEAL
    * EFICIENCIA_REAL
    / 100
)


# ============================================================
# ENCABEZADO
# ============================================================

st.title("🌊 MISIÓN 05 — Investigá el río")

st.error("""
🚨 **ALERTA AMBIENTAL**

Se recibió un aviso por una posible alteración
de la calidad del agua en un curso superficial.

Tu equipo de Ingeniería Ambiental fue convocado
para realizar una campaña de medición.
""")

st.markdown("""
### 🎯 Tu misión

Determinar si existe una modificación espacial del pH
y decidir si la evidencia obtenida es suficientemente
confiable para respaldar un diagnóstico.

**Importante:**

No conocemos el pH real del río.

Todo lo que concluyamos deberá surgir de nuestras mediciones.
""")

st.divider()


# ============================================================
# MAPA CONCEPTUAL
# ============================================================

st.header("🗺️ Zona de estudio")

st.code("""
                 DIRECCIÓN DEL FLUJO →

 P1 ───────── P2 ───────── P3 ─── P4 ───────────── P5
                              │
                              │
                         DESCARGA
                         INDUSTRIAL
""")

estaciones_visibles = rio[
    ["Estacion", "Distancia_km"]
].copy()

st.dataframe(
    estaciones_visibles,
    use_container_width=True,
    hide_index=True
)

st.info("""
Tenemos cinco estaciones.

P1 y P2 permiten conocer las condiciones previas.

P3 coincide con la zona de interés.

P4 y P5 permiten estudiar qué ocurre aguas abajo.
""")


# ============================================================
# FASE 1
# ============================================================

st.divider()

st.header("FASE 1️⃣ — ¿Confiamos en nuestro instrumento?")

st.markdown("""
Antes de salir al campo debemos comprobar
cómo está respondiendo nuestro pH-metro.

Disponemos de tres patrones certificados:

**pH 4.00 · pH 7.00 · pH 10.00**
""")


# ============================================================
# GENERAR CALIBRACIÓN
# ============================================================

rng_cal = np.random.default_rng(
    st.session_state.m5_semilla
)

buffers = np.array([
    4.0,
    7.0,
    10.0
])

ruido_cal = rng_cal.normal(
    0,
    RUIDO_REAL,
    len(buffers)
)

e_buffers = (
    OFFSET_REAL
    + PENDIENTE_REAL * (buffers - 7)
    + ruido_cal
)

df_cal = pd.DataFrame({
    "Buffer_pH": buffers,
    "Potencial_mV": e_buffers
})


# ============================================================
# MOSTRAR BUFFERS
# ============================================================

st.subheader("🧪 Mediciones de los patrones")

st.dataframe(
    df_cal,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# REGRESIÓN
# ============================================================

m, b = np.polyfit(
    df_cal["Buffer_pH"],
    df_cal["Potencial_mV"],
    1
)

pred = (
    m * df_cal["Buffer_pH"] + b
)

ss_res = np.sum(
    (df_cal["Potencial_mV"] - pred) ** 2
)

ss_tot = np.sum(
    (
        df_cal["Potencial_mV"]
        - df_cal["Potencial_mV"].mean()
    ) ** 2
)

r2 = (
    1 - ss_res / ss_tot
    if ss_tot > 0
    else 1.0
)

respuesta = (
    abs(m)
    / abs(PENDIENTE_IDEAL)
    * 100
)

offset_estimado = (
    m * 7 + b
)


# ============================================================
# GRÁFICO CALIBRACIÓN
# ============================================================

ph_linea = np.linspace(
    3.5,
    10.5,
    100
)

e_linea = (
    m * ph_linea + b
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.scatter(
    buffers,
    e_buffers,
    s=130,
    label="Buffers medidos"
)

ax.plot(
    ph_linea,
    e_linea,
    label="Recta de calibración"
)

ax.set_xlabel("pH conocido")

ax.set_ylabel("Potencial medido (mV)")

ax.set_title(
    "Respuesta experimental del instrumento"
)

ax.grid(True)

ax.legend()

st.pyplot(fig)


# ============================================================
# DIAGNÓSTICO
# ============================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Pendiente",
    f"{m:.2f} mV/pH"
)

c2.metric(
    "Respuesta",
    f"{respuesta:.1f} %"
)

c3.metric(
    "R²",
    f"{r2:.5f}"
)


st.markdown("""
### 🧠 Antes de continuar

Preguntate:

- ¿La respuesta es aproximadamente lineal?
- ¿La pendiente es razonable?
- ¿Existe un desplazamiento?
- ¿Usarías este instrumento sin calibrarlo?
""")


# ============================================================
# BOTÓN CALIBRAR
# ============================================================

if st.button(
    "🎯 Aceptar calibración y continuar",
    type="primary"
):

    st.session_state.m5_calibrado = True

    st.session_state.m5_m = m
    st.session_state.m5_b = b

    st.success(
        "Calibración registrada. El equipo está listo para la campaña."
    )


# ============================================================
# FASE 2
# ============================================================

if st.session_state.m5_calibrado:

    st.divider()

    st.header("FASE 2️⃣ — Salimos al campo")

    st.markdown("""
    El instrumento está calibrado.

    En cada estación realizaremos **tres réplicas independientes**.

    ¿Por qué tres?

    Porque una única lectura no nos permite observar
    la variabilidad de la medición.
    """)

    if st.button(
        "🌊 Iniciar campaña de muestreo",
        type="primary"
    ):

        rng_campo = np.random.default_rng(
            st.session_state.m5_semilla + 100
        )

        resultados = []

        for _, fila in rio.iterrows():

            for replica in range(1, 4):

                ruido = rng_campo.normal(
                    0,
                    RUIDO_REAL
                )

                potencial = (
                    OFFSET_REAL
                    + PENDIENTE_REAL
                    * (fila["pH_real"] - 7)
                    + ruido
                )

                ph_estimado = (
                    potencial
                    - st.session_state.m5_b
                ) / st.session_state.m5_m

                resultados.append({

                    "Estacion":
                        fila["Estacion"],

                    "Distancia_km":
                        fila["Distancia_km"],

                    "Replica":
                        replica,

                    "Potencial_mV":
                        potencial,

                    "pH_estimado":
                        ph_estimado
                })

        st.session_state.m5_resultados = (
            pd.DataFrame(resultados)
        )


# ============================================================
# FASE 3
# ============================================================

if st.session_state.m5_resultados is not None:

    df = st.session_state.m5_resultados

    st.divider()

    st.header("FASE 3️⃣ — Abrimos la libreta de campo")

    st.dataframe(
        df.round(3),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    Ahora tenemos **datos**, no conclusiones.

    El siguiente trabajo es transformar esos datos
    en información.
    """)


    # ========================================================
    # PANDAS
    # ========================================================

    resumen = (
        df.groupby(
            ["Estacion", "Distancia_km"],
            as_index=False
        )
        .agg(
            pH_promedio=(
                "pH_estimado",
                "mean"
            ),

            desviacion=(
                "pH_estimado",
                "std"
            ),

            minimo=(
                "pH_estimado",
                "min"
            ),

            maximo=(
                "pH_estimado",
                "max"
            )
        )
        .sort_values(
            "Distancia_km"
        )
    )


    st.subheader(
        "📊 Resumen estadístico por estación"
    )

    st.dataframe(
        resumen.round(3),
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # PERFIL ESPACIAL
    # ========================================================

    st.subheader(
        "📈 Perfil espacial del río"
    )

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )

    ax2.errorbar(
        resumen["Distancia_km"],
        resumen["pH_promedio"],
        yerr=resumen["desviacion"],
        marker="o",
        markersize=8,
        capsize=5
    )

    ax2.axvline(
        2.0,
        linestyle="--",
        label="Zona de descarga"
    )

    ax2.set_xlabel(
        "Distancia a lo largo del río (km)"
    )

    ax2.set_ylabel(
        "pH estimado"
    )

    ax2.set_title(
        "Perfil espacial de pH"
    )

    ax2.grid(True)

    ax2.legend()

    st.pyplot(fig2)


    # ========================================================
    # FASE 4
    # ========================================================

    st.divider()

    st.header(
        "FASE 4️⃣ — Pensá como Ingeniera/o Ambiental"
    )

    st.markdown("""
    Ya no mires el código.

    Mirá solamente la evidencia.

    ### Preguntas

    **1.** ¿P1 y P2 presentan condiciones semejantes?

    **2.** ¿Dónde aparece el mayor cambio?

    **3.** ¿Qué ocurre después de P3?

    **4.** ¿P4 muestra recuperación parcial?

    **5.** ¿Qué sucede en P5?

    **6.** ¿Las tres réplicas son suficientemente consistentes?

    **7.** ¿Podemos afirmar causalidad solamente con estas mediciones?

    **8.** ¿Qué otras variables ambientales medirías?
    """)


    # ========================================================
    # HIPÓTESIS
    # ========================================================

    st.subheader(
        "📝 Construí tu hipótesis"
    )

    hipotesis = st.text_area(
        "¿Qué creés que está ocurriendo en el río?",
        height=120,
        placeholder=(
            "A partir de los datos obtenidos..."
        )
    )

    evidencia = st.text_area(
        "¿Qué evidencia respalda tu interpretación?",
        height=120,
        placeholder=(
            "Las estaciones P... muestran..."
        )
    )

    limitaciones = st.text_area(
        "¿Qué limitaciones tiene esta investigación?",
        height=120,
        placeholder=(
            "No podemos concluir todavía que..."
        )
    )


    # ========================================================
    # CIERRE
    # ========================================================

    st.divider()

    st.success("""
    ## 🌊 MISIÓN COMPLETADA

    Un instrumento no produce conocimiento
    simplemente porque muestra un número.

    El conocimiento aparece cuando podemos explicar:

    **cómo medimos**

    ↓

    **cómo calibramos**

    ↓

    **qué incertidumbre existe**

    ↓

    **qué patrón muestran los datos**

    ↓

    **qué podemos concluir**

    ↓

    **y qué todavía NO podemos concluir.**
    """)
