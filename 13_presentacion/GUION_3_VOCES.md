# Guion de la defensa — 3 voces

Proyecto: sistema de antenas y red para la aldea Babilonia (Chisec, Alta Verapaz). Evaluación: 5 de noviembre de 2026. Duración total ≈ 17 min 15 s.

| Persona | Diapositivas | Tiempo aprox. |
|---|---|---|
| Kevin Gabriel González Donis | 1, 2, 3, 4, 5, 6, 7 | 6 min 30 s |
| Maximiliano González De León | 8, 9, 10, 11, 12, 13 | 6 min 45 s |
| Diego Andre Cuellar Butcher | 14, 15, 16, 17 | 4 min 00 s |

Cada diapositiva trae el mismo texto en sus notas de orador. Las cifras salen del libro Memoria_Calculo_Babilonia.xlsx y del informe LaTeX.

## Diapositiva 1. Internet para Babilonia: una torre, tres sectores y Starlink
**Habla: Kevin Gabriel González Donis** · ≈ 30 s

Buenos días. Somos Kevin González, Maximiliano González y Diego Cuellar, y les presentamos el diseño de un sistema de antenas para llevar internet a la aldea Babilonia, en Chisec, Alta Verapaz. La idea en una frase: una sola torre de 30 metros con tres antenas sectoriales en 5 GHz, alimentada por energía solar y conectada a internet con Starlink, que da servicio a las 109 casas de la aldea. Yo explico el problema y la arquitectura; Maximiliano presenta el cálculo de propagación, el presupuesto de enlace y la capacidad; y Diego cierra con energía, costos y marco legal.

## Diapositiva 2. Una aldea de unas 380 personas sin red fija
**Habla: Kevin Gabriel González Donis** · ≈ 60 s

El problema es de acceso. Según el Censo 2018 solo el 29 % de los guatemaltecos usa internet, y las brechas más grandes están en el área rural. Babilonia, en Chisec, Alta Verapaz, no tiene fibra ni red fija. Pero Starlink está disponible: en la página de cobertura de Starlink medimos 145 a 276 Mbps de bajada en las coordenadas de la aldea. Eso nos da una conexión a internet; lo que falta es llevarla desde un punto hasta cada casa. Ese es el problema de antenas que resolvemos. Nos pusimos tres metas medibles: que al menos el 95 % de las casas tenga un enlace útil con 10 dB de margen en bajada y subida, que cada casa pueda tener 25 Mbps en hora pico, y que el sistema tenga dos días de autonomía de energía, con costos calculados y cumpliendo la regulación de la SIT.

## Diapositiva 3. 109 casas georreferenciadas en 800 m
**Habla: Kevin Gabriel González Donis** · ≈ 60 s

Elegimos Babilonia, en Chisec. No hay censo a nivel de aldea, así que contamos las casas sobre la imagen satelital: son 109 edificaciones, que numeramos una por una. Las pasamos a coordenadas con seis vectores torre-casa medidos en Google Earth, con una escala de 0.514 metros por píxel; el error de posición es de unos 10 metros. Aclaramos que la imagen puede estar desactualizada, que puede haber casas en construcción o tapadas por árboles, y que es difícil distinguir una casa grande de dos juntas; tomamos las posiciones como correctas. Suponemos 95 viviendas habitadas por 4 personas, unas 380 habitantes, algo por encima de los 300 de referencia, pero el diseño depende de los puntos de servicio, no de los habitantes. La distancia a la torre va de 50 a 420 metros, con mediana de 198.

## Diapositiva 4. Dos arquitecturas comparadas, una elegida
**Habla: Kevin Gabriel González Donis** · ≈ 60 s

Comparamos dos arquitecturas técnicamente distintas. La A es una torre central con acceso punto-multipunto en 5 GHz: una antena sectorial por zona y una antena direccional en cada casa. La B es una malla Wi-Fi exterior con ocho a diez nodos en postes por toda la aldea. La A necesita energía solar en un solo sitio, tiene capacidad predecible porque cada sector tiene su propio canal, un solo salto de latencia y un presupuesto de enlace que podemos verificar casa por casa. La B necesita energía en cada poste, su capacidad cae con cada salto y hay muchos puntos de falla. Elegimos la A. Su riesgo es que la torre es un punto único de falla, y lo cubrimos con dos días de autonomía de baterías y equipo de repuesto.

## Diapositiva 5. Una torre de 30 m con tres sectores de 120°
**Habla: Kevin Gabriel González Donis** · ≈ 60 s

Así funciona el sistema. Arriba de la torre, a 30 metros, va el plato Starlink Performance de tercera generación, que trae el internet. Por Ethernet baja a un router en un gabinete al pie de la torre, que alimenta por PoE tres radios Rocket Prism, cada uno con una antena sectorial de 120 grados: los sectores S1, S2 y S3, con 38, 39 y 32 casas. Cada casa tiene una antena direccional LiteBeam de 23 dBi en un mástil de 6 metros sobre el techo, apuntando a la torre, y un router Wi-Fi adentro. Además dejamos dos puntos de acceso comunitarios. Todo el equipo de la torre, unos 158 watts, lo alimentan tres paneles solares y dos baterías que Diego explicará al final.

## Diapositiva 6. Inventario de equipos con datos de ficha
**Habla: Kevin Gabriel González Donis** · ≈ 60 s

Estos son los equipos, con datos de las hojas del fabricante. La antena sectorial es la Ubiquiti AM-5G16-120: 15.5 dBi, ancho de haz horizontal de 137 grados medido a 6 dB y 8 grados en vertical, con 4 grados de inclinación de fábrica. Los radios son Rocket Prism 5AC Gen2, con 28 dBm de potencia y sensibilidad de menos 96 a menos 65 dBm según la modulación. Las 109 antenas de casa son LiteBeam de 23 dBi. El plato es Starlink Performance, con 145 Mbps de diseño. También evaluamos la sectorial de 19 dBi: gana 3 dB pero su haz vertical de 4 grados es muy sensible a un error de montaje y pesa casi seis kilos en la torre; la descartamos. Los precios de cada equipo están en el libro de Excel y en el informe, con su fuente.

## Diapositiva 7. Cortes horizontal y vertical de la sectorial
**Habla: Kevin Gabriel González Donis** · ≈ 60 s

Estos son los patrones de radiación de la sectorial. Quiero ser claro con el origen: no son patrones medidos, son un modelo calibrado con los datos de la ficha. En horizontal, la ficha da 137 grados a 6 dB, que son los puntos rojos; eso equivale a unos 97 grados a mitad de potencia. En vertical, la antena es una apertura lineal: para una apertura uniforme el ancho de haz es 0.886 veces la longitud de onda entre la longitud de la antena. Con 5.17 centímetros de longitud de onda y 36.7 centímetros de antena, da 7.2 grados, muy cerca de los 8 grados de la ficha; también salen el primer nulo y los lóbulos laterales a menos 13 dB. La ficha no publica la relación frente-espalda, por eso usamos un tope de 25 dB y verificamos su efecto en la interferencia.

## Diapositiva 8. El relieve ayuda; la vegetación manda
**Habla: Maximiliano González De León** · ≈ 75 s

Medimos en Google Earth las elevaciones del centro y de las cuatro esquinas, y seis perfiles torre-casa. El terreno es una hondonada casi plana, entre 205 y 212 metros, con una subida brusca en el extremo este hasta unos 237 metros. Con terreno desnudo, la línea de vista está libre desde la torre hacia las 109 casas: el relieve no es el problema. El problema es la vegetación: con una máscara de color sobre la foto satelital estimamos que 53 % de la imagen es copa de árbol. Con copas de 20 metros calculamos la pérdida con el modelo de Weissberger: con una torre de 12 metros, 19 casas pasan de 30 dB de pérdida; con 24 metros, 11; con 30 metros, solo 4; con 36, 2. No intentamos despejar las copas, porque eso requeriría más de 100 metros de torre, sino presupuestar esa pérdida. Por eso elegimos 30 metros: la mediana de pérdida por follaje es 12 dB y el máximo, 41 dB, en la casa 26.

## Diapositiva 9. Tres canales evitan la interferencia entre sectores
**Habla: Maximiliano González De León** · ≈ 60 s

Dividimos la aldea en tres sectores de 120 grados con ejes en 150, 270 y 30 grados, que reparten las casas en 38, 39 y 32. Cada sector usa un canal propio de 20 MHz dentro de la banda de 5725 a 5850 MHz: 5745, 5785 y 5825 MHz, con polarización dual y los tres radios sincronizados por GPS para que las tramas de bajada y subida coincidan. Verificamos que esto sea necesario: calculamos, para cada casa, la potencia del sector propio contra la de los sectores vecinos. Con un solo canal para los tres sectores, la relación portadora-interferencia tiene una mediana de apenas 8 dB y 40 casas se quedarían sin enlace útil. Con los tres canales del plan, ninguna casa queda sin enlace.

## Diapositiva 10. Ejemplo del peor caso: casa 26, subida
**Habla: Maximiliano González De León** · ≈ 90 s

Calculamos el presupuesto de enlace para cada una de las 109 casas, en bajada y en subida. La potencia recibida es la potencia de transmisión más la ganancia efectiva de la antena del sector, ya descontados los desfases respecto a su eje, menos pérdidas de jumper, más la ganancia de la antena de casa, menos la pérdida en espacio libre, el follaje, la desalineación y la lluvia. Les muestro el peor caso, la casa 26, en el sector S2, en subida. Está a 398 metros; la ganancia efectiva del sector hacia ella es 15.1 dBi; la pérdida en espacio libre a 5.8 GHz es 99.7 dB; el rayo atraviesa 147 metros de follaje, que con Weissberger son 41.2 dB. Transmitiendo 25 dBm con una antena de 23 dBi, la potencia recibida es menos 79.6 dBm. La sensibilidad de BPSK es menos 96, que con 3 dB de penalización conservadora por el canal de 20 MHz son menos 93: el margen es 13.4 dB, sobre nuestro mínimo de 10. Incluso el peor enlace cumple.

## Diapositiva 11. Las 109 casas tienen enlace útil
**Habla: Maximiliano González De León** · ≈ 60 s

Este es el resultado para toda la aldea. Cada punto es una casa y su color indica la modulación máxima que alcanza en bajada con 10 dB de margen. Las 109 casas, el 100 %, tienen enlace útil tanto en bajada como en subida, así que superamos nuestra meta del 95 %. El margen mínimo es 16.4 dB en bajada y 13.4 dB en subida, y la mediana pasa de 45 dB. Sesenta y siete casas alcanzan 256QAM y las casas más lejanas del oeste, con más follaje, usan 64QAM o 16QAM. Las 14 casas a menos de 100 metros quedan en los lóbulos de elevación de la sectorial, pero su corta distancia mantiene márgenes de más de 39 dB. Como el diseño cumple, no se activa la regla de contingencia que fijamos: mástil de 10 metros o antena mayor si más de seis casas bajaban de 10 dB.

## Diapositiva 12. Cada sector usa menos de la mitad de su aire
**Habla: Maximiliano González De León** · ≈ 60 s

Para la capacidad, suponemos que en el año 3 el 90 % de las casas contrata el servicio, que en hora pico el 25 % está activo a la vez y que cada usuario activo demanda 4 Mbps de bajada y 0.5 de subida. Con la tasa de cada casa según su modulación y una eficiencia del 65 %, el sector S1 usa el 44 % de su aire en bajada, S2 el 48 % y S3 el 34 %. Es decir, hay holgura. El backhaul Starlink, con un pico agregado de 98 Mbps contra los 145 Mbps de diseño, se usa al 68 %. Si la demanda crece a 6 Mbps por usuario activo, el sector más cargado sube a 81 %. Con 8 Mbps, S2 se saturaría y la acción sería añadir un cuarto sector o un segundo radio. Y si el uso del backhaul pasa del 70 %, un segundo terminal Starlink en una fase 2.

## Diapositiva 13. El diseño aguanta copas de 22 m y 2° de error
**Habla: Maximiliano González De León** · ≈ 60 s

Probamos qué pasa si nuestros supuestos fallan. Recalculamos todo el modelo para varios escenarios. Con torre de 36 metros el peor margen sube a 20 dB; con copas de 15 metros, a 25 dB. Con copas de 25 metros, en vez de 20, una sola casa, la 26, cae por debajo de 10 dB y se aplica la contingencia. Con un desvanecimiento adicional de 6 dB por lluvia fuerte o árboles mojados, una casa cae a 7.4 dB en subida. Con un error de montaje de 2 grados de inclinación, las 109 casas siguen conectadas; con 4 grados, 4 casas se pierden, por eso la inclinación se verifica en campo. Y una torre de 24 metros no es suficiente en el peor escenario, lo que confirma la altura de 30 metros.

## Diapositiva 14. La torre se alimenta sola con sol y baterías
**Habla: Diego Andre Cuellar Butcher** · ≈ 60 s

Gracias, Maximiliano. Les cuento cómo se alimenta la torre. La energía no es el foco de este proyecto, así que la dimensionamos de forma sencilla. La carga continua es de unos 158 watts: el plato Starlink con 100 watts, tres radios de 9.5 watts, un router y 10 % de pérdidas de conversión. Son 3.8 kilovatios-hora al día. Con dos días de autonomía y 90 % de profundidad de descarga, necesitamos 8.4 kilovatios-hora, es decir dos baterías de litio-fosfato de hierro de 5.12 kWh, que dan 2.4 días. Para recargar en el mes menos soleado, con unas 3.5 horas solar pico, que es un supuesto típico de la zona, se necesitan 1.44 kilovatios pico: tres paneles de 550 watts. Con esto, la torre es autosustentable sin red eléctrica. El costo aproximado del sistema de energía completo, con paneles, baterías, controlador, inversor y estructura, es de unos 74 mil quetzales, antes de flete e imprevistos.

## Diapositiva 15. Q4,050 por hogar de CAPEX y Q87 al mes de OPEX
**Habla: Diego Andre Cuellar Butcher** · ≈ 75 s

Los costos están en el libro de Excel con cada precio, su estado y su fuente, al tipo de cambio de 7.6445 quetzales por dólar. Algunos precios son publicados, como el plato Starlink, los radios, las antenas y las baterías; otros son estimaciones que deben cotizarse en Guatemala, y así están marcados. El CAPEX de diseño, con 109 puntos equipados, es de unos 397 mil quetzales, unos 52 mil dólares, incluyendo 10 % de flete y aduana y 10 % de imprevistos. Dividido entre los 98 hogares del año 3 son 4,050 quetzales por hogar. La mayor parte son las antenas y la instalación en las casas, seguida por la energía y la torre. El OPEX mensual del año 3 es de 8,530 quetzales: la suscripción Starlink con su plan de 2 terabytes más bloques extra, mantenimiento, un técnico local de medio tiempo, reservas para reponer antenas y baterías, seguro y administración. Por hogar son 87 quetzales al mes. Agregando la amortización del CAPEX a cinco años, la tarifa de equilibrio es de 155 quetzales por hogar al mes. Proponemos 175 quetzales, con lo que el CAPEX se recupera en unos 46 meses.

## Diapositiva 16. Operación como empresa registrada ante la SIT
**Habla: Diego Andre Cuellar Butcher** · ≈ 60 s

Para el marco legal, asumimos que el proyecto lo ejecuta una empresa operadora ya legalizada. La Ley General de Telecomunicaciones, el Decreto 94-96, establece que la Superintendencia de Telecomunicaciones administra el espectro y la Tabla Nacional de Atribución de Frecuencias. Nuestros tres canales, 5745, 5785 y 5825 MHz, están dentro de la banda de 5725 a 5850 MHz, que figura entre las bandas de 5 GHz de Guatemala según una referencia regional; la potencia máxima y las condiciones exactas hay que confirmarlas en la tabla vigente, y lo declaramos así, porque no pudimos acceder al texto oficial. La empresa inscribe el servicio en el registro de telecomunicaciones. Starlink fue autorizado por la SIT en mayo de 2023 y el backhaul se contrata como servicio comercial Business. Además se requiere el acuerdo con la comunidad, a través del COCODE, para el terreno de la torre y el permiso municipal de Chisec para la obra civil. Para el análisis académico, asumimos que los derechos de uso del espectro están disponibles.

## Diapositiva 17. Una torre, tres sectores y todas las casas conectadas
**Habla: Diego Andre Cuellar Butcher** · ≈ 45 s

Para concluir: una sola torre de 30 metros, con tres sectores de 5 GHz y backhaul Starlink, conecta las 109 casas de Babilonia con un margen de al menos 13.4 dB en el peor enlace de subida. El relieve de la hondonada es favorable; la vegetación es lo que determina la altura de la torre y el presupuesto de enlace. Los tres canales con sincronía GPS son necesarios para evitar interferencia entre sectores. El sistema es robusto frente a variaciones razonables y tiene margen para crecer. Cuesta unos 4,050 quetzales por hogar y se sostiene con una tarifa de alrededor de 155 quetzales al mes. Sus limitaciones: los patrones de antena son modelos calibrados con las fichas, la altura de copas es un supuesto y varios precios deben cotizarse localmente. Con esto terminamos; Kevin, Maximiliano y yo estamos listos para sus preguntas. KEVIN responde sobre arquitectura y equipos; MAXIMILIANO sobre propagación, enlace y capacidad; DIEGO sobre energía, costos y marco legal.

## Preguntas frecuentes (reparto)
- **Kevin:** ¿por qué una torre y no una malla? ¿por qué esa antena sectorial? ¿cómo se eligió la aldea?
- **Maximiliano:** ¿cómo se calculó el follaje? ¿qué pasa con las casas cercanas? ¿cómo se validó el modelo? ¿qué supuestos son más sensibles?
- **Diego:** ¿cuánto cuesta por hogar? ¿qué precios son estimados? ¿qué dice la SIT sobre la banda de 5 GHz? ¿cómo se alimenta la torre?
