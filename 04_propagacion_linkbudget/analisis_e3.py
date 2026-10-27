"""E3: interferencia, sensibilidad y figuras. Uso: python3 analisis_e3.py  (escribe CSV y figuras)."""
import os, sys, math, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import linkbudget as lb, rfmodel as R
FIG = '../11_informe_latex/figuras/'; os.makedirs(FIG, exist_ok=True)
A = lb.ANT['AM-5G16-120']; H = {h['id']: h for h in R.load_houses()}; cache = {}
base = lb.run('AM-5G16-120', 30, 0, 20, cache)
NF, ACR = 6.0, 30.0   # [S] figura de ruido 6 dB; rechazo de canal adyacente 30 dB (canales separados 40 MHz, 20 MHz de ancho)
NOISE = -174 + 10 * math.log10(20e6) + NF
def snr_req(m): return m[3] + lb.BW_PEN - NOISE
def gap(h, sec, tilt=0.0):
    da = h['az'] - lb.SECT[sec]; drop = 30 - (h['z'] - R.Z0) - 6; el = math.degrees(math.atan2(drop, h['d']))
    return A['g'] - lb.az_loss(da, A) - lb.el_loss(el - (A['tilt_el'] + tilt), A)
def sinr_rows(reuse1):
    rows = []
    for o in base:
        h = H[o['casa']]; s = o['sector']; gs = gap(h, s); pr = o['Pr_dl_BPSK_dBm']
        i_lin = 0.0
        for t in lb.SECT:
            if t == s: continue
            pi = pr - (gs - gap(h, t)) - (0 if reuse1 else ACR)
            i_lin += 10 ** (pi / 10)
        n_lin = 10 ** (NOISE / 10); sinr = pr - 10 * math.log10(n_lin + i_lin)
        ci = pr - 10 * math.log10(i_lin) if i_lin else 99
        best = None
        for m in lb.MCS:
            p = m[4] + (pr - 28) if False else pr - (28 - m[4])   # potencia recibida con la Tx de ese MCS
            sn = p - 10 * math.log10(n_lin + i_lin * 10 ** (-(28 - m[4]) / 10))
            if sn - snr_req(m) >= 3.0 and p - (m[3] + lb.BW_PEN) >= lb.M_REQ: best = m   # 3 dB de margen sobre SNR requerida (ademas de 10 dB de enlace)
        rows.append((o['casa'], s, round(ci, 1), best[0] if best else 'ninguno', round(lb.phy(best), 1) if best else 0.0))
    return rows
def cap_from(rate_by_house, adopt=0.9, dem=1.0):
    res = {}
    for s in lb.SECT:
        hs = [o for o in base if o['sector'] == s]
        u = sum(adopt * dem / (lb.ETA_MAC * rate_by_house[o['casa']]) for o in hs if rate_by_house[o['casa']] > 0) / lb.DL_SHARE
        res[s] = round(u, 2)
    return res
plan = sinr_rows(False); reuse = sinr_rows(True)
rp = {r[0]: r[4] for r in plan}; rr = {r[0]: r[4] for r in reuse}
with open('interferencia_por_casa.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['casa', 'sector', 'C/I_cocanal_dB', 'MCS_plan_3canales', 'R_plan_Mbps', 'MCS_1canal', 'R_1canal_Mbps'])
    for a, b in zip(plan, reuse): w.writerow([a[0], a[1], b[2], a[3], a[4], b[3], b[4]])
ci = np.array([r[2] for r in reuse])
print('C/I cocanal (reuso 1): min %.1f mediana %.1f p10 %.1f dB' % (ci.min(), np.median(ci), np.percentile(ci, 10)))
print('MCS plan 3 canales:', {k: sum(1 for r in plan if r[3] == k) for k in sorted({r[3] for r in plan})})
print('MCS reuso 1 canal :', {k: sum(1 for r in reuse if r[3] == k) for k in sorted({r[3] for r in reuse})})
print('utilizacion DL plan 3 canales', cap_from(rp), '| reuso 1 canal', cap_from(rr))
# ---- Sensibilidad
sc = []
def scen(name, **kw):
    out = lb.run('AM-5G16-120', kw.get('H', 30), kw.get('tilt', 0), kw.get('hc', 20), cache if kw.get('H', 30) == 30 and kw.get('hc', 20) == 20 else {}, extra_loss=kw.get('extra', 0))
    md = [o['margen_dl_BPSK_dB'] for o in out]; mu = [o['margen_ul_BPSK_dB'] for o in out]
    ok = sum(1 for o in out if o['R_dl_Mbps'] > 0 and o['R_ul_Mbps'] > 0); lo = sum(1 for a, b in zip(md, mu) if min(a, b) - 0 < lb.M_REQ + 0)
    cap = lb.capacity(out)
    sc.append((name, ok, round(min(md), 1), round(min(mu), 1), round(float(np.median(md)), 1), max(c['util_dl'] for c in cap.values()), sum(1 for o in out if o['L_follaje_dB'] > 30)))
scen('Base: torre 30 m, copa 20 m'); scen('Torre 24 m', H=24); scen('Torre 36 m', H=36)
scen('Copa 15 m', hc=15); scen('Copa 25 m', hc=25); scen('Copa 25 m + torre 24 m', hc=25, H=24)
scen('Desvanecimiento extra 6 dB (lluvia fuerte/arboles mojados)', extra=6.0)
scen('Error de montaje +2 grados inclinacion', tilt=2); scen('Error de montaje +4 grados inclinacion', tilt=4)
with open('sensibilidad_escenarios.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['escenario', 'casas_enlace_util_DL_y_UL', 'margen_min_DL_dB', 'margen_min_UL_dB', 'margen_mediano_DL_dB', 'util_max_DL', 'casas_follaje_>30dB']); w.writerows(sc)
for s in sc: print(s)
# demanda
for lab, ad, dm in (('Año 1 (60 %)', .6, 1.0), ('Año 3 (90 %)', .9, 1.0), ('Año 5 (100 % + 6 Mbps pico)', 1.0, 1.5), ('Año 5 (100 % + 8 Mbps pico)', 1.0, 2.0)):
    o = lb.capacity(base, adopt=ad, dem_dl=dm); print(lab, {k: v['util_dl'] for k, v in o.items()})
# ---- Figuras
plt.rcParams.update({'font.size': 9, 'axes.grid': True, 'grid.alpha': .3})
az = np.linspace(-180, 180, 721); el = np.linspace(-40, 40, 801)
gh = np.array([-lb.az_loss(a, A) for a in az]); gv = np.array([-lb.el_loss(e, A) for e in el])
def hpbw(x, y, thr=-3):
    i = np.where(y >= thr)[0]; return x[i[-1]] - x[i[0]]
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
ax[0].plot(az, gh, 'b'); ax[0].axhline(-3, c='gray', ls=':'); ax[0].axhline(-6, c='gray', ls='--')
for s in (-68.5, 68.5): ax[0].plot(s, -6, 'ro')
ax[0].set(title='Corte horizontal (acimut) AM-5G16-120', xlabel='Ángulo respecto al eje (°)', ylabel='Ganancia relativa (dB)', ylim=(-30, 2), xlim=(-180, 180))
ax[0].text(-175, -28, f'HPBW(3 dB) modelo = {hpbw(az, gh):.0f}°; ficha: 137° a 6 dB (puntos rojos)\nF/B y lóbulos: tope supuesto 25 dB [S]', fontsize=7)
ax[1].plot(el, gv, 'g'); ax[1].axhline(-3, c='gray', ls=':')
ax[1].set(title='Corte vertical (elevación) AM-5G16-120', xlabel='Ángulo respecto al eje (°)', ylabel='Ganancia relativa (dB)', ylim=(-30, 2), xlim=(-40, 40))
ax[1].text(-39, -28, f'HPBW(3 dB) modelo = {hpbw(el, gv):.1f}° (apertura L=0,367 m: 0,886λ/L = {0.886*lb.LAM/0.367*57.2958:.1f}°)\nficha: 8°; 1.er nulo y lóbulos de la apertura uniforme', fontsize=7)
plt.tight_layout(); plt.savefig(FIG + 'fig_patron_sectorial_H_V.png', dpi=200); plt.close()
fig = plt.figure(figsize=(9, 4)); a1 = fig.add_subplot(121, projection='polar'); a2 = fig.add_subplot(122, projection='polar')
a1.plot(np.radians(az), np.maximum(gh, -30) + 30, 'b'); a1.set_title('Polar horizontal (0 dB = 30 en radio)', fontsize=8); a1.set_theta_zero_location('N'); a1.set_rticks([10, 20, 27, 30])
e2 = np.radians(el); a2.plot(e2, np.maximum(gv, -30) + 30, 'g'); a2.set_title('Polar vertical (elevación)', fontsize=8); a2.set_theta_zero_location('E'); a2.set_thetalim(-np.pi / 2, np.pi / 2)
plt.tight_layout(); plt.savefig(FIG + 'fig_patron_sectorial_polar.png', dpi=200); plt.close()
# patrón efectivo por casa: elevacion respecto de la direccion de las casas
cols = {'256QAM 5/6': '#08519c', '256QAM 3/4': '#3182bd', '64QAM 5/6': '#31a354', '64QAM 3/4': '#74c476', '64QAM 2/3': '#a1d99b', '16QAM 3/4': '#fd8d3c', '16QAM 1/2': '#e6550d'}
fig, ax = plt.subplots(figsize=(9, 4.6))
for o in base:
    h = H[o['casa']]; ax.scatter(h['x'], h['y'], c=cols.get(o['MCS_dl'], 'k'), s=26, edgecolor='k', lw=.3)
    if o['casa'] in (26, 27, 97, 30): ax.annotate(str(o['casa']), (h['x'], h['y']), fontsize=7, xytext=(3, 3), textcoords='offset points')
ax.scatter(0, 0, marker='^', s=140, c='r', zorder=5, label='Torre 30 m')
for s, b in lb.SECT.items():
    for edge in (b - 60, b + 60): ax.plot([0, 450 * math.sin(math.radians(edge))], [0, 450 * math.cos(math.radians(edge))], 'k--', lw=.6)
    ax.text(300 * math.sin(math.radians(b)), 300 * math.cos(math.radians(b)), s, fontsize=11, weight='bold', alpha=.5)
for r in (100, 200, 300, 400): ax.add_patch(plt.Circle((0, 0), r, fill=False, ls=':', color='gray'))
for k, v in cols.items(): ax.scatter([], [], c=v, label=k, edgecolor='k', lw=.3)
ax.set(aspect='equal', xlabel='Este (m)', ylabel='Norte (m)', title='Modulación máxima en bajada por casa (margen ≥ 10 dB)'); ax.legend(fontsize=6, loc='upper left', ncol=2); plt.tight_layout(); plt.savefig(FIG + 'fig_cobertura_mcs.png', dpi=200); plt.close()
fig, ax = plt.subplots(1, 3, figsize=(11, 3.2))
ax[0].hist([o['L_follaje_dB'] for o in base], bins=15, color='#4c9a2a'); ax[0].set(title='Pérdida por follaje (Weissberger)', xlabel='dB', ylabel='Casas')
ax[1].hist([o['margen_dl_BPSK_dB'] for o in base], bins=15, color='#3182bd', alpha=.8, label='Bajada'); ax[1].hist([o['margen_ul_BPSK_dB'] for o in base], bins=15, color='#e6550d', alpha=.6, label='Subida'); ax[1].axvline(10, c='k', ls='--'); ax[1].legend(); ax[1].set(title='Margen sobre BPSK 1/2', xlabel='dB')
ax[2].scatter([o['dist_m'] for o in base], [o['margen_ul_BPSK_dB'] for o in base], s=10, c='#e6550d'); ax[2].axhline(10, c='k', ls='--'); ax[2].set(title='Margen de subida vs distancia', xlabel='m', ylabel='dB')
plt.tight_layout(); plt.savefig(FIG + 'fig_histogramas_enlace.png', dpi=200); plt.close()
fig, ax = plt.subplots(figsize=(7, 3.4)); labs = [s[0] for s in sc]; ax.barh(range(len(sc)), [s[2] for s in sc], color='#3182bd'); ax.set_yticks(range(len(sc))); ax.set_yticklabels(labs, fontsize=7); ax.axvline(10, c='r', ls='--'); ax.invert_yaxis()
ax.set(xlabel='Margen mínimo de bajada sobre BPSK 1/2 (dB)', title='Sensibilidad del peor enlace'); plt.tight_layout(); plt.savefig(FIG + 'fig_sensibilidad.png', dpi=200); plt.close()
print('figuras listas')
