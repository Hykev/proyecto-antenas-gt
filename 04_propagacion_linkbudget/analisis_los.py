"""Altura minima de torre por casa (despeje del 60 % de la 1a zona de Fresnel, 5.8 GHz).
Terreno: interpolacion RBF de perfiles Google Earth + esquinas + centro.
Copas: mascara por color sobre la foto satelital (supuesto de altura de copa por escenario).
Salida: 04_propagacion_linkbudget/los_altura_minima_por_casa.csv  y resumen por pantalla.
Uso: python3 -I analisis_los.py
"""
import json, math, csv, os
import numpy as np, cv2
from scipy.interpolate import RBFInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
S, AX, AY, Z0 = 0.514, 829, 291, 206.0
F = 5.8e9; LAM = 3e8 / F
HR = 6.0          # altura del CPE sobre el terreno de la casa (mastil sobre techo), m
IGN = 10.0        # no se cuenta copa a menos de 10 m del CPE (se elige la fachada/techo despejado)
D0 = 15.0         # inicio del trayecto desde la torre (base)
LAT0, LON0 = 15.889080840599476, -90.53176683391113
MLAT = 110600.0; MLON = 111320 * math.cos(math.radians(LAT0))
corn = [(15.890315778569091, -90.5349611723952, 215), (15.88965312986891, -90.52805576420171, 239),
        (15.887815774335364, -90.52824366646549, 247), (15.88813204164675, -90.53524302579086, 227)]
pts = [(0.0, 0.0, Z0)] + [((lo - LON0) * MLON, (la - LAT0) * MLAT, z) for la, lo, z in corn]
for p in json.load(open(os.path.join(ROOT, '04_propagacion_linkbudget', 'perfiles_google_earth.json'))):
    a = math.radians(p['azimut_torre_a_casa_deg'])
    for d, z in p['puntos_dist_desde_torre_m_elev_m']: pts.append((d * math.sin(a), d * math.cos(a), z))
P = np.array(pts); rbf = RBFInterpolator(P[:, :2], P[:, 2], kernel='thin_plate_spline', smoothing=2.0)
im = cv2.imread(os.path.join(ROOT, '14_fuentes', 'evidencias', 'casas_numeradas_109.png')); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
h, s, v = [hsv[..., i].astype(int) for i in range(3)]
can = ((h >= 55) & (h <= 115) & (s >= 45) & (v <= 112))
org = cv2.dilate(cv2.inRange(hsv, (8, 150, 150), (24, 255, 255)), np.ones((5, 5), np.uint8)) > 0
can &= ~org
can = cv2.morphologyEx(can.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)); can = cv2.morphologyEx(can, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
rows = list(csv.DictReader(open(os.path.join(ROOT, '01_comunidad_demanda', 'casas_109_coordenadas_aprox.csv'))))
SC = {'sin_copas': 0, 'copa15': 15, 'copa20': 20, 'copa25': 25}
out = []
for r in rows:
    x, y, D = float(r['x_m_este']), float(r['y_m_norte']), float(r['dist_torre_m']); zh = float(r['elev_interpolada_m']); zr = zh + HR
    d = np.arange(D0, D - 1.0, 1.0); fx, fy = x * d / D, y * d / D
    terr = rbf(np.column_stack([fx, fy]))
    pxs = np.clip(np.round(AX + fx / S).astype(int), 0, can.shape[1] - 1); pys = np.clip(np.round(AY - fy / S).astype(int), 0, can.shape[0] - 1)
    c = can[pys, pxs] > 0
    r1 = np.sqrt(LAM * d * (D - d) / D); f60 = 0.6 * r1
    rec = dict(casa=r['casa'], sector=r['sector'], dist_m=round(D, 1), elev_m=round(zh, 1), prof_copa_m=int(c.sum()), frac_copa=round(float(c.mean()), 2))
    for nm, hc in SC.items():
        hcs = np.where(c & (d < D - IGN), hc, 0.0)
        need = (terr + hcs + f60 - zr * d / D) / (1 - d / D) - Z0
        rec['H_min_' + nm] = round(float(max(need.max(), 0)), 1)
    hcs = np.where(c, 20.0, 0.0); need = (terr + hcs + f60 - zr * d / D) / (1 - d / D) - Z0
    rec['H_min_copa20_sin_ignorar_cerca'] = round(float(max(need.max(), 0)), 1)
    out.append(rec)
with open(os.path.join(HERE, 'los_altura_minima_por_casa.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('Porcentaje de casas con linea de vista (Fresnel 60 %) segun altura de torre H:')
print('H(m)  ' + '  '.join(f'{k:>10}' for k in list(SC) + ['c20_sin_ign']))
for H in (12, 18, 24, 30, 36, 42, 48):
    vals = [100 * np.mean([o['H_min_' + k] <= H for o in out]) for k in SC] + [100 * np.mean([o['H_min_copa20_sin_ignorar_cerca'] <= H for o in out])]
    print(f'{H:>4}  ' + '  '.join(f'{v:>9.0f}%' for v in vals))
for k in ('sin_copas', 'copa20'):
    a = np.array([o['H_min_' + k] for o in out]); print(k, 'H_min mediana', np.median(a), 'p90', np.percentile(a, 90), 'max', a.max())
bad = sorted(out, key=lambda o: -o['H_min_copa20'])[:12]
print('peores casas (H_min con copa 20):', [(o['casa'], o['H_min_copa20'], o['dist_m'], o['sector']) for o in bad])

# ---- Profundidad de follaje atravesada por el rayo y perdida (Weissberger, f en GHz, d en m)
def weissberger(dm, fg=5.8):
    if dm <= 0: return 0.0
    return 0.45 * fg ** 0.284 * dm if dm <= 14 else 1.33 * fg ** 0.284 * min(dm, 400) ** 0.588
HS = (12, 18, 24, 30, 36)
fol = {H: [] for H in HS}
for r in rows:
    x, y, D = float(r['x_m_este']), float(r['y_m_norte']), float(r['dist_torre_m']); zr = float(r['elev_interpolada_m']) + HR
    d = np.arange(D0, D - 1.0, 1.0); fx, fy = x * d / D, y * d / D
    terr = rbf(np.column_stack([fx, fy]))
    pxs = np.clip(np.round(AX + fx / S).astype(int), 0, can.shape[1] - 1); pys = np.clip(np.round(AY - fy / S).astype(int), 0, can.shape[0] - 1)
    c = (can[pys, pxs] > 0) & (d < D - IGN)
    for H in HS:
        zl = (Z0 + H) + (zr - (Z0 + H)) * d / D
        inside = c & (zl < terr + 20.0)        # el rayo esta dentro de la copa (20 m)
        dep = float(inside.sum())
        fol[H].append((r['casa'], dep, weissberger(dep)))
print('\nProfundidad de follaje (copa 20 m) y perdida Weissberger a 5.8 GHz segun altura de torre:')
for H in HS:
    dp = np.array([a[1] for a in fol[H]]); ls = np.array([a[2] for a in fol[H]])
    print(f'H={H:>2} m: profundidad mediana {np.median(dp):5.0f} m, p90 {np.percentile(dp,90):5.0f} m | perdida mediana {np.median(ls):4.1f} dB, p90 {np.percentile(ls,90):4.1f} dB, max {ls.max():4.1f} dB | casas con perdida > 30 dB: {int((ls>30).sum())}, > 25 dB: {int((ls>25).sum())}, sin follaje (< 1 dB): {int((ls<1).sum())}')
with open(os.path.join(HERE, 'follaje_por_casa_H30.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['casa', 'profundidad_follaje_m', 'perdida_weissberger_5p8GHz_dB'])
    for a in fol[30]: w.writerow([a[0], round(a[1]), round(a[2], 1)])
