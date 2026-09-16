import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# CONSTANTES
# ==================================================

R = 8.314462618
F = 96485.33212


# ==================================================
# TÍTULO
# ==================================================

st.title("🧪 MISIÓN 03 — Construí tu pH-metro")

st.markdown(
    """
    Ya sabemos que una modificación química puede producir
    una modificación del potencial eléctrico.

    Ahora utilizaremos ese principio para construir
    nuestro primer instrumento virtual:

    # un pH-metro.
    """
)

st.divider()


# ==================================================
# MUESTRA AMBIENTAL
# ==================================================

st.subheader("🌎 Seleccioná la muestra ambiental")

muestras = {
    "Agua de lluvia": 5.6,
    "Río": 7.2,
    "Laguna": 7.8,
    "Agua subterránea": 7.0,
    "Efluente ácido": 4.2,
    "Efluente alcalino": 9.5,
    "Muestra personalizada": 7.0,
}

muestra = st.selectbox(
    "Muestra",
    list(muestras.keys())
)

if muestra == "Muestra personalizada":

    ph = st.slider(
        "pH real de la muestra",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1
    )

else:

    ph = muestras[muestra]

    st.info(
        f"pH asignado para la simulación: {ph:.2f}"
    )


# ==================================================
# TEMPERATURA
# ==================================================

st.subheader("🌡️ Condiciones del experimento")

temperatura_c = st.slider(
    "Temperatura de la muestra (°C)",
    min_value=0.0,
    max_value=60.0,
    value=25.0,
    step=1.0
)

temperatura_k = temperatura_c + 273.15


# ==================================================
# PENDIENTE DE NERNST
# ==================================================

pendiente_v = (
    2.303
    * R
    * temperatura_k
    / F
)

pendiente_mv = pendiente_v * 1000


# ==================================================
# RESPUESTA IDEAL DEL ELECTRODO
# ==================================================

e_mv = -pendiente_mv * (ph - 7.0)


# ==================================================
# ACTIVIDAD DE H+
# ==================================================

actividad_h = 10 ** (-ph)


# ==================================================
# INSTRUMENTO
# ==================================================

st.divider()

st.subheader("🔬 pH-metro virtual")

col1, col2 = st.columns([1, 1])


with col1:

    st.markdown(
        """
        ### Sistema de medición

        ```text
                    pH-METRO
                       │
                       │
                  ┌────┴────┐
                  │         │
               electrodo
               combinado
                  │
                  │
             ┌─────────┐
             │ MUESTRA │
             └─────────┘
        ```
        """
    )


with col2:

    st.markdown("### 📟 Pantalla digital")

    c1, c2 = st.columns(2)

    c1.metric(
        "pH",
        f"{ph:.2f}"
    )

    c2.metric(
        "Potencial",
        f"{e_mv:.2f} mV"
    )

    c3, c4 = st.columns(2)

    c3.metric(
        "Temperatura",
        f"{temperatura_c:.1f} °C"
    )

    c4.metric(
        "Pendiente Nernst",
        f"{pendiente_mv:.2f} mV/pH"
    )


# ==================================================
# QUÍMICA
# ==================================================

st.divider()

st.subheader("⚛️ ¿Qué está midiendo realmente?")

c1, c2, c3 = st.columns(3)

c1.metric(
    "pH",
    f"{ph:.2f}"
)

c2.metric(
    "Actividad H⁺",
    f"{actividad_h:.2e}"
)

c3.metric(
    "Potencial",
    f"{e_mv:.2f} mV"
)

st.latex(
    r"pH=-\log_{10}(a_{H^+})"
)

st.latex(
    r"E=-S(T)(pH-7)"
)


# ==================================================
# GENERAR CURVA COMPLETA
# ==================================================

ph_array = np.linspace(
    0,
    14,
    141
)

e_array = (
    -pendiente_mv
    * (ph_array - 7)
)

df = pd.DataFrame(
    {
        "pH": ph_array,
        "Potencial_mV": e_array
    }
)


# ==================================================
# GRÁFICA
# ==================================================

st.divider()

st.subheader("📈 Respuesta del electrodo")

fig, ax = plt.subplots()

ax.plot(
    df["pH"],
    df["Potencial_mV"]
)

ax.scatter(
    [ph],
    [e_mv],
    s=100
)

ax.axhline(
    0,
    linewidth=1
)

ax.axvline(
    7,
    linewidth=1
)

ax.set_xlabel("pH")

ax.set_ylabel(
    "Potencial del electrodo (mV)"
)

ax.set_title(
    f"Respuesta ideal a {temperatura_c:.1f} °C"
)

ax.grid(True)

st.pyplot(fig)


# ==================================================
# DATOS
# ==================================================

with st.expander(
    "📊 Ver datos generados con pandas"
):

    st.dataframe(
        df,
        use_container_width=True
    )


# ==================================================
# DESAFÍO
# ==================================================

st.divider()

st.subheader("🎯 Experimento 01")

st.markdown(
    """
    Configurá la temperatura en **25 °C**.

    Después analizá sucesivamente:

    - pH 4
    - pH 5
    - pH 6
    - pH 7
    - pH 8
    - pH 9
    - pH 10

    ### Preguntas

    1. ¿Qué ocurre en pH 7?
    2. ¿Qué ocurre con el signo del potencial?
    3. ¿Cuántos mV cambia aproximadamente por unidad de pH?
    4. ¿La relación E vs. pH es lineal?
    """
)


# ==================================================
# EXPERIMENTO DE TEMPERATURA
# ==================================================

st.subheader("🌡️ Experimento 02")

st.markdown(
    """
    Elegí una misma muestra.

    Ahora modificá solamente la temperatura:

    **5 → 15 → 25 → 35 → 45 °C**

    Observá:

    - la pendiente;
    - el potencial;
    - la gráfica.

    ### Pregunta

    ¿Por qué la temperatura afecta la respuesta
    del electrodo?
    """
)


# ==================================================
# IDEA CLAVE
# ==================================================

st.success(
    """
    IDEA CLAVE

    El pH-metro no mide directamente "pH".

    El electrodo genera una diferencia de potencial
    relacionada con la actividad de H⁺.

    El instrumento transforma esa señal eléctrica
    en una lectura de pH.
    """
)
