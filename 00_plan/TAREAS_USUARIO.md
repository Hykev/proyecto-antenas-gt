# TAREAS PARA TI (actualizado 27-oct-2026)

## Lo que ya está listo
- **Excel** (`12_excel_memoria/Memoria_Calculo_Babilonia.xlsx`): 12 hojas con fórmulas visibles.
- **Informe en LaTeX** (`11_informe_latex/informe.tex`, ya compilado: `informe.pdf`, 24 páginas).
- **Presentación** de 17 diapositivas (artefacto en Claude, descargable como PPTX/PDF) y **guion de 3 voces** (`13_presentacion/GUION_3_VOCES.md` y `Guion_3_voces.docx`).
- Código de la simulación: `04_propagacion_linkbudget/` (Python).

## TAREA 1 (necesito de ti, ≈ 20 min): contrastar 4 enlaces con CloudRF
El profesor pide contrastar al menos un cálculo con una herramienta de RF. Abre tu cuenta de CloudRF (https://cloudrf.com), crea un enlace punto a punto ("Path"/"Link") por cada fila y apunta los resultados. Parámetros comunes:
- **Transmisor (torre):** lat 15.889081, lon −90.531767; altura de antena 30 m sobre el suelo; frecuencia 5800 MHz; potencia 28 dBm (0.63 W); ganancia de antena 15.5 dBi.
- **Receptor (casa):** altura 6 m; ganancia 23 dBi; sensibilidad −93 dBm.
- Modelo de propagación: el que ofrezca por defecto (p. ej. ITM/Longley-Rice). Corre cada enlace **dos veces**: sin clutter/vegetación y con clutter (vegetación) si la opción existe.

| Enlace | Casa | Lat | Lon | Dist. | Mi modelo (FSPL / Pr con Tx 28 dBm) |
|---|---|---|---|---|---|
| 1 | 26 | 15.889468 | −90.535463 | 398 m | 99.7 dB / −76.6 dBm (incluye 41.2 dB de follaje) |
| 2 | 43 | 15.889521 | −90.531682 | 50 m | 82.4 dB / −36.0 dBm |
| 3 | 55 | 15.890135 | −90.530678 | 165 m | 92.1 dB / −36.3 dBm |
| 4 | 93 | 15.889282 | −90.528014 | 402 m | 99.8 dB / −55.2 dBm |

**Qué me mandas:** una captura de cada resultado (donde se vea la pérdida de trayecto en dB y la potencia recibida en dBm). Con eso completo la Tabla 11 del informe y agrego una diapositiva de validación. Si CloudRF no deja poner 15.5 dBi, usa la opción de antena genérica más cercana y dime cuál.

## TAREA 2 (opcional, 5 min): verificar horas solar pico
Supuse 3.5 kWh/m²/día en el mes menos soleado. Verifica en https://power.larc.nasa.gov/data-access-viewer/ (parámetro "ALLSKY_SFC_SW_DWN", coordenadas 15.889, −90.532) y dime el valor del mes más bajo; si es menor de 3.0 ajusto los paneles.

## TAREA 3 (antes del 5-nov): ensayar con tus compañeros
Cada quien lee su parte del guion (`Guion_3_voces.docx`): Kevin diapositivas 1–7 (6.5 min), Maximiliano 8–13 (6.75 min), Diego 14–17 (4 min).

## Pendiente de decisión del profesor (si lo mencionas en clase)
Población ≈ 380 (95 viviendas × 4.0). Si pide ≈ 300: 3.2 hab/vivienda (`DECISIONES.md`, D03).
