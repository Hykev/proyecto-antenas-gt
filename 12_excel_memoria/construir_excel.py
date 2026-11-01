"""Genera Memoria_Calculo_Babilonia.xlsx (version simplificada, formulas visibles).
Uso: python3 -I construir_excel.py   (desde 12_excel_memoria; luego recalcular con LibreOffice)"""
import csv, os, re, sys
sys.path.insert(0, '../04_propagacion_linkbudget')
import rfmodel as R
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

F = 'Arial'; BLUE = Font(name=F, color='0000FF', size=10); BLK = Font(name=F, size=10); BOLD = Font(name=F, bold=True, size=10); WH = Font(name=F, bold=True, color='FFFFFF', size=10)
IT = Font(name=F, italic=True, size=9, color='555555')
HDR = PatternFill('solid', fgColor='1F4E78'); KEY = PatternFill('solid', fgColor='FFF2CC'); GREY = PatternFill('solid', fgColor='EDEDED')
thin = Side(style='thin', color='BBBBBB'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
wb = Workbook(); wb.remove(wb.active)
def sheet(name, widths):
    ws = wb.create_sheet(name); ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths, 1): ws.column_dimensions[L(i)].width = w
    return ws
def hdr(ws, row, vals, col=1, h=None):
    for i, v in enumerate(vals):
        c = ws.cell(row, col + i, v); c.font = WH; c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center'); c.border = BOX
    if h: ws.row_dimensions[row].height = h
def put(ws, r, c, v, font=None, fmt=None, fill=None, wrap=False):
    x = ws.cell(r, c, v); x.border = BOX
    x.font = font or (BLK if (isinstance(v, str) and v.startswith('=')) or isinstance(v, str) else BLUE)
    if fmt: x.number_format = fmt
    if fill: x.fill = fill
    if wrap: x.alignment = Alignment(wrap_text=True, vertical='top')
    return x
def title(ws, t, sub=None):
    ws['A1'] = t; ws['A1'].font = Font(name=F, bold=True, size=14, color='1F4E78')
    if sub: ws['A2'] = sub; ws['A2'].font = IT
def note(ws, r, text, c=1): ws.cell(r, c, text).font = IT

LB = list(csv.DictReader(open('../04_propagacion_linkbudget/linkbudget_por_casa.csv'))); LBd = {int(x['casa']): x for x in LB}
H = {h['id']: h for h in R.load_houses()}

# ============================ SUPUESTOS ============================
ws = sheet('Supuestos', [46, 13, 11, 74]); title(ws, 'Supuestos y parámetros de diseño', 'Azul = dato de entrada (se puede cambiar y todo el libro se recalcula). Negro = fórmula. Fondo amarillo = supuesto clave.')
hdr(ws, 4, ['Parámetro', 'Valor', 'Unidad', 'Fuente o nota'])
SUP = {}
rows = [
 ('Frecuencia de diseño', 'f', 5.8, 'GHz', 'Centro de la banda 5725-5850 MHz [F28]', 0),
 ('Longitud de onda', 'lam', '=299792458/(B5*1E9)', 'm', 'c / f', 0),
 ('Altura de la torre', 'Htow', 30, 'm', 'Elegida por análisis de follaje (ver hoja Validacion)', 1),
 ('Elevación del terreno en la torre', 'Z0', 206, 'm s. n. m.', 'Google Earth [F12]', 0),
 ('Altura del CPE sobre el terreno (mástil en el techo)', 'hcpe', 6, 'm', 'Supuesto de diseño', 0),
 ('Potencia Tx del radio sectorial (AP)', 'Pap', 28, 'dBm', 'Ficha Rocket Prism 5AC Gen2 [F24]', 0),
 ('Potencia Tx del CPE', 'Pcpe', 25, 'dBm', 'Ficha LiteBeam 5AC Gen2 [F27]', 0),
 ('Ganancia del CPE LiteBeam 5AC Gen2', 'Gcpe', 23, 'dBi', 'Ficha [F27]', 0),
 ('Ganancia de la sectorial AM-5G16-120', 'gap0', 15.5, 'dBi', 'Ficha: 15-16 dBi, se usa el valor medio [F25]', 0),
 ('Pérdida de jumpers y conectores en el AP', 'Lfeed', 0.5, 'dB', 'Supuesto', 0),
 ('Pérdida por desalineación del CPE', 'Lmis', 1.0, 'dB', 'Supuesto', 0),
 ('Pérdida por lluvia (trayectos < 0.5 km)', 'Lrain', 0.3, 'dB', 'Orden de magnitud según UIT-R P.838 (por verificar)', 0),
 ('Penalización de sensibilidad por canal de 20 MHz', 'pen', 3.0, 'dB', 'Supuesto conservador: la ficha no aclara el ancho de canal de sus sensibilidades', 1),
 ('Margen de diseño exigido', 'Mreq', 10, 'dB', 'Criterio del proyecto: un MCS es utilizable si su margen es al menos este valor', 1),
 ('Ancho de haz horizontal a 6 dB (sectorial)', 'az6', 137, '°', 'Ficha [F25]', 0),
 ('Inclinación de fábrica en elevación (sectorial)', 'tilt', 4, '°', 'Ficha [F25]', 0),
 ('Inclinación mecánica adicional', 'mech', 0, '°', 'Decisión de diseño', 1),
 ('Largo físico de la antena sectorial', 'Lant', 0.367, 'm', 'Ficha [F25]', 0),
 ('Tope de atenuación azimutal (lóbulos laterales y F/B)', 'capaz', 25, 'dB', 'Supuesto: la ficha no publica F/B', 1),
 ('Piso de atenuación en elevación', 'capel', 25, 'dB', 'Supuesto', 0),
 ('Acimut del eje del sector S1', 'b1', 150, '°', 'S1 cubre 90-210°', 0),
 ('Acimut del eje del sector S2', 'b2', 270, '°', 'S2 cubre 210-330°', 0),
 ('Acimut del eje del sector S3', 'b3', 30, '°', 'S3 cubre 330-90°', 0),
 ('Adopción en el año de diseño (año 3)', 'adopt', 0.9, '', 'Supuesto', 1),
 ('Simultaneidad en hora pico', 'sim', 0.25, '', 'Supuesto', 1),
 ('Tasa por usuario activo, bajada', 'ru_dl', 4, 'Mbps', 'Supuesto (video, mensajería, estudio en línea)', 0),
 ('Tasa por usuario activo, subida', 'ru_ul', 0.5, 'Mbps', 'Supuesto', 0),
 ('Eficiencia MAC (TDD)', 'eta', 0.65, '', 'Supuesto', 1),
 ('Fracción de la trama para bajada', 'dlsh', 0.75, '', 'Supuesto', 1),
 ('Tipo de cambio', 'fx', 7.6445, 'GTQ/USD', 'Trading Economics, 26-oct-2026 [F22]', 0),
 ('Alimentación eléctrica de la torre', 'pw', 'No se dimensiona', '', 'Fuera del alcance del proyecto; se asume suministro en el sitio (la carga ronda 160 W continuos)', 0),
]
r = 5
for lab, key, val, unit, nt, k in rows:
    put(ws, r, 1, lab, BOLD); c = put(ws, r, 2, val, BLK if isinstance(val, str) else BLUE, fill=KEY if k else None); put(ws, r, 3, unit); put(ws, r, 4, nt, wrap=True)
    SUP[key] = f'Supuestos!$B${r}'; r += 1
S = lambda k: SUP[k]
# derivados
put(ws, r, 1, 'Diferencia de potencia CPE frente al AP', BOLD); put(ws, r, 2, f'={S("Pap")}-{S("Pcpe")}', fmt='0.0'); put(ws, r, 3, 'dB'); put(ws, r, 4, 'Se usa para pasar los umbrales de bajada a subida'); SUP['cpeoff'] = f'Supuestos!$B${r}'; r += 2
ws.cell(r, 1, 'Tabla de modulaciones del radio (Rocket Prism 5AC Gen2) [F24]').font = BOLD; r += 1
hdr(ws, r, ['MCS', 'Sensibilidad (dBm)', 'Tx máx. (dBm)', 'Tasa PHY 20 MHz (Mbps) = 2 flujos x 52 subportadoras x bits x código / 3.6 µs; umbral con penalización = sensibilidad + penalización'], h=44)
ws.cell(r, 5, 'Bits/símbolo').font = BOLD; ws.cell(r, 6, 'Código').font = BOLD; ws.cell(r, 7, 'Umbral (dBm)').font = BOLD
ws.column_dimensions['E'].width = 12; ws.column_dimensions['F'].width = 9; ws.column_dimensions['G'].width = 13
mcs = [('BPSK 1/2', 1, .5, -96, 28), ('QPSK 1/2', 2, .5, -95, 28), ('QPSK 3/4', 2, .75, -92, 28), ('16QAM 1/2', 4, .5, -90, 28), ('16QAM 3/4', 4, .75, -86, 28), ('64QAM 2/3', 6, 2 / 3, -83, 28), ('64QAM 3/4', 6, .75, -77, 27), ('64QAM 5/6', 6, 5 / 6, -74, 26), ('256QAM 3/4', 8, .75, -69, 24), ('256QAM 5/6', 8, 5 / 6, -65, 22)]
M0 = r + 1
for i, m in enumerate(mcs):
    rr = M0 + i
    put(ws, rr, 1, m[0], BLUE); put(ws, rr, 2, m[3], BLUE); put(ws, rr, 3, m[4], BLUE); put(ws, rr, 4, f'=2*52*E{rr}*F{rr}/3.6', fmt='0.0'); put(ws, rr, 5, m[1], BLUE); put(ws, rr, 6, m[2], BLUE, '0.000'); put(ws, rr, 7, f'=B{rr}+{S("pen")}', fmt='0.0')
M1 = M0 + len(mcs) - 1
MN, MTX, MRATE, MTH = [f'Supuestos!${c}${M0}:${c}${M1}' for c in 'ACDG']
TH0 = f'Supuestos!$G${M0}'; TX0 = f'Supuestos!$C${M0}'
ws.cell(M1 + 2, 1, 'Fuentes [Fxx]: ver hoja Fuentes. Los datos de ficha tienen incertidumbre de unos ±2 dB.').font = IT

# ============================ ANTENAS Y RADIO ============================
wa = sheet('Antenas_Radio', [22, 22, 12, 12, 12, 14, 14, 14, 16, 12, 12, 10, 36]); title(wa, 'Inventario de antenas y plan de radio', 'Datos de ficha salvo los marcados como supuesto o derivado.')
hdr(wa, 4, ['ID', 'Modelo', 'Cant.', 'Sitio', 'Altura (m)', 'Frecuencia (GHz)', 'Ganancia (dBi)', 'HPBW H (°)', 'HPBW V (°)', 'Polarización', 'Acimut (°)', 'Tilt (°)', 'Fuente / nota'], h=36)
ant = [('Sectorial S1', 'AM-5G16-120', 1, 'Torre', 30, '5.1-5.85', 15.5, '137 (a 6 dB)', '8', 'Dual H/V', 150, 4, 'Ficha [F25]. F/B no indicado: tope supuesto 25 dB'),
       ('Sectorial S2', 'AM-5G16-120', 1, 'Torre', 30, '5.1-5.85', 15.5, '137 (a 6 dB)', '8', 'Dual H/V', 270, 4, 'Ficha [F25]'),
       ('Sectorial S3', 'AM-5G16-120', 1, 'Torre', 30, '5.1-5.85', 15.5, '137 (a 6 dB)', '8', 'Dual H/V', 30, 4, 'Ficha [F25]'),
       ('CPE (por casa)', 'LiteBeam 5AC Gen2', 109, 'Techo de cada casa', 6, '5.15-5.875', 23, '~10 (derivado)', '~10 (derivado)', 'Dual H/V', 'Hacia la torre', 'Al horizonte', 'Ficha [F27]; haz derivado de 70 lambda/D'),
       ('Plato backhaul', 'Starlink Performance Gen 3', 1, 'Torre', 31, 'Ku/Ka', 'n/d', 'n/d', 'n/d', 'n/d', 'Cielo abierto', '-', 'No se publican parámetros del terminal ni del satélite; se usa el desempeño medido [F09]')]
for i, a in enumerate(ant):
    for j, v in enumerate(a): put(wa, 5 + i, 1 + j, v, BLUE if j in (2, 4, 6, 10, 11) else BLK, wrap=(j == 12))
wa.cell(11, 1, 'Plan de radio (una portadora por sector, GPS sincronizado)').font = BOLD
hdr(wa, 12, ['Sector', 'Radio', 'Banda', 'Frecuencia central (MHz)', 'Ancho de canal (MHz)', 'Potencia Tx (dBm)', 'Polarización', 'Reutilización', 'Interferencia esperada'], h=36)
plan = [('S1', 'Rocket Prism 5AC Gen2', '5725-5850', 5745, 20, 28, 'H/V (MIMO 2x2)', 'Canal propio', 'Baja: separado 40 MHz de S2'),
        ('S2', 'Rocket Prism 5AC Gen2', '5725-5850', 5785, 20, 28, 'H/V (MIMO 2x2)', 'Canal propio', 'Baja: separado 40 MHz de S1 y S3'),
        ('S3', 'Rocket Prism 5AC Gen2', '5725-5850', 5825, 20, 28, 'H/V (MIMO 2x2)', 'Canal propio', 'Baja: separado 40 MHz de S2')]
for i, a in enumerate(plan):
    for j, v in enumerate(a): put(wa, 13 + i, 1 + j, v, BLUE if j in (3, 4, 5) else BLK)
note(wa, 17, 'Con un solo canal para los tres sectores el C/I cocanal mínimo es 0 dB y 40 casas quedarían sin MCS útil; con tres canales ninguna (cálculo en Python, ver informe).')

# ============================ LINK BUDGET ============================
wl = sheet('LinkBudget', [24, 7, 10, 10, 10, 10, 8, 9, 9, 10, 10, 10, 10, 10, 9, 10, 10, 10, 10, 10, 9, 11, 11, 11, 11, 11, 10, 14, 10, 14, 11, 10, 10])
title(wl, 'Presupuesto de enlace de los casos representativos (torre → CPE), bajada y subida', 'El enunciado pide casos representativos y extremos, no repetir las 109 casas. Azul = datos de entrada por casa; el resto son fórmulas. Las 109 casas se calcularon con linkbudget.py y dan el mismo resultado.')
cols = ['Caso', 'Casa', 'Acimut torre-casa (°)', 'Distancia horizontal (m)', 'Elevación terreno casa (m)', 'Follaje atravesado (m)', 'Sector', 'Eje del sector (°)', 'Δ acimut (°)', 'Desnivel antena-CPE (m)', 'Distancia 3D (m)', 'Elevación del rayo (°)', 'Δ elevación (°)',
        'Pérd. patrón acimut (dB)', 'u (apertura)', 'Pérd. patrón elev. (dB)', 'Ganancia AP efectiva (dBi)', 'EIRP del AP (dBm)', 'FSPL (dB)', 'Pérd. follaje (dB)', 'Otras pérd. (dB)', 'Pr bajada (dBm)', 'Umbral BPSK (dBm)', 'Margen bajada (dB)', 'Pr subida (dBm)', 'Margen subida (dB)',
        'MCS útiles bajada', 'MCS bajada', 'MCS útiles subida', 'MCS subida', 'Conclusión', 'Radio Fresnel 1 al centro (m)', '60 % de Fresnel (m)']
hdr(wl, 4, cols, h=62)
casos = [('Peor caso S2 (subida)', 26), ('Peor caso S1', 107), ('Peor caso S3', 86), ('Casa más cercana', 43), ('Casa de distancia mediana', 35), ('Casa con vegetación moderada', 55), ('Casa en el borde este (elevada)', 93)]
for i, (lab, c) in enumerate(casos):
    r = 5 + i; h = H[c]
    put(wl, r, 1, lab, BOLD); put(wl, r, 2, c, BLUE); put(wl, r, 3, round(h['az'], 2), BLUE, '0.0'); put(wl, r, 4, round(h['d'], 1), BLUE, '0.0'); put(wl, r, 5, round(h['z'], 1), BLUE, '0.0'); put(wl, r, 6, int(LBd[c]['follaje_m']), BLUE, '0')
    put(wl, r, 7, f'=IF(AND(C{r}>=90,C{r}<210),"S1",IF(AND(C{r}>=210,C{r}<330),"S2","S3"))')
    put(wl, r, 8, f'=IF(G{r}="S1",{S("b1")},IF(G{r}="S2",{S("b2")},{S("b3")}))')
    put(wl, r, 9, f'=MOD(C{r}-H{r}+180,360)-180', fmt='0.0')
    put(wl, r, 10, f'={S("Htow")}-(E{r}-{S("Z0")})-{S("hcpe")}', fmt='0.0')
    put(wl, r, 11, f'=SQRT(D{r}^2+J{r}^2)', fmt='0.0')
    put(wl, r, 12, f'=DEGREES(ATAN2(D{r},J{r}))', fmt='0.00')
    put(wl, r, 13, f'=L{r}-({S("tilt")}+{S("mech")})', fmt='0.00')
    put(wl, r, 14, f'=MIN(6*(2*I{r}/{S("az6")})^2,{S("capaz")})', fmt='0.0')
    put(wl, r, 15, f'=PI()*{S("Lant")}/{S("lam")}*SIN(RADIANS(M{r}))', fmt='0.000')
    put(wl, r, 16, f'=IF(ABS(O{r})<1E-9,0,MIN(-20*LOG10(MAX(ABS(SIN(O{r})/O{r}),1E-6)),{S("capel")}))', fmt='0.0')
    put(wl, r, 17, f'={S("gap0")}-N{r}-P{r}', fmt='0.0')
    put(wl, r, 18, f'={S("Pap")}-{S("Lfeed")}+Q{r}', fmt='0.0')
    put(wl, r, 19, f'=32.44+20*LOG10(K{r}/1000)+20*LOG10({S("f")}*1000)', fmt='0.0')
    put(wl, r, 20, f'=IF(F{r}<=0,0,IF(F{r}<=14,0.45*{S("f")}^0.284*F{r},1.33*{S("f")}^0.284*MIN(F{r},400)^0.588))', fmt='0.0')
    put(wl, r, 21, f'={S("Lmis")}+{S("Lrain")}', fmt='0.0')
    put(wl, r, 22, f'=R{r}-S{r}-T{r}-U{r}+{S("Gcpe")}', fmt='0.0')
    put(wl, r, 23, f'={TH0}', fmt='0.0')
    put(wl, r, 24, f'=V{r}-W{r}', fmt='0.0')
    put(wl, r, 25, f'={S("Pcpe")}+{S("Gcpe")}+Q{r}-{S("Lfeed")}-S{r}-T{r}-U{r}', fmt='0.0')
    put(wl, r, 26, f'=Y{r}-W{r}', fmt='0.0')
    put(wl, r, 27, f'=SUMPRODUCT(--({MTX}-{S("Pap")}+{S("Pap")}-S{r}-T{r}-U{r}+{S("Gcpe")}-{S("Lfeed")}+Q{r}-0-{MTH}>={S("Mreq")}))', fmt='0')
    wl.cell(r, 27).value = f'=SUMPRODUCT(--({MTX}-{S("Lfeed")}+Q{r}-S{r}-T{r}-U{r}+{S("Gcpe")}-{MTH}>={S("Mreq")}))'
    put(wl, r, 28, f'=IF(AA{r}=0,"ninguno",INDEX({MN},AA{r}))')
    put(wl, r, 29, f'=SUMPRODUCT(--({MTX}-{S("cpeoff")}-{S("Lfeed")}+Q{r}-S{r}-T{r}-U{r}+{S("Gcpe")}-{MTH}>={S("Mreq")}))', fmt='0')
    put(wl, r, 30, f'=IF(AC{r}=0,"ninguno",INDEX({MN},AC{r}))')
    put(wl, r, 31, f'=IF(AND(X{r}>={S("Mreq")},Z{r}>={S("Mreq")}),"Cumple","No cumple")')
    put(wl, r, 32, f'=SQRT({S("lam")}*(D{r}/2)*(D{r}/2)/D{r})', fmt='0.0'); put(wl, r, 33, f'=0.6*AF{r}', fmt='0.0')
wl.freeze_panes = 'C5'
LBr = f'LinkBudget!$X$5:$X${4+len(casos)}'; LBu = f'LinkBudget!$Z$5:$Z${4+len(casos)}'
n = 5 + len(casos) + 1
txt = ['Fórmulas: FSPL = 32.44 + 20 log10(d_km) + 20 log10(f_MHz).  Pr = EIRP − FSPL − pérdida de follaje − otras pérdidas + G_CPE (bajada);  subida: Pr = P_CPE + G_CPE + G_AP_efectiva − L_feed − pérdidas.',
       'Ganancia efectiva del AP = G_AP − pérdida de patrón en acimut − pérdida de patrón en elevación. Acimut: 6·(2Δ/HPBW6)², con tope. Elevación: apertura uniforme, |sin u / u| con u = π·L/λ·sin(Δel).',
       'Follaje (Weissberger): 0.45·f^0.284·d si d ≤ 14 m;  1.33·f^0.284·d^0.588 si 14 < d ≤ 400 m (f en GHz, d en metros de follaje atravesado).',
       'Margen = Pr − (sensibilidad BPSK 1/2 + penalización). Un MCS superior es utilizable si su margen es ≥ margen de diseño. El peor caso de subida es la casa 26: margen mayor que 10 dB, cumple.',
       'Backhaul: el enlace Starlink es un servicio comercial; no se calcula con Friis (no hay datos de ficha del terminal ni del satélite). Se usa el desempeño medido en la zona: 145/21 Mbps y 32 ms [F09, F11].',
       'Fresnel: con el terreno desnudo la altura mínima de torre que despeja el 60 % de la primera zona es ≤ 2.8 m para las 109 casas (cálculo en Python); la torre de 30 m despeja de sobra. La pérdida limitante es la vegetación.']
for i, t_ in enumerate(txt): note(wl, n + i, t_)

# ============================ CAPACIDAD ============================
wk = sheet('Capacidad', [40, 13, 13, 13, 13, 13, 60]); title(wk, 'Cobertura, capacidad por sector y backhaul', 'Utilización de aire = adopción · demanda · Σ(1/R_i) / (η_MAC · fracción de trama). Σ(1/R_i) sale del cálculo por casa (Python, 109 casas).')
hdr(wk, 4, ['Sector', 'Casas', 'Distancia máx. (m)', 'Margen mín. bajada (dB)', 'Margen mín. subida (dB)', 'Σ(1/R) bajada (1/Mbps)', 'Σ(1/R) subida (1/Mbps)'], h=44)
for i, s in enumerate(('S1', 'S2', 'S3')):
    d = [x for x in LB if x['sector'] == s]; r = 5 + i
    put(wk, r, 1, s, BOLD); put(wk, r, 2, len(d), BLUE); put(wk, r, 3, round(max(float(x['dist_m']) for x in d)), BLUE); put(wk, r, 4, round(min(float(x['margen_dl_BPSK_dB']) for x in d), 1), BLUE, '0.0'); put(wk, r, 5, round(min(float(x['margen_ul_BPSK_dB']) for x in d), 1), BLUE, '0.0')
    put(wk, r, 6, round(sum(1 / float(x['R_dl_Mbps']) for x in d), 4), BLUE, '0.0000'); put(wk, r, 7, round(sum(1 / float(x['R_ul_Mbps']) for x in d), 4), BLUE, '0.0000')
put(wk, 8, 1, 'Total', BOLD); put(wk, 8, 2, '=SUM(B5:B7)', fmt='0'); put(wk, 8, 3, '=MAX(C5:C7)', fmt='0'); put(wk, 8, 4, '=MIN(D5:D7)', fmt='0.0'); put(wk, 8, 5, '=MIN(E5:E7)', fmt='0.0')
wk.cell(10, 1, 'MCS máximo utilizable en bajada (109 casas)').font = BOLD
hdr(wk, 11, ['MCS', 'Casas', '', '', '', '', ''])
vc = {}
for x in LB: vc[x['MCS_dl']] = vc.get(x['MCS_dl'], 0) + 1
order = ['256QAM 5/6', '256QAM 3/4', '64QAM 5/6', '64QAM 3/4', '64QAM 2/3', '16QAM 3/4', '16QAM 1/2']
for i, m in enumerate(order): put(wk, 12 + i, 1, m, BLK); put(wk, 12 + i, 2, vc.get(m, 0), BLUE)
put(wk, 19, 1, 'Casas con enlace útil (bajada y subida)', BOLD); put(wk, 19, 2, '=SUM(B12:B18)', fmt='0'); put(wk, 19, 3, '=B19/B8', fmt='0%'); note(wk, 19, 'Meta: ≥ 95 %', 7)
Rmin = min(float(x['R_dl_Mbps']) for x in LB)
put(wk, 20, 1, 'Velocidad útil mínima de bajada por casa (Mbps)', BOLD); put(wk, 20, 2, round(Rmin, 1), BLUE, '0.0'); put(wk, 20, 3, f'=B20*{S("eta")}*{S("dlsh")}', fmt='0.0'); note(wk, 20, 'B = PHY de la peor casa (casa 26); C = útil = PHY · η · fracción de bajada', 7)
wk.cell(22, 1, 'Utilización del aire por sector').font = BOLD
hdr(wk, 23, ['Escenario', 'Adopción', 'Tasa por usuario activo (Mbps)', 'Util. S1 bajada', 'Util. S2 bajada', 'Util. S3 bajada', 'Nota'], h=44)
sc = [('Año 1', .6, 4, ''), ('Año 3 (diseño)', f'={S("adopt")}', f'={S("ru_dl")}', 'Caso de diseño'), ('Año 5, 6 Mbps', 1.0, 6, 'Crecimiento'), ('Año 5, 8 Mbps', 1.0, 8, 'S2 se saturaría: habría que añadir un cuarto sector o un segundo radio')]
for i, (nm, a, p, nt) in enumerate(sc):
    r = 24 + i; put(wk, r, 1, nm); put(wk, r, 2, a, BLUE if not isinstance(a, str) else BLK, '0%'); put(wk, r, 3, p, BLUE if not isinstance(p, str) else BLK)
    for j in range(3): put(wk, r, 4 + j, f'=B{r}*C{r}*{S("sim")}*$F${5+j}/({S("eta")}*{S("dlsh")})', fmt='0%')
    put(wk, r, 7, nt)
wk.cell(29, 1, 'Utilización en subida, año 3').font = BOLD
for j in range(3): put(wk, 30, 4 + j, f'={S("adopt")}*{S("ru_ul")}*{S("sim")}*$G${5+j}/({S("eta")}*(1-{S("dlsh")}))', fmt='0%')
put(wk, 30, 1, 'Utilización en subida (S1, S2, S3)'); 
wk.cell(32, 1, 'Backhaul Starlink (año 3)').font = BOLD
bh = [('Hogares con servicio', 98, '', 'casas', 'Adopción del año 3 sobre 109 puntos (se cuentan además 2 puntos comunitarios)'),
      ('Pico agregado de bajada', f'=B33*{S("sim")}*{S("ru_dl")}', '0.0', 'Mbps', 'hogares · simultaneidad · tasa por usuario activo'),
      ('Pico agregado de subida', f'=B33*{S("sim")}*{S("ru_ul")}', '0.0', 'Mbps', ''),
      ('Starlink bajada de diseño', 145, '0', 'Mbps', 'Límite inferior medido en la zona [F09]'),
      ('Starlink subida de diseño', 21, '0', 'Mbps', '[F11]'),
      ('Uso del backhaul, bajada', '=B34/B36', '0%', '', 'Si pasa de 70 % se planifica un segundo terminal'),
      ('Uso del backhaul, subida', '=B35/B37', '0%', '', '')]
for i, (a, b, f_, u, nt) in enumerate(bh):
    r = 33 + i; put(wk, r, 1, a); put(wk, r, 2, b, BLUE if not isinstance(b, str) else BLK, f_ or None); put(wk, r, 3, u); put(wk, r, 7, nt)

# ============================ VALIDACION ============================
wv = sheet('Validacion', [34, 12, 12, 13, 13, 13, 14, 14, 15, 16]); title(wv, 'Validación con CloudRF y escenarios de sensibilidad', 'CloudRF (perfil de trayecto, 5800 MHz, torre 30 m AGL, receptor 6 m AGL). Capturas en 14_fuentes/evidencias/cloudrf_sim*.png [F31].')
hdr(wv, 4, ['Casa', 'Distancia 3D (m)', 'G efectiva (dBi)', 'FSPL propia (dB)', 'Pr propia (dBm)', 'Pr CloudRF sin veg. (dBm)', 'Diferencia (dB)', 'Pr CloudRF con veg. (dBm)', 'Pérdida por vegetación CloudRF (dB)', 'Follaje propio, copas de 20 m (dB)'], h=58)
CRd = {26: (-56.7, -56.7), 43: (-58.5, -64.3), 55: (-50.2, -56.1), 93: (-66.8, -66.8)}
wv.cell(3, 1, 'Pr = Ptx + G efectiva − FSPL (sin ganancia del CPE ni pérdidas propias extra, igual que CloudRF)').font = IT
for i, c in enumerate((26, 43, 55, 93)):
    r = 5 + i; x = LBd[c]
    put(wv, r, 1, c, BOLD); put(wv, r, 2, float(x['dist3d_m']), BLUE, '0.0'); put(wv, r, 3, float(x['G_ap_ef_dBi']), BLUE, '0.0'); put(wv, r, 4, f'=32.44+20*LOG10(B{r}/1000)+20*LOG10({S("f")}*1000)', fmt='0.0')
    put(wv, r, 5, f'={S("Pap")}+C{r}-D{r}', fmt='0.0'); put(wv, r, 6, CRd[c][0], BLUE, '0.0'); put(wv, r, 7, f'=F{r}-E{r}', fmt='0.0'); put(wv, r, 8, CRd[c][1], BLUE, '0.0'); put(wv, r, 9, f'=F{r}-H{r}', fmt='0.0'); put(wv, r, 10, float(x['L_follaje_dB']), BLUE, '0.0')
put(wv, 9, 1, 'Diferencia máxima sin vegetación (dB)', BOLD); put(wv, 9, 7, '=MAX(ABS(MIN(G5:G8)),ABS(MAX(G5:G8)))', fmt='0.0')
for i, t_ in enumerate(['Sin vegetación coinciden dentro de 1.3 dB: se validan FSPL, geometría y presupuesto. CloudRF solo penaliza los árboles que cortan la línea de vista o la zona de Fresnel,',
                        'y usa copas de unos 10 m; el modelo propio supone copas de 20 m y es más conservador (casas 26 y 93). El valor real queda entre ambos: medir copas en campo antes de construir.']): note(wv, 10 + i, t_)
wv.cell(13, 1, 'Escenarios de sensibilidad (se recalcula todo el modelo para las 109 casas)').font = BOLD
hdr(wv, 14, ['Escenario', 'Casas con enlace útil', 'Margen mín. bajada (dB)', 'Margen mín. subida (dB)', 'Margen mediano bajada (dB)', 'Util. máx. bajada', 'Casas con > 30 dB de follaje', 'Cumple (≥ 10 dB subida)'], h=44)
for i, x in enumerate(list(csv.reader(open('../04_propagacion_linkbudget/sensibilidad_escenarios.csv')))[1:]):
    r = 15 + i
    put(wv, r, 1, x[0].replace('arboles', 'árboles').replace('inclinacion', 'inclinación'), BLK)
    put(wv, r, 2, int(x[1]), BLUE); put(wv, r, 3, float(x[2]), BLUE, '0.0'); put(wv, r, 4, float(x[3]), BLUE, '0.0'); put(wv, r, 5, float(x[4]), BLUE, '0.0'); put(wv, r, 6, float(x[5]), BLUE, '0%'); put(wv, r, 7, int(x[6]), BLUE)
    put(wv, r, 8, f'=IF(D{r}>={S("Mreq")},"Sí","No")')
note(wv, 25, 'Lectura: el diseño soporta copas hasta ~22 m y 2° de error de montaje. Con torre de 24 m y copas de 25 m falla; por eso la torre es de 30 m. Si algo falla, primero se sube la ganancia del CPE o se usa un mástil de 10 m en esas casas.')

# ============================ COSTOS ============================
wc = sheet('Costos', [50, 13, 8, 12, 9, 13, 14, 52]); title(wc, 'Presupuesto: BOM, CAPEX, OPEX y tarifa (quetzales)', 'Precios con fuente indicada; "Estimación" = valor de planificación que debe cotizarse en Guatemala. Tipo de cambio en la hoja Supuestos.')
hdr(wc, 4, ['Ítem', 'Función', 'Cant.', 'Precio unit.', 'Moneda', 'Precio unit. (Q)', 'Subtotal (Q)', 'Fuente / nota'], h=30)
bom = [('Plato Starlink Performance (Gen 3)', 'Backhaul', 1, 1499, 'USD', 'Precio de planificación [F19, F20]'),
 ('Adaptador de tubo Starlink', 'Backhaul', 1, 480, 'GTQ', 'Tienda Starlink Guatemala [F23]'),
 ('Cable Starlink Performance 50 m', 'Backhaul', 1, 1300, 'GTQ', 'Tienda Starlink Guatemala [F23]'),
 ('Radio Rocket Prism 5AC Gen2', 'Radio sectorial', 3, 307.78, 'USD', 'Ficha y precio [F24]'),
 ('Antena sectorial AM-5G16-120', 'Radio sectorial', 3, 79, 'USD', 'Tienda del fabricante [F25]'),
 ('Router PoE + switch central', 'Red en torre', 1, 250, 'USD', 'Estimación'),
 ('Inyectores PoE 24 V para radios', 'Red en torre', 3, 25, 'USD', 'Estimación'),
 ('CPE LiteBeam 5AC Gen2', 'Abonado', 109, 64.83, 'USD', 'Tienda del fabricante [F27]'),
 ('Mástil galvanizado 6 m para CPE', 'Abonado', 109, 25, 'USD', 'Estimación'),
 ('Cable UTP exterior 15 m + conectores', 'Abonado', 109, 12, 'USD', 'Estimación'),
 ('Router Wi-Fi interior', 'Abonado', 109, 30, 'USD', 'Estimación'),
 ('Punto de acceso comunitario exterior', 'Comunidad', 2, 179, 'USD', 'Estimación'),
 ('Torre ventada 30 m (obra civil y pararrayos)', 'Torre', 1, 7500, 'USD', 'Estimación (rango regional US$4,000-8,000)'),
 ('Puesta a tierra y protección contra descargas', 'Torre', 1, 800, 'USD', 'Estimación'),
 ('Cable UTP blindado y accesorios de torre', 'Torre', 1, 250, 'USD', 'Estimación'),
 ('Instalación de torre y radios', 'Instalación', 1, 3000, 'USD', 'Estimación'),
 ('Instalación de CPE en casas (mano de obra)', 'Instalación', 109, 20, 'USD', 'Estimación'),
 ('Transporte y viáticos', 'Instalación', 1, 1500, 'USD', 'Estimación')]
B0 = 5
for i, (nm, fn, q, pu, mon, src) in enumerate(bom):
    r = B0 + i; put(wc, r, 1, nm); put(wc, r, 2, fn); put(wc, r, 3, q, BLUE); put(wc, r, 4, pu, BLUE, '#,##0.00'); put(wc, r, 5, mon); put(wc, r, 6, f'=IF(E{r}="USD",D{r}*{S("fx")},D{r})', fmt='#,##0'); put(wc, r, 7, f'=C{r}*F{r}', fmt='#,##0'); put(wc, r, 8, src, wrap=True)
BN = B0 + len(bom) - 1; t = BN + 2
put(wc, t, 1, 'Subtotal de ítems', BOLD); put(wc, t, 7, f'=SUM(G{B0}:G{BN})', BOLD, '#,##0')
put(wc, t + 1, 1, 'Flete y aduana (% de equipos)'); put(wc, t + 1, 6, 0.10, BLUE, '0%', KEY); put(wc, t + 1, 7, f'=G{t}*F{t+1}', fmt='#,##0'); put(wc, t + 1, 8, 'Supuesto. IVA acreditable para la empresa operadora')
put(wc, t + 2, 1, 'Imprevistos (%)'); put(wc, t + 2, 6, 0.10, BLUE, '0%', KEY); put(wc, t + 2, 7, f'=(G{t}+G{t+1})*F{t+2}', fmt='#,##0'); put(wc, t + 2, 8, 'Supuesto')
put(wc, t + 3, 1, 'CAPEX TOTAL (Q)', BOLD); put(wc, t + 3, 7, f'=SUM(G{t}:G{t+2})', BOLD, '#,##0', KEY)
put(wc, t + 4, 1, 'CAPEX TOTAL (US$)'); put(wc, t + 4, 7, f'=G{t+3}/{S("fx")}', fmt='#,##0')
put(wc, t + 5, 1, 'Hogares con servicio (año 3)'); put(wc, t + 5, 7, '=Capacidad!B33', fmt='0')
put(wc, t + 6, 1, 'CAPEX por hogar (Q)', BOLD); put(wc, t + 6, 7, f'=G{t+3}/G{t+5}', BOLD, '#,##0', KEY); put(wc, t + 6, 8, 'Se equipan 109 puntos (máximo); se divide entre los hogares que contratan en el año 3')
CAPX = f'Costos!$G${t+3}'; CAPH = f'Costos!$G${t+6}'; HOG = f'Costos!$G${t+5}'
cpe_r = B0 + [b[0] for b in bom].index('CPE LiteBeam 5AC Gen2')
o = t + 9
wc.cell(o - 1, 1, 'OPEX mensual (año 3)').font = BOLD
hdr(wc, o, ['Concepto', '', '', '', '', 'Entrada', 'Q por mes', 'Nota'])
opx = [('Puntos con consumo (hogares + 2 comunitarios)', f'={HOG}+2', None, '0', 'Hogares con servicio más 2 puntos de acceso comunitarios'),
       ('Consumo por punto (GB/mes)', 25, None, '0', 'Supuesto'),
       ('Consumo total (GB/mes)', None, f'=F{o+1}*F{o+2}', '#,##0', ''),
       ('Bloques extra de 50 GB (el plan incluye 2 TB)', None, f'=ROUNDUP(MAX(0,G{o+3}-2000)/50,0)', '0', 'Plan Prioridad Local 2 TB [F08]'),
       ('Plan Starlink 2 TB', 2970, None, '#,##0', 'Captura starlink.com Guatemala, 23-oct-2026 [F08]'),
       ('Bloque adicional de 50 GB', 140, None, '#,##0', '[F08]'),
       ('Suscripción Starlink', None, f'=F{o+5}+G{o+4}*F{o+6}', '#,##0', ''),
       ('Mantenimiento (2 % anual del CAPEX)', 0.02, f'=F{o+8}*{CAPX}/12', '#,##0', 'Supuesto'),
       ('Técnico local (medio tiempo)', 2000, None, '#,##0', 'Supuesto'),
       ('Reposición de CPE (5 % anual de su costo)', 0.05, f'=F{o+10}*G{cpe_r}/12', '#,##0', 'Supuesto'),
       ('Seguro (1 % anual del CAPEX)', 0.01, f'=F{o+11}*{CAPX}/12', '#,##0', 'Supuesto'),
       ('Administración, cobranza y soporte', 500, None, '#,##0', 'Supuesto')]
for i, (nm, ent, frm, fm, nt) in enumerate(opx):
    r = o + 1 + i; put(wc, r, 1, nm)
    if ent is not None: put(wc, r, 6, ent, BLUE if not isinstance(ent, str) else BLK, '0%' if isinstance(ent, float) and ent < 1 else fm)
    if frm: put(wc, r, 7, frm, fmt=fm)
    put(wc, r, 8, nt)
# Q por mes para los que solo tienen entrada monetaria
for rr in (o + 5, o + 9, o + 12):
    wc.cell(rr, 7).value = f'=F{rr}'; wc.cell(rr, 7).number_format = '#,##0'; wc.cell(rr, 7).border = BOX; wc.cell(rr, 7).font = BLK
wc.cell(o + 5, 7).value = f'=F{o+5}'
# suscripcion (fila o+7) ya suma; las demas filas de Q por mes se suman evitando doble conteo
sub_r = o + 7
rows_sum = [sub_r, o + 8, o + 9, o + 10, o + 11, o + 12]
put(wc, o + 14, 1, 'OPEX MENSUAL TOTAL (Q)', BOLD); put(wc, o + 14, 7, '=' + '+'.join(f'G{x}' for x in rows_sum), BOLD, '#,##0', KEY)
put(wc, o + 15, 1, 'OPEX por hogar y mes (Q)', BOLD); put(wc, o + 15, 7, f'=G{o+14}/{HOG}', BOLD, '#,##0.0', KEY)
put(wc, o + 16, 1, 'Amortización del CAPEX a 5 años, por hogar y mes (Q)'); put(wc, o + 16, 7, f'={CAPH}/60', fmt='#,##0.0')
put(wc, o + 17, 1, 'TARIFA DE EQUILIBRIO por hogar y mes (Q)', BOLD); put(wc, o + 17, 7, f'=G{o+15}+G{o+16}', BOLD, '#,##0.0', KEY); put(wc, o + 17, 8, 'OPEX más CAPEX amortizado, sin utilidad')
put(wc, o + 18, 1, 'Tarifa propuesta (Q por mes)'); put(wc, o + 18, 7, 150, BLUE, '#,##0', KEY); put(wc, o + 18, 8, 'Decisión comercial; comparar con planes de datos móviles rurales')
put(wc, o + 19, 1, 'Ingreso mensual con la tarifa propuesta (Q)'); put(wc, o + 19, 7, f'=G{o+18}*{HOG}', fmt='#,##0')
put(wc, o + 20, 1, 'Excedente mensual después del OPEX (Q)'); put(wc, o + 20, 7, f'=G{o+19}-G{o+14}', fmt='#,##0')
put(wc, o + 21, 1, 'Recuperación simple del CAPEX (meses)', BOLD); put(wc, o + 21, 7, f'=IF(G{o+20}>0,{CAPX}/G{o+20},"no se recupera")', BOLD, '0', KEY)
note(wc, o + 23, 'CAPEX por hogar y OPEX por hogar son indicadores de costo, no equivalen automáticamente a una tarifa comercial (según el enunciado).')
COST = dict(capx=CAPX, caph=CAPH, opex=f'Costos!$G${o+14}', opexh=f'Costos!$G${o+15}', eq=f'Costos!$G${o+17}', tar=f'Costos!$G${o+18}', pay=f'Costos!$G${o+21}')

# ============================ METAS Y RESULTADOS ============================
wm = sheet('Metas_Resultados', [58, 20, 16, 12, 56]); title(wm, 'Metas del proyecto frente a resultados', 'Resultados enlazados a las demás hojas.')
hdr(wm, 4, ['Meta', 'Criterio', 'Resultado', 'Cumple', 'Dónde se calcula'], h=30)
met = [('Casas con enlace útil (margen ≥ 10 dB) en bajada y subida', '≥ 95 % (≥ 104 de 109)', '=Capacidad!B19', '=IF(C5>=104,"Sí","No")', 'Capacidad (cálculo por casa en Python)', '0'),
       ('Margen mínimo de bajada sobre BPSK (peor caso)', '≥ 10 dB', f'=MIN({LBr})', '=IF(C6>=10,"Sí","No")', 'LinkBudget', '0.0'),
       ('Margen mínimo de subida sobre BPSK (peor caso)', '≥ 10 dB', f'=MIN({LBu})', '=IF(C7>=10,"Sí","No")', 'LinkBudget', '0.0'),
       ('Velocidad útil mínima de bajada por casa (Mbps)', '≥ 25 Mbps', '=Capacidad!C20', '=IF(C8>=25,"Sí","No")', 'Capacidad', '0.0'),
       ('Utilización máxima del aire en bajada, año 3', '< 100 %', '=MAX(Capacidad!D25:F25)', '=IF(C9<1,"Sí","No")', 'Capacidad', '0%'),
       ('Uso del backhaul Starlink en bajada, año 3', '< 70 %', '=Capacidad!B38', '=IF(C10<0.7,"Sí","No")', 'Capacidad', '0%'),
       ('Diferencia máxima con CloudRF sin vegetación (dB)', '≤ 3 dB', '=Validacion!G9', '=IF(C11<=3,"Sí","No")', 'Validacion', '0.0'),
       ('CAPEX total (Q)', 'Informativo', f'={COST["capx"]}', '', 'Costos', '#,##0'),
       ('CAPEX por hogar (Q)', 'Informativo', f'={COST["caph"]}', '', 'Costos', '#,##0'),
       ('OPEX por hogar y mes (Q)', 'Informativo', f'={COST["opexh"]}', '', 'Costos', '#,##0.0'),
       ('Tarifa de equilibrio por hogar y mes (Q)', 'Informativo', f'={COST["eq"]}', '', 'Costos', '#,##0.0'),
       ('Recuperación del CAPEX con la tarifa propuesta (meses)', 'Informativo', f'={COST["pay"]}', '', 'Costos', '0')]
for i, (a, b, c, d, e, fm) in enumerate(met):
    r = 5 + i; put(wm, r, 1, a, BOLD); put(wm, r, 2, b); put(wm, r, 3, c, fmt=fm); put(wm, r, 4, d); put(wm, r, 5, e)
note(wm, 18, 'Aldea: Babilonia, Chisec, Alta Verapaz. 109 edificaciones georreferenciadas, unos 380 habitantes (4 por vivienda, supuesto). Torre en 15.889081, -90.531767.')

# ============================ FUENTES ============================
wf = sheet('Fuentes', [7, 70, 70, 14]); title(wf, 'Fuentes de datos', 'Copia resumida de 14_fuentes/FUENTES.md (solo las usadas en el informe).')
hdr(wf, 4, ['ID', 'Dato', 'Fuente / enlace', 'Fecha'])
skip = {'F21', 'F29', 'F30'}
r = 5
for l in open('../14_fuentes/FUENTES.md', encoding='utf-8'):
    if not l.startswith('| F'): continue
    p = [x.strip() for x in l.strip().strip('|').split('|')]
    if p[0] in skip: continue
    put(wf, r, 1, p[0], BOLD); put(wf, r, 2, p[1], wrap=True); put(wf, r, 3, p[2], wrap=True); put(wf, r, 4, p[3] if len(p) > 3 else ''); wf.row_dimensions[r].height = 30; r += 1

wb._sheets = [wb[n] for n in ['Metas_Resultados', 'Supuestos', 'Antenas_Radio', 'LinkBudget', 'Capacidad', 'Validacion', 'Costos', 'Fuentes']]
wb.save('Memoria_Calculo_Babilonia.xlsx'); print('ok')
