# Registro de decisiones y supuestos

| ID | Fecha | Decisión / supuesto | Motivo | Se revisa en |
|---|---|---|---|---|
| D01 | 22-oct | Modalidad A (simulación) con cálculos propios | Rúbrica y medios disponibles | — |
| D02 | 23-oct | Aldea Babilonia, Chisec, Alta Verapaz | Sin fibra, Starlink disponible, relieve interesante | — |
| D03 | 25-oct | 109 edificaciones, 95 viviendas, 4.0 hab/vivienda → ≈ 380 hab | Conteo real; profesor admite más de 300 sin excederse mucho; referencia nacional 4.5 | Si el profesor pide ≈ 300: 3.2 hab/vivienda |
| D04 | 25-oct | 109 puntos de servicio de diseño; adopción 60 % año 1, 90 % año 3 | Dimensiona el peor caso | E5 |
| D05 | 25-oct | Starlink: diseñar con 145 Mbps ↓ / 21 Mbps ↑ / 32 ms (límite inferior) | Capturas Starlink 23-oct | — |
| D06 | 26-oct | 1 torre central + 3 sectores 120° (azimut 90/210/330°) | Pocos equipos, carga equilibrada 37/39/33 casas | E3 |
| D07 | 26-oct | **Torre de 30 m** (antes 24 m provisional) | Pérdida por follaje: 4 casas > 30 dB con 30 m vs 11 con 24 m; 36 m aporta poco | E3 (presupuesto de enlace) |
| D08 | 26-oct | Contingencia: si > 6 casas (≈ 5 %) quedan con margen < 10 dB → CPE mayor/mástil 10 m, luego nodo de relevo este, luego más altura | El relieve no limita; el follaje sí | E3 |
| D09 | 26-oct | Esquina sup. der. = **239 m** (confirmado por Kevin) | Evidencia visual | — |
| D10 | 26-oct | Georreferenciación calibrada con 6 vectores medidos: 0.514 m/px, norte arriba, torre en píxel (829, 291); ±10 m. Se asume que las posiciones colocadas a mano son correctas (márgenes: imagen desactualizada, casas nuevas o tapadas, casas contiguas) | Pedido de Kevin; residuos 2–9 m | — |
| D11 | 25-oct | Copas: 20–25 m entre casas, 25–30 m en bordes | Observación de imágenes | E3 |
| D12 | 26-oct | Vegetación: máscara de color sobre foto satelital, copa 20 m, últimos 10 m ignorados; pérdida con Weissberger a 5.8 GHz | No existe otro dato de copas; modelo citado (F17) | E3: sensibilidad copa 15/20/25 m |
| D13 | 26-oct | **Plato Starlink Performance (Gen 3)** (categoría *Empresas* de la tienda GT; "Alto Rendimiento" = Performance). Precio de planificación US$1,499 ≈ Q11,457 (rebaja a US$999 ≈ Q7,636); consumo de diseño 100 W continuos; fuente avanzada DC opcional (Q1,800) | La tienda GT no vende el plato; fuentes externas F18–F22 | Cuando se vea el precio en la contratación Business |
| D14 | 26-oct | Línea de vista con terreno desnudo libre para las 109 casas; el criterio de diseño es presupuesto de enlace con pérdida por follaje, no despeje de copas | Resultado de `analisis_los.py` | E3 |
| D15 | 26-oct | Router propio (PoE) en la torre; no se compra Router 3 de Starlink | El plato Performance trae Ethernet para routers de terceros (F20); ahorra Q1,100 | E2 |
| D16 | 26-oct | **Sectorial AM-5G16-120 (15.5 dBi, 120°) + Rocket Prism 5AC Gen2**, inclinación mecánica 0° (4° de fábrica), 3 unidades | `linkbudget.py`: 109/109 casas con enlace útil en bajada y subida, margen BPSK mínimo 16.4 dB (↓) / 13.4 dB (↑, casa 26). La AM-5G19-120 (18.9 dBi, haz vertical 4°) da +3 dB pero deja casas cercanas fuera del haz y es sensible a ±1° de error de montaje | E3 (sensibilidad) |
| D17 | 26-oct | **CPE LiteBeam 5AC Gen2 (23 dBi)** en las 109 casas; PowerBeam como mejora para casas 26 y 27 si el margen real baja de 10 dB | Margen mínimo 13.4 dB ya cumple la meta (>= 10 dB) | E3 |
| D18 | 26-oct | Parámetros del modelo (supuestos declarados): sensibilidad −3 dB por 20 MHz, Tx del CPE 3 dB bajo el AP, eficiencia MAC 0.65, 75 % del aire para bajada, F/B y lóbulos laterales limitados a 25 dB (no vienen en la hoja de datos) | Informar como supuestos en el informe | E3 |
| D19 | 26-oct | Plan de frecuencias: S1 5745, S2 5785, S3 5825 MHz, 20 MHz, GPS sync | Con un solo canal 40 casas quedan sin MCS útil (C/I mín. 0 dB); con tres canales 0 | E3 |
