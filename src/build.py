#!/usr/bin/env python3
"""Genera site/ HTML estático del directorio de cargadores eléctricos."""
import json, os, re, html, sys
D=os.path.dirname(os.path.abspath(__file__)); S=f"{D}/site"; os.makedirs(S,exist_ok=True)
E=html.escape
DATA=json.load(open(f"{D}/data/cargadores.json"))
FECHA=DATA["fecha"]
C=DATA["conteos"]
CSS=("body{font-family:system-ui,sans-serif;max-width:960px;margin:auto;padding:1rem;line-height:1.5;color:#222}"
     "table{border-collapse:collapse;width:100%;font-size:.88em}td,th{border:1px solid #ccc;padding:.35rem;text-align:left;vertical-align:top}"
     ".aviso{background:#fff4d6;padding:.6rem;border-radius:6px}footer{margin-top:2rem;font-size:.85rem;color:#555}"
     "nav a{margin-right:.8rem}code{background:#f4f4f4;padding:0 .2em}")
NAV=('<nav><a href="index.html">Inicio</a>'
     '<a href="valencia.html">Valencia</a>'
     '<a href="las-palmas.html">Las Palmas</a>'
     '<a href="santa-cruz-de-tenerife.html">Santa Cruz de Tenerife</a>'
     '<a href="como-cargar.html">Cómo cargar</a></nav>')

def page(fn,title,body):
    h=f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Cargadores eléctricos España</title>
<meta name="description" content="{E(title)}. Directorio con fuentes públicas citadas.">
<style>{CSS}</style></head><body>
{NAV}
<h1>{E(title)}</h1>{body}
<footer><p><strong>Aviso:</strong> esta web no es oficial ni gestiona recargas. Los datos salen de fuentes públicas enlazadas; compruébalos siempre en la fuente (disponibilidad y precio pueden cambiar). Revisado el {FECHA}. Ingresos del proyecto: 0&nbsp;€.</p></footer></body></html>"""
    open(f"{S}/{fn}","w",encoding="utf-8").write(h)

def maps_link(lat,lon,label="mapa"):
    try:
        if lat in (None,"","sin datos") or lon in (None,"","sin datos"):
            return "—"
        la=float(str(lat).replace(",",".")); lo=float(str(lon).replace(",","."))
        return f'<a href="https://www.openstreetmap.org/?mlat={la}&amp;mlon={lo}#map=17/{la}/{lo}" rel="noopener noreferrer">{E(label)}</a>'
    except Exception:
        return "—"

# Index
page("index.html","Cargadores eléctricos en España",f"""
<p>Directorio de puntos de recarga de acceso público, empezando por <strong>Valencia</strong> y <strong>Canarias</strong> (Las Palmas y Santa Cruz de Tenerife). Solo datos reales con fuente citada.</p>
<p class="aviso">La exportación CSV nacional de RIPREE (MITECO) devolvió una página HTML de la sede en dos intentos; para Canarias usamos el mirror oficial del Gobierno de Canarias. Para Valencia provincia usamos Open Charge Map (export público) y, en la ciudad, el Geoportal del Ayuntamiento.</p>
<h2>Provincias publicadas</h2>
<ul>
<li><a href="valencia.html">Valencia</a> — {C['valencia_ocm_pois']} ubicaciones (Open Charge Map, CP 46) · {C['valencia_ayto_estaciones']} cargadores municipales del Ayuntamiento de València ({C['valencia_ayto_tomas']} tomas)</li>
<li><a href="las-palmas.html">Las Palmas</a> — {C['las_palmas_instalaciones']} instalaciones · {C['las_palmas_conectores']} conectores (RIPREE / MITECO vía datos.canarias.es)</li>
<li><a href="santa-cruz-de-tenerife.html">Santa Cruz de Tenerife</a> — {C['tenerife_instalaciones']} instalaciones · {C['tenerife_conectores']} conectores (RIPREE / MITECO vía datos.canarias.es)</li>
</ul>
<p>Guía: <a href="como-cargar.html">cómo cargar y tipos de conector</a>.</p>
<p>Fuentes base: <a href="{DATA['fuentes']['datos_gob']}">catálogo datos.gob.es (RIPREE)</a>, <a href="{DATA['fuentes']['canarias_ripree']}">datos abiertos Canarias</a>, <a href="{DATA['fuentes']['valencia_ayto']}">Geoportal València</a>, <a href="{DATA['fuentes']['ocm_web']}">Open Charge Map</a>.</p>
""")

# Cómo cargar
page("como-cargar.html","Cómo cargar un coche eléctrico y tipos de conector",f"""
<p>Resumen verificable para quien empieza. No sustituye el manual de tu coche ni las condiciones del operador del punto.</p>
<h2>AC frente a DC</h2>
<ul>
<li><strong>AC (corriente alterna)</strong>: carga «lenta» o «semirrápida» en destino (casa, calle, parking). El cargador de a bordo del coche convierte a DC. Potencias típicas en vía pública: 3,7–22&nbsp;kW.</li>
<li><strong>DC (corriente continua)</strong>: carga rápida en electrolineras; el punto entrega DC al pack. Potencias habituales desde ~50&nbsp;kW hasta 150–350&nbsp;kW según instalación.</li>
</ul>
<h2>Conectores frecuentes en España</h2>
<table><tr><th>Conector</th><th>Uso habitual</th></tr>
<tr><td>Tipo 2 (Mennekes / IEC 62196-2)</td><td>AC en Europa; el más habitual en vía pública y destinos</td></tr>
<tr><td>CCS Combo 2 (IEC 62196-3 / IEC_62196_T2_COMBO)</td><td>DC rápida en coches europeos recientes</td></tr>
<tr><td>CHAdeMO</td><td>DC rápida (más frecuente en modelos japoneses antiguos)</td></tr>
<tr><td>Schuko / doméstico</td><td>Emergencia o carga muy lenta; no es el estándar de vía pública</td></tr>
</table>
<p>Los nombres de conector en Canarias (p. ej. <code>IEC_62196_T2_COMBO</code>) salen del registro RIPREE. Fuente del registro: <a href="{DATA['fuentes']['datos_gob']}">Puntos de recarga — datos.gob.es / MITECO</a>.</p>
<h2>Antes de enchufar</h2>
<ol>
<li>Comprueba en la app del operador o en el punto si está libre y el precio (€/kWh o sesión).</li>
<li>Mira que el conector y la potencia sean compatibles con tu coche.</li>
<li>La disponibilidad en tiempo real <strong>no</strong> está en esta web (sin datos aquí).</li>
</ol>
<p class="aviso">Precios y horarios: cuando el dataset los trae, los mostramos; si no, «sin datos». Verifica siempre en el operador.</p>
""")

def table_canarias(prov):
    items=[x for x in DATA['canarias'] if x['provincia']==prov]
    items=sorted(items, key=lambda x:(x.get('municipio') or '', x.get('nombre') or ''))
    tr=[]
    for it in items:
        tr.append(
            "<tr>"
            f"<td>{E(it['nombre'])}</td>"
            f"<td>{E(it['direccion'])}<br><small>{E(it['municipio'])} · CP {E(str(it['cp']))}</small></td>"
            f"<td>{E(it['operador'])}</td>"
            f"<td>{it['n_conectores']}: {E(it.get('conectores_resumen') or 'sin datos')}</td>"
            f"<td>{maps_link(it.get('lat'), it.get('lon'))}</td>"
            f"<td><a href=\"{E(it['fuente'])}\">fuente</a></td>"
            "</tr>"
        )
    n_inst=len(items); n_conn=sum(x['n_conectores'] for x in items)
    body=f"""<p>{n_inst} instalaciones con {n_conn} conectores registrados en la provincia de {E(prov)}.</p>
<p>Fuente: <a href="{DATA['fuentes']['canarias_ripree']}">Instalaciones de puntos de recarga — datos abiertos Gobierno de Canarias</a> (RIPREE / MITECO). Fecha de revisión de esta web: {FECHA}.</p>
<p class="aviso">Cada fila es una <em>instalación</em> (puede tener varios conectores). Disponibilidad en tiempo real: sin datos aquí.</p>
<table><tr><th>Instalación</th><th>Dirección</th><th>Operador</th><th>Conectores</th><th>Mapa</th><th>Fuente</th></tr>
{''.join(tr)}</table>"""
    return body, n_inst, n_conn

body, n_i, n_c = table_canarias("Las Palmas")
page("las-palmas.html", f"Cargadores eléctricos en Las Palmas ({n_i} instalaciones)", body)

body, n_i, n_c = table_canarias("Santa Cruz de Tenerife")
page("santa-cruz-de-tenerife.html", f"Cargadores eléctricos en Santa Cruz de Tenerife ({n_i} instalaciones)", body)

# Valencia
ay=sorted(DATA['valencia_ayto'], key=lambda x: x.get('direccion') or '')
tr_ay=[]
for it in ay:
    precio=it.get('precio') or 'sin datos'
    obs=it.get('observacion') or 'sin datos'
    tr_ay.append(
        "<tr>"
        f"<td>{E(it['nombre'])}</td>"
        f"<td>{E(it['direccion'])}</td>"
        f"<td>{E(str(it.get('conectores_resumen') or 'sin datos'))}</td>"
        f"<td>{E(str(precio))}</td>"
        f"<td>{E(str(obs))}</td>"
        f"<td>{maps_link(it.get('lat'), it.get('lon'))}</td>"
        f"<td><a href=\"{E(it['fuente'])}\">fuente</a></td>"
        "</tr>"
    )

ocm=sorted(DATA['valencia_ocm'], key=lambda x:(x.get('municipio') or '', x.get('nombre') or ''))
tr_ocm=[]
for it in ocm:
    src=it.get('fuente') or DATA['fuentes']['ocm_web']
    tr_ocm.append(
        "<tr>"
        f"<td>{E(it.get('nombre') or 'sin datos')}</td>"
        f"<td>{E(it.get('direccion') or 'sin datos')}<br><small>{E(it.get('municipio') or '')} · CP {E(str(it.get('cp') or 'sin datos'))}</small></td>"
        f"<td>{E(it.get('operador') or 'sin datos')}</td>"
        f"<td>{E(it.get('conectores') or 'sin datos')}</td>"
        f"<td>{E(str(it.get('puntos') or 'sin datos'))}</td>"
        f"<td>{E(it.get('estado') or 'sin datos')}</td>"
        f"<td>{maps_link(it.get('lat'), it.get('lon'))}</td>"
        f"<td><a href=\"{E(src)}\">OCM</a></td>"
        "</tr>"
    )

page("valencia.html", f"Cargadores eléctricos en Valencia ({C['valencia_ocm_pois']} ubicaciones OCM)", f"""
<p>Dos capas de datos, ambas citadas:</p>
<ol>
<li><strong>Cargadores municipales del Ayuntamiento de València</strong> ({C['valencia_ayto_estaciones']} estaciones / {C['valencia_ayto_tomas']} tomas): Geoportal municipal.</li>
<li><strong>Ubicaciones en la provincia</strong> (código postal 46xxx): {C['valencia_ocm_pois']} puntos de Open Charge Map (export público GitHub <a href="{DATA['fuentes']['ocm_export']}">ocm-export</a>).</li>
</ol>
<p class="aviso">RIPREE nacional (CSV MITECO): {E(DATA['fuentes']['ripree_nacional_estado'])}. Por eso en Valencia provincia no hay aún el listado RIPREE; usamos OCM + datos municipales.</p>

<h2>1. Ayuntamiento de València (vía pública)</h2>
<p>Fuente: <a href="{DATA['fuentes']['valencia_ayto']}">Geoportal València — capa cargadores</a>.</p>
<table><tr><th>Punto</th><th>Emplazamiento</th><th>Conector / potencia</th><th>Precio</th><th>Observación</th><th>Mapa</th><th>Fuente</th></tr>
{''.join(tr_ay)}</table>

<h2>2. Provincia de Valencia (Open Charge Map, CP 46)</h2>
<p>Fuente: <a href="{DATA['fuentes']['ocm_web']}">Open Charge Map</a> · export <a href="{DATA['fuentes']['ocm_export']}">ocm-export/data/ES</a>. Filtrado por código postal que empieza por 46. Licencias mixtas según proveedor en cada POI.</p>
<table><tr><th>Nombre</th><th>Dirección</th><th>Operador</th><th>Conectores</th><th>Puntos</th><th>Estado OCM</th><th>Mapa</th><th>Fuente</th></tr>
{''.join(tr_ocm)}</table>
""")

# verify internal links
bad=[]
for f in os.listdir(S):
    if not f.endswith('.html'): continue
    for h in re.findall(r'href="([^"#:]+\.html)"', open(f"{S}/{f}",encoding='utf-8').read()):
        if not os.path.exists(f"{S}/{h}"): bad.append((f,h))
print("paginas", sorted(os.listdir(S)))
print("Enlaces internos:", "PASA" if not bad else f"FALLA {bad}")
print("conteos", C)
sys.exit(1 if bad else 0)
