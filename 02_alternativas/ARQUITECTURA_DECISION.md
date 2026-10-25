# E2 — Arquitectura (v2, 25-oct-2026)

## 1. ¿Tan poco equipo cubre la zona?
**En distancia, sí.** La casa más lejana está a 382 m de la torre central; un radio sectorial de 5 GHz alcanza más de 1 km con línea de vista. Lo que limita no es el alcance sino: (a) el **relieve** (el centro es el punto más bajo, 206 m vs 215–247 m en las esquinas), (b) la **vegetación** (copas de 20–25 m entre las casas), (c) las **casas cercanas** a la torre (20 de 109 a ≤ 100 m, fuera del haz vertical) y (d) la **capacidad** por sector.

Por eso el diseño tiene pocos equipos, pero cada decisión se calcula: 3 sectores co-ubicados con plan de frecuencias, enlaces por tramo de distancia, pérdida por follaje, ángulo de inclinación, interferencia entre sectores, enlace de subida y capacidad.

## 2. Decisión (preliminar, validar con perfiles en E3)
- **1 torre central** en el claro (15.88908, -90.53177) con **Starlink + 3 sectores 5 GHz de 120°**.
- Sectores (azimut desde el norte), balanceados por casas:

| Sector | Azimut | Casas | Dist. máx. |
|---|---|---|---|
| S1 | 95°–215° (este-sur-suroeste) | 31 | 365 m |
| S2 | 215°–335° (oeste-noroeste) | 39 | 382 m |
| S3 | 335°–95° (norte-noreste) | 39 | 364 m |

Figura: `11_informe_latex/figuras/fig_aldea_sectores_prelim.png`. Lista por casa: `01_comunidad_demanda/casas_109_coordenadas_aprox.csv`.
- **Altura de torre provisional: 24 m** (para presupuestar). Con el modelo de terreno preliminar, a 18 m unas 25 casas quedarían con el techo sobre la punta de la torre; a 24 m unas 12; a 30 m unas 7. Ese modelo sobrestima el relieve (usa esquinas en bosque), así que la altura final sale de los perfiles reales.
- **Contingencia con regla de decisión:** si en E3 más del 10 % de las casas no cumple despeje del 60 % de la primera zona de Fresnel con copas de 20 m, se añade un **Nodo Este** (zona alta, ~247 m) alimentado por enlace punto a punto 5 GHz desde la torre. Si no, se mantiene una sola torre.
- **Una CPE por casa** (exterior, 20–23 dBi, a ~6 m sobre el techo) + router Wi-Fi interior. Capacidad de diseño: 109 CPE (65 el año 1).
- **2 hotspots comunitarios** (lugares por definir; la escuela figura cerrada en Maps).
- **Un solo Starlink Business** (Prioridad Local); segundo terminal en fase 2 si el uso pico supera el 70 %.

## 3. Alternativas comparadas
| | A — Torre central PtMP 5 GHz (elegida) | B — Malla Wi-Fi exterior |
|---|---|---|
| Topología | 1 torre, 3 sectores, CPE por casa | 8–10 nodos en postes, multisalto |
| Sitios con energía solar | 1 | 8–10 |
| Capacidad | Predecible; 28–35 Mbps pico por sector | Cae con cada salto |
| Riesgo | Línea de vista a los extremos | Mantenimiento y robo de nodos; latencia |
| Costo relativo | Menor | Mayor (energía por nodo) |

## 4. Equipos a fijar con datasheet (siguiente paso)
| Rol | Cantidad | Tipo preliminar |
|---|---|---|
| Backhaul satelital | 1 | Starlink Business (Estándar o Alto Rendimiento: **confirmar en tienda**) |
| Radio + antena sectorial 5 GHz | 3 | PtMP, sector 120° (o 90° + solape), ~16–18 dBi, inclinación mecánica |
| Switch/router PoE | 1 | Con 4–6 puertos PoE |
| CPE exterior | 109 (65 año 1) | 5 GHz, 20–23 dBi |
| Router Wi-Fi interior | 109 | Wi-Fi 5/6 económico |
| Hotspots | 2 | AP exterior 2.4/5 GHz |
| Torre | 1 | Ventada, 24 m (provisional) |
| Energía | 1 sistema | FV + LiFePO₄ (E5) |

## 5. Herramientas
- **CloudRF**: principal (cobertura, enlaces, clutter/vegetación, exportables).
- **UISP Design Center**: apoyo para línea de vista y Fresnel (comparación basada en conocimiento general; se confirma al usarla).
- **Google Earth Pro**: perfiles de elevación, KMZ.
- **Python/Excel**: cálculos propios, siempre; el simulador se usa para contrastar.
