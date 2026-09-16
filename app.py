import streamlit as st


st.set_page_config(
    page_title="Métodos Instrumentales Lab",
    page_icon="🔬",
    layout="wide"
)


st.title("🔬 Métodos Instrumentales Lab")

st.subheader("Ingeniería Ambiental")


st.markdown(
    """
    Bienvenidas y bienvenidos al Laboratorio Virtual
    de Métodos Instrumentales.

    Este espacio fue diseñado para **experimentar** con
    los conceptos que estudiamos en clase.

    No buscamos solamente utilizar ecuaciones.

    Queremos observar, predecir, experimentar,
    equivocarnos y volver a intentar.
    """
)


st.divider()


st.header("⚡ Métodos Potenciométricos")


col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("MISIÓN 01")

    st.markdown(
        """
        ### ¿Cómo puede medirse química con electricidad?

        Potencial eléctrico.

        Electrodo indicador.

        Electrodo de referencia.

        Diferencia de potencial.
        """
    )


with col2:

    st.subheader("MISIÓN 02")

    st.markdown(
        """
        ### La ecuación de Nernst

        Actividad química.

        Potencial eléctrico.

        Temperatura.

        Respuesta nernstiana.
        """
    )


with col3:

    st.subheader("MISIÓN 03")

    st.markdown(
        """
        ### Construí tu pH-metro

        Actividad de H⁺.

        Electrodo de vidrio.

        Temperatura.

        pH-metro ideal.
        """
    )


st.divider()


st.info(
    """
    💡 Idea central del laboratorio:

    SISTEMA AMBIENTAL → SENSOR → SEÑAL →
    DATOS → INFORMACIÓN → DECISIÓN
    """
)
