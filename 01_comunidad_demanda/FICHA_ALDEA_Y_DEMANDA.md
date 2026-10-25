# E1 — Ficha de la aldea y modelo de demanda (v2, 25-oct-2026)

## 1. Identificación
- **Aldea Babilonia**, municipio de Chisec, departamento de Alta Verapaz, Guatemala. (El mapa de Starlink la rotula "Nueva Babilonia"; en el informe se usa *Babilonia* y se menciona la otra denominación una vez.)
- Centro (claro central): **15.889081, -90.531767**, elevación **206 m s. n. m.**
- Sin registro de censo específico (INE, Censo 2018, no desagrega a este nivel). Población y viviendas son **supuestos de diseño** declarados.
- Evidencia: `14_fuentes/evidencias/`.

## 2. Geometría (esquinas aportadas, fórmula haversine)
| Dato | Valor |
|---|---|
| Lado norte / sur | 742 m / 749 m |
| Lado oeste / este | 245 m / 205 m |
| Área aproximada | 16.7 ha |
| Orientación del eje largo | ≈ 5.7° respecto al este-oeste (baja hacia el este) |
| Distancia centro → esquinas | 368, 402, 386, 402 m |

## 3. Terreno: 5 elevaciones medidas (Google Earth)
| Punto | Coordenadas | Elevación | Evidencia |
|---|---|---|---|
| Centro (claro) | 15°53'20.7"N 90°31'54.4"W | **206 m** | `elev_centro_206m.png` |
| Esquina sup. izq. | 15°53'25.1"N 90°32'05.9"W | 215 m | `elev_esquina_sup_izq_215m.png` |
| Esquina sup. der. | 15°53'22.8"N 90°31'41.0"W | **239 m** | `elev_esquina_sup_der_239m.png` |
| Esquina inf. izq. | 15°53'17.3"N 90°32'06.9"W | 227 m | `elev_esquina_inf_izq_227m.png` |
| Esquina inf. der. | 15°53'16.1"N 90°31'41.7"W | 247 m | `elev_esquina_inf_der_247m.png` |

> Nota: en el mensaje se indicó 214 m para la esquina sup. der.; la captura muestra **239 m**. Se usa 239 m (evidencia). Confirmar.

**Lectura del relieve.** El centro es el punto **más bajo** de las 5 mediciones: las cuatro esquinas están 9–41 m más arriba, más hacia el este/sureste (239–247 m). La vista oblicua (`earth_vista_oblicua_babilonia.png`) muestra la aldea en una hondonada abierta al sur, con lomas boscosas al norte. Consecuencia de diseño: desde una torre central, los extremos quedan "cuesta arriba" y hay que verificar línea de vista con perfiles reales (E3).

Modelo de terreno **preliminar** (ajuste cuadrático a las 5 alturas, solo para ordenar ideas): elevación estimada de las casas entre 203 y 238 m, **incertidumbre ≈ ±10 m**. No se usa para resultados finales; se reemplaza por perfiles de Google Earth/CloudRF.

**Vegetación (supuesto):** árboles de copa de 20–25 m entre casas y bosque de 25–30 m en los bordes (observación en imágenes; Google Earth no muestra relieve de copas). A validar.

## 4. Viviendas: 109 contadas y numeradas
- Conteo visual: **109 edificaciones** numeradas 1–109 (`casas_numeradas_109.png`, figura del informe).
- Posiciones aproximadas: detecté automáticamente los 109 marcadores (109 de 109) y transcribí sus números (todos únicos). Georreferenciación con norte arriba, escala 0.465 m/px (±10 %) y ancla en el centro del claro ⇒ **posición ±30 m**. Archivos: `casas_109_coordenadas_aprox.csv`, `10_cartografia_kmz/babilonia_preliminar.kmz` (abrir en Google Earth y corregir), script `10_cartografia_kmz/generar_geo.py`.
- Distancia a la torre central: mínima 49 m, mediana 179 m, p90 319 m, **máxima 382 m**.

| Distancia a la torre | Casas |
|---|---|
| < 50 m | 1 |
| 50–100 m | 19 |
| 100–200 m | 41 |
| 200–300 m | 33 |
| 300–400 m | 15 |

## 5. Población (supuestos, ver `00_plan/DECISIONES.md` D03)
| Parámetro | Valor |
|---|---|
| Edificaciones contadas | 109 |
| Viviendas habitadas | 95 (≈ 87 %); el resto: tiendas, iglesia, bodegas, edificios comunitarios o secundarios |
| Personas por vivienda | 4.0 (referencia nacional Censo 2018: 4.5; no se halló el dato de Alta Verapaz) |
| **Habitantes** | **≈ 380** (enunciado de referencia: 300; +27 %, dentro de lo que el profesor dijo aceptable) |
| Puntos de servicio de diseño | **109** (todas las edificaciones pueden tener CPE) |

## 6. Starlink en la zona (capturas del 23-oct-2026)
- Disponible ahora en 15.88908, -90.53177.
- Descarga **145–276 Mbps**; subida **21–39 Mbps**; latencia **22–32 ms**.
- Valores de diseño (límite inferior): **145 / 21 Mbps**, 32 ms.
- Planes Business Prioridad Local: 50 GB Q310 · 500 GB Q870 · 1 TB Q1,570 · 2 TB Q2,970 · +50 GB Q140/mes.

## 7. Modelo de demanda (supuestos explícitos)
| Parámetro | Año 1 | Año 3 (diseño) |
|---|---|---|
| Puntos de servicio con CPE | 65 (60 %) | 98 (90 %) + 2 hotspots comunitarios |
| Consumo mensual por punto | 25 GB | 25 GB |
| **Consumo mensual total** | **≈ 1.6 TB** | **≈ 2.55 TB** |
| Simultaneidad hora pico | 25 % | 25 % |
| Tasa media por usuario activo (bajada / subida) | 4 / 0.5 Mbps | 4 / 0.5 Mbps |
| **Tráfico pico agregado, bajada** | **≈ 65 Mbps** | **≈ 98 Mbps** |
| Tráfico pico agregado, subida | ≈ 8 Mbps | ≈ 12 Mbps |
| Uso del backhaul (145 / 21 Mbps) | 45 % / 39 % | 68 % / 58 % |
| Pico por sector (S1 / S2 / S3), año 3 | 28 / 35 / 35 Mbps (31 / 39 / 39 casas) | |

Plan Starlink: año 1 **Prioridad Local 2 TB** (Q2,970/mes); año 3 2 TB + 11 bloques de 50 GB (Q2,970 + 11 × Q140 = **Q4,510/mes**). Si el uso pico supera el 70 % del backhaul, se añade un segundo terminal (fase 2).

## 8. Metas medibles
1. ≥ 95 % de los 109 puntos con enlace útil (margen ≥ 15 dB) respecto al umbral del MCS elegido.
2. ≥ 25 Mbps por punto en hora pico (año 3).
3. Autonomía energética 24 h + 1 día nublado; disponibilidad ≥ 99 %.
4. CAPEX y OPEX dentro del presupuesto de E5.
(Se afinan en E3–E5.)
