"""Genera Memoria_Calculo_Babilonia.xlsx con formulas visibles. Uso: python3 -I construir_excel.py"""
import csv, os, sys
sys.path.insert(0, '../04_propagacion_linkbudget')
import rfmodel as R
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.comments import Comment

F = 'Arial'; BLUE = Font(name=F, color='0000FF', size=10); BLK = Font(name=F, size=10); BOLD = Font(name=F, bold=True, size=10); WH = Font(name=F, bold=True, color='FFFFFF', size=10)
HDR = PatternFill('solid', fgColor='1F4E78'); KEY = PatternFill('solid', fgColor='FFF2CC'); GREY = PatternFill('solid', fgColor='EDEDED')
thin = Side(style='thin', color='BBBBBB'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
wb = Workbook()
def sheet(name, widths=None):
    ws = wb.create_sheet(name); ws.sheet_view.showGridLines = False
    for i, w in enumerate(widths or [], 1): ws.column_dimensions[L(i)].width = w
    return ws
def hdr(ws, row, vals, col=1):
    for i, v in enumerate(vals):
        c = ws.cell(row, col + i, v); c.font = WH; c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center'); c.border = BOX
def put(ws, r, c, v, font=BLK, fmt=None, fill=None, wrap=False):
    x = ws.cell(r, c, v); x.font = font; x.border = BOX
    if fmt: x.number_format = fmt
    if fill: x.fill = fill
    if wrap: x.alignment = Alignment(wrap_text=True, vertical='top')
    return x
def title(ws, t, sub=None):
    ws['A1'] = t; ws['A1'].font = Font(name=F, bold=True, size=14, color='1F4E78')
    if sub: ws['A2'] = sub; ws['A2'].font = Font(name=F, italic=True, size=9, color='555555')
wb.remove(wb.active)

# ===================== SUPUESTOS =====================
ws = sheet('Supuestos', [44, 4, 14, 12, 70]); title(ws, 'Supuestos y parámetros de diseño', 'Azul = dato de entrada (cámbielo y todo el libro se recalcula). Negro = fórmula. Amarillo = supuesto clave.')
hdr(ws, 4, ['Parámetro', '', 'Valor', 'Unidad', 'Fuente / nota'])
SUP = {}
rows = [
 ('Frecuencia de diseño', 'f', 5.8, 'GHz', 'Canal central de la banda 5725–5850 MHz (F28)', None),
 ('Longitud de onda', 'lam', '=299792458/(C5*1E9)', 'm', 'c / f', None),
 ('Altura de la torre', 'Htow', 30, 'm', 'Decisión D07 (análisis de follaje, FUENTES F17)', 'k'),
 ('Elevación del terreno en la torre', 'Z0', 206, 'm s. n. m.', 'Google Earth (F12)', None),
 ('Altura del CPE sobre el terreno (mástil)', 'hcpe', 6, 'm', 'Supuesto de diseño (mástil sobre techo)', None),
 ('Ganancia del CPE LiteBeam 5AC Gen2', 'Gcpe', 23, 'dBi', 'Ficha F27', None),
 ('Pérdida de jumpers/conectores en el AP', 'Lfeed', 0.5, 'dB', 'Supuesto', None),
 ('Pérdida por desalineación del CPE', 'Lmis', 1.0, 'dB', 'Supuesto', None),
 ('Pérdida por lluvia (trayecto ≤ 0.42 km)', 'Lrain', 0.3, 'dB', 'UIT-R P.838-3, valor aproximado (por verificar)', None),
 ('Penalización de sensibilidad por canal de 20 MHz', 'pen', 3.0, 'dB', 'Supuesto conservador: la ficha F24 da la sensibilidad en otro ancho de canal', 'k'),
 ('Tx del CPE por debajo del AP', 'cpeoff', 3.0, 'dB', '25 dBm (CPE) frente a 28 dBm (AP)', None),
 ('Margen de diseño exigido (M_req)', 'Mreq', 10, 'dB', 'Criterio del proyecto (FICHA §9)', 'k'),
 ('Eficiencia MAC (TDD)', 'eta', 0.65, '', 'Supuesto', 'k'),
 ('Fracción de la trama para bajada', 'dlsh', 0.75, '', 'Supuesto', 'k'),
 ('Ganancia sectorial AM-5G16-120', 'gap0', 15.5, 'dBi', 'Ficha F25: 15–16 dBi (valor medio)', None),
 ('Ancho de haz horizontal a 6 dB', 'az6', 137, '°', 'Ficha F25', None),
 ('Inclinación de fábrica (elevación)', 'tilt', 4, '°', 'Ficha F25', None),
 ('Inclinación mecánica adicional', 'mech', 0, '°', 'Decisión D16', 'k'),
 ('Largo físico de la antena sectorial', 'Lant', 0.367, 'm', 'Ficha F25 (367 mm)', None),
 ('Tope de atenuación azimutal (F/B y laterales)', 'capaz', 25, 'dB', 'SUPUESTO: la ficha no da F/B', 'k'),
 ('Piso de atenuación en elevación', 'capel', 25, 'dB', 'SUPUESTO', 'k'),
 ('Acimut del eje S1 / S2 / S3', 'b1', 150, '°', 'Sector S1: 90–210°', None),
 ('', 'b2', 270, '°', 'Sector S2: 210–330°', None),
 ('', 'b3', 30, '°', 'Sector S3: 330–90°', None),
 ('Adopción de diseño (año 3)', 'adopt', 0.9, '', 'D04', 'k'),
 ('Demanda media por suscriptor en hora pico (bajada)', 'dem_dl', 1.0, 'Mbps', '4 Mbps por usuario activo × 25 % de simultaneidad', None),
 ('Demanda media por suscriptor en hora pico (subida)', 'dem_ul', 0.125, 'Mbps', '0.5 Mbps × 25 %', None),
 ('Tipo de cambio', 'fx', 7.6445, 'GTQ/USD', 'F22 (26-oct-2026)', 'k'),
]
r = 5
for lab, key, val, unit, note, k in rows:
    put(ws, r, 1, lab, BOLD if lab else BLK); put(ws, r, 3, val, BLUE if not str(val).startswith('=') else BLK, fill=KEY if k else None); put(ws, r, 4, unit); put(ws, r, 5, note, wrap=True)
    SUP[key] = f'Supuestos!$C${r}'; r += 1
S = lambda k: SUP[k]
# ===================== MCS =====================
wm = sheet('MCS', [14, 10, 10, 14, 12, 14, 16]); title(wm, 'Tabla de modulaciones del Rocket Prism 5AC Gen2', 'Fuente F24 (netxl). La sensibilidad es la de la ficha (±2 dB). Tasa PHY = 2 flujos × 52 subportadoras × bits × codificación / 3.6 µs (canal 20 MHz, supuesto).')
hdr(wm, 4, ['Modulación', 'Bits/símbolo', 'Codificación', 'Sensibilidad (dBm)', 'Tx máx. (dBm)', 'Tasa PHY 20 MHz (Mbps)', 'Sens. + penalización (dBm)'])
mcs = [('BPSK 1/2', 1, .5, -96, 28), ('QPSK 1/2', 2, .5, -95, 28), ('QPSK 3/4', 2, .75, -92, 28), ('16QAM 1/2', 4, .5, -90, 28), ('16QAM 3/4', 4, .75, -86, 28), ('64QAM 2/3', 6, 2 / 3, -83, 28), ('64QAM 3/4', 6, .75, -77, 27), ('64QAM 5/6', 6, 5 / 6, -74, 26), ('256QAM 3/4', 8, .75, -69, 24), ('256QAM 5/6', 8, 5 / 6, -65, 22)]
for i, m in enumerate(mcs):
    rr = 5 + i
    for j, v in enumerate(m): put(wm, rr, 1 + j, v, BLUE, fmt='0.000' if j == 2 else None)
    put(wm, rr, 6, f'=2*52*B{rr}*C{rr}/3.6', fmt='0.0'); put(wm, rr, 7, f'=D{rr}+{S("pen")}', fmt='0.0')
M0, M1 = 5, 14   # filas de la tabla
MN, MS, MT, MR = f'MCS!$A${M0}:$A${M1}', f'MCS!$G${M0}:$G${M1}', f'MCS!$E${M0}:$E${M1}', f'MCS!$F${M0}:$F${M1}'
# ===================== CASAS =====================
fol = {int(x['casa']): int(x['follaje_m']) for x in csv.DictReader(open('../04_propagacion_linkbudget/linkbudget_por_casa.csv'))}
H = R.load_houses()
wc = sheet('Enlace_por_casa', [7, 9, 9, 9, 9, 8, 9, 9, 9, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 8, 8, 13, 10, 10, 11, 11])
title(wc, 'Presupuesto de enlace por casa (torre 30 m → CPE), bajada y subida', 'Azul: datos de entrada por casa (georreferenciación, terreno y profundidad de follaje de rfmodel.py). Todas las demás columnas son fórmulas.')
cols = ['Casa', 'Acimut torre→casa (°)', 'Distancia horiz. (m)', 'Elev. terreno casa (m)', 'Follaje atravesado (m)', 'Sector', 'Eje sector (°)', 'Δ acimut (°)', 'Desnivel antena–CPE (m)', 'Distancia 3D (m)', 'Elevación del rayo (°)', 'Δ elev. respecto al haz (°)',
        'Pérd. patrón azimut (dB)', 'u (apertura)', 'Pérd. patrón elev. (dB)', 'Ganancia AP efectiva (dBi)', 'FSPL (dB)', 'Pérd. follaje Weissberger (dB)', 'Pérdida total de trayecto (dB)', 'Margen DL sobre BPSK (dB)', 'Margen UL sobre BPSK (dB)', 'N.º MCS útiles DL', 'N.º MCS útiles UL', 'MCS DL', 'Tasa DL (Mbps)', 'Tasa UL (Mbps)', 'Carga aire DL', 'Carga aire UL']
cols = cols[:23] + ['MCS DL', 'Tasa DL (Mbps)', 'Tasa UL (Mbps)', 'Carga aire DL', 'Carga aire UL']
hdr(wc, 4, cols); wc.row_dimensions[4].height = 58
R0 = 5
for i, h in enumerate(H):
    r = R0 + i
    put(wc, r, 1, h['id'], BLUE); put(wc, r, 2, round(h['az'], 2), BLUE, '0.00'); put(wc, r, 3, round(h['d'], 1), BLUE, '0.0'); put(wc, r, 4, round(h['z'], 1), BLUE, '0.0'); put(wc, r, 5, fol[h['id']], BLUE, '0')
    put(wc, r, 6, f'=IF(AND(B{r}>=90,B{r}<210),"S1",IF(AND(B{r}>=210,B{r}<330),"S2","S3"))')
    put(wc, r, 7, f'=IF(F{r}="S1",{S("b1")},IF(F{r}="S2",{S("b2")},{S("b3")}))')
    put(wc, r, 8, f'=MOD(B{r}-G{r}+180,360)-180', fmt='0.0')
    put(wc, r, 9, f'={S("Htow")}-(D{r}-{S("Z0")})-{S("hcpe")}', fmt='0.0')
    put(wc, r, 10, f'=SQRT(C{r}^2+I{r}^2)', fmt='0.0')
    put(wc, r, 11, f'=DEGREES(ATAN2(C{r},I{r}))', fmt='0.00')
    put(wc, r, 12, f'=K{r}-({S("tilt")}+{S("mech")})', fmt='0.00')
    put(wc, r, 13, f'=MIN(6*(2*H{r}/{S("az6")})^2,{S("capaz")})', fmt='0.0')
    put(wc, r, 14, f'=PI()*{S("Lant")}/{S("lam")}*SIN(RADIANS(L{r}))', fmt='0.000')
    put(wc, r, 15, f'=IF(ABS(N{r})<1E-9,0,MIN(-20*LOG10(MAX(ABS(SIN(N{r})/N{r}),1E-6)),{S("capel")}))', fmt='0.0')
    put(wc, r, 16, f'={S("gap0")}-M{r}-O{r}', fmt='0.0')
    put(wc, r, 17, f'=32.44+20*LOG10(J{r}/1000)+20*LOG10({S("f")}*1000)', fmt='0.0')
    put(wc, r, 18, f'=IF(E{r}<=0,0,IF(E{r}<=14,0.45*{S("f")}^0.284*E{r},1.33*{S("f")}^0.284*MIN(E{r},400)^0.588))', fmt='0.0')
    put(wc, r, 19, f'=Q{r}+R{r}+{S("Lmis")}+{S("Lrain")}+{S("Lfeed")}-P{r}-{S("Gcpe")}', fmt='0.0')
    put(wc, r, 20, f'=MCS!$E${M0}-S{r}-MCS!$G${M0}', fmt='0.0')
    put(wc, r, 21, f'=T{r}-{S("cpeoff")}', fmt='0.0')
    put(wc, r, 22, f'=SUMPRODUCT(--({MT}-$S{r}-{MS}>={S("Mreq")}))', fmt='0')
    put(wc, r, 23, f'=SUMPRODUCT(--({MT}-{S("cpeoff")}-$S{r}-{MS}>={S("Mreq")}))', fmt='0')
    put(wc, r, 24, f'=IF(V{r}=0,"ninguno",INDEX({MN},V{r}))')
    put(wc, r, 25, f'=IF(V{r}=0,0,INDEX({MR},V{r}))', fmt='0.0')
    put(wc, r, 26, f'=IF(W{r}=0,0,INDEX({MR},W{r}))', fmt='0.0')
    put(wc, r, 27, f'=IF(Y{r}>0,{S("adopt")}*{S("dem_dl")}/({S("eta")}*Y{r}),0)', fmt='0.0000')
    put(wc, r, 28, f'=IF(Z{r}>0,{S("adopt")}*{S("dem_ul")}/({S("eta")}*Z{r}),0)', fmt='0.0000')
RN = R0 + len(H) - 1
wc.freeze_panes = 'B5'
for c in range(23, 24): pass
# columnas reordenadas: borrar encabezado sobrante (la tabla ya tiene 28 columnas)
CR = lambda col: f'Enlace_por_casa!${col}${R0}:${col}${RN}'
# ===================== CAPACIDAD =====================
wk = sheet('Capacidad', [34, 12, 12, 12, 14, 60]); title(wk, 'Capacidad por sector y backhaul Starlink', 'Utilización de aire = suma(demanda / (η_MAC · tasa PHY de cada casa)) / fracción de trama. Menor a 100 % = la demanda cabe.')
hdr(wk, 4, ['Sector', 'Casas', 'Suscriptores (adopción)', 'Util. aire bajada', 'Util. aire subida', 'Nota'])
for i, s in enumerate(('S1', 'S2', 'S3')):
    r = 5 + i; put(wk, r, 1, s, BOLD); put(wk, r, 2, f'=COUNTIF({CR("F")},A{r})'); put(wk, r, 3, f'=B{r}*{S("adopt")}', fmt='0.0')
    put(wk, r, 4, f'=SUMIF({CR("F")},A{r},{CR("AA")})/{S("dlsh")}', fmt='0.0%'); put(wk, r, 5, f'=SUMIF({CR("F")},A{r},{CR("AB")})/(1-{S("dlsh")})', fmt='0.0%')
put(wk, 5, 6, 'Año 3 (90 % de adopción, 4 Mbps de pico por usuario activo, 25 % simultaneidad)', wrap=True)
wk['A9'] = 'Escenarios de crecimiento (escala lineal sobre la utilización base)'; wk['A9'].font = BOLD
hdr(wk, 10, ['Escenario', 'Adopción', 'Pico por usuario activo (Mbps)', 'Util. S1', 'Util. S2', 'Util. S3'])
sc = [('Año 1', .6, 4), ('Año 3 (base)', .9, 4), ('Año 5, 6 Mbps', 1.0, 6), ('Año 5, 8 Mbps', 1.0, 8)]
for i, (n, a, p) in enumerate(sc):
    r = 11 + i; put(wk, r, 1, n); put(wk, r, 2, a, BLUE, '0%'); put(wk, r, 3, p, BLUE)
    for j in range(3): put(wk, r, 4 + j, f'=$D${5+j}*(B{r}/{S("adopt")})*(C{r}/(4))', fmt='0.0%')
wk['A16'] = 'Backhaul Starlink'; wk['A16'].font = BOLD
hdr(wk, 17, ['Concepto', 'Año 1', 'Año 3', 'Unidad', '', 'Nota'])
bh = [('Puntos con CPE', 65, 98, 'casas', 'D04: 60 % / 90 % de 109 + 2 hotspots'), ('Simultaneidad pico', .25, .25, '', 'Supuesto'), ('Tasa por usuario activo bajada', 4, 4, 'Mbps', 'Supuesto (video SD/HD, mensajería)'), ('Tasa por usuario activo subida', .5, .5, 'Mbps', 'Supuesto')]
for i, (n, a, b, u, nt) in enumerate(bh):
    r = 18 + i; put(wk, r, 1, n); put(wk, r, 2, a, BLUE); put(wk, r, 3, b, BLUE); put(wk, r, 4, u); put(wk, r, 6, nt)
put(wk, 22, 1, 'Pico agregado bajada'); put(wk, 22, 2, '=B18*B19*B20', fmt='0.0'); put(wk, 22, 3, '=C18*C19*C20', fmt='0.0'); put(wk, 22, 4, 'Mbps')
put(wk, 23, 1, 'Pico agregado subida'); put(wk, 23, 2, '=B18*B19*B21', fmt='0.0'); put(wk, 23, 3, '=C18*C19*C21', fmt='0.0'); put(wk, 23, 4, 'Mbps')
put(wk, 24, 1, 'Starlink bajada (diseño, límite inferior)'); put(wk, 24, 2, 145, BLUE); put(wk, 24, 3, 145, BLUE); put(wk, 24, 4, 'Mbps'); put(wk, 24, 6, 'F09 (captura starlink.com 23-oct-2026)')
put(wk, 25, 1, 'Starlink subida (diseño)'); put(wk, 25, 2, 21, BLUE); put(wk, 25, 3, 21, BLUE); put(wk, 25, 4, 'Mbps'); put(wk, 25, 6, 'F11')
put(wk, 26, 1, 'Uso del backhaul bajada'); put(wk, 26, 2, '=B22/B24', fmt='0%'); put(wk, 26, 3, '=C22/C24', fmt='0%')
put(wk, 27, 1, 'Uso del backhaul subida'); put(wk, 27, 2, '=B23/B25', fmt='0%'); put(wk, 27, 3, '=C23/C25', fmt='0%')
put(wk, 28, 1, 'Consumo mensual por punto (GB)'); put(wk, 28, 2, 25, BLUE); put(wk, 28, 3, 25, BLUE); put(wk, 28, 6, 'Supuesto')
put(wk, 29, 1, 'Consumo mensual total (TB)'); put(wk, 29, 2, '=B18*B28/1000', fmt='0.00'); put(wk, 29, 3, '=C18*C28/1000', fmt='0.00')
# ===================== INTERFERENCIA / SENSIBILIDAD =====================
wi = sheet('Interferencia', [8, 9, 16, 18, 14, 16, 14]); title(wi, 'Plan de frecuencias e interferencia entre sectores', 'Resultados de analisis_e3.py (modelo C/I entre sectores; ruido −95 dBm; rechazo de canal adyacente 30 dB, supuestos). Valores calculados fuera de Excel.')
hdr(wi, 4, ['Sector', 'Canal (MHz)', 'Ancho (MHz)', 'Eje (°)', 'Polarización', 'Sincronía', ''])
for i, (s, ch, b) in enumerate((('S1', 5745, 150), ('S2', 5785, 270), ('S3', 5825, 30))):
    for j, v in enumerate((s, ch, 20, b, 'Doble (H/V)', 'GPS')): put(wi, 5 + i, 1 + j, v, BLUE if j in (1, 2, 3) else BLK)
hdr(wi, 10, ['Casa', 'Sector', 'C/I cocanal (dB)', 'MCS plan 3 canales', 'Tasa plan (Mbps)', 'MCS con 1 solo canal', 'Tasa 1 canal (Mbps)'])
it = list(csv.DictReader(open('../04_propagacion_linkbudget/interferencia_por_casa.csv')))
for i, x in enumerate(it):
    r = 11 + i
    for j, k in enumerate(['casa', 'sector', 'C/I_cocanal_dB', 'MCS_plan_3canales', 'R_plan_Mbps', 'MCS_1canal', 'R_1canal_Mbps']):
        v = x[k]; v = float(v) if j in (2, 4, 6) else (int(v) if j == 0 else v); put(wi, r, 1 + j, v, BLUE)
IE = 10 + len(it)
put(wi, 6 + 0, 9, 'Resumen', BOLD); put(wi, 7, 9, 'C/I cocanal mínimo (dB)'); put(wi, 7, 10, f'=MIN(C11:C{IE})', fmt='0.0'); put(wi, 8, 9, 'C/I cocanal mediana (dB)'); put(wi, 8, 10, f'=MEDIAN(C11:C{IE})', fmt='0.0')
put(wi, 9, 9, 'Casas sin MCS útil: plan 3 canales'); put(wi, 9, 10, f'=COUNTIF(D11:D{IE},"ninguno")'); put(wi, 10, 9, 'Casas sin MCS útil: 1 solo canal'); put(wi, 10, 10, f'=COUNTIF(F11:F{IE},"ninguno")')
wi.column_dimensions['I'].width = 34
wsn = sheet('Sensibilidad', [48, 16, 14, 14, 14, 12, 14]); title(wsn, 'Escenarios de sensibilidad', 'Resultados de analisis_e3.py (se recalcula todo el modelo por escenario).')
hdr(wsn, 4, ['Escenario', 'Casas con enlace útil ↓ y ↑', 'Margen mín. ↓ (dB)', 'Margen mín. ↑ (dB)', 'Margen mediano ↓ (dB)', 'Util. máx. DL', 'Casas > 30 dB follaje'])
for i, x in enumerate(csv.reader(open('../04_propagacion_linkbudget/sensibilidad_escenarios.csv'))):
    if i == 0: continue
    for j, v in enumerate(x):
        put(wsn, 4 + i, 1 + j, v if j == 0 else float(v), BLUE, '0.0%' if j == 5 else None)
wsn['A16'] = 'Criterio: un enlace es útil si hay un MCS con margen ≥ 10 dB; margen mínimo < 10 dB activa la contingencia D08 (mástil de 10 m / CPE de mayor ganancia / relevo).'; wsn['A16'].font = Font(name=F, italic=True, size=9)
exec(open('parte2.py', encoding='utf-8').read())
