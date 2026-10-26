# E2 — Arquitectura (v3, 26-oct-2026)

## 1. ¿Tan poco equipo cubre la zona?
**En distancia, sí:** la casa más lejana está a 420 m y un radio de 5 GHz con línea de vista llega a más de 1 km. Los datos medidos muestran que:
- **El relieve no limita:** con terreno desnudo, todas las casas ven la torre (el extremo este queda 30 m más alto que la base, pero el perfil sube de forma suave hasta los últimos ~70 m).
- **La vegetación sí:** 53 % de la imagen es copa y el rayo atraviesa una mediana de 18 m de follaje con torre de 30 m (p90: 73 m).
- **Las casas cercanas** (14 a ≤ 100 m, 2 a ≤ 60 m) quedan fuera del haz vertical y se tratan con inclinación y márgenes.
- **La capacidad** (≈ 30–35 Mbps de pico por sector en el año 3).

Por eso hay pocos equipos, pero cada decisión se calcula: tres sectores co-ubicados, plan de frecuencias, enlaces por rango de distancia, pérdida por follaje, inclinación, interferencia, subida y capacidad.

## 2. Decisión (v3)
- **1 torre central ventada de 30 m** en el claro (15.88908, -90.53177): **Starlink + 3 sectores 5 GHz de 120°**.
- **Por qué 30 m:** con 24 m, 11 casas superarían 30 dB de pérdida por follaje; con 30 m, 4; con 36 m, 2 (poco beneficio extra y más costo). No se intenta "despejar" las copas (haría falta > 100 m): se presupuesta la pérdida.
- **Sectores** (azimut desde el norte), equilibrados por casas:

| Sector | Azimut | Casas | Dist. máx. | Pico año 3 |
|---|---|---|---|---|
| S1 | 90°–210° (este-sur-suroeste) | 37 | 405 m | 33 Mbps |
| S2 | 210°–330° (oeste-noroeste) | 39 | 421 m | 35 Mbps |
| S3 | 330°–90° (norte-noreste) | 33 | 402 m | 30 Mbps |

Figura: `11_informe_latex/figuras/fig_aldea_sectores_prelim.png`.
- **Una CPE por casa** (exterior, 20–23 dBi) en mástil de 6 m sobre el techo (casas con árbol al lado: elegir lado y altura despejados). Capacidad de diseño: 109 CPE (65 el año 1).
- **2 hotspots comunitarios** (lugares por definir; la escuela figura cerrada en Maps).
- **1 Starlink Business** (Prioridad Local) en la torre; plato en tubo con adaptador de tubo; cable Starlink de 45 m. Segundo terminal en fase 2.

## 3. Contingencia con regla de decisión (reemplaza a la regla v2)
Al terminar el presupuesto de enlace (E3) con equipos reales: si **más de 6 casas (≈ 5 %)** quedan con margen < 10 dB, se aplican en orden: (1) CPE de mayor ganancia o mástil de 10 m en esas casas; (2) nodo de relevo en la zona alta del este (≈ 237 m) enlazado por punto a punto; (3) más altura de torre. Casas candidatas: 26, 27, 97, 30, 5, 6, 3, 104, 107.

## 4. Alternativas comparadas
| | A — Torre central PtMP 5 GHz (elegida) | B — Malla Wi-Fi exterior |
|---|---|---|
| Topología | 1 torre, 3 sectores, CPE por casa | 8–10 nodos en postes, multisalto |
| Sitios con energía solar | 1 | 8–10 |
| Capacidad | Predecible; ≈ 30–35 Mbps por sector | Cae con cada salto |
| Efecto del follaje | Un solo trayecto largo por casa | Trayectos cortos pero muchos saltos y puntos de falla |
| Costo relativo | Menor | Mayor (energía y mantenimiento por nodo) |

## 5. Equipos (siguiente paso: fichas técnicas)
| Rol | Cantidad | Tipo preliminar |
|---|---|---|
| Backhaul satelital | 1 | Starlink Standard 4 (o 4X) para Business; kit y consumo: **pendiente de precio** (ver tareas) |
| Radio + antena sectorial 5 GHz | 3 | PtMP, sector 120° (o 90° + solape), ~16–18 dBi, inclinación mecánica |
| Switch/router PoE | 1 | 4–6 puertos PoE |
| CPE exterior | 109 (65 año 1) | 5 GHz, 20–23 dBi, PoE |
| Router Wi-Fi interior | 109 | Wi-Fi 5/6 económico |
| Hotspots | 2 | AP exterior 2.4/5 GHz |
| Torre | 1 | Ventada, 30 m |
| Energía | 1 sistema | FV + LiFePO₄ (E5) |
| Accesorios Starlink | — | Adaptador de tubo Q565, cable 45 m Q1,220, fuente avanzada Q1,800 (opcional según kit) |

## 6. Herramientas
CloudRF (principal) · UISP Design Center (apoyo) · Google Earth Pro (perfiles/KMZ) · Python/Excel (cálculos propios; el simulador contrasta).
