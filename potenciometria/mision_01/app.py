import streamlit as st

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Misión 01 - Potenciometría",
    page_icon="⚡",
    layout="wide"
)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("⚡ MISIÓN 01 — ¿Cómo puede medirse química con electricidad?")

st.markdown(
    """
    En esta primera misión vamos a estudiar una idea fundamental:

    **un instrumento potenciométrico mide una diferencia de potencial eléctrico.**

    Todavía no estudiaremos por qué la química modifica el potencial.
    Eso aparecerá en la Misión 02 con la ecuación de Nernst.
    """
)

st.divider()

# --------------------------------------------------
# CONTROLES
# --------------------------------------------------

st.subheader("🧪 Laboratorio virtual")

col1, col2 = st.columns(2)

with col1:
    e_indicador = st.slider(
        "Potencial del electrodo indicador (mV)",
        min_value=-300.0,
        max_value=300.0,
        value=120.0,
        step=1.0
    )

with col2:
    e_referencia = st.slider(
        "Potencial del electrodo de referencia (mV)",
        min_value=-300.0,
        max_value=300.0,
        value=200.0,
        step=1.0
    )

# --------------------------------------------------
# CÁLCULO
# --------------------------------------------------

e_celda = e_indicador - e_referencia

# --------------------------------------------------
# RESULTADOS
# --------------------------------------------------

st.subheader("📟 Lectura del instrumento")

m1, m2, m3 = st.columns(3)

m1.metric(
    "Electrodo indicador",
    f"{e_indicador:.1f} mV"
)

m2.metric(
    "Electrodo de referencia",
    f"{e_referencia:.1f} mV"
)

m3.metric(
    "Potencial de celda",
    f"{e_celda:.1f} mV"
)

st.markdown(
    f"""
    ### Cálculo

    \[
    E_{{celda}} =
    E_{{indicador}} -
    E_{{referencia}}
    \]

    \[
    E_{{celda}} =
    {e_indicador:.1f}
    -
    {e_referencia:.1f}
    =
    {e_celda:.1f}\ mV
    \]
    """
)

st.divider()

# --------------------------------------------------
# ESQUEMA CONCEPTUAL
# --------------------------------------------------

st.subheader("🔬 ¿Qué está ocurriendo?")

st.code(
    """
              VOLTÍMETRO
                  │
                  │  mide ΔE
                  │
        ┌─────────┴─────────┐
        │                   │
        │                   │
  ELECTRODO            ELECTRODO
  INDICADOR             REFERENCIA
        │                   │
        │                   │
        └─────────┬─────────┘
                  │
               MUESTRA
    """,
    language=None
)

st.info(
    """
    El instrumento no mide un "potencial absoluto".

    Mide la diferencia entre el electrodo indicador
    y el electrodo de referencia.
    """
)

st.divider()

# --------------------------------------------------
# DESAFÍO DIDÁCTICO
# --------------------------------------------------

st.subheader("🎯 Desafío")

st.markdown(
    """
    Probá lo siguiente:

    - dejá fijo el electrodo de referencia;
    - modificá solamente el electrodo indicador;
    - observá qué ocurre con el potencial de celda.

    Después hacé lo contrario:

    - dejá fijo el indicador;
    - modificá la referencia.

    **Pregunta:**

    ¿Por qué sería conveniente que el electrodo de referencia
    permanezca lo más estable posible?
    """
)

# --------------------------------------------------
# IDEA CLAVE
# --------------------------------------------------

st.success(
    """
    IDEA CLAVE

    Electrodo indicador → cambia con el sistema químico.

    Electrodo de referencia → permanece estable.

    Instrumento → mide la diferencia entre ambos.
    """
)
