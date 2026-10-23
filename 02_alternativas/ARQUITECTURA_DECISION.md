# E2 — Arquitectura elegida (versión preliminar, se confirma con perfiles de terreno)

## 1. Respuesta corta
- **No se instala Starlink por casa.** Un solo Starlink Business en una torre central alimenta toda la aldea; es lo que hace viable el costo (≈ GTQ 3,000/mes repartidos entre ~75 hogares).
- **Antenas centrales + un receptor pequeño por casa.** Tres antenas sectoriales en la torre y un CPE (antena receptora exterior) en cada vivienda suscrita.
- Además hay **2 puntos comunitarios** (salón comunal y un segundo punto) para quienes aún no tengan CPE.
- Aparte de Starlink hace falta: torre, radios sectoriales, switch PoE/router, CPEs, routers Wi-Fi interiores y sistema solar con baterías.

## 2. Alternativas comparadas (se formaliza con matriz ponderada en el informe)
| | A — Torre central PtMP 5 GHz (elegida) | B — Malla Wi-Fi (mesh) outdoor |
|---|---|---|
| Topología | 1 torre, 3 sectores, CPE por casa | 6–8 nodos en postes, multisalto |
| Antenas "grandes" | 3 sectoriales + CPE | 6–8 nodos omni/semi-sectoriales |
| Ventajas | Pocos puntos con energía, capacidad predecible, control | Sin torre alta, resiliencia |
| Desventajas | Depende de línea de vista; follaje | Cada nodo necesita energía; capacidad cae con saltos; más mantenimiento |
| Energía | 1 sitio solar | 6–8 sitios solares |

## 3. Equipos a decidir con datasheet (E2 completa) — qué necesito de ti después
| Rol | Cantidad | Tipo preliminar |
|---|---|---|
| Backhaul satelital | 1 | Starlink Business, hardware a confirmar en checkout (Estándar vs Alto Rendimiento; el de alto rendimiento es el recomendable para uso fijo continuo, **por confirmar**) |
| Sectores 5 GHz | 3 | Radio PtMP + antena sectorial 90–120°, ~17 dBi |
| Switch/Router PoE | 1 | Router con PoE para alimentar radios |
| CPE por casa | 45 en año 1 (hasta 75) | CPE 5 GHz exterior, 20–23 dBi, PoE |
| Router Wi-Fi interior | 1 por casa | Wi-Fi 5/6 económico |
| Hotspots comunitarios | 2 | AP Wi-Fi 2.4/5 GHz exterior |
| Torre | 1 | Torre/mástil ventado ~18 m (a confirmar con perfiles y copa de árboles) |
| Energía | 1 sistema | FV + LiFePO₄ (E5) |

Precios exactos: cuando te pase los modelos concretos (fin de E2), me das los precios locales.

## 4. Sitio de la torre (preliminar)
Claro central cerca de 15.88908, -90.53177. Alcance máximo ≈ 400 m (esquinas a 368–402 m), dentro del rango típico de un enlace PtMP 5 GHz, pero con follaje denso. Se valida con perfiles de elevación y pérdida por vegetación (E3).

## 5. Herramienta de simulación
- **CloudRF = herramienta principal**: permite definir parámetros de antena/ganancia/potencia, altura, clutter/vegetación, y exportar mapas de cobertura y enlaces para el informe.
- **UISP Design Center = apoyo**: útil para validar línea de vista, zonas de Fresnel y listado de equipos de forma rápida; da menos control de modelo de propagación y de patrones personalizados (esta comparación es de mi conocimiento general, no la he verificado en esta sesión; lo comprobamos al usarlas).
- **Google Earth Pro**: perfiles de elevación y exportación de ubicaciones a KMZ.
- Cálculos propios (Python/Excel) siempre; el simulador se usa para contrastar, no para sustituirlos.
