import streamlit as st


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Métodos Instrumentales Lab",
    page_icon="🔬",
    layout="wide"
)


# ============================================================
# PORTADA
# ============================================================

def inicio():

    st.title("🔬 Métodos Instrumentales Lab")

    st.subheader("Ingeniería Ambiental")

    st.markdown(
        """
        Bienvenidas y bienvenidos al **Laboratorio Virtual
        de Métodos Instrumentales**.

        En este espacio no vamos simplemente a estudiar
        instrumentos.

        Vamos a **construirlos conceptualmente,
        experimentar con ellos, calibrarlos y utilizarlos
        para resolver problemas ambientales**.
        """
    )

    st.divider()

    st.header("🧠 Nuestra forma de aprender")

    st.markdown(
        """
        Cada método seguirá aproximadamente este recorrido:

        ### FENÓMENO
        ↓
        ### INSTRUMENTO
        ↓
        ### SEÑAL
        ↓
        ### MODELO
        ↓
        ### CALIBRACIÓN
        ↓
        ### MUESTRA DESCONOCIDA
        ↓
        ### PROBLEMA AMBIENTAL
        """
    )

    st.divider()

    st.header("🧭 Nuestro laboratorio")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success(
            """
            ### ⚡ Potenciometría

            **DISPONIBLE**

            5 misiones

            Desde el potencial eléctrico
            hasta una campaña ambiental.
            """
        )

        st.info(
            """
            **Instrumento construido:**

            pH-metro virtual
            """
        )

    with col2:

        st.markdown(
            """
            ### ⚖️ Electrogravimetría

            🔒 Próximamente

            **Pregunta futura:**

            ¿Podemos determinar cuánto analito
            existe convirtiéndolo en materia
            y pesándolo?
            """
        )

        st.markdown(
            """
            ### 📉 Polarografía

            🔒 Próximamente

            **Pregunta futura:**

            ¿Qué información química podemos
            obtener estudiando corriente y potencial?
            """
        )

    with col3:

        st.markdown(
            """
            ### 🧬 Cromatografía

            🔒 Próximamente

            ¿Cómo podemos separar una mezcla
            para descubrir qué contiene?
            """
        )

        st.markdown(
            """
            ### 🌈 Espectroscopía

            🔒 Próximamente

            ¿Qué podemos aprender observando
            cómo la materia interactúa con
            la radiación?
            """
        )

    st.divider()

    st.markdown(
        """
        ### 🔬 Métodos que iremos incorporando

        **Potenciometría** ✓

        Electrogravimetría · Polarografía ·
        Cromatografía · Cromatografía gaseosa ·
        HPLC · Espectrometría de masas ·
        UV-Visible · Infrarrojo ·
        Absorción atómica
        """
    )

    st.success(
        """
        ### Idea central

        Un instrumento no genera conocimiento
        simplemente porque produce un número.

        Debemos comprender **qué mide, cómo lo mide,
        cómo se calibra y qué podemos concluir
        a partir de sus datos**.
        """
    )


# ============================================================
# DEFINICIÓN DE PÁGINAS
# ============================================================

pagina_inicio = st.Page(
    inicio,
    title="Inicio",
    icon="🏠",
    default=True
)


mision_01 = st.Page(
    "modulos/potenciometria/mision_01.py",
    title="Misión 01 · Electricidad",
    icon="⚡"
)

mision_02 = st.Page(
    "modulos/potenciometria/mision_02.py",
    title="Misión 02 · Nernst",
    icon="📈"
)

mision_03 = st.Page(
    "modulos/potenciometria/mision_03.py",
    title="Misión 03 · pH-metro",
    icon="🧪"
)

mision_04 = st.Page(
    "modulos/potenciometria/mision_04.py",
    title="Misión 04 · Calibración",
    icon="🎯"
)

mision_05 = st.Page(
    "modulos/potenciometria/mision_05.py",
    title="Misión 05 · Investigá el río",
    icon="🌊"
)


# ============================================================
# NAVEGACIÓN
# ============================================================

pg = st.navigation(
    {
        "Laboratorio": [
            pagina_inicio
        ],

        "⚡ Potenciometría": [
            mision_01,
            mision_02,
            mision_03,
            mision_04,
            mision_05
        ]
    }
)


pg.run()
