# ===================== ENERGIA =====================
we = sheet('Energia', [46, 12, 12, 14, 62]); title(we, 'Energía solar de la torre (dimensionamiento breve)', 'No es el foco del proyecto: dimensionamiento simple, costos aproximados. Todo con fórmulas.')
hdr(we, 4, ['Carga en la torre', 'Cantidad', 'Potencia unit. (W)', 'Potencia (W)', 'Fuente / nota'])
loads = [('Starlink Performance Gen 3', 1, 100, 'F18/F21: 75–100 W; se usa el valor alto'), ('Rocket Prism 5AC Gen2', 3, 9.5, 'F24'), ('Router + switch gigabit', 1, 15, 'Supuesto')]
for i, (n, q, p, nt) in enumerate(loads):
    r = 5 + i; put(we, r, 1, n); put(we, r, 2, q, BLUE); put(we, r, 3, p, BLUE); put(we, r, 4, f'=B{r}*C{r}', fmt='0.0'); put(we, r, 5, nt, wrap=True)
EN = {}
def erow(r, lab, val, unit_note, key=None, fmt=None, inp=False, fill=None):
    put(we, r, 1, lab, BOLD); put(we, r, 4, val, BLUE if inp else BLK, fmt, fill); put(we, r, 5, unit_note, wrap=True)
    if key: EN[key] = f'Energia!$D${r}'
erow(8, 'Pérdidas de conversión (inversor, PoE)', 0.10, 'Supuesto 10 %', 'loss', '0%', True)
erow(9, 'Potencia continua total (W)', '=SUM(D5:D7)*(1+D8)', '', 'W', '0.0')
erow(10, 'Energía diaria (kWh/día)', '=D9*24/1000', '', 'kwh', '0.00')
erow(11, 'Autonomía requerida sin sol (días)', 2, 'Decisión: 2 días (meta de disponibilidad ≥ 99 %)', 'aut', '0.0', True, KEY)
erow(12, 'Profundidad de descarga permitida (LiFePO4)', 0.9, 'Supuesto típico LiFePO4', 'dod', '0%', True)
erow(13, 'Capacidad requerida (kWh)', '=D10*D11/D12', '', 'cap', '0.0')
erow(14, 'Capacidad por batería 48 V / 100 Ah (kWh)', 5.12, 'F29: Relion RB48V100 (5.12 kWh)', 'cb', '0.00', True)
erow(15, 'Baterías necesarias (unidades)', '=ROUNDUP(D13/D14,0)', '', 'nbat', '0')
erow(16, 'Horas solar pico, mes más desfavorable (kWh/m²/día)', 3.5, 'SUPUESTO típico de la zona; verificar en NASA POWER (opcional)', 'psh', '0.0', True, KEY)
erow(17, 'Rendimiento global del sistema FV (PR)', 0.75, 'Supuesto típico', 'pr', '0.00', True)
erow(18, 'Potencia FV requerida (kW)', '=D10/(D16*D17)', '', 'kwp', '0.00')
erow(19, 'Potencia por panel (W)', 550, 'Panel monocristalino de 550 W (formato estándar, F30)', 'wp', '0', True)
erow(20, 'Paneles necesarios (unidades)', '=ROUNDUP(D18*1000/D19,0)', '', 'npan', '0')
erow(21, 'Autonomía real con las baterías instaladas (días)', '=D15*D14*D12/D10', '', 'autr', '0.0')
# ===================== BOM =====================
wb_ = sheet('BOM_CAPEX', [40, 15, 9, 9, 12, 8, 14, 15, 15, 38]); title(wb_, 'Lista de materiales y CAPEX (Q)', 'Cantidades y precios en azul. Estado: "Fuente" = precio publicado (ver hoja Fuentes); "Estimación" = precio aproximado del autor, por cotizar.')
hdr(wb_, 4, ['Ítem', 'Categoría', 'Cant. diseño', 'Cant. año 1', 'Precio unit.', 'Moneda', 'Precio unit. (Q)', 'Total diseño (Q)', 'Total año 1 (Q)', 'Estado / fuente'])
bom = [
 ('Starlink Performance (Gen 3), plato', 'Backhaul', 1, 1, 1499, 'USD', 'Fuente F19/F20 (precio de planificación; rebaja a US$999)'),
 ('Adaptador de tubo Starlink', 'Backhaul', 1, 1, 480, 'GTQ', 'Fuente F23 (tienda GT)'),
 ('Cable Starlink Performance 50 m', 'Backhaul', 1, 1, 1300, 'GTQ', 'Fuente F23 (tienda GT)'),
 ('Radio Rocket Prism 5AC Gen2', 'Radio', 3, 3, 307.78, 'USD', 'Fuente F24'),
 ('Antena sectorial AM-5G16-120', 'Radio', 3, 3, 79, 'USD', 'Fuente F25'),
 ('Router PoE + switch central', 'Red', 1, 1, 250, 'USD', 'Estimación'),
 ('Inyectores PoE 24 V para radios', 'Red', 3, 3, 25, 'USD', 'Estimación'),
 ('CPE LiteBeam 5AC Gen2', 'Abonado', 109, 65, 64.83, 'USD', 'Fuente F27'),
 ('Mástil galvanizado 6 m para CPE', 'Abonado', 109, 65, 25, 'USD', 'Estimación'),
 ('Cable UTP exterior 15 m + conectores', 'Abonado', 109, 65, 12, 'USD', 'Estimación'),
 ('Router Wi-Fi interior', 'Abonado', 109, 65, 30, 'USD', 'Estimación'),
 ('Punto de acceso comunitario exterior', 'Comunidad', 2, 2, 179, 'USD', 'Estimación'),
 ('Torre ventada 30 m (obra civil, vientos, pararrayos)', 'Torre', 1, 1, 7500, 'USD', 'Estimación (rango regional US$4,000–8,000)'),
 ('Puesta a tierra y protección contra descargas', 'Torre', 1, 1, 800, 'USD', 'Estimación'),
 ('Cable UTP blindado y accesorios de torre', 'Torre', 1, 1, 250, 'USD', 'Estimación'),
 ('Panel solar 550 W', 'Energía', f'={EN["npan"]}', f'={EN["npan"]}', 165, 'USD', 'Estimación'),
 ('Batería LiFePO4 48 V 100 Ah (5.12 kWh)', 'Energía', f'={EN["nbat"]}', f'={EN["nbat"]}', 3495.95, 'USD', 'Fuente F29'),
 ('Controlador MPPT + inversor 1 kW', 'Energía', 1, 1, 950, 'USD', 'Estimación'),
 ('Estructura de paneles, protecciones y gabinete', 'Energía', 1, 1, 1300, 'USD', 'Estimación'),
 ('Instalación de torre y radios (cuadrilla)', 'Servicios', 1, 1, 3000, 'USD', 'Estimación'),
 ('Instalación de CPE en casas (mano de obra)', 'Servicios', 109, 65, 20, 'USD', 'Estimación'),
 ('Transporte y viáticos', 'Servicios', 1, 1, 1500, 'USD', 'Estimación'),
]
BR0 = 5
for i, (n, cat, qd, q1, pu, mon, st) in enumerate(bom):
    r = BR0 + i; put(wb_, r, 1, n); put(wb_, r, 2, cat); put(wb_, r, 3, qd, BLUE if not str(qd).startswith('=') else BLK); put(wb_, r, 4, q1, BLUE if not str(q1).startswith('=') else BLK)
    put(wb_, r, 5, pu, BLUE, '#,##0.00'); put(wb_, r, 6, mon); put(wb_, r, 7, f'=IF(F{r}="USD",E{r}*{S("fx")},E{r})', fmt='#,##0'); put(wb_, r, 8, f'=C{r}*G{r}', fmt='#,##0'); put(wb_, r, 9, f'=D{r}*G{r}', fmt='#,##0'); put(wb_, r, 10, st, wrap=True)
BRN = BR0 + len(bom) - 1; t = BRN + 2
def trow(r, lab, fd, f1, fmt='#,##0', bold=False, inp=False):
    put(wb_, r, 1, lab, BOLD if bold else BLK)
    for c, f in ((8, fd), (9, f1)):
        put(wb_, r, c, f, BLUE if inp else (BOLD if bold else BLK), fmt, KEY if bold else None)
put(wb_, t, 1, 'Flete, aduana y gastos de importación (% de equipos)', BLK); put(wb_, t, 7, 0.10, BLUE, '0%', KEY); put(wb_, t, 10, 'Supuesto; IVA 12 % se considera acreditable (empresa legalizada)', wrap=True)
put(wb_, t + 1, 1, 'Imprevistos (%)', BLK); put(wb_, t + 1, 7, 0.10, BLUE, '0%', KEY); put(wb_, t + 1, 10, 'Supuesto', wrap=True)
trow(t + 2, 'Subtotal ítems', f'=SUM(H{BR0}:H{BRN})', f'=SUM(I{BR0}:I{BRN})')
trow(t + 3, 'Flete y aduana', f'=H{t+2}*$G${t}', f'=I{t+2}*$G${t}')
trow(t + 4, 'Imprevistos', f'=(H{t+2}+H{t+3})*$G${t+1}', f'=(I{t+2}+I{t+3})*$G${t+1}')
trow(t + 5, 'CAPEX TOTAL (Q)', f'=SUM(H{t+2}:H{t+4})', f'=SUM(I{t+2}:I{t+4})', bold=True)
trow(t + 6, 'CAPEX TOTAL (US$)', f'=H{t+5}/{S("fx")}', f'=I{t+5}/{S("fx")}')
trow(t + 7, 'Hogares con servicio (puntos CPE)', 98, 65, '0', inp=True)
trow(t + 8, 'CAPEX por hogar (Q)', f'=H{t+5}/H{t+7}', f'=I{t+5}/I{t+7}', bold=True)
put(wb_, t + 9, 1, 'Nota: la columna "diseño" equipa 109 puntos (máximo), pero el CAPEX por hogar divide entre los 98 puntos de adopción del año 3.', Font(name=F, italic=True, size=9))
CAPX = f'BOM_CAPEX!$H${t+5}'; CAP1 = f'BOM_CAPEX!$I${t+5}'; CAPH = f'BOM_CAPEX!$H${t+8}'; CAPH1 = f'BOM_CAPEX!$I${t+8}'
cpe_row = BR0 + [b[0] for b in bom].index('CPE LiteBeam 5AC Gen2'); bat_row = BR0 + [b[0] for b in bom].index('Batería LiFePO4 48 V 100 Ah (5.12 kWh)')
# ===================== OPEX =====================
wo = sheet('OPEX_Tarifa', [52, 16, 16, 62]); title(wo, 'OPEX mensual, costo por hogar y tarifa de equilibrio (Q)', 'Plan Starlink: Prioridad Local 2 TB Q2,970/mes + bloques de 50 GB a Q140 (F08).')
hdr(wo, 4, ['Concepto', 'Año 1', 'Año 3', 'Nota'])
put(wo, 5, 1, 'Puntos con servicio (CPE + 2 hotspots)'); put(wo, 5, 2, 67, BLUE); put(wo, 5, 3, 100, BLUE); put(wo, 5, 4, 'Año 1: 65 + 2; año 3: 98 + 2')
put(wo, 6, 1, 'Consumo mensual por punto (GB)'); put(wo, 6, 2, 25, BLUE); put(wo, 6, 3, 25, BLUE); put(wo, 6, 4, 'Supuesto')
put(wo, 7, 1, 'Consumo total (GB/mes)'); put(wo, 7, 2, '=B5*B6', fmt='#,##0'); put(wo, 7, 3, '=C5*C6', fmt='#,##0')
put(wo, 8, 1, 'Bloques extra de 50 GB'); put(wo, 8, 2, '=ROUNDUP(MAX(0,B7-2000)/50,0)', fmt='0'); put(wo, 8, 3, '=ROUNDUP(MAX(0,C7-2000)/50,0)', fmt='0')
put(wo, 9, 1, 'Plan Starlink 2 TB (Q/mes)'); put(wo, 9, 2, 2970, BLUE, '#,##0'); put(wo, 9, 3, 2970, BLUE, '#,##0'); put(wo, 9, 4, 'F08')
put(wo, 10, 1, 'Bloque extra de 50 GB (Q)'); put(wo, 10, 2, 140, BLUE); put(wo, 10, 3, 140, BLUE); put(wo, 10, 4, 'F08')
put(wo, 11, 1, 'Suscripción Starlink (Q/mes)', BOLD); put(wo, 11, 2, '=B9+B8*B10', fmt='#,##0'); put(wo, 11, 3, '=C9+C8*C10', fmt='#,##0')
for c in (2, 3): pass
put(wo, 12, 1, 'Mantenimiento (2 % anual del CAPEX)'); put(wo, 12, 2, f'=0.02*{CAP1}/12', fmt='#,##0'); put(wo, 12, 3, f'=0.02*{CAPX}/12', fmt='#,##0'); put(wo, 12, 4, 'Supuesto')
put(wo, 13, 1, 'Técnico local (medio tiempo)'); put(wo, 13, 2, 2000, BLUE, '#,##0'); put(wo, 13, 3, 2000, BLUE, '#,##0'); put(wo, 13, 4, 'Supuesto')
put(wo, 14, 1, 'Reserva de reposición de CPE (5 % anual)'); put(wo, 14, 2, f'=0.05*BOM_CAPEX!I{cpe_row}/12', fmt='#,##0'); put(wo, 14, 3, f'=0.05*BOM_CAPEX!H{cpe_row}/12', fmt='#,##0'); put(wo, 14, 4, 'Supuesto')
put(wo, 15, 1, 'Reserva de reposición de baterías (vida 10 años)'); put(wo, 15, 2, f'=BOM_CAPEX!I{bat_row}/120', fmt='#,##0'); put(wo, 15, 3, f'=BOM_CAPEX!H{bat_row}/120', fmt='#,##0'); put(wo, 15, 4, 'LiFePO4 ≈ 6,000 ciclos (supuesto)')
put(wo, 16, 1, 'Seguro (1 % anual del CAPEX)'); put(wo, 16, 2, f'=0.01*{CAP1}/12', fmt='#,##0'); put(wo, 16, 3, f'=0.01*{CAPX}/12', fmt='#,##0'); put(wo, 16, 4, 'Supuesto')
put(wo, 17, 1, 'Administración, cobranza y soporte'); put(wo, 17, 2, 500, BLUE, '#,##0'); put(wo, 17, 3, 500, BLUE, '#,##0'); put(wo, 17, 4, 'Supuesto')
put(wo, 18, 1, 'OPEX MENSUAL TOTAL (Q)', BOLD); put(wo, 18, 2, '=SUM(B11:B17)', BOLD, '#,##0', KEY); put(wo, 18, 3, '=SUM(C11:C17)', BOLD, '#,##0', KEY)
put(wo, 19, 1, 'Hogares con servicio'); put(wo, 19, 2, 65, BLUE); put(wo, 19, 3, 98, BLUE)
put(wo, 20, 1, 'OPEX por hogar por mes (Q)', BOLD); put(wo, 20, 2, '=B18/B19', BOLD, '#,##0.0', KEY); put(wo, 20, 3, '=C18/C19', BOLD, '#,##0.0', KEY)
put(wo, 21, 1, 'Amortización del CAPEX a 5 años por hogar y mes (Q)'); put(wo, 21, 2, f'={CAPH1}/60', fmt='#,##0.0'); put(wo, 21, 3, f'={CAPH}/60', fmt='#,##0.0')
put(wo, 22, 1, 'TARIFA DE EQUILIBRIO por hogar y mes (Q)', BOLD); put(wo, 22, 2, '=B20+B21', BOLD, '#,##0.0', KEY); put(wo, 22, 3, '=C20+C21', BOLD, '#,##0.0', KEY); put(wo, 22, 4, 'OPEX + CAPEX amortizado, sin margen de utilidad')
put(wo, 23, 1, 'Tarifa propuesta (Q/mes)'); put(wo, 23, 3, 175, BLUE, '#,##0', KEY); put(wo, 23, 4, 'Decisión comercial (compárese con planes móviles rurales)')
put(wo, 24, 1, 'Ingreso mensual año 3 (Q)'); put(wo, 24, 3, '=C23*C19', fmt='#,##0'); put(wo, 25, 1, 'Margen mensual año 3 tras OPEX (Q)'); put(wo, 25, 3, '=C24-C18', fmt='#,##0')
put(wo, 26, 1, 'Recuperación simple del CAPEX (meses)'); put(wo, 26, 3, f'=IF(C25>0,{CAPX}/C25,"no se recupera")', fmt='0'); put(wo, 26, 4, 'Con 98 hogares pagando la tarifa propuesta')
# ===================== LEGAL =====================
wl = sheet('Legal', [30, 52, 52]); title(wl, 'Marco legal y regulatorio (Guatemala)', 'Se asume que somos parte de una empresa operadora ya legalizada. Las citas marcadas "por verificar" deben contrastarse con el texto oficial.')
hdr(wl, 4, ['Tema', 'Qué exige / dice', 'Cómo lo cumple el proyecto'])
legal = [('Ley General de Telecomunicaciones (Decreto 94-96)', 'Regula el uso del espectro y los servicios de telecomunicaciones; la SIT es el ente regulador (F05, por verificar en texto oficial).', 'Se opera bajo una empresa con registro ante la SIT; el servicio se presta como acceso a internet de banda ancha.'),
 ('Tabla Nacional de Atribución de Frecuencias (TNAF)', 'La SIT administra la TNAF (F06). Referencia regional: 5725–5850 MHz figura como banda 5 GHz usable en Guatemala; límites de potencia y certificación deben confirmarse en la TNAF vigente (F28, por verificar).', 'Los tres canales (5745/5785/5825 MHz, 20 MHz) quedan dentro de 5725–5850 MHz; equipos con certificación FCC/CE; potencia total dentro del límite aplicable (por verificar).'),
 ('Registro de operador y servicio', 'Los prestadores de servicios inscriben ante el Registro de Telecomunicaciones (ORC) (F04).', 'La empresa operadora inscribe el servicio y la aldea como zona de cobertura.'),
 ('Starlink', 'La SIT autorizó Starlink en mayo de 2023 (F02); el servicio es comercial con planes Business en Guatemala (F08).', 'El backhaul se contrata como cliente Business (Prioridad Local); no se revende sin registro del servicio.'),
 ('Uso del terreno de la torre', 'Se requiere autorización del propietario o de la comunidad (usufructo/servidumbre) y permisos municipales.', 'Acuerdo con la COCODE/alcalde auxiliar para el claro central; obra civil con permiso municipal de Chisec.'),
 ('Seguridad de la torre', 'Cimentación, vientos y pararrayos calculados por un profesional; señalización si aplica (aviación civil, por verificar).', 'Torre ventada de 30 m con pararrayos y puesta a tierra incluidos en el CAPEX.'),
 ('Sanciones', 'La LGT prevé multas por operar sin título o fuera de la banda (art. 81, F05, por verificar).', 'Operación solo en banda atribuida y con registro; plan de frecuencias documentado en esta memoria.')]
for i, row in enumerate(legal):
    for j, v in enumerate(row): put(wl, 5 + i, 1 + j, v, BOLD if j == 0 else BLK, wrap=True)
    wl.row_dimensions[5 + i].height = 62
# ===================== FUENTES =====================
wf = sheet('Fuentes', [7, 60, 60, 14, 28]); title(wf, 'Fuentes y trazabilidad', 'Copia de 14_fuentes/FUENTES.md (se actualizó con F28–F30).')
hdr(wf, 4, ['ID', 'Dato usado', 'Fuente', 'Consulta', 'Estado'])
fu = [l.strip().strip('|').split('|') for l in open('../14_fuentes/FUENTES.md', encoding='utf-8') if l.startswith('| F')]
for i, row in enumerate(fu):
    for j, v in enumerate(row[:5]): put(wf, 5 + i, 1 + j, v.strip(), wrap=True)
    wf.row_dimensions[5 + i].height = 45
# ===================== RESUMEN =====================
wr = sheet('Resumen', [52, 20, 66]); title(wr, 'Memoria de cálculo — Sistema de antenas y red para la aldea Babilonia (Chisec, Alta Verapaz)', 'Universidad del Istmo · Antenas y Propagación 2026 · Modalidad A (simulación) · Equipo: Kevin Gabriel González Donis, Maximiliano González De León, Diego Andre Cuellar Butcher')
hdr(wr, 4, ['Indicador', 'Valor', 'Nota'])
res = [('Casas / puntos de servicio de diseño', f'=COUNT({CR("A")})', 'Datos de entrada: hoja Enlace_por_casa', '0'),
 ('Población estimada (95 viviendas × 4.0 hab.)', '=95*4', 'Supuesto D03', '0'),
 ('Altura de la torre (m)', f'={S("Htow")}', 'D07', '0'),
 ('Distancia máxima a la torre (m)', f'=MAX({CR("C")})', '', '0'),
 ('Casas con enlace útil en bajada (margen ≥ 10 dB)', f'=COUNTIF({CR("X")},"<>ninguno")', 'Meta: ≥ 95 % (≥ 104)', '0'),
 ('Casas con enlace útil en subida', f'=COUNTIF({CR("Z")},">0")', '', '0'),
 ('Margen mínimo de bajada sobre BPSK (dB)', f'=MIN({CR("T")})', '', '0.0'),
 ('Margen mínimo de subida sobre BPSK (dB)', f'=MIN({CR("U")})', 'Casa 26 (41 dB de follaje)', '0.0'),
 ('Margen mediano de bajada (dB)', f'=MEDIAN({CR("T")})', '', '0.0'),
 ('Pérdida de follaje máxima (dB)', f'=MAX({CR("R")})', 'Weissberger a 5.8 GHz', '0.0'),
 ('Utilización de aire máx. en bajada (año 3)', '=MAX(Capacidad!D5:D7)', 'Menor a 100 % = cabe', '0.0%'),
 ('Uso del backhaul Starlink en bajada (año 3)', '=Capacidad!C26', 'Pico agregado vs 145 Mbps', '0%'),
 ('Potencia continua de la torre (W)', f'={EN["W"]}', '', '0'),
 ('Paneles / baterías', f'={EN["npan"]}&" × 550 W / "&{EN["nbat"]}&" × 5.12 kWh"', 'Autonomía ≈ 2.4 días', None),
 ('CAPEX total de diseño (Q)', f'={CAPX}', 'BOM_CAPEX', '#,##0'),
 ('CAPEX por hogar (Q)', f'={CAPH}', '', '#,##0'),
 ('OPEX mensual año 3 (Q)', '=OPEX_Tarifa!C18', '', '#,##0'),
 ('OPEX por hogar por mes, año 3 (Q)', '=OPEX_Tarifa!C20', '', '#,##0.0'),
 ('Tarifa de equilibrio por hogar y mes (Q)', '=OPEX_Tarifa!C22', 'OPEX + CAPEX a 5 años', '#,##0.0')]
for i, (a, b, c, f) in enumerate(res):
    put(wr, 5 + i, 1, a, BOLD); put(wr, 5 + i, 2, b, BLK, f); put(wr, 5 + i, 3, c)
r = 5 + len(res) + 1; wr.cell(r, 1, 'Contenido del libro').font = BOLD
idx = [('Supuestos', 'Todos los parámetros de entrada (azules) con su fuente'), ('MCS', 'Tabla de modulaciones del radio y tasas PHY'), ('Enlace_por_casa', 'Presupuesto de enlace de las 109 casas, con fórmulas'), ('Capacidad', 'Utilización por sector, crecimiento y backhaul'),
       ('Interferencia', 'Plan de frecuencias y C/I entre sectores'), ('Sensibilidad', 'Escenarios de torre, copa, desvanecimiento y montaje'), ('Energia', 'Dimensionamiento solar y baterías'), ('BOM_CAPEX', 'Lista de materiales y CAPEX en Q'), ('OPEX_Tarifa', 'OPEX, costo por hogar y tarifa'), ('Legal', 'Marco regulatorio (SIT)'), ('Fuentes', 'Trazabilidad de datos')]
for i, (a, b) in enumerate(idx): put(wr, r + 1 + i, 1, a, BOLD); put(wr, r + 1 + i, 2, b); wr.merge_cells(start_row=r + 1 + i, start_column=2, end_row=r + 1 + i, end_column=3)
order = ['Resumen', 'Supuestos', 'MCS', 'Enlace_por_casa', 'Capacidad', 'Interferencia', 'Sensibilidad', 'Energia', 'BOM_CAPEX', 'OPEX_Tarifa', 'Legal', 'Fuentes']
wb._sheets = [wb[n] for n in order]
wb.save('Memoria_Calculo_Babilonia.xlsx'); print('ok')
