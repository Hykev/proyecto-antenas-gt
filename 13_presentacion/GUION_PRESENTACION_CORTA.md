# Guion: presentación corta (5 minutos)

**Proyecto:** Internet para Babilonia, Chisec, Alta Verapaz · **Presentan:** Kevin, Maximiliano y Diego
**Tono:** casual, sin tecnicismos. Cada quien habla ~1:40 min.

---

## PARTE 1. Lo que se dice (≈ 5 min)

### Slide 1 · Portada — Kevin (15 s)
"Hola profe, hola a todos. Somos Kevin, Maximiliano y Diego. Va a ser una presentación cortita: qué hicimos, qué retos tuvimos cada uno y qué aprendimos."

### Slide 2 · Qué hicimos — Kevin (45 s)
*(imagen: diagrama del sistema)*
"Babilonia es una aldea de Chisec con casi nada de internet. Diseñamos cómo llevárselo: Starlink trae la señal del satélite, una torre de 30 metros la reparte con tres antenas, cada una cubre una parte de la aldea, y cada casa tiene una antenita pequeña. Es una simulación, pero con cálculos reales."

### Slide 3 · Reto de Kevin — Kevin (40 s)
*(imagen: mapa de casas numeradas)*
"Mi parte fue la arquitectura. Comparé dos ideas: una torre con tres sectores o muchos postes con WiFi. Ganó la torre porque necesita menos equipos. Luego tuve que repartir las casas en tres zonas, como se ve en el mapa, y apuntar cada antena. Lo más difícil fue escoger equipos reales y que las cuentas dieran."

### Slide 4 · Reto de Maximiliano — Maximiliano (50 s)
*(imagen: pérdida por follaje vs. altura de torre)*
"Yo me encargué de la señal. El reto fue la vegetación: la selva se come señal. Calculé cuánta se pierde y cómo mejora si subimos la torre. Con 30 metros todas las casas se pueden conectar; con una torre más baja varias quedarían mal."

### Slide 5 · Reto de Maximiliano, parte 2 — Maximiliano (45 s)
*(imagen: simulación CloudRF de una casa)*
"Para no confiar solo en mis cuentas las comparé con un simulador en línea, CloudRF. Sin árboles coincidimos casi exacto. Con árboles el simulador es más optimista que nosotros; preferimos ser cautelosos, y lo ideal sería medir en la aldea."

### Slide 6 · Reto de Diego — Diego (60 s)
*(imagen: gráfica de costos)*
"Yo vi el dinero y la ley. Armé la lista de equipos con precios aproximados y calculé cuánto cobrar al mes para que el proyecto se sostenga. Instalar cuesta unos Q3,131 por hogar. También revisé que fuera legal: la SIT regula las frecuencias en Guatemala y Starlink ya está autorizado. Lo difícil fue que algunos precios son estimados."

### Slide 7 · Lo que aprendimos — los tres (35 s)
- **Kevin:** "Cada decisión técnica cambia el costo."
- **Maximiliano:** "El terreno y los árboles mandan."
- **Diego:** "Hay que cuidar presupuesto y ley desde el principio."
- **Todos:** "Trabajar juntos evita errores. Gracias, ¿preguntas?"

---

## PARTE 2. RESPALDO — NO SE DICE EN LA PRESENTACIÓN
*Solo para responder si el profesor pregunta qué hizo cada quien. Explicado en palabras simples.*

### Kevin González — arquitectura y antenas
- **Qué hizo:** decidió el diseño general: una torre de 30 m con 3 sectores de 120° y Starlink como conexión a internet; comparó con la alternativa de WiFi mesh en 8–10 postes.
- **Cómo:** ubicó las 109 casas, las repartió en 3 sectores (38, 39 y 32 casas) y eligió equipos reales (radios Ubiquiti Rocket Prism, antenas sectoriales y una antena LiteBeam por casa).
- **Si preguntan "¿por qué una torre?":** menos equipos, menos mantenimiento y cobertura suficiente para todas las casas.

### Maximiliano González — propagación y simulación
- **Qué hizo:** calculó si la señal llega a cada casa (pérdida en el aire, árboles, ángulo de la antena) y comparó con CloudRF.
- **Resultado:** las 109 casas quedan con enlace útil; margen mínimo de unos 13–16 dB. Sin árboles coincide con CloudRF (±1.3 dB); con árboles nuestro modelo es más conservador.
- **Si preguntan "¿qué es el margen?":** cuánta señal sobra por encima del mínimo para funcionar; más margen = más estable con lluvia o niebla.

### Diego Cuellar — costos y marco legal
- **Qué hizo:** lista de equipos con precios, costo de instalación y gasto mensual; tarifa propuesta; revisión de la ley.
- **Cifras:** inversión ≈ Q306,860 (≈ US$40,100), ≈ Q3,131 por hogar; gasto mensual ≈ Q7,862; tarifa propuesta Q150/mes; recuperación ≈ 45 meses.
- **Legal:** la SIT regula el espectro (Ley General de Telecomunicaciones, Decreto 94-96); usamos la banda de 5 GHz; Starlink ya fue autorizado en Guatemala. Suponemos que somos una empresa ya legalizada. Detalles de potencia máxima: por confirmar con la SIT.
- **Si preguntan por electricidad/paneles solares:** quedó fuera del alcance; se asume que el sitio ya tiene energía.

### Preguntas probables
1. **¿Es real o simulado?** Simulación con datos y precios reales, contrastada con CloudRF.
2. **¿Cuántas personas se conectan?** 109 casas; capacidad usada: ~44–48 % por sector, 68 % en Starlink.
3. **¿Qué mejorarían?** Medir la altura real de los árboles en la aldea y pedir cotizaciones locales.
