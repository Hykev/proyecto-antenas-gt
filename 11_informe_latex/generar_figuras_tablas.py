"""Genera figuras y tablas .tex del informe a partir de CSV y del Excel (valores recalculados)."""
import os, sys, json, math, csv
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from openpyxl import load_workbook
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); os.chdir(HERE)
os.makedirs('tablas', exist_ok=True); FIG = 'figuras/'
plt.rcParams.update({'font.size': 9})
UNI = {'^': '\\textasciicircum{}', '·': '$\\cdot$', '<': '$<$', '>': '$>$', '≈': '$\\approx$', '≤': '$\\leq$', '≥': '$\\geq$', '−': '-', '↔': '$\\leftrightarrow$', '→': '$\\rightarrow$', '↓': 'DL', '↑': 'UL', '²': '$^2$', '₂': '$_2$', 'Ω': 'Ohm', '“': '"', '”': '"', '’': "'", 'µ': '$\\mu$'}
def tx(s):
    s = str(s).replace('\\', '').replace('%', '\\%').replace('&', '\\&').replace('_', '\\_').replace('#', '\\#').replace('$', '\\$')
    for a, b in UNI.items(): s = s.replace(a, b)
    return s
df = pd.read_csv('../04_propagacion_linkbudget/linkbudget_por_casa.csv')
# ---------- diagrama del sistema ----------
def box(ax, x, y, w, h, t, c='#dbe9f7', fs=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02', fc=c, ec='#1F4E78', lw=1)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs)
def arrow(ax, a, b, t=''):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='->', color='#333', lw=1.2));
    if t: ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + .12, t, ha='center', fontsize=7)
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis('off')
box(ax, .1, 3.2, 1.6, .9, 'Constelación\nStarlink', '#e8e8e8'); box(ax, 2.2, 3.2, 1.9, .9, 'Plato Starlink\nPerformance Gen 3\n(torre, 30 m)', '#fff2cc')
box(ax, 2.2, 1.8, 1.9, .9, 'Router + switch PoE\n(gabinete, torre)', '#dbe9f7');
for i, (s, ch) in enumerate((('S1', '5745'), ('S2', '5785'), ('S3', '5825'))): box(ax, 5.0, 3.3 - i * 1.15, 2.0, .85, f'Rocket Prism + AM-5G16-120\nSector {s} · {ch} MHz', '#dbe9f7', 7)
box(ax, 7.8, 3.3, 2.0, .85, 'CPE LiteBeam 5AC\n(38 casas, S1)', '#fce4d6'); box(ax, 7.8, 2.15, 2.0, .85, 'CPE LiteBeam 5AC\n(39 casas, S2)', '#fce4d6'); box(ax, 7.8, 1.0, 2.0, .85, 'CPE LiteBeam 5AC\n(32 casas, S3)', '#fce4d6')
arrow(ax, (1.7, 3.65), (2.2, 3.65), 'Ku/Ka'); arrow(ax, (3.15, 3.2), (3.15, 2.7), 'Ethernet'); arrow(ax, (4.1, 2.25), (5.0, 3.7)); arrow(ax, (4.1, 2.25), (5.0, 2.55)); arrow(ax, (4.1, 2.25), (5.0, 1.4))
for i in range(3): arrow(ax, (7.0, 3.7 - i * 1.15), (7.8, 3.7 - i * 1.15 - (0 if i == 0 else 0.0) - (0 if i == 0 else -0.0)))
ax.text(5, .25, 'Cada CPE: router Wi-Fi en la casa · 2 puntos de acceso comunitarios', fontsize=8, style='italic')
plt.tight_layout(); plt.savefig(FIG + 'fig_diagrama_sistema.png', dpi=200); plt.close()
# ---------- arquitectura B ----------
rng = np.random.default_rng(3); fig, ax = plt.subplots(figsize=(6.5, 3.4))
pts = np.array([(-350, 20), (-250, 90), (-250, -80), (-120, 40), (-120, -70), (0, 0), (120, 50), (120, -60), (250, 40), (350, -20)])
for i in range(len(pts)):
    for j in range(i + 1, len(pts)):
        if np.hypot(*(pts[i] - pts[j])) < 170: ax.plot(*zip(pts[i], pts[j]), color='#999', lw=.8)
ax.scatter(*pts.T, s=70, c='#3182bd', zorder=3); ax.scatter(0, 0, s=170, marker='^', c='r', zorder=4, label='Nodo con Starlink (pasarela)')
ax.set(xlabel='Este (m)', ylabel='Norte (m)', title='Alternativa B: malla Wi-Fi exterior (10 nodos en postes)', aspect='equal'); ax.legend(fontsize=7, loc='lower left'); plt.tight_layout(); plt.savefig(FIG + 'fig_arquitectura_B.png', dpi=200); plt.close()
# ---------- perfiles ----------
prof = json.load(open('../04_propagacion_linkbudget/perfiles_google_earth.json')); fig, ax = plt.subplots(figsize=(8, 3.8))
for p in prof:
    d, z = zip(*p['puntos_dist_desde_torre_m_elev_m']); ax.plot(d, z, marker='o', ms=3, label=f"{p['perfil']}: casa {p['casa']} (az {p['azimut_torre_a_casa_deg']:.0f}°)")
ax.plot([0, 0], [206, 236], 'r', lw=3); ax.text(5, 232, 'Torre 30 m', color='r', fontsize=8)
ax.set(xlabel='Distancia desde la torre (m)', ylabel='Elevación (m s. n. m.)', title='Perfiles de terreno torre–casa (Google Earth)'); ax.legend(fontsize=7); ax.grid(alpha=.3); plt.tight_layout(); plt.savefig(FIG + 'fig_perfiles_terreno.png', dpi=200); plt.close()
# ---------- follaje vs altura ----------
H = [12, 18, 24, 30, 36]; n30 = [19, 18, 11, 4, 2]; med = [17.1, 17.1, 15.2, 12.0, 10.8]; p90 = [33.6, 33.6, 29.9, 27.4, 24.8]; mx = [54.3, 54.3, 45.7, 41.2, 37.8]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2)); ax[0].bar([str(h) for h in H], n30, color='#e6550d'); ax[0].set(xlabel='Altura de torre (m)', ylabel='Casas con > 30 dB de follaje', title='Casas críticas vs altura')
for k, v in (('Mediana', med), ('p90', p90), ('Máxima', mx)): ax[1].plot(H, v, marker='o', label=k)
ax[1].set(xlabel='Altura de torre (m)', ylabel='Pérdida por follaje (dB)', title='Pérdida Weissberger a 5.8 GHz'); ax[1].legend(); ax[1].grid(alpha=.3); plt.tight_layout(); plt.savefig(FIG + 'fig_follaje_vs_altura.png', dpi=200); plt.close()
# ---------- tablas desde datos ----------
# 1) sectores
rows = []
cap = {'S1': (.437, .177), 'S2': (.484, .206), 'S3': (.340, .131)}
for s in ('S1', 'S2', 'S3'):
    d = df[df.sector == s]; rows.append((s, len(d), f'{d.dist_m.max():.0f}', f'{d.L_follaje_dB.median():.1f}', f'{d.margen_dl_BPSK_dB.min():.1f}', f'{d.margen_ul_BPSK_dB.min():.1f}', f'{100*cap[s][0]:.0f}\\,\\% / {100*cap[s][1]:.0f}\\,\\%'))
open('tablas/t_sectores.tex', 'w').write('\\begin{tabular}{lrrrrrr}\\toprule Sector & Casas & Dist. máx. (m) & Follaje mediano (dB) & Margen mín. DL (dB) & Margen mín. UL (dB) & Util. aire DL/UL\\\\\\midrule\n' + '\\\\\n'.join(' & '.join(map(str, r)) for r in rows) + '\\\\\\bottomrule\\end{tabular}\n')
# 2) rangos
bins = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500)]; rows = []
for a, b in bins:
    d = df[(df.dist_m >= a) & (df.dist_m < b)]
    if len(d): rows.append((f'{a}--{b}', len(d), f'{d.G_ap_ef_dBi.median():.1f}', f'{d.FSPL_dB.median():.1f}', f'{d.L_follaje_dB.median():.1f}', f'{d.margen_dl_BPSK_dB.median():.1f}', f'{d.margen_ul_BPSK_dB.min():.1f}', tx(d.MCS_dl.mode()[0])))
open('tablas/t_rangos.tex', 'w').write('\\begin{tabular}{lrrrrrrl}\\toprule Rango (m) & Casas & $G_{AP}$ efec. (dBi) & FSPL (dB) & Follaje (dB) & Margen DL med. (dB) & Margen UL mín. (dB) & MCS DL más común\\\\\\midrule\n' + '\\\\\n'.join(' & '.join(map(str, r)) for r in rows) + '\\\\\\bottomrule\\end{tabular}\n')
# 3) peores casos y casos tipo
sel = []
for s in ('S1', 'S2', 'S3'):
    d = df[df.sector == s]; sel.append((f'Peor {s}', d.loc[d.margen_ul_BPSK_dB.idxmin()]))
sel.append(('Casa más cercana', df.loc[df.dist_m.idxmin()])); sel.append(('Casa mediana', df.iloc[(df.dist_m - df.dist_m.median()).abs().argsort().iloc[0]]))
lines = ['\\begin{tabular}{lrrrrrrrrrr}\\toprule Caso & Casa & Dist. (m) & $\\Delta$az (°) & $\\Delta$el (°) & $G_{AP}$ ef. & FSPL & Follaje & Margen DL & Margen UL & MCS DL \\\\\\midrule']
for n, r in sel: lines.append(f'{n} & {int(r.casa)} & {r.dist_m:.0f} & {r.dAz_deg:.1f} & {r.dEl_deg:.1f} & {r.G_ap_ef_dBi:.1f} & {r.FSPL_dB:.1f} & {r.L_follaje_dB:.1f} & {r.margen_dl_BPSK_dB:.1f} & {r.margen_ul_BPSK_dB:.1f} & {tx(r.MCS_dl)}\\\\')
open('tablas/t_casos.tex', 'w').write('\n'.join(lines) + '\n\\bottomrule\\end{tabular}\n')
# 4) MCS usados
vc = df.MCS_dl.value_counts(); order = ['256QAM 5/6', '256QAM 3/4', '64QAM 5/6', '64QAM 3/4', '64QAM 2/3', '16QAM 3/4', '16QAM 1/2']
open('tablas/t_mcs.tex', 'w').write('\\begin{tabular}{lr}\\toprule MCS (bajada, DL) & Casas\\\\\\midrule\n' + '\\\\\n'.join(f'{tx(m)} & {int(vc.get(m, 0))}' for m in order if vc.get(m, 0)) + '\\\\\\bottomrule\\end{tabular}\n')
# 5) BOM compacto y costos desde el Excel recalculado
wb = load_workbook('../12_excel_memoria/Memoria_Calculo_Babilonia.xlsx', data_only=True); w = wb['Costos']
items = []; r = 5
while w.cell(r, 1).value and w.cell(r, 3).value is not None and not str(w.cell(r, 1).value).startswith('Subtotal'):
    items.append((w.cell(r, 1).value, w.cell(r, 2).value, w.cell(r, 3).value, w.cell(r, 6).value, w.cell(r, 7).value, w.cell(r, 8).value)); r += 1
cats = {}
for n_, fn, q, pu, tot, src in items: cats[fn] = cats.get(fn, 0) + tot
L = ['\\begin{tabular}{p{6.2cm}rrrl}\\toprule Ítem & Cant. & P. unit. (Q) & Subtotal (Q) & Precio\\\\\\midrule']
for n_, fn, q, pu, tot, src in items:
    est = 'Estim.' if 'Estim' in str(src) else 'Ficha/tienda'
    L.append(f'{tx(n_)} & {int(q)} & {pu:,.0f} & {tot:,.0f} & {est}\\\\'.replace(',', '\\,'))
sub = w.cell(r + 1, 7).value; fl = w.cell(r + 2, 7).value; im = w.cell(r + 3, 7).value; capx = w.cell(r + 4, 7).value; caph = w.cell(r + 7, 7).value
for lab, v in (('Subtotal', sub), ('Flete y aduana (10 \\%)', fl), ('Imprevistos (10 \\%)', im), ('CAPEX total', capx), ('CAPEX por hogar (98 hogares)', caph)):
    L.append(f'\\midrule \\textbf{{{lab}}} & & & \\textbf{{{v:,.0f}}} & \\\\'.replace(',', '\\,'))
open('tablas/t_bom.tex', 'w').write('\n'.join(L) + '\n\\bottomrule\\end{tabular}\n')
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2)); ks = sorted(cats, key=cats.get, reverse=True); ax[0].barh(ks, [cats[k] / 1000 for k in ks], color='#3182bd'); ax[0].invert_yaxis(); ax[0].set(xlabel='Miles de Q (antes de flete e imprevistos)', title='CAPEX por función')
o0 = [i for i in range(1, 80) if str(w.cell(i, 1).value).startswith('OPEX mensual (año 3)')][0]
op = {}
for i in range(o0 + 2, o0 + 14):
    n_ = w.cell(i, 1).value; v = w.cell(i, 7).value
    if n_ in ('Suscripción Starlink', 'Mantenimiento (2 % anual del CAPEX)', 'Técnico local (medio tiempo)', 'Reposición de CPE (5 % anual de su costo)', 'Seguro (1 % anual del CAPEX)', 'Administración, cobranza y soporte'): op[n_] = v
lab = ['Starlink', 'Mantenimiento', 'Técnico local', 'Reposición CPE', 'Seguro', 'Administración']; val = list(op.values())
ax[1].barh(lab, val, color='#e6550d'); ax[1].invert_yaxis(); ax[1].set(xlabel='Q por mes', title='OPEX mensual (año 3)'); plt.tight_layout(); plt.savefig(FIG + 'fig_costos.png', dpi=200); plt.close()
L = ['\\begin{tabular}{lr}\\toprule Concepto & Q por mes\\\\\\midrule']
for n_, lb_ in zip(op, lab): L.append(f'{lb_} & {op[n_]:,.0f}\\\\'.replace(',', '\\,'))
tot_op = w.cell(o0 + 15, 7).value; ph = w.cell(o0 + 16, 7).value; am = w.cell(o0 + 17, 7).value; eq = w.cell(o0 + 18, 7).value; pay = w.cell(o0 + 22, 7).value
L.append(f'\\midrule \\textbf{{OPEX mensual}} & \\textbf{{{tot_op:,.0f}}}\\\\ OPEX por hogar y mes & {ph:,.1f}\\\\ Amortización del CAPEX (5 años) por hogar y mes & {am:,.1f}\\\\ \\textbf{{Tarifa de equilibrio por hogar y mes}} & \\textbf{{{eq:,.1f}}}\\\\'.replace(',', '\\,'))
open('tablas/t_opex.tex', 'w').write('\n'.join(L) + '\n\\bottomrule\\end{tabular}\n')
json.dump(dict(capx=capx, caph=caph, opex=tot_op, opexh=ph, am=am, eq=eq, pay=pay, sub=sub), open('costos_resumen.json', 'w'))
# 6) sensibilidad
sv = pd.read_csv('../04_propagacion_linkbudget/sensibilidad_escenarios.csv'); L = ['\\begin{tabular}{p{6.6cm}rrrr}\\toprule Escenario & Casas útiles & Margen DL mín. (dB) & Margen UL mín. (dB) & Casas $>$30 dB\\\\\\midrule']
for _, r_ in sv.iterrows(): L.append(f'{tx(r_.iloc[0])} & {int(r_.iloc[1])} & {r_.iloc[2]:.1f} & {r_.iloc[3]:.1f} & {int(r_.iloc[6])}\\\\')
open('tablas/t_sens.tex', 'w').write('\n'.join(L) + '\n\\bottomrule\\end{tabular}\n')
print('listo', round(capx), round(eq, 1), round(pay, 1))
