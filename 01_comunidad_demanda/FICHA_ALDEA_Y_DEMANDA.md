# E1 — Ficha de la aldea y modelo de demanda

## 1. Identificación
- **Aldea Babilonia**, municipio de Chisec, departamento de Alta Verapaz, Guatemala. (El mapa de Starlink la rotula "Nueva Babilonia"; en el informe se usa *Babilonia* y se menciona la otra denominación una vez.)
- Centro aproximado: **15.889081, -90.531767**
- Sin registro de censo específico para la aldea (INE, Censo 2018, no desagrega a este nivel y el portal estuvo caído el 23-oct-2026). Población y viviendas son **supuestos de diseño** declarados.
- Evidencia: `14_fuentes/evidencias/` (capturas Maps y Starlink).

## 2. Geometría (calculada con las 4 esquinas aportadas, fórmula haversine)

| Dato | Valor |
|---|---|
| Lado norte / sur | 742 m / 749 m |
| Lado oeste / este | 245 m / 205 m |
| Área aproximada | 16.7 ha |
| Densidad | ≈ 4.5 viviendas/ha (75 viviendas) |
| Distancia centro → esquinas | 368, 402, 386, 402 m |
| **Alcance máximo requerido desde el centro** | **≈ 400 m** |

Nota: la estimación visual inicial (800 × 271 m) se corrige con el cálculo: ≈ 745 × 225 m. Hay calles que sobresalen del rectángulo; se tratan como margen del 10 %.

Coordenadas locales de las esquinas respecto al centro (x este, y norte, en m): TL (-342, 137) · TR (397, 63) · BR (377, -140) · BL (-372, -105).

## 3. Supuestos de población y viviendas
| Parámetro | Valor | Origen |
|---|---|---|
| Viviendas | 75 (rango 60–75) | Conteo visual en imagen satelital, Kevin, 23-oct-2026 |
| Habitantes | ≈ 300 | Enunciado del curso; equivale a 4.0 hab/vivienda |
| Escuela | Maps marca "Babilonia Chisec" como cerrada permanentemente | Captura Maps; **no se asume escuela operativa** |
| Punto comunitario | Salón comunal / edificio de la antigua escuela (supuesto, por confirmar) | Decisión de diseño |

## 4. Entorno radioeléctrico (de la imagen satelital)
- Vegetación tropical densa alrededor y entre las casas → pérdida por follaje relevante en 5 GHz; se modela en E3.
- Claro abierto cerca del centro (donde Maps marca la aldea): **sitio candidato de la torre**, por confirmar propiedad (supuesto: terreno comunal/municipal).
- Starlink: cobertura "Disponible ahora" y descarga **145–276 Mbps** en la zona (capturas del 23-oct-2026). Para diseñar se usa el límite inferior: **145 Mbps**.

## 5. Modelo de demanda (supuestos explícitos)

| Parámetro | Año 1 | Año 3 (diseño) | Nota |
|---|---|---|---|
| Hogares suscritos | 45 (60 %) | 75 (100 %) | Adopción supuesta |
| Puntos comunitarios | 2 | 2 | Salón comunal + punto de reunión |
| Consumo mensual por hogar | 25 GB | 25 GB | Supuesto rural (mensajería, video SD) |
| Consumo mensual total | ≈ 1.2 TB | ≈ 1.9 TB | 1.125 TB y 1.875 TB + comunitarios |
| Simultaneidad hora pico | 25 % | 25 % | Supuesto |
| Tasa media por usuario activo | 4 Mbps | 4 Mbps | Video SD/HD, supuesto |
| **Tráfico pico agregado** | **≈ 45 Mbps** | **≈ 75 Mbps** | 45×0.25×4 y 75×0.25×4 |
| Uso del backhaul Starlink (145 Mbps) | 31 % | 52 % | Holgado |
| Tráfico pico por sector (3 sectores, 25 casas) | ≈ 25 Mbps | ≈ 25 Mbps | Se contrasta con capacidad real en E4 |

Plan Starlink Business que encaja: **Prioridad Local 2 TB (GTQ 2,970/mes)** en diseño final; Prioridad Local 1 TB (GTQ 1,570/mes) en año 1. Bloques extra de 50 GB a GTQ 140/mes. (Precios de captura oficial, 23-oct-2026.)

## 6. Metas medibles (para la tabla "metas vs resultados")
1. Cobertura de ≥ 95 % de las viviendas con nivel de señal que permita ≥ MCS útil (≥ 25 Mbps por hogar en hora pico).
2. Margen de desvanecimiento ≥ 15 dB en los enlaces sector–CPE.
3. Disponibilidad de energía ≥ 99 % con 24 h de autonomía + 1 día de nubes.
4. Inversión inicial y OPEX mensual dentro del presupuesto calculado en E5.

(Se afinan en E3–E5.)
