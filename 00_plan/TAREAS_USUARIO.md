# TAREAS PARA TI (actualizado 26-oct-2026)

## Hechas
Aldea, 109 casas, elevaciones de esquinas, 6 perfiles de elevación, subida y latencia de Starlink, precios de accesorios, nombres del equipo.

## AHORA

### 1. Dar permiso a Claude para escribir en tu repo de GitHub (3 min)
El repo `Hykev/proyecto-antenas-gt` existe y mi sesión lo ve, pero **GitHub rechaza mis pushes** porque la app de Claude no está instalada en tu cuenta.
1. Entra a <https://github.com/apps/claude/installations/select_target>, elige tu cuenta (**Hykev**).
2. Elige *Only select repositories* → `proyecto-antenas-gt` → *Install*.
3. Si ya estaba instalada, reconecta GitHub en <https://claude.ai/customize/connectors?auth_start=github&auth_start_force=1> y vuelve a autorizar.
4. Avísame y subo todo.

**Mientras tanto (plan B, 2 min):** te mandé `proyecto-antenas-gt.bundle`, que contiene todo el historial. Desde tu computadora:
```
git clone proyecto-antenas-gt.bundle proyecto-antenas-gt
cd proyecto-antenas-gt
git remote set-url origin https://github.com/Hykev/proyecto-antenas-gt.git
git push -u origin main
```

### 2. Precio del kit Starlink y su consumo eléctrico
En la misma página de la tienda (<https://starlink.com/gt/public/shop?tag=PRD_TAG-V4>), **arriba de los accesorios**, deben aparecer los kits (Standard 4, Standard 4X, Mini, etc.). Mándame captura con su **precio** y, si la tienda tiene la ficha técnica, el **consumo en vatios**. No encontré "Alto Rendimiento": el catálogo lista "Performance (Gen 3)" solo como compatible de accesorios. El consumo lo necesito para dimensionar los paneles solares.

### 3. Corrige las posiciones en Google Earth solo si notas errores grandes
Abre `10_cartografia_kmz/babilonia_preliminar.kmz` (ya con la calibración nueva). Con los 6 vectores que mediste, las casas de control tienen error de 2–9 m; las demás deberían estar en ±10 m. Si ves alguna fuera de su casa por más de 20 m, avísame el número.

## DESPUÉS (no hagas nada todavía)
- Parámetros de CloudRF (cuando fije los equipos).
- 3–5 precios locales de equipos (E5).
- Si el profesor prefiere población ≈ 300: 3.2 hab/vivienda (`DECISIONES.md`, D03).

## Lo que ya no necesito
Perfiles de elevación, elevaciones de casas, altura de árboles (usé 20 m como supuesto declarado, con sensibilidad en E3).
