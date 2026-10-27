# E3 — Resultados: presupuesto de enlace, plan de frecuencias, interferencia y sensibilidad (26-oct-2026)
Scripts: `linkbudget.py`, `exportar_linkbudget.py`, `analisis_e3.py`. Datos: `linkbudget_por_casa.csv`, `interferencia_por_casa.csv`, `sensibilidad_escenarios.csv`. Figuras en `11_informe_latex/figuras/`.

## 1. Plan de frecuencias (D19)
| Sector | Acimut eje | Canal (centro) | Ancho | Pol. | Tx AP |
|---|---|---|---|---|---|
| S1 | 150° | 5745 MHz | 20 MHz | doble (H/V, MIMO 2×2) | hasta 28 dBm (según MCS) |
| S2 | 270° | 5785 MHz | 20 MHz | doble | idem |
| S3 | 30° | 5825 MHz | 20 MHz | doble | idem |
Canales separados 40 MHz entre sí, sincronía GPS en los tres radios (misma relación de tramas TDD, evita interferencia entre bajada y subida). Supuesto: derechos de uso del espectro disponibles para el análisis académico; la parte regulatoria se trata en la sección legal.

## 2. Interferencia entre sectores
Modelo: potencia interferente = potencia del sector propio − (ganancia propia − ganancia del sector vecino hacia esa casa); rechazo de canal adyacente 30 dB [S]; ruido −95 dBm (20 MHz, NF 6 dB [S]).
| Escenario | Casas sin MCS usable | MCS típico | Utilización aire bajada S1/S2/S3 |
|---|---|---|---|
| **3 canales (plan)** | **0** | 256QAM 3/4–5/6 en 57 casas; 64QAM en 50 | 46 / 48 / 36 % |
| 1 solo canal (reúso 1) | 40 | 16QAM 1/2 o peor | 95 / 144 / 80 % |
En reúso 1 la relación portadora/interferencia (C/I) cocanal tiene mínimo 0 dB, mediana 8 dB y p10 1 dB: los sectores de 120° casi no se aíslan entre sí con el F/B supuesto de 25 dB. Con tres canales el plan cumple y la bajada pasa de 94 % a 46–48 % de utilización máxima. **Esto justifica el plan de tres canales.**

## 3. Sensibilidad (config. AM-5G16-120, inclinación 0°)
| Escenario | Casas con enlace útil ↓ y ↑ | Margen mín. ↓ / ↑ (dB) | Casas > 30 dB de follaje |
|---|---|---|---|
| **Base: torre 30 m, copa 20 m** | **109** | **16.4 / 13.4** | 4 |
| Torre 24 m | 108 | 11.3 / 8.3 | 11 |
| Torre 36 m | 109 | 20.1 / 17.1 | 2 |
| Copa 15 m | 109 | 25.5 / 22.5 | 1 |
| Copa 25 m | 108 | 8.7 / 5.7 | 16 |
| Copa 25 m + torre 24 m (peor combinación) | 106 | 2.7 / −0.3 | 19 |
| Desvanecimiento extra 6 dB | 108 | 10.4 / 7.4 | 4 |
| Error de montaje +2° | 109 | 14.4 / 11.4 | 4 |
| Error de montaje +4° | 105 | 6.6 / 3.6 | 4 |
**Lectura:** el diseño base aguanta copas hasta ≈ 22 m y errores de 2°; con copas de 25 m, 1 casa (la 26) cae bajo 10 dB y se aplica la contingencia D08 (≤ 6 casas bajo 10 dB: mástil de 10 m o CPE PowerBeam). La torre de 24 m no es suficiente en el peor escenario, lo que confirma D07 (30 m).

## 4. Crecimiento de la demanda (utilización de aire en bajada, S1/S2/S3)
| Escenario | S1 | S2 | S3 |
|---|---|---|---|
| Año 1 (60 % de adopción, 4 Mbps pico) | 29 % | 32 % | 23 % |
| Año 3 (90 %) | 44 % | 48 % | 34 % |
| Año 5 (100 %, 6 Mbps pico) | 73 % | 81 % | 57 % |
| Año 5 (100 %, 8 Mbps pico) | 97 % | 107 % | 76 % |
Con 6 Mbps de pico el diseño aguanta; con 8 Mbps el sector S2 se satura: acción de crecimiento = cuarto sector o segundo radio por sector (decisión futura, fuera de CAPEX inicial).
