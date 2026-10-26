"""Presupuesto de enlace torre -> 109 casas (bajada y subida), 5.8 GHz, comparacion de dos antenas sectoriales.
Todo parametro con fuente en 03_antenas_patrones/FICHAS_EQUIPOS.md. Supuestos marcados con [S].
Uso: python3 -I linkbudget.py  -> imprime resumen y escribe linkbudget_por_casa.csv
"""
import math, csv, os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rfmodel as R
F_GHZ = 5.8; LAM = R.C0 / (F_GHZ * 1e9)
# ---- Radio (Rocket Prism 5AC Gen2, ficha F24): (modulacion, bits/simbolo, codificacion, sens_dBm, Tx_dBm)
MCS = [('BPSK 1/2', 1, .5, -96, 28), ('QPSK 1/2', 2, .5, -95, 28), ('QPSK 3/4', 2, .75, -92, 28), ('16QAM 1/2', 4, .5, -90, 28), ('16QAM 3/4', 4, .75, -86, 28),
       ('64QAM 2/3', 6, 2 / 3, -83, 28), ('64QAM 3/4', 6, .75, -77, 27), ('64QAM 5/6', 6, 5 / 6, -74, 26), ('256QAM 3/4', 8, .75, -69, 24), ('256QAM 5/6', 8, 5 / 6, -65, 22)]
SC20, TSYM = 52, 3.6e-6                         # subportadoras de datos en 20 MHz y simbolo con GI corto (OFDM tipo 802.11ac) [S: formula de tasa PHY]
def phy(m): return 2 * SC20 * m[1] * m[2] / TSYM / 1e6   # Mbps, 2x2 MIMO, canal 20 MHz
BW_PEN = 3.0     # [S] penalizacion de sensibilidad por canal de 20 MHz (la ficha no indica ancho de canal)
CPE_TX_OFF = 3.0 # [S] CPE: 25 dBm max frente a 28 dBm del AP => -3 dB en todos los MCS
M_REQ = 10.0     # dB de margen de diseno exigido sobre la sensibilidad del MCS usable
L_FEED, L_MIS, L_RAIN = 0.5, 1.0, 0.3   # [S] jumpers AP; desalineacion CPE; lluvia 5.8 GHz sobre <=0.42 km (UIT-R P.838-3, ver informe)
ETA_MAC, DL_SHARE = 0.65, 0.75           # [S] eficiencia MAC TDD y fraccion de trama para bajada
G_CPE = 23.0     # LiteBeam 5AC Gen2 (ficha F25)
ANT = {   # ficha UI store (AM-5G16-120) y proveedores (AM-5G19-120); largo fisico de la antena para el modelo de apertura
    'AM-5G16-120': dict(g=15.5, az6=137.0, el_bw=8.0, tilt_el=4.0, L=0.367, price_usd=79.0),
    'AM-5G19-120': dict(g=18.85, az6=123.0, el_bw=4.0, tilt_el=2.0, L=0.700, price_usd=None)}
def az_loss(da, a):   # modelo gaussiano calibrado con el ancho de haz a 6 dB de la ficha; tope [S] 25 dB (F/B no figura en la ficha)
    da = (da + 180) % 360 - 180; return min(6.0 * (2 * da / a['az6']) ** 2, 25.0)
def el_loss(de, a):   # apertura lineal uniforme de longitud L (principio fisico: HPBW ~ 0.886 lambda/L); piso [S] 25 dB
    u = math.pi * a['L'] / LAM * math.sin(math.radians(de))
    v = 1.0 if abs(u) < 1e-9 else abs(math.sin(u) / u)
    return min(-20 * math.log10(max(v, 1e-6)), 25.0)
def fspl(d_m): return 32.44 + 20 * math.log10(d_m / 1000.0) + 20 * math.log10(F_GHZ * 1000.0)
SECT = {'S1': 150.0, 'S2': 270.0, 'S3': 30.0}   # azimut de boresight (centro de 90-210, 210-330, 330-90)
def sector_of(az):
    return 'S1' if 90 <= az < 210 else ('S2' if 210 <= az < 330 else 'S3')
def run(model='AM-5G16-120', Htow=30.0, mech_tilt=3.0, hc=20.0, foliage_cache={}, verbose=False, extra_loss=0.0):
    a = ANT[model]; fol = foliage_cache.setdefault('F', R.Foliage()); houses = R.load_houses(); out = []
    for h in houses:
        key = (h['id'], Htow, hc)
        if key not in foliage_cache: foliage_cache[key] = fol.depth(h, Htow, hc=hc)
        dep = foliage_cache[key]; Lf = R.weissberger(dep, F_GHZ)
        s = sector_of(h['az']); da = h['az'] - SECT[s]
        drop = Htow - (h['z'] - R.Z0) - 6.0                       # desnivel antena - CPE (m)
        dist3d = math.hypot(h['d'], drop); el = math.degrees(math.atan2(drop, h['d']))
        de = el - (a['tilt_el'] + mech_tilt)
        gap = a['g'] - az_loss(da, a) - el_loss(de, a)           # ganancia efectiva del AP hacia la casa
        fs = fspl(dist3d)
        other = Lf + L_MIS + L_RAIN + extra_loss
        pr_dl = {m[0]: m[4] + gap - L_FEED + G_CPE - fs - other for m in MCS}
        pr_dl0 = MCS[0][4] + gap - L_FEED + G_CPE - fs - other    # a Tx de 28 dBm
        pr_ul0 = (MCS[0][4] - CPE_TX_OFF) + G_CPE + gap - L_FEED - fs - other
        # MCS usable: el mayor con margen >= M_REQ (cada MCS con su propia Tx y sensibilidad)
        best_dl = None; best_ul = None
        for m in MCS:
            pdl = (m[4]) + gap - L_FEED + G_CPE - fs - other; pul = (m[4] - CPE_TX_OFF) + G_CPE + gap - L_FEED - fs - other
            if pdl - (m[3] + BW_PEN) >= M_REQ: best_dl = m
            if pul - (m[3] + BW_PEN) >= M_REQ: best_ul = m
        out.append(dict(casa=h['id'], sector=s, dist_m=round(h['d'], 1), dist3d_m=round(dist3d, 1), el_deg=round(el, 2), dAz_deg=round(da, 1), dEl_deg=round(de, 2),
                        G_ap_ef_dBi=round(gap, 1), FSPL_dB=round(fs, 1), follaje_m=int(dep), L_follaje_dB=round(Lf, 1), Pr_dl_BPSK_dBm=round(pr_dl0, 1), Pr_ul_BPSK_dBm=round(pr_ul0, 1),
                        margen_dl_BPSK_dB=round(pr_dl0 - (MCS[0][3] + BW_PEN), 1), margen_ul_BPSK_dB=round(pr_ul0 - (MCS[0][3] + BW_PEN), 1),
                        MCS_dl=best_dl[0] if best_dl else 'ninguno', MCS_ul=best_ul[0] if best_ul else 'ninguno',
                        R_dl_Mbps=round(phy(best_dl), 1) if best_dl else 0.0, R_ul_Mbps=round(phy(best_ul), 1) if best_ul else 0.0))
    return out
def summarize(out, name=''):
    n = len(out); md = np.array([o['margen_dl_BPSK_dB'] for o in out]); mu = np.array([o['margen_ul_BPSK_dB'] for o in out])
    dl_ok = sum(o['R_dl_Mbps'] > 0 for o in out); ul_ok = sum(o['R_ul_Mbps'] > 0 for o in out)
    print(f'[{name}] casas con MCS bajada usable (margen>=10 dB): {dl_ok}/{n} | subida: {ul_ok}/{n} | margen BPSK bajada min {md.min():.1f} med {np.median(md):.1f} dB | subida min {mu.min():.1f} med {np.median(mu):.1f} dB')
    return dl_ok, ul_ok
if __name__ == '__main__':
    cache = {}
    print('=== Comparacion de antenas y tilt mecanico (torre 30 m, copa 20 m) ===')
    for model in ANT:
        for tilt in (0, 1, 2, 3, 4, 6, 8):
            summarize(run(model, 30, tilt, 20, cache), f'{model} tilt mec {tilt}')

# ---------------- Capacidad por sector (aire compartido, equidad de tiempo de aire) ----------------
ADOPT = 0.90; DEM_DL, DEM_UL = 1.0, 0.125     # Mbps medios por suscriptor en hora pico (4 Mbps x 25 % ; 0.5 Mbps x 25 %)
def capacity(out, adopt=ADOPT, dem_dl=DEM_DL, dem_ul=DEM_UL):
    res = {}
    for s in ('S1', 'S2', 'S3'):
        hs = [o for o in out if o['sector'] == s]; n = len(hs)
        udl = sum(adopt * dem_dl / (ETA_MAC * o['R_dl_Mbps']) for o in hs if o['R_dl_Mbps'] > 0) / DL_SHARE
        uul = sum(adopt * dem_ul / (ETA_MAC * o['R_ul_Mbps']) for o in hs if o['R_ul_Mbps'] > 0) / (1 - DL_SHARE)
        rates = [o['R_dl_Mbps'] for o in hs if o['R_dl_Mbps'] > 0]
        harm = len(rates) / sum(1 / r for r in rates)
        cap_net = ETA_MAC * DL_SHARE * harm            # Mbps netos de bajada si todos tuvieran igual demanda (media armonica)
        res[s] = dict(n=n, subs=round(adopt * n, 1), demanda_dl=round(adopt * n * dem_dl, 1), cap_dl_neta=round(cap_net, 1), util_dl=round(udl, 2), util_ul=round(uul, 2))
    return res
def mcs_hist(out):
    from collections import Counter; c = Counter(o['MCS_dl'] for o in out); return {m[0]: c.get(m[0], 0) for m in MCS} | {'ninguno': c.get('ninguno', 0)}
def meets25(out): return sum(1 for o in out if ETA_MAC * DL_SHARE * 0 + ETA_MAC * o['R_dl_Mbps'] >= 25.0)
if __name__ == '__main__':
    print('\n=== Detalle de configuraciones candidatas ===')
    for model, tilt in (('AM-5G16-120', 0), ('AM-5G16-120', 1), ('AM-5G16-120', 2), ('AM-5G19-120', 2), ('AM-5G19-120', 1)):
        out = run(model, 30, tilt, 20, cache); print(f'\n--- {model}, tilt mecanico {tilt} (total {ANT[model]["tilt_el"] + tilt:.0f} deg) ---')
        print('MCS bajada:', {k: v for k, v in mcs_hist(out).items() if v}); print('casas con >=25 Mbps netos (un solo usuario activo):', meets25(out), '/109')
        for s, r in capacity(out).items(): print(' ', s, r)
        w = sorted(out, key=lambda o: o['margen_ul_BPSK_dB'])[:4]; print('  peores (subida):', [(o['casa'], o['sector'], o['dist_m'], o['L_follaje_dB'], o['dEl_deg'], o['margen_ul_BPSK_dB']) for o in w])
