# Guía paso a paso: contraste con CloudRF (4 enlaces)

Los nombres de menús (Site/Tx, Mobile/Rx, Clutter, Output, Path Profile Tool, Run) salen de la documentación oficial de CloudRF: https://cloudrf.com/documentation/04-web-interface-functions.html. Las etiquetas exactas de cada campo pueden variar un poco; si algo no coincide, mándame una captura.

## Qué se compara
Pérdida de trayecto (*Path Loss*, dB) y potencia recibida (*Received Power*, dBm) de 4 enlaces torre → casa. Para que solo se compare la propagación, cada enlace usa como ganancia de transmisión la **ganancia efectiva** que ya calculé (incluye la pérdida del patrón de la antena hacia esa casa).

| Enlace | Casa | Lat Rx | Lon Rx | Dist. | Ganancia Tx a usar | Mi pérdida sin follaje | Mi pérdida con follaje | Mi Pr esperada* |
|---|---|---|---|---|---|---|---|---|
| 1 | 26 | 15.889468 | −90.535463 | 398 m | 15.1 dBi | 99.7 dB | 140.9 dB | −76.6 dBm |
| 2 | 43 | 15.889521 | −90.531682 | 50 m | −2.8 dBi | 82.4 dB | 82.4 dB | −36.0 dBm |
| 3 | 55 | 15.890135 | −90.530678 | 165 m | 14.1 dBi | 92.1 dB | 99.5 dB | −36.3 dBm |
| 4 | 93 | 15.889282 | −90.528014 | 402 m | 5.0 dBi | 99.8 dB | 109.4 dB | −55.2 dBm |

\*Mi Pr incluye 0.5 dB de jumpers, 1 dB de desalineación y 0.3 dB de lluvia, que CloudRF no incluye; espera una diferencia de ≈ 1.8 dB solo por eso.

## Datos comunes
- Torre (Tx): lat 15.889081, lon −90.531767; altura de antena 30 m sobre el suelo; frecuencia 5800 MHz; potencia 28 dBm (0.63 W).
- Casa (Rx): altura 6 m; ganancia 23 dBi; sensibilidad −93 dBm.

## Pasos
1. Entra a https://cloudrf.com e inicia sesión. Abre la interfaz web (mapa).
2. En el menú **Site/Tx** escribe la latitud y longitud de la torre, la altura (30 m), la frecuencia (5800 MHz), la potencia (28 dBm) y la ganancia de antena del enlace (tabla de arriba).
3. Pulsa el botón **Path Profile Tool** del Function Menu.
4. En el menú **Mobile/Rx** escribe la latitud y longitud de la casa, altura 6 m y ganancia 23 dBi.
5. Primera corrida, **sin vegetación**: en el menú **Clutter** deja el modo sin clutter (o desactívalo) y pulsa **Run**.
6. Captura de pantalla donde se vean el perfil (Terrain, Fresnel, LOS) y los datos *Distance, Frequency, Model, Path Loss, Received Power*. Guarda también el enlace **PNG** si aparece.
7. Segunda corrida, **con vegetación**: en **Clutter** activa un modo que use la capa de vegetación (por ejemplo *Soft/NLOS* con una atenuación mínima) y vuelve a pulsar **Run**. Captura igual.
8. Repite los pasos 2 a 7 para las 4 casas (8 capturas en total). En cada enlace cambia solo la ganancia Tx y la casa.
9. Anota en la tabla: Path Loss y Received Power de cada corrida y el modelo que CloudRF indique (por ejemplo ITM).
10. Envíame las 8 capturas (o la tabla llena). Con eso completo la Tabla 11 del informe y la diapositiva de validación.

## Cómo se interpreta
- Sin vegetación debe salir cerca de mi pérdida sin follaje (± 3 a 4 dB; CloudRF suma pérdidas por difracción y suelo).
- Con vegetación, CloudRF y Weissberger usan modelos distintos: se espera una diferencia mayor; lo importante es comparar el orden de magnitud y explicar la diferencia.
