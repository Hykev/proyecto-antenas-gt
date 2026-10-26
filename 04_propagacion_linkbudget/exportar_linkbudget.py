import csv, importlib.util, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linkbudget as lb
out = lb.run("AM-5G16-120", 30, 0, 20, {})
keys = list(out[0].keys())
with open('linkbudget_por_casa.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(out)
print(len(out), 'filas;', keys)
cap = lb.capacity(out); print(cap); print(lb.mcs_hist(out))
dl = sorted(o['margen_dl_BPSK_dB'] for o in out); ul = sorted(o['margen_ul_BPSK_dB'] for o in out)
print('min/mediana margen DL', dl[0], dl[len(dl)//2], 'UL', ul[0], ul[len(ul)//2])
print('casas <=100 m:', [(o['casa'], o['dist_m'], o['dEl_deg'], o['MCS_dl']) for o in out if o['dist_m'] <= 100])
