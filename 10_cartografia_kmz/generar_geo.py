"""Genera CSV, KMZ y figura de sectores de la aldea Babilonia.
Entradas: casas_pixeles_foto9.json  [[num, px, py], ...] (centros de marcadores de la foto 9)
Georreferenciacion: ajuste de similitud con 6 vectores torre-casa medidos en Google Earth
(casas 25, 93, 55, 5, 109, 31): escala 0.514 m/px, rotacion -0.07 deg (norte arriba), torre en pixel (829,291);
residuos 2-9 m en las casas de control.
Uso: python3 generar_geo.py
"""
import json, math, csv, zipfile, os
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S, AX, AY = 0.514, 829, 291
LAT0, LON0, Z0 = 15.889080840599476, -90.53176683391113, 206.0
MLAT = 110600.0; MLON = 111320 * math.cos(math.radians(LAT0))
CORN = {'Sup. izq.': (15.890315778569091, -90.5349611723952, 215), 'Sup. der.': (15.88965312986891, -90.52805576420171, 239),
        'Inf. der.': (15.887815774335364, -90.52824366646549, 247), 'Inf. izq.': (15.88813204164675, -90.53524302579086, 227)}
def loc(lat, lon): return ((lon - LON0) * MLON, (lat - LAT0) * MLAT)
cl = [(*loc(a, b), z) for a, b, z in CORN.values()]
from scipy.interpolate import RBFInterpolator
_pts = [(0.0, 0.0, Z0)] + [(x, y, z) for x, y, z in cl]
for p in json.load(open(os.path.join(ROOT, '04_propagacion_linkbudget', 'perfiles_google_earth.json'))):
    a = math.radians(p['azimut_torre_a_casa_deg'])
    for d, z in p['puntos_dist_desde_torre_m_elev_m']: _pts.append((d * math.sin(a), d * math.cos(a), z))
_P = np.array(_pts); _rbf = RBFInterpolator(_P[:, :2], _P[:, 2], kernel='thin_plate_spline', smoothing=2.0)
def zt(x, y): return float(_rbf(np.array([[x, y]]))[0])   # terreno interpolado desde perfiles + esquinas + centro
def ll(x, y): return (LAT0 + y / MLAT, LON0 + x / MLON)
rows = json.load(open(os.path.join(HERE, 'casas_pixeles_foto9.json')))
H = []
for n, px, py in rows:
    x, y = (px - AX) * S, -(py - AY) * S
    H.append(dict(id=int(n), px=px, py=py, x=x, y=y, d=math.hypot(x, y), az=math.degrees(math.atan2(x, y)) % 360, z=zt(x, y)))
H.sort(key=lambda h: h['id'])
_az = np.array([h['az'] for h in H])
PHI = min(range(0, 120, 5), key=lambda p: (max(((_az - (p + 120 * k)) % 360 < 120).sum() for k in range(3)), p))  # equilibra carga por sector
def sector(az): return int(((az - PHI) % 360) // 120)
with open(os.path.join(ROOT, '01_comunidad_demanda', 'casas_109_coordenadas_aprox.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['casa', 'x_m_este', 'y_m_norte', 'lat', 'lon', 'dist_torre_m', 'azimut_deg', 'sector', 'elev_interpolada_m'])
    for h in H:
        la, lo = ll(h['x'], h['y']); w.writerow([h['id'], round(h['x'], 1), round(h['y'], 1), f'{la:.6f}', f'{lo:.6f}', round(h['d'], 1), round(h['az'], 1), 'S%d' % (sector(h['az']) + 1), round(h['z'], 1)])
# ---- KMZ
COL = ['ff3c14dc', 'ff32cd32', 'ffe6a020']  # aabbggrr
def pm(name, lat, lon, desc, style): return f'<Placemark><name>{name}</name><description>{desc}</description><styleUrl>#{style}</styleUrl><Point><coordinates>{lon:.6f},{lat:.6f},0</coordinates></Point></Placemark>'
k = ['<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Babilonia - Proyecto antenas</name>']
for i, c in enumerate(COL): k.append(f'<Style id="s{i}"><IconStyle><color>{c}</color><scale>0.7</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle><LabelStyle><scale>0.6</scale></LabelStyle></Style>')
k.append('<Style id="torre"><IconStyle><scale>1.3</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/triangle.png</href></Icon></IconStyle></Style>')
k.append('<Style id="esq"><IconStyle><scale>0.9</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png</href></Icon></IconStyle></Style>')
k.append('<Style id="lin"><LineStyle><color>ff00ffff</color><width>2</width></LineStyle></Style>')
k.append('<Folder><name>Torre candidata y esquinas</name>')
k.append(pm('Torre central (candidata)', LAT0, LON0, 'Claro central, elev. 206 m (Google Earth). Starlink + 3 sectores 5 GHz.', 'torre'))
for nme, (a, b, z) in CORN.items(): k.append(pm(f'Esquina {nme} ({z} m)', a, b, f'Elevacion Google Earth: {z} m', 'esq'))
k.append('</Folder><Folder><name>Sectores (azimut)</name>')
for i in range(3):
    for a0 in (PHI + 120 * i,):
        for az in (a0,):
            x, y = 400 * math.sin(math.radians(az)), 400 * math.cos(math.radians(az)); la, lo = ll(x, y)
            k.append(f'<Placemark><name>Limite sector S{i+1} az {az % 360} deg</name><styleUrl>#lin</styleUrl><LineString><tessellate>1</tessellate><coordinates>{LON0:.6f},{LAT0:.6f},0 {lo:.6f},{la:.6f},0</coordinates></LineString></Placemark>')
k.append('</Folder><Folder><name>Casas (109, posicion calibrada +-10 m en casas de control; arrastrar para corregir)</name>')
for h in H:
    la, lo = ll(h['x'], h['y']); s = sector(h['az'])
    k.append(pm(f"Casa {h['id']}", la, lo, f"Sector S{s+1}; dist. a torre {h['d']:.0f} m; azimut {h['az']:.0f} deg; elev. interpolada (+-3 m salvo extremos) {h['z']:.0f} m", f's{s}'))
k.append('</Folder></Document></kml>')
with zipfile.ZipFile(os.path.join(HERE, 'babilonia_preliminar.kmz'), 'w', zipfile.ZIP_DEFLATED) as z: z.writestr('doc.kml', ''.join(k))
# ---- Figura
im = cv2.imread(os.path.join(ROOT, '14_fuentes', 'evidencias', 'casas_numeradas_109.png'))
ov = im.copy(); R = lambda d: int(d / S)
cols = [(60, 60, 255), (60, 220, 60), (255, 170, 60)]
for i in range(3):
    a0 = PHI + 120 * i
    pts = [(AX, AY)] + [(int(AX + R(420) * math.sin(math.radians(a0 + t))), int(AY - R(420) * math.cos(math.radians(a0 + t)))) for t in range(0, 121, 4)]
    cv2.fillPoly(ov, [np.array(pts)], cols[i])
im = cv2.addWeighted(ov, 0.22, im, 0.78, 0)
for d in (100, 200, 300, 400): cv2.circle(im, (AX, AY), R(d), (255, 255, 255), 1, cv2.LINE_AA); cv2.putText(im, f'{d} m', (AX + 4, AY - R(d) - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
for i in range(3):
    a = math.radians(PHI + 120 * i); cv2.line(im, (AX, AY), (int(AX + R(420) * math.sin(a)), int(AY - R(420) * math.cos(a))), cols[i], 2, cv2.LINE_AA)
    am = math.radians(PHI + 120 * i + 60); cv2.putText(im, f'S{i+1}', (int(AX + R(120) * math.sin(am)) - 12, int(AY - R(120) * math.cos(am)) + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 4, cv2.LINE_AA); cv2.putText(im, f'S{i+1}', (int(AX + R(120) * math.sin(am)) - 12, int(AY - R(120) * math.cos(am)) + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cols[i], 2, cv2.LINE_AA)
cv2.drawMarker(im, (AX, AY), (0, 255, 255), cv2.MARKER_TRIANGLE_UP, 26, 3)
os.makedirs(os.path.join(ROOT, '11_informe_latex', 'figuras'), exist_ok=True)
cv2.imwrite(os.path.join(ROOT, '11_informe_latex', 'figuras', 'fig_aldea_sectores_prelim.png'), im)
n = [sum(1 for h in H if sector(h['az']) == i) for i in range(3)]
print('PHI',PHI,'| casas por sector', n, '| max dist por sector', [round(max(h['d'] for h in H if sector(h['az']) == i)) for i in range(3)])
