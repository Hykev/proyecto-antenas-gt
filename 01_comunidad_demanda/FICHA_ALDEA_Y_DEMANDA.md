# E1 — Ficha de la aldea y modelo de demanda (v3, 26-oct-2026)

## 1. Identificación
- **Aldea Babilonia**, municipio de Chisec, departamento de Alta Verapaz, Guatemala. (El mapa de Starlink la rotula "Nueva Babilonia"; en el informe se usa *Babilonia* y se menciona la otra denominación una vez.)
- Centro (claro central, sitio de la torre): **15.889081, -90.531767**, elevación **206 m s. n. m.**
- Sin registro de censo específico (INE, Censo 2018, no desagrega a este nivel). Población y viviendas son **supuestos de diseño** declarados.
- Evidencia: `14_fuentes/evidencias/`.

## 2. Geometría
Esquinas aportadas (haversine): lados norte/sur 742/749 m, oeste/este 245/205 m, 16.7 ha, eje largo inclinado ≈ 5.7° respecto al este-oeste.
Con la calibración de la sección 4, las casas ocupan ≈ 810 × 320 m (más que el rectángulo de esquinas, que era aproximado).

## 3. Terreno (elevaciones medidas con Google Earth)
**Puntos:** centro 206 m · esquina sup. izq. 215 m · **sup. der. 239 m (confirmado)** · inf. izq. 227 m · inf. der. 247 m.

**Perfiles torre ↔ casa** (las capturas P1, P3, P4, P5, P6 estaban dibujadas casa → torre; se invirtieron; la captura 6 era un duplicado de la 5):

| Perfil | Casa | Largo medido | Azimut torre→casa | Elev. casa | Mín.–máx. |
|---|---|---|---|---|---|
| P1 | 25 (oeste) | 422.2 m | 281.0° | ≈ 209.5 m | 205.2–210.7 |
| P2 | 93 (este) | 405.9 m | 87.1° | **237.9 m** | 206.1–237.9 |
| P3 | 55 (norte) | 160.0 m | 42.3° | 211.6 m | 206.1–211.6 |
| P4 | 5 (sur) | 200.9 m | 232.9° | ≈ 205.6 m | 205.2–206.1 |
| P5 | 109 (sureste) | 404.8 m | 99.7° | **236.5 m** | 206.0–236.5 |
| P6 | 31 (noroeste) | 338.2 m | 294.3° | 214.9 m | 205.6–214.9 |

**Lectura del relieve:** el terreno es una **hondonada casi plana a 205–212 m** (oeste, norte, sur y centro), con **subida brusca en el extremo este**: de ≈ 218 m a 331 m del centro a ≈ 237 m a 405 m. Las casas del extremo este (93, 109 y vecinas) están ≈ 30 m **por encima** de la base de la torre. Con terreno desnudo, la línea de vista desde una torre de ≥ 3 m a todas las casas está libre (`los_altura_minima_por_casa.csv`): **el relieve no es el factor limitante; lo es la vegetación.**
Terreno interpolado (RBF) desde perfiles + esquinas + centro; error en las 6 casas de control ≤ 1 m; fuera de las líneas medidas la incertidumbre es de ≈ ±3 m.

## 4. Viviendas: 109 numeradas y georreferenciadas
- 109 edificaciones numeradas 1–109 sobre la imagen (`casas_numeradas_109.png`); posiciones colocadas a mano por Kevin una a una. Márgenes de error declarados: imagen desactualizada, casas en construcción, casas tapadas por árboles, y dificultad para distinguir una casa grande de dos adyacentes.
- Detección automática de los 109 marcadores y transcripción de sus números (109 únicos).
- **Calibración:** ajuste de similitud con los 6 vectores torre-casa medidos en Google Earth: escala **0.514 m/px**, rotación −0.07° (norte arriba), torre en el píxel (829, 291). Residuos en las casas de control: 2–9 m (distancias) y < 3° (azimuts). El resto de casas hereda la precisión del ajuste y la de los marcadores: **≈ ±10 m**.
- Archivos: `casas_109_coordenadas_aprox.csv`, `10_cartografia_kmz/babilonia_preliminar.kmz`, `10_cartografia_kmz/generar_geo.py`.

**Distancia a la torre central:** mín. 50 m · mediana 198 m · p90 354 m · **máx. 420 m**.
| Distancia | Casas |
|---|---|
| < 50 m | 1 |
| 50–100 m | 13 |
| 100–200 m | 41 |
| 200–300 m | 28 |
| 300–400 m | 23 |
| 400–500 m | 3 |

## 5. Vegetación (determinante)
- Máscara de copas por color sobre la foto satelital: **53 %** de la imagen es copa de árboles (`04_propagacion_linkbudget/analisis_los.py`). Supuestos: copa de 20 m; los últimos 10 m antes del CPE no cuentan (se monta el CPE en un mástil sobre el techo, en el lado más despejado).
- Pérdida por follaje (Weissberger, 5.8 GHz) de rayo que atraviesa copas, según altura de torre:

| Torre | Profundidad mediana / p90 | Pérdida mediana / p90 / máx. | Casas con > 30 dB |
|---|---|---|---|
| 12 m | 33 / 104 m | 17.1 / 33.6 / 54.3 dB | 19 |
| 18 m | 33 / 104 m | 17.1 / 33.6 / 54.3 dB | 18 |
| 24 m | 27 / 85 m | 15.2 / 29.9 / 45.7 dB | 11 |
| **30 m** | **18 / 73 m** | **12.0 / 27.4 / 41.2 dB** | **4** |
| 36 m | 15 / 62 m | 10.8 / 24.8 / 37.8 dB | 2 |

- Casas más afectadas con 30 m: **26 (41 dB), 27 (37), 97 (31), 30 (30)**; a continuación 5, 6, 3, 104, 107. Se tratan en el presupuesto de enlace (E3).

## 6. Población (supuestos, `00_plan/DECISIONES.md` D03)
109 edificaciones → **95 viviendas habitadas** (≈ 87 %; el resto: tiendas, iglesia, bodegas, edificios comunitarios o secundarios) × **4.0 hab/vivienda** (nacional 2018: 4.5) = **≈ 380 habitantes** (+27 % sobre 300). Puntos de servicio de diseño: **109**.

## 7. Starlink en la zona (capturas del 23-oct-2026)
Disponible ahora · descarga 145–276 Mbps · subida 21–39 Mbps · latencia 22–32 ms · diseño con 145 / 21 Mbps / 32 ms.
Prioridad Local: 50 GB Q310 · 500 GB Q870 · 1 TB Q1,570 · 2 TB Q2,970 · +50 GB Q140/mes. Plato: Performance (Gen 3), ver `07_costos/plato_starlink_referencia.md`; accesorios: `07_costos/precios_starlink_accesorios_GTQ.csv`.

## 8. Modelo de demanda
| Parámetro | Año 1 | Año 3 (diseño) |
|---|---|---|
| Puntos con CPE | 65 (60 %) | 98 (90 %) + 2 hotspots |
| Consumo mensual por punto | 25 GB | 25 GB |
| **Consumo mensual total** | **≈ 1.6 TB** | **≈ 2.55 TB** |
| Simultaneidad hora pico | 25 % | 25 % |
| Tasa por usuario activo (↓ / ↑) | 4 / 0.5 Mbps | 4 / 0.5 Mbps |
| **Pico agregado ↓ / ↑** | **65 / 8 Mbps** | **98 / 12 Mbps** |
| Uso del backhaul (↓ / ↑) | 45 % / 39 % | 68 % / 58 % |
| Pico por sector S1 / S2 / S3 (37 / 39 / 33 casas) | — | 33 / 35 / 30 Mbps |

Plan Starlink: año 1 Prioridad Local 2 TB (**Q2,970/mes**); año 3 2 TB + 11 bloques de 50 GB = **Q4,510/mes**. Segundo terminal en fase 2 si el uso pico supera el 70 %.

## 9. Metas medibles
1. ≥ 95 % de los 109 puntos con enlace útil (margen ≥ 10 dB sobre el umbral del MCS elegido).
2. ≥ 25 Mbps por punto en hora pico (año 3).
3. Autonomía energética 24 h + 1 día nublado; disponibilidad ≥ 99 %.
4. CAPEX y OPEX dentro del presupuesto de E5.
