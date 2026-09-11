# MISIÓN 01 — ¿Cómo puede medirse química con electricidad?

## Métodos Instrumentales — Ingeniería Ambiental

Esta misión introduce los fundamentos conceptuales de la potenciometría.

Todavía no utilizaremos la ecuación de Nernst.

El objetivo es comprender primero una idea esencial:

> Un instrumento potenciométrico mide una diferencia de potencial eléctrico entre dos electrodos.

---

# 1. Objetivos de aprendizaje

Al finalizar esta misión, el estudiante debería poder:

- explicar qué es una diferencia de potencial;
- distinguir entre electrodo indicador y electrodo de referencia;
- comprender por qué se necesitan dos electrodos;
- calcular el potencial de una celda sencilla;
- interpretar el signo del potencial medido;
- explicar por qué el electrodo de referencia debe ser estable;
- reconocer que el instrumento mide una señal eléctrica, no directamente una concentración química.

---

# 2. Idea fundamental

La potenciometría permite obtener información química a partir de una señal eléctrica.

El esquema general es:

Sistema químico
↓
Electrodo
↓
Potencial eléctrico
↓
Instrumento
↓
Datos
↓
Información química

En esta primera misión nos concentraremos solamente en la parte eléctrica.

---

# 3. ¿Qué mide el instrumento?

Un voltímetro no mide un potencial eléctrico absoluto.

Mide una diferencia de potencial entre dos puntos.

En potenciometría utilizamos:

- un electrodo indicador;
- un electrodo de referencia.

La diferencia de potencial medida puede expresarse de manera simplificada como:

E_celda = E_indicador - E_referencia

donde:

- E_celda es la diferencia de potencial medida por el instrumento;
- E_indicador es el potencial del electrodo sensible al sistema químico;
- E_referencia es el potencial del electrodo de referencia.

---

# 4. Electrodo indicador

El electrodo indicador es el electrodo cuyo potencial cambia cuando cambian determinadas condiciones químicas de la muestra.

Conceptualmente:

Sistema químico
↓
Electrodo indicador
↓
Cambio de potencial

En esta misión modificaremos manualmente su potencial.

Más adelante aprenderemos por qué una modificación química puede generar ese cambio.

---

# 5. Electrodo de referencia

El electrodo de referencia proporciona un potencial conocido y estable.

Su función puede compararse con el nivel del mar utilizado para medir alturas.

Una altura necesita un punto de referencia.

De manera similar, un potencial eléctrico debe medirse respecto de otro potencial.

Por eso podemos pensar:

Electrodo de referencia = "nivel del mar eléctrico"

---

# 6. La celda potenciométrica

Nuestro sistema conceptual puede representarse así:

                    VOLTÍMETRO
                        │
                        │ mide ΔE
                        │
             ┌──────────┴──────────┐
             │                     │
             │                     │
        ELECTRODO             ELECTRODO
        INDICADOR              REFERENCIA
             │                     │
             │                     │
             └──────────┬──────────┘
                        │
                     MUESTRA

El instrumento mide la diferencia de potencial entre ambos electrodos.

---

# 7. Ejemplo

Supongamos:

E_indicador = 250 mV

E_referencia = 200 mV

Entonces:

E_celda = 250 mV - 200 mV

E_celda = +50 mV

Si ahora:

E_indicador = 150 mV

E_referencia = 200 mV

obtenemos:

E_celda = -50 mV

El signo indica cuál de los dos potenciales es mayor según la convención utilizada.

---

# 8. Experimento virtual

Ejecutar:

```bash
streamlit run app.py
