# PLAN MAESTRO — Proyecto Final Antenas y Propagación 2026

**Universidad del Istmo · Ing. Victor Hugo Alvarado · Evaluación final: jueves 5 nov 2026**
**Hoy (inicio): jueves 22 oct 2026 → quedan 14 días.**
**Equipo declarado: 3 integrantes (Integrante A, B, C — ver sección 6).**

---

## 0. Concepto original del proyecto (propuesta)

**"Aldea Conectada Solar"**: una red comunitaria Wi-Fi alimentada 100 % por energía solar, cuya fuente de Internet es un terminal **Starlink Business** instalado en un sitio elevado, con **3 sectores 5 GHz PtMP** para distribuir a las viviendas y **hotspots Wi-Fi 2.4/5 GHz** en puntos comunitarios (escuela, salón comunal).
Se presenta como un proyecto de un **operador ya legalizado ante la SIT** (supuesto declarado), que lo implementa como programa de inclusión digital rural.

Lo que lo hace original: (1) sistema integrado conectividad + energía (dimensionamiento FV/baterías propio), (2) comparación de dos arquitecturas técnicamente distintas con matriz ponderada, (3) análisis de lluvia/vegetación tropical, (4) capa legal SIT, (5) análisis de sensibilidad y de crecimiento de demanda.

---

## 1. Qué pide el documento y cómo lo agrupé (lo repetitivo, unificado)

El PDF repite varias veces las mismas exigencias (secciones 4, 5–8, 10, Anexo A y Anexo B). Las consolidé en **7 bloques de trabajo**. Cada bloque produce evidencia que se reutiliza en informe, Excel, presentación y planos.

| Bloque | Qué incluye | Rúbrica (pts) | Carpeta |
|---|---|---|---|
| B1 Comunidad y demanda | Aldea, mapa, 300 hab → viviendas → clientes → tráfico pico, metas | 8 | 01 |
| B2 Alternativas | 2 arquitecturas, criterios, matriz, elección | 6 | 02 |
| B3 Antenas y patrones | Inventario, fichas, HPBW, F/B, lóbulos, sectorización, plan de frecuencias | 18 + 12 = 30 | 03 |
| B4 Propagación y link budget | FSPL, Fresnel, vegetación, lluvia, perfiles, EIRP, margen, uplink | 14 + 14 = 28 | 04 |
| B5 Cobertura, capacidad, interferencia | Mapas RF, hogares servidos, backhaul, SINR | 8 + 7 = 15 | 05 |
| B6 Simulación y sensibilidad | Radio Mobile/CloudRF/UISP, contraste con cálculo propio, 2 sensibilidades | 7 | 06 |
| B7 Costos, energía, legal | BOM, CAPEX/OPEX en Q, solar, marco SIT | 4 | 07, 08, 09 |
| Informe y defensa | LaTeX/PDF, PPTX, script de 3 integrantes | 2 | 11, 12 |

Peso crítico: **criterios 03–06 = 58 puntos** → son la prioridad técnica. Costos pesan poco (4 pts): se hacen aproximados pero coherentes.

---

## 2. Etapas y calendario (22 oct → 5 nov)

| Etapa | Fechas | Entregables internos | Quién interviene |
|---|---|---|---|
| **E0 Arranque** | Jue 22 oct | Repo, plan, decisiones preliminares, fuentes iniciales | Claude (hecho) |
| **E1 Aldea y demanda** | 22–23 oct | Aldea elegida con coordenadas reales, mapa, tabla de supuestos, demanda pico | **Tú**: verificar aldea en Google Earth (ver TAREAS_USUARIO) |
| **E2 Alternativas y diseño RF** | 24–25 oct | Matriz A vs B, topología, selección de antenas/radios, fichas | Claude + tú validas precios en tiendas |
| **E3 Propagación y link budget** | 26–27 oct | Perfiles de terreno, Fresnel, FSPL, link budget por trayecto, uplink | **Tú**: exportar perfiles de Google Earth/Radio Mobile |
| **E4 Patrones, cobertura y capacidad** | 28 oct | Patrones H/V, mapas, capacidad por sector, interferencia | Claude calcula; **tú** corres simulación en Radio Mobile/CloudRF |
| **E5 Energía, costos, legal** | 29 oct | Dimensionamiento FV, BOM, CAPEX/OPEX, legal SIT | Claude + verificación de precios |
| **E6 Sensibilidades y validación** | 30 oct | 2 sensibilidades, tabla metas vs resultados, contraste simulador/cálculo | Claude + tú |
| **E7 Informe LaTeX + XLSX + KMZ** | 31 oct–2 nov | PDF, Excel con fórmulas, KMZ, planos | Claude; tú compilas en Overleaf si hace falta |
| **E8 Presentación y script** | 3 nov | PPTX + guion de 3 voces | Claude; tú ensayas |
| **E9 Revisión final** | 4 nov | Checklist Anexo A, QA de cifras | Ambos |
| **Evaluación** | **Jue 5 nov** | Entrega y defensa | Equipo |

Nota: el documento dice que los hitos intermedios no son obligatorios; esto es solo organización nuestra.

---

## 3. Decisiones técnicas PRELIMINARES (se confirman con datos reales en E1–E3)

| Tema | Decisión preliminar | Motivo |
|---|---|---|
| Backhaul | **Starlink Business** (Local o Global Priority), 1 terminal en sitio elevado | Aldea sin fibra; Starlink con licencia SIT desde mayo 2023 |
| Acceso | **5 GHz PtMP, 3 sectores de 120°** (Alt. A) | Cubre ~360°, pocas antenas (pedido del docente) |
| Alternativa B | **Wi-Fi mesh outdoor (6–8 nodos omni/semi-sector 5 GHz + 2.4 GHz)** | Técnicamente distinta: sin torre, topología multisalto |
| Terminal usuario | CPE 5 GHz de 20–23 dBi + router Wi-Fi interior | Mejor margen que Wi-Fi directo |
| Puntos comunitarios | 2 hotspots (escuela y salón) | Valor social, cubre quienes no tengan CPE |
| Energía | Solar FV + baterías LiFePO₄ en la torre; ~24 h autonomía + 1 día nubes | Aldea sin red confiable |
| Torre | Mástil/torre ventada de ~12–18 m según Fresnel | Se fija con perfil real |
| Legal | Operador ORC SIT existente; banda de uso libre 5 GHz/2.4 GHz; Starlink con título propio | Ver `08_legal_SIT` |

**Pendiente de verificar con fuentes oficiales**: Qué bandas exactamente declara de uso libre la TNAF vigente de Guatemala (no pude confirmarlo aún). No lo afirmaremos hasta tener la cita.

---

## 4. Datos ya investigados (con fuentes)

- Starlink Guatemala: planes Residencial Lite desde Q365, Max desde Q545, Roam 100 GB Q410, Roam Ilimitado Q820 (precios leídos 1 oct 2026) — <https://livinginguatemala.com/digital-nomad/starlink-in-guatemala/>
- Lanzamiento de Starlink en Guatemala: 14 jul 2023; SIT autorizó el 19 may 2023 — <https://www.revistaeyn.com/tecnologia-cultura-digital/starlink-llega-a-guatemala-con-precios-especiales-DC14436342>
- Alza de precios Starlink 2026 (EE. UU.; tendencia, no precios GT) — <https://www.satelliteinternet.com/resources/starlink-2026-price-increase/>
- Requisitos para servicios satelitales (licencia de proveedor, usuario de facilidades satelitales, registro ORC) — artículo 2022, a verificar en SIT — <https://www.bloomberglinea.com/2022/11/16/starlink-de-elon-musk-en-guatemala-que-necesita-para-que-pueda-operar/>
- Marco legal: Decreto 94-96 (LGT), Acuerdo Gubernativo 574-98 (reglamento satelital), sanciones art. 81 — <https://livinginguatemala.com/guides/satellite-messengers-guatemala>
- TNAF administrada por la SIT — <https://dplnews.com/?p=270771>
- Censo 2018: solo 29 % de personas de 7+ años usa Internet; brechas fuertes en Alta Verapaz y Quiché — <https://dplnews.com/censo-refleja-brechas-en-el-uso-de-internet/>

**Aviso de honestidad**: las cifras del Business plan de Starlink Guatemala (Local/Global Priority) y el precio estándar del kit NO están confirmadas; hay que leerlas en <https://www.starlink.com/gt/business> o en el checkout con una dirección real (ver TAREAS_USUARIO).

---

## 5. Cómo se verá cada entregable del PDF del curso

| # | Entregable | Archivo | Etapa |
|---|---|---|---|
| 1 | Informe técnico PDF | `11_informe_latex/main.tex` | E7 |
| 2 | Memoria de cálculos XLSX (fórmulas visibles) | `04_propagacion_linkbudget/memoria_calculos.xlsx` | E3–E6 |
| 3 | Proyecto de simulación + capturas | `06_simulacion/` | E4 |
| 4 | Fichas de equipos | `13_fichas_equipos/` (enlaces + PDFs) | E2 |
| 5 | Planos y KMZ | `10_cartografia_kmz/` | E3 |
| 6 | Presupuesto valorizado | `07_costos/presupuesto.xlsx` | E5 |
| 7 | Presentación + guion 3 voces | `12_presentacion_defensa/` | E8 |
| 8 | Evidencia física | **No aplica** (Modalidad A: Simulación) — se justifica | — |

**Modalidad elegida: A (Simulación)**, con cálculos propios en Python/Excel contrastados contra el simulador.

---

## 6. Reparto simulado entre 3 integrantes

- **Integrante A — RF y antenas**: antenas, patrones, plan de frecuencias, link budget.
- **Integrante B — Terreno, simulación y capacidad**: aldea, perfiles, Fresnel, mapas, capacidad, interferencia, sensibilidades.
- **Integrante C — Energía, costos, legal y documentación**: solar, BOM, CAPEX/OPEX, marco SIT, informe y bibliografía.
- Todos participan en la defensa; el guion de 3 voces va en `12_presentacion_defensa/guion.md` (E8).

(Usa tus nombres reales cuando me los digas.)

---

## 7. Cuidado con una IA calificadora

- Cada cifra con **unidad, fuente y método**.
- Trazabilidad: la hoja de Excel y el PDF deben dar **los mismos números**.
- Coherencia de cantidades (3 sectores = 3 antenas en inventario, BOM, mapa, link budget).
- No presentar datos inventados como medidos: lo simulado se rotula como simulado.
- Reconocer limitaciones (p. ej., rain fade en Ku de Starlink, estimaciones de adopción).

---

## 8. Próximo paso inmediato

1. Confirmar la aldea (ver `TAREAS_USUARIO.md`, Tarea 1).
2. Con coordenadas reales, descargo/obtengo elevaciones y empiezo E1–E2.
