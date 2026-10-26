"""Modelo comun: terreno interpolado, mascara de copas, follaje (Weissberger) y datos de casas.
Parametros iguales a analisis_los.py (misma calibracion y mismos supuestos)."""
import json, math, csv, os
import numpy as np, cv2
from scipy.interpolate import RBFInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
S, AX, AY, Z0 = 0.514, 829, 291, 206.0
LAT0, LON0 = 15.889080840599476, -90.53176683391113
MLAT = 110600.0; MLON = 111320 * math.cos(math.radians(LAT0))
C0 = 3e8
CORN = [(15.890315778569091, -90.5349611723952, 215), (15.88965312986891, -90.52805576420171, 239),
        (15.887815774335364, -90.52824366646549, 247), (15.88813204164675, -90.53524302579086, 227)]
def build_terrain():
    pts = [(0.0, 0.0, Z0)] + [((lo - LON0) * MLON, (la - LAT0) * MLAT, z) for la, lo, z in CORN]
    for p in json.load(open(os.path.join(ROOT, '04_propagacion_linkbudget', 'perfiles_google_earth.json'))):
        a = math.radians(p['azimut_torre_a_casa_deg'])
        for d, z in p['puntos_dist_desde_torre_m_elev_m']: pts.append((d * math.sin(a), d * math.cos(a), z))
    P = np.array(pts); return RBFInterpolator(P[:, :2], P[:, 2], kernel='thin_plate_spline', smoothing=2.0)
def build_canopy():
    im = cv2.imread(os.path.join(ROOT, '14_fuentes', 'evidencias', 'casas_numeradas_109.png')); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    h, s, v = [hsv[..., i].astype(int) for i in range(3)]
    can = ((h >= 55) & (h <= 115) & (s >= 45) & (v <= 112))
    org = cv2.dilate(cv2.inRange(hsv, (8, 150, 150), (24, 255, 255)), np.ones((5, 5), np.uint8)) > 0
    can &= ~org
    can = cv2.morphologyEx(can.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)); return cv2.morphologyEx(can, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
def load_houses():
    rows = list(csv.DictReader(open(os.path.join(ROOT, '01_comunidad_demanda', 'casas_109_coordenadas_aprox.csv'))))
    return [dict(id=int(r['casa']), x=float(r['x_m_este']), y=float(r['y_m_norte']), d=float(r['dist_torre_m']), az=float(r['azimut_deg']), z=float(r['elev_interpolada_m'])) for r in rows]
def weissberger(dm, fg=5.8):
    if dm <= 0: return 0.0
    return 0.45 * fg ** 0.284 * dm if dm <= 14 else 1.33 * fg ** 0.284 * min(dm, 400) ** 0.588
class Foliage:
    def __init__(self): self.rbf = build_terrain(); self.can = build_canopy()
    def depth(self, h, H, hc=20.0, hr=6.0, ign=10.0, d0=15.0):
        """profundidad de follaje (m) atravesada por el rayo torre(H)->CPE de la casa h"""
        x, y, D = h['x'], h['y'], h['d']; zr = h['z'] + hr
        d = np.arange(d0, D - 1.0, 1.0); fx, fy = x * d / D, y * d / D
        terr = self.rbf(np.column_stack([fx, fy]))
        px = np.clip(np.round(AX + fx / S).astype(int), 0, self.can.shape[1] - 1); py = np.clip(np.round(AY - fy / S).astype(int), 0, self.can.shape[0] - 1)
        c = (self.can[py, px] > 0) & (d < D - ign)
        zl = (Z0 + H) + (zr - (Z0 + H)) * d / D
        return float((c & (zl < terr + hc)).sum())
