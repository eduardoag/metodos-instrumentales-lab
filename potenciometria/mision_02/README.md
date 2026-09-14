# MISIÓN 02 — La ecuación de Nernst

## Métodos Instrumentales — Ingeniería Ambiental

En la Misión 01 aprendimos que un sistema potenciométrico
mide una diferencia de potencial entre un electrodo indicador
y un electrodo de referencia.

Ahora aparece una nueva pregunta:

> ¿Por qué la composición química de una muestra puede
> modificar el potencial de un electrodo?

La ecuación de Nernst establece la conexión entre
el equilibrio químico y el potencial eléctrico.

---

# 1. Objetivos de aprendizaje

Al finalizar esta misión, el estudiante debería poder:

- interpretar la ecuación de Nernst;
- identificar sus variables;
- relacionar actividad química y potencial;
- comprender el efecto de la temperatura;
- comprender el efecto del número de electrones;
- reconocer el carácter logarítmico de la respuesta;
- diferenciar actividad y concentración;
- calcular una actividad desconocida a partir de un potencial.

---

# 2. La conexión fundamental

En potenciometría buscamos transformar información química
en una señal eléctrica medible.

Actividad química
        ↓
Equilibrio electroquímico
        ↓
Potencial del electrodo
        ↓
Instrumento
        ↓
Datos
        ↓
Información química

La ecuación de Nernst describe matemáticamente
una parte fundamental de esta transformación.

---

# 3. Ecuación de Nernst

Para una reacción electroquímica:

E = E° - (RT/nF) ln(Q)

donde:

E  = potencial en las condiciones del experimento

E° = potencial estándar

R  = constante universal de los gases

T  = temperatura absoluta en kelvin

n  = número de electrones intercambiados

F  = constante de Faraday

Q  = cociente de reacción

---

# 4. ¿Qué es Q?

Q es el cociente de reacción.

Su expresión depende de la reacción química considerada.

Para una reacción general:

aA + bB ⇌ cC + dD

podemos escribir conceptualmente:

Q = (a_C^c · a_D^d) / (a_A^a · a_B^b)

donde a representa actividad química.

Las actividades de sólidos puros y líquidos puros
se toman como unidad en el tratamiento termodinámico usual.

---

# 5. Forma logarítmica

Como:

ln(x) = 2.303 log10(x)

podemos escribir:

E = E° - (2.303 RT/nF) log10(Q)

A 25 °C:

T = 298.15 K

y:

2.303 RT/F ≈ 0.05916 V

Por lo tanto, para n = 1 aparece una magnitud
aproximada de:

59.16 mV por década

El signo concreto de la pendiente depende de cómo
se haya escrito la reacción y, por tanto, de Q.

---

# 6. Nuestro sistema simplificado

En el simulador utilizamos conceptualmente:

M^(n+) + n e- ⇌ M(s)

Para este caso:

E = E° + (RT/nF) ln(a)

y:

E = E° + (2.303 RT/nF) log10(a)

Esto permite estudiar fácilmente el efecto
de la actividad sobre el potencial.

---

# 7. Actividad y concentración

La ecuación de Nernst está formulada rigurosamente
en términos de actividad química.

Podemos expresar:

a_i = γ_i (c_i / c°)

donde:

a_i = actividad

γ_i = coeficiente de actividad

c_i = concentración

c° = concentración estándar

En una solución suficientemente ideal:

γ_i ≈ 1

pero en sistemas reales esta aproximación puede dejar
de ser válida.

Esto es especialmente importante en muestras ambientales.

---

# 8. Experimento A — Una década

Configurar:

T = 25 °C
n = 1
E° = 0 mV

Evaluar:

a = 1
a = 0.1
a = 0.01
a = 0.001
a = 0.0001

Registrar:

| Actividad | log10(a) | E (mV) |
|----------:|---------:|-------:|
| 1         | 0        |        |
| 0.1       | -1       |        |
| 0.01      | -2       |        |
| 0.001     | -3       |        |
| 0.0001    | -4       |        |

Pregunta:

¿Cuánto cambia aproximadamente E cada vez que
la actividad disminuye diez veces?

---

# 9. Experimento B — Número de electrones

Mantener:

T = 25 °C
E° = 0 mV

Comparar:

n = 1
n = 2
n = 3

Registrar la pendiente obtenida.

| n | Pendiente aproximada (mV/década) |
|--:|----------------------------------:|
| 1 |                                   |
| 2 |                                   |
| 3 |                                   |

Pregunta:

¿Qué relación existe entre n y la pendiente?

---

# 10. Experimento C — Temperatura

Mantener:

n = 1
E° = 0 mV

Comparar:

5 °C
15 °C
25 °C
35 °C
45 °C

Pregunta:

¿Cómo cambia la pendiente cuando aumenta la temperatura?

---

# 11. Experimento D — Efecto de E°

Mantener constantes:

T
n
actividad

Modificar solamente E°.

Pregunta:

¿Cambia la pendiente de la recta?

¿O cambia su posición vertical?

---

# 12. Preguntas de discusión

1. ¿Por qué la relación entre actividad y potencial
   no es lineal cuando representamos E frente a actividad?

2. ¿Por qué aparece una recta cuando representamos
   E frente a log10(actividad)?

3. ¿Por qué debemos utilizar kelvin en la ecuación?

4. ¿De dónde surge el famoso valor de 59.16 mV?

5. ¿Es 59.16 mV una constante universal?

6. ¿Qué ocurre si n = 2?

7. ¿Por qué actividad y concentración no son
   exactamente lo mismo?

---

# 13. Idea fundamental

La potenciometría no mide directamente una concentración.

Mide una señal eléctrica.

La ecuación de Nernst proporciona un modelo que relaciona
esa señal con el estado químico del sistema.

QUÍMICA → ELECTRICIDAD → INFORMACIÓN

---

# 14. Pregunta abierta

Hasta ahora hicimos:

actividad conocida → potencial

Pero en un análisis químico real normalmente queremos
resolver el problema contrario:

potencial medido → actividad desconocida

Ese será nuestro próximo desafío.
