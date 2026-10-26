# E3 — Fichas técnicas de los equipos de radio (26-oct-2026)

Valores tomados de hojas de datos de fabricante o distribuidores (enlaces abajo). Lo que **no** aparece en la hoja de datos se marca como supuesto.

## 1. Radio de la estación base: Ubiquiti Rocket Prism 5AC Gen2 (RP-5AC-Gen2) ×3
| Parámetro | Valor |
|---|---|
| Banda | 5150–5875 MHz; canales PtMP 10/20/30/40 MHz |
| Potencia Tx máx. | 28 dBm |
| Sensibilidad (±2 dB, canal de 40 MHz) | BPSK 1/2 −96 · QPSK 1/2 −95 · QPSK 3/4 −92 · 16QAM 1/2 −90 · 16QAM 3/4 −86 · 64QAM 2/3 −83 · 64QAM 3/4 −77 · 64QAM 5/6 −74 · 256QAM 3/4 −69 · 256QAM 5/6 −65 dBm |
| Consumo / alimentación | 9.5 W, PoE pasivo 24 V |
| Conectores / sincronía | 2×RP-SMA, GPS |
| Tamaño / peso | 88×40×230 mm, 400 g |
| Precio referencia | US$307.78 (PanaCompu, Panamá; sin existencias el día de consulta) |

Fuente (F24): https://www.netxl.com/ubiquiti/docs/Rocket%20Prism%20AC%20Gen2%20Datasheet.pdf

**Supuesto:** la tabla de sensibilidad es para 40 MHz; para 20 MHz se mejora +3 dB en teoría, pero se aplica la penalización inversa (−3 dB) para ser conservadores (D18).

## 2. Antena sectorial: Ubiquiti AM-5G16-120 ×3 (elegida)
| Parámetro | Valor |
|---|---|
| Ganancia | 15.0–16.0 dBi (se usa 15.5) |
| Banda | 5.10–5.85 GHz |
| Ancho de haz horizontal / vertical (a 6 dB) | 137° / 118° (el plano elevación indicado como 8° eléctrico) |
| Inclinación de fábrica | 4° |
| Aislamiento de polarización cruzada | ≥ 22 dB |
| VSWR | ≤ 1.5:1 |
| Dimensiones / peso | 367×63×41 mm, 1.1 kg |
| Viento | 26 N a 160 km/h; resiste 200 km/h |
| Precio | US$79 (MSRP Ubiquiti) |

Fuente (F25): https://uk.store.ui.com/uk/en/products/am-5g1

**Relación con la física:** una apertura lineal uniforme de largo L tiene ancho de haz ≈ 0.886·λ/L. Con λ = 5.17 cm (5.8 GHz) y L = 0.367 m resulta 7.2°, coincidente con el valor de hoja de datos (8°). Es un arreglo de elementos en la dimensión vertical y un reflector que da el ancho de 120° en horizontal.

**No disponible en la hoja de datos:** relación frente/espalda y lóbulos laterales. Se supone un tope de 25 dB (D18) y se advierte en el informe.

### Alternativa evaluada: AM-5G19-120 (18.6–19.1 dBi, haz vertical 4°, 5.9 kg, ~AUD 294)
Fuente (F26): https://www.csd.com.au (ficha del distribuidor). Con 1–2° de inclinación mecánica conecta 109/109 casas con margen mínimo 14–15 dB; sin inclinación pierde 1–2 casas y es más sensible al montaje. Pesa cinco veces más (carga sobre la torre). **Descartada.**

## 3. CPE: Ubiquiti LiteBeam 5AC Gen2 (LBE-5AC-Gen2) ×109
| Parámetro | Valor |
|---|---|
| Ganancia | 23 dBi, doble polaridad |
| Potencia Tx máx. | 25 dBm (se usan 25 dBm; 3 dB por debajo del AP) |
| Sensibilidad máx. | −96 dBm |
| Consumo | 7 W, PoE pasivo 24 V |
| Dimensiones / peso | 358×272×272 mm, 0.98 kg |
| Temperatura / viento | −40 a 70 °C, 200 km/h |
| Precio | US$64.83 (CDW) |

Fuente (F27): https://store.ui.com y distribuidor CDW. No se encontró el ancho de haz en la hoja; se **deriva** ≈ 70·λ/D ≈ 10° (D = 0.358 m).

## 4. Resumen del enlace elegido (ver `04_propagacion_linkbudget/linkbudget_por_casa.csv`)
- Torre 30 m, copa 20 m, 5.8 GHz, inclinación mecánica 0°.
- Casas con enlace útil (margen ≥ 10 dB): **109/109** en bajada y subida.
- Margen BPSK mínimo / mediano: bajada 16.4 / 45.1 dB; subida 13.4 / 42.1 dB.
- MCS en bajada: 256QAM 5/6 en 47 casas, 256QAM 3/4 en 20, 64QAM en 40, 16QAM en 2.
- Utilización de aire en hora pico (año 3): S1 44 %, S2 48 %, S3 34 % bajada; 18 / 21 / 13 % subida.
- Casas a ≤ 100 m (14): ángulo de elevación hasta 20°; con la inclinación total de 4° y haz de 8° quedan con 256QAM, salvo la 42 y la 49 y la 51 que bajan un escalón.
