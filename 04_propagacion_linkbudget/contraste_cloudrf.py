"""Contraste con CloudRF (4 enlaces, sin y con vegetacion). Define Pr 'a la CloudRF':
Ptx(28 dBm) + G_ap_efectiva - FSPL(3D) - L_follaje, SIN ganancia del CPE y SIN las perdidas extra propias (feeder 0.5, desalin. 1.0, lluvia 0.3)."""
import csv, os
from rfmodel import Foliage, load_houses, weissberger
HERE = os.path.dirname(os.path.abspath(__file__))
lb = {int(r['casa']): r for r in csv.DictReader(open(os.path.join(HERE, 'linkbudget_por_casa.csv')))}
H = {h['id']: h for h in load_houses()}
# lecturas de las capturas de CloudRF (Pr sin y con vegetacion, path-loss, distancia, downtilt, EIRP)
CR = {26: dict(d=0.398, dt=2.77, eirp=43.1, pl=61.6, sin=-56.7, con=-56.7),
      43: dict(d=0.05, dt=23.72, eirp=25.2, pl=61.5, sin=-58.5, con=-64.3),
      55: dict(d=0.165, dt=4.0, eirp=42.1, pl=55.0, sin=-50.2, con=-56.1),
      93: dict(d=0.402, dt=0.2, eirp=33.0, pl=71.8, sin=-66.8, con=-66.8)}
F = Foliage(); rows = []
for c, v in CR.items():
    r = lb[c]; g = float(r['G_ap_ef_dBi']); fspl = float(r['FSPL_dB'])
    sin_p = 28 + g - fspl
    out = dict(casa=c, dist_m=float(r['dist_m']), G_ef=g, FSPL=fspl, pr_propia_sinveg=round(sin_p, 1), pr_cr_sinveg=v['sin'], dif_sinveg=round(v['sin'] - sin_p, 1),
               perd_veg_cr=round(v['sin'] - v['con'], 1), pr_cr_conveg=v['con'])
    for hc in (20, 10):
        m = F.depth(H[c], 30.0, hc=hc); L = weissberger(m)
        out[f'foll_m_hc{hc}'] = round(m); out[f'L_foll_hc{hc}'] = round(L, 1); out[f'pr_propia_conveg_hc{hc}'] = round(sin_p - L, 1)
    rows.append(out)
keys = list(rows[0]); w = csv.DictWriter(open(os.path.join(HERE, 'contraste_cloudrf.csv'), 'w', newline=''), keys); w.writeheader(); w.writerows(rows)
for o in rows: print(o)
