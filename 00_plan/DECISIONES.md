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
