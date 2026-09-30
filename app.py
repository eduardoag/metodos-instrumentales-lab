import streamlit as st
from datetime import datetime, time
from zoneinfo import ZoneInfo


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Métodos Instrumentales Lab",
    page_icon="🔬",
    layout="wide"
)


# ============================================================
# CONTROL DE ACCESO: ALUMNOS Y DOCENTE
# ============================================================

from datetime import timedelta
from hmac import compare_digest

# Modo temporal de pruebas: True = acceso libre; False = horario y clave activos.
MODO_PRUEBAS = False

TZ_TUCUMAN = ZoneInfo("America/Argentina/Tucuman")
DIA_CLASE = 2  # lunes=0, miércoles=2
HORA_INICIO = time(14, 30)
HORA_FIN = time(17, 30)  # límite exclusivo


def hora_local():
    """Hora real en Tucumán, independiente del servidor de Cloud."""
    return datetime.now(TZ_TUCUMAN)


def horario_de_clase(instante):
    return (
        instante.weekday() == DIA_CLASE
        and HORA_INICIO <= instante.time() < HORA_FIN
    )


def proxima_clase(instante):
    """Próximo miércoles a las 14:30, en hora de Tucumán."""
    dias = (DIA_CLASE - instante.weekday()) % 7
    fecha = instante.date() + timedelta(days=dias)
    comienzo = datetime.combine(fecha, HORA_INICIO, tzinfo=TZ_TUCUMAN)
    if comienzo <= instante:
        comienzo += timedelta(days=7)
    return comienzo


def clave_docente():
    """La contraseña sólo se lee desde Streamlit Secrets."""
    try:
        valor = st.secrets.get("DOCENTE_PASSWORD", "")
        return str(valor) if valor else ""
    except (FileNotFoundError, KeyError):
        return ""


# Se mantiene la autorización sólo en la sesión actual del navegador.
if "docente_autenticado" not in st.session_state:
    st.session_state.docente_autenticado = False


@st.fragment(run_every="1s")
def pantalla_cerrada():
    """Actualiza el contador y abre la app al comenzar la clase."""
    instante = hora_local()
    if horario_de_clase(instante):
        st.rerun(scope="app")

    restante = max(0, int((proxima_clase(instante) - instante).total_seconds()))
    dias, resto = divmod(restante, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)

    st.markdown("### ⏳ Próxima apertura del laboratorio")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Días", f"{dias:02d}")
    c2.metric("Horas", f"{horas:02d}")
    c3.metric("Minutos", f"{minutos:02d}")
    c4.metric("Segundos", f"{segundos:02d}")
    st.caption(f"Hora de Tucumán: {instante:%d/%m/%Y · %H:%M:%S}")


@st.fragment(run_every="10s")
def vigilar_horario():
    """Cierra sesiones estudiantiles al terminar el horario."""
    instante = hora_local()
    if not st.session_state.docente_autenticado and not horario_de_clase(instante):
        st.rerun(scope="app")


ahora = hora_local()
acceso_docente = st.session_state.docente_autenticado
laboratorio_abierto = horario_de_clase(ahora)

if not (MODO_PRUEBAS or laboratorio_abierto or acceso_docente):
    st.title("🔬 Métodos Instrumentales Lab")
    st.warning("🔒 Laboratorio cerrado")
    st.markdown(
        "El laboratorio abre **todos los miércoles de 14:30 a 17:30**, "
        "hora de Tucumán, Argentina."
    )
    pantalla_cerrada()
    st.divider()

    with st.expander("🔑 Acceso privado para el docente"):
        with st.form("formulario_docente", clear_on_submit=True):
            password = st.text_input("Contraseña docente", type="password")
            ingresar = st.form_submit_button("Ingresar al laboratorio")
        if ingresar:
            secreto = clave_docente()
            if not secreto:
                st.error("Falta configurar DOCENTE_PASSWORD en Streamlit Secrets.")
            elif compare_digest(password.encode("utf-8"), secreto.encode("utf-8")):
                st.session_state.docente_autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")

    st.stop()

# Control visible en la barra lateral de la aplicación habilitada.
with st.sidebar:
    if MODO_PRUEBAS:
        st.info("🧪 Modo de pruebas: acceso libre temporal")
    elif acceso_docente:
        st.success("🔑 Sesión docente")
        if st.button("Cerrar sesión docente", key="salir_docente"):
            st.session_state.docente_autenticado = False
            st.rerun()
    else:
        st.success("🟢 Laboratorio abierto · miércoles 14:30–17:30")
        vigilar_horario()

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

            **DISPONIBLE · 5 MISIONES COMPLETAS**

            Desde la construcción de la celda electrolítica
            y la ley de Faraday hasta el control del proceso,
            el pesaje y el análisis de un efluente industrial.
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

        **Potenciometría** ✓ · **Electrogravimetría** ✓ (5 misiones cada una)

        Polarografía ·
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
    icon="⚡",
    url_path="potenciometria_mision_01"
)

mision_02 = st.Page(
    "modulos/potenciometria/mision_02.py",
    title="Misión 02 · Nernst",
    icon="📈",
    url_path="potenciometria_mision_02"
)

mision_03 = st.Page(
    "modulos/potenciometria/mision_03.py",
    title="Misión 03 · pH-metro",
    icon="🧪",
    url_path="potenciometria_mision_03"
)

mision_04 = st.Page(
    "modulos/potenciometria/mision_04.py",
    title="Misión 04 · Calibración",
    icon="🎯",
    url_path="potenciometria_mision_04"
)

mision_05 = st.Page(
    "modulos/potenciometria/mision_05.py",
    title="Misión 05 · Investigá el río",
    icon="🌊",
    url_path="potenciometria_mision_05"
)


electro_mision_01 = st.Page(
    "modulos/electrogravimetria/mision_01.py",
    title="Misión 01 · Celda electrolítica",
    icon="⚖️",
    url_path="electrogravimetria_mision_01"
)

electro_mision_02 = st.Page(
    "modulos/electrogravimetria/mision_02.py",
    title="Misión 02 · Ley de Faraday",
    icon="🧮",
    url_path="electrogravimetria_mision_02"
)


electro_mision_03 = st.Page(
    "modulos/electrogravimetria/mision_03.py",
    title="Misión 03 · Control del proceso",
    icon="🎛️",
    url_path="electrogravimetria_mision_03"
)


electro_mision_04 = st.Page(
    "modulos/electrogravimetria/mision_04.py",
    title="Misión 04 · Pesaje y recuperación",
    icon="⚗️",
    url_path="electrogravimetria_mision_04"
)


electro_mision_05 = st.Page(
    "modulos/electrogravimetria/mision_05.py",
    title="Misión 05 · Efluente industrial",
    icon="🏭",
    url_path="electrogravimetria_mision_05"
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
        ],

        "⚖️ Electrogravimetría": [
            electro_mision_01,
            electro_mision_02,
            electro_mision_03,
            electro_mision_04,
            electro_mision_05
        ]
    }
)


pg.run()
