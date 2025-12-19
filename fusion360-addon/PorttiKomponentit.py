import adsk.core, adsk.fusion, traceback
import json, os

handlers = []

# -------------------------------
# APU: parametrien luonti/haku
# -------------------------------

def get_or_create_param(design, name, expression, unit='mm'):
    user_params = design.userParameters
    existing = user_params.itemByName(name)
    if existing:
        return existing
    val_input = adsk.core.ValueInput.createByString(f'{expression} {unit}')
    return user_params.add(name, val_input, unit, '')

# -------------------------------
# APU: JSON-luku
# -------------------------------

def load_config():
    this_dir = os.path.dirname(__file__)
    cfg_path = os.path.join(this_dir, 'layout_config.json')
    with open(cfg_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# -------------------------------
# APU: luo johto 3D-bodyjna
# -------------------------------

def create_wire_body(root, plane, x1, y1, x2, y2, z_height, radius, color, name):
    """Luo pyöreä johto kahden pisteen välille"""
    try:
        sketches = root.sketches
        extrudes = root.features.extrudeFeatures
        
        # Luo ympyrä johdon alkupisteeseen
        wire_sk = sketches.add(plane)
        wire_sk.name = f'Wire_{name}'
        circles = wire_sk.sketchCurves.sketchCircles
        center = adsk.core.Point3D.create(x1, y1, 0)
        circles.addByCenterRadius(center, radius)
        
        if wire_sk.profiles.count == 0:
            return None
            
        prof = wire_sk.profiles.item(0)
        
        # Laske johdon pituus ja suunta
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        
        # Extrude johdon suuntaan
        wire_ext_in = extrudes.createInput(
            prof,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        wire_dist = adsk.core.ValueInput.createByReal(length)
        wire_ext_in.setDistanceExtent(False, wire_dist)
        wire_ext = extrudes.add(wire_ext_in)
        wire_body = wire_ext.bodies.item(0)
        wire_body.name = name
        
        # Siirrä ja kierrä johto oikeaan paikkaan
        move_feats = root.features.moveFeatures
        bodies_col = adsk.core.ObjectCollection.create()
        bodies_col.add(wire_body)
        
        # Laske rotaatio
        import math
        angle = math.atan2(dy, dx)
        
        transform = adsk.core.Matrix3D.create()
        # Rotaatio Z-akselin ympäri
        transform.setToRotation(angle, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(x1, y1, 0))
        # Siirto Z-suunnassa
        transform.translation = adsk.core.Vector3D.create(0, 0, z_height)
        
        move_input = move_feats.createInput(bodies_col, transform)
        move_feats.add(move_input)
        
        return wire_body
    except:
        return None

# -------------------------------
# APU: tyhjennä malli
# -------------------------------

def clear_design(root, design):
    # Poista kaikki bodyt
    for i in reversed(range(root.bRepBodies.count)):
        b = root.bRepBodies.item(i)
        b.deleteMe()
    # Poista kaikki sketsit
    for i in reversed(range(root.sketches.count)):
        s = root.sketches.item(i)
        s.deleteMe()
    # Poista käyttäjän luomat appearances
    for i in reversed(range(design.appearances.count)):
        app = design.appearances.item(i)
        if '_appearance' in app.name:
            app.deleteMe()

# -------------------------------
# VARSINAINEN LAYOUT-TOIMINTO
# -------------------------------

def run_layout():
    app = adsk.core.Application.get()
    ui  = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent

    try:
        cfg = load_config()

        # -------------------------
        # 1) Tyhjennä malli ensin
        # -------------------------
        clear_design(root, design)

        # -------------------------
        # 2) Parametrit (levy, slot, reiät, lohkot)
        # -------------------------

        plate_cfg = cfg['plate']
        slots_cfg = cfg['slots']
        mh_cfg = cfg['mount_holes']

        plate_w_param = get_or_create_param(design, 'plate_width', plate_cfg['width'])
        plate_h_param = get_or_create_param(design, 'plate_height', plate_cfg['height'])
        plate_t_param = get_or_create_param(design, 'plate_thickness', plate_cfg['thickness'])

        slot_w_param = get_or_create_param(design, 'slot_width', slots_cfg['width'])
        slot_h_param = get_or_create_param(design, 'slot_height', slots_cfg['height'])

        mh_d_param = get_or_create_param(design, 'mount_hole_diameter', mh_cfg['diameter'])
        mh_o_param = get_or_create_param(design, 'mount_hole_offset', mh_cfg['offset'])

        # Lohkoparametrit
        block_param_map = {}  # param_name -> (w_param, h_param, t_param)
        for b in cfg['blocks']:
            pname = b['param_name']
            w_p = get_or_create_param(design, f'{pname}_width', b['width'])
            h_p = get_or_create_param(design, f'{pname}_height', b['height'])
            t_p = get_or_create_param(design, f'{pname}_thickness', b['thickness'])
            block_param_map[b['name']] = (pname, w_p, h_p, t_p)

        # -------------------------
        # 3) Luo Testilevy
        # -------------------------

        w = plate_w_param.value      # Fusionin sisäisissä yksiköissä (cm)
        h = plate_h_param.value
        t = plate_t_param.value

        sketches = root.sketches
        xy_plane = root.xYConstructionPlane
        plate_sk = sketches.add(xy_plane)
        plate_sk.name = 'Testilevy_sketsi'
        lines = plate_sk.sketchCurves.sketchLines

        p1 = adsk.core.Point3D.create(-w/2, -h/2, 0)
        p2 = adsk.core.Point3D.create( w/2, -h/2, 0)
        p3 = adsk.core.Point3D.create( w/2,  h/2, 0)
        p4 = adsk.core.Point3D.create(-w/2,  h/2, 0)

        lines.addByTwoPoints(p1, p2)
        lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p4)
        lines.addByTwoPoints(p4, p1)

        plate_prof = plate_sk.profiles.item(0)
        extrudes = root.features.extrudeFeatures
        ext_input = extrudes.createInput(
            plate_prof,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(t)
        ext_input.setDistanceExtent(False, distance)
        plate_ext = extrudes.add(ext_input)
        plate_body = plate_ext.bodies.item(0)
        plate_body.name = 'Testilevy'
        plate_ext.timelineObject.name = 'Testilevyn extrude'

        # -------------------------
        # 4) Etsi levyn yläpinta
        # -------------------------

        top_face = None
        max_z = None
        for i in range(plate_body.faces.count):
            f = plate_body.faces.item(i)
            geom = f.geometry
            if geom.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
                # Normaalin suunnan perusteella haetaan yläpinta (Z+)
                normal = geom.normal
                if max_z is None or normal.z > max_z:
                    max_z = normal.z
                    top_face = f

        if not top_face:
            ui.messageBox('Ei löytynyt levyn tasopintaa.')
            return

        # -------------------------
        # 5) Luo lohkot JSONista
        # -------------------------

        block_centers = {}  # name -> (x, y, z)

        # Värit lohkoille
        colors = [
            adsk.core.Color.create(255, 100, 100, 255),  # Punainen
            adsk.core.Color.create(100, 255, 100, 255),  # Vihreä
            adsk.core.Color.create(100, 100, 255, 255),  # Sininen
            adsk.core.Color.create(255, 255, 100, 255),  # Keltainen
            adsk.core.Color.create(255, 100, 255, 255),  # Magenta
            adsk.core.Color.create(100, 255, 255, 255),  # Syaani
            adsk.core.Color.create(255, 150, 100, 255),  # Oranssi
            adsk.core.Color.create(150, 100, 255, 255),  # Violetti
            adsk.core.Color.create(255, 200, 100, 255),  # Kulta
            adsk.core.Color.create(100, 200, 150, 255),  # Turkoosi
            adsk.core.Color.create(200, 150, 100, 255),  # Ruskea
            adsk.core.Color.create(150, 150, 255, 255),  # Vaaleansininen
            adsk.core.Color.create(255, 150, 200, 255),  # Vaaleanpunainen
            adsk.core.Color.create(150, 255, 150, 255),  # Vaaleanvihreä
        ]

        for idx, b in enumerate(cfg['blocks']):
            name = b['name']
            pname, w_p, h_p, t_p = block_param_map[name]

            bw = w_p.value
            bh = h_p.value
            bt = t_p.value

            x_rel = b['x_rel']
            y_rel = b['y_rel']

            # x_rel ja y_rel ovat normalisoituja koordinaatteja (-1 to 1)
            # mutta w ja h ovat koko levyn mitat, joten kerrotaan vain
            cx = x_rel * w
            cy = y_rel * h

            # Luo sketsi XY-tasolla origossa (ei top_facella)
            blk_sk = sketches.add(xy_plane)
            blk_sk.name = f'Lohko_sketsi_{name}'
            
            # Jos komponentti on iso (yli 3cm leveys), käytä pyöristettyjä kulmia
            if bw > 3.0:
                # Pyöristetyt kulmat - HUOM: pisteet OFFSET cx, cy
                lines_b = blk_sk.sketchCurves.sketchLines
                arcs = blk_sk.sketchCurves.sketchArcs
                r = 0.3  # 3mm radius
                
                # Kulmat hieman sisempänä + offset (cx, cy)
                bp1 = adsk.core.Point3D.create(cx - bw/2 + r, cy - bh/2, 0)
                bp2 = adsk.core.Point3D.create(cx + bw/2 - r, cy - bh/2, 0)
                bp3 = adsk.core.Point3D.create(cx + bw/2, cy - bh/2 + r, 0)
                bp4 = adsk.core.Point3D.create(cx + bw/2, cy + bh/2 - r, 0)
                bp5 = adsk.core.Point3D.create(cx + bw/2 - r, cy + bh/2, 0)
                bp6 = adsk.core.Point3D.create(cx - bw/2 + r, cy + bh/2, 0)
                bp7 = adsk.core.Point3D.create(cx - bw/2, cy + bh/2 - r, 0)
                bp8 = adsk.core.Point3D.create(cx - bw/2, cy - bh/2 + r, 0)
                
                lines_b.addByTwoPoints(bp1, bp2)
                lines_b.addByTwoPoints(bp3, bp4)
                lines_b.addByTwoPoints(bp5, bp6)
                lines_b.addByTwoPoints(bp7, bp8)
                
                # Pyöristetyt kulmat
                arcs.addFillet(lines_b.item(0), bp2, lines_b.item(1), bp3, r)
                arcs.addFillet(lines_b.item(1), bp4, lines_b.item(2), bp5, r)
                arcs.addFillet(lines_b.item(2), bp6, lines_b.item(3), bp7, r)
                arcs.addFillet(lines_b.item(3), bp8, lines_b.item(0), bp1, r)
            else:
                # Tavalliset terävät kulmat pienille komponenteille + OFFSET (cx, cy)
                lines_b = blk_sk.sketchCurves.sketchLines
                bp1 = adsk.core.Point3D.create(cx - bw/2, cy - bh/2, 0)
                bp2 = adsk.core.Point3D.create(cx + bw/2, cy - bh/2, 0)
                bp3 = adsk.core.Point3D.create(cx + bw/2, cy + bh/2, 0)
                bp4 = adsk.core.Point3D.create(cx - bw/2, cy + bh/2, 0)
                
                lines_b.addByTwoPoints(bp1, bp2)
                lines_b.addByTwoPoints(bp2, bp3)
                lines_b.addByTwoPoints(bp3, bp4)
                lines_b.addByTwoPoints(bp4, bp1)

            if blk_sk.profiles.count == 0:
                continue

            blk_prof = blk_sk.profiles.item(0)
            blk_ext_in = extrudes.createInput(
                blk_prof,
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            
            # Extrude yksinkertaisesti
            blk_dist = adsk.core.ValueInput.createByReal(bt)
            blk_ext_in.setDistanceExtent(False, blk_dist)
            
            blk_ext = extrudes.add(blk_ext_in)
            blk_body = blk_ext.bodies.item(0)
            blk_body.name = f'{name} ({int(bw*10)}x{int(bh*10)}x{int(bt*10)}mm)'  # Nimi + mitat
            blk_ext.timelineObject.name = f'Lohko {name}'
            
            # Siirrä body Z-suunnassa ylöspäin levyn pinnalle
            # XY on jo oikein sketchissä, joten vain Z-siirto
            move_feats = root.features.moveFeatures
            bodies_col = adsk.core.ObjectCollection.create()
            bodies_col.add(blk_body)
            
            transform = adsk.core.Matrix3D.create()
            transform.translation = adsk.core.Vector3D.create(0, 0, t)
            
            move_input = move_feats.createInput(bodies_col, transform)
            move_feats.add(move_input)
            
            # Asetetaan väri suoraan bodyyn
            color = colors[idx % len(colors)]
            try:
                # Yksinkertainen tapa: käytä material-väriä
                blk_body.material = design.materials.item(0)  # Default material
                # Vaihtoehtoinen tapa: custom graphics
                blk_body.opacity = 0.8
            except:
                pass

            # Lohkon keskipiste
            block_centers[name] = (cx, cy, t + bt/2)

        # -------------------------
        # 5b) Komponenttien nimet teksteinä levyn sivuilla + viivoilla
        # -------------------------
        
        text_sk = sketches.add(xy_plane)
        text_sk.name = 'Komponenttinimet_ja_viivat'
        
        text_margin = 1.5  # 1.5cm marginaali levyn reunasta tekstille
        
        # Jaa komponentit neljään ryhmään Y-koordinaatin mukaan ensin
        # Pitkät sivut (top/bottom): y_rel poikkeaa nollasta
        # Lyhyet sivut (left/right): y_rel lähellä nollaa, jaa X:n mukaan
        y_threshold = 0.15  # Kynnysarvo keskirivin määrittämiseen
        
        left_components = []   # Keskirivin vasen puoli (x < 0)
        right_components = []  # Keskirivin oikea puoli (x > 0)
        top_components = []    # Yläreuna (y > threshold)
        bottom_components = [] # Alareuna (y < -threshold)
        
        for b in cfg['blocks']:
            x_rel = b['x_rel']
            y_rel = b['y_rel']
            
            # ENSIN: Määritä rivi Y-koordinaatin mukaan
            if y_rel > y_threshold:  # Ylärivi (x,3)
                top_components.append(b)
            elif y_rel < -y_threshold:  # Alarivi (x,1)
                bottom_components.append(b)
            else:  # Keskirivi (x,2) - jaa X:n mukaan
                if x_rel < 0:  # Vasemmalle lyhyelle reunalle
                    left_components.append(b)
                else:  # Oikealle lyhyelle reunalle
                    right_components.append(b)
        
        # Piirrä vasemman lyhyen reunan tekstit ja viivat (keskirivi, x < 0)
        # Levitetään tekstit Y-suunnassa, ettei mene päällekkäin
        left_count = len(left_components)
        for idx, b in enumerate(left_components):
            name = b['name']
            pname, w_p, h_p, t_p = block_param_map[name]
            
            x_rel = b['x_rel']
            y_rel = b['y_rel']
            cx = x_rel * w
            cy = y_rel * h
            
            # Tekstin paikka: X vakio vasemmalla, Y levitetty tasaisesti
            text_x = -w/2 - text_margin - 1.5  # X vakio vasemmalla
            # Levitä tekstit 2.5 cm välein
            text_spacing = 2.5
            if left_count > 1:
                total_height = (left_count - 1) * text_spacing
                start_y = -total_height / 2
                text_y = start_y + idx * text_spacing
            else:
                text_y = 0
            
            try:
                # Luo teksti
                text_input = text_sk.sketchTexts.createInput(name, 0.4, adsk.core.Point3D.create(text_x, text_y, 0))
                text_obj = text_sk.sketchTexts.add(text_input)
                
                # Vedä viiva tekstistä komponenttiin
                line_start = adsk.core.Point3D.create(text_x + len(name) * 0.25, text_y, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
            except Exception as e:
                # Vedä vain viiva jos teksti ei toimi
                line_start = adsk.core.Point3D.create(text_x, text_y, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
        
        # Piirrä oikean lyhyen reunan tekstit ja viivat (keskirivi, x > 0)
        # Levitetään tekstit Y-suunnassa, ettei mene päällekkäin
        right_count = len(right_components)
        for idx, b in enumerate(right_components):
            name = b['name']
            pname, w_p, h_p, t_p = block_param_map[name]
            
            x_rel = b['x_rel']
            y_rel = b['y_rel']
            cx = x_rel * w
            cy = y_rel * h
            
            # Tekstin paikka: X vakio oikealla, Y levitetty tasaisesti
            text_x = w/2 + text_margin + 0.5  # X vakio oikealla
            # Levitä tekstit 2.5 cm välein
            text_spacing = 2.5
            if right_count > 1:
                total_height = (right_count - 1) * text_spacing
                start_y = -total_height / 2
                text_y = start_y + idx * text_spacing
            else:
                text_y = 0
            
            try:
                # Luo teksti
                text_input = text_sk.sketchTexts.createInput(name, 0.4, adsk.core.Point3D.create(text_x, text_y, 0))
                text_obj = text_sk.sketchTexts.add(text_input)
                
                # Vedä viiva tekstistä komponenttiin
                line_start = adsk.core.Point3D.create(text_x - 0.2, text_y, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
            except Exception as e:
                # Vedä vain viiva jos teksti ei toimi
                line_start = adsk.core.Point3D.create(text_x, text_y, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
        
        # Piirrä yläreunalle (pitkä reuna) tekstit ja viivat (ylärivi, y > threshold)
        for b in top_components:
            name = b['name']
            pname, w_p, h_p, t_p = block_param_map[name]
            
            x_rel = b['x_rel']
            y_rel = b['y_rel']
            cx = x_rel * w
            cy = y_rel * h
            
            # Tekstin paikka: SAMALLA X-TASOLLA kuin komponentti, Y vakio ylhäällä
            text_x = cx  # Sama X-koordinaatti kuin komponentilla
            text_y = h/2 + text_margin  # Y vakio yläreunalla
            
            try:
                text_input = text_sk.sketchTexts.createInput(name, 0.4, adsk.core.Point3D.create(text_x, text_y, 0))
                text_obj = text_sk.sketchTexts.add(text_input)
                
                line_start = adsk.core.Point3D.create(text_x, text_y - 0.2, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
            except:
                line_start = adsk.core.Point3D.create(text_x, text_y, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
        
        # Piirrä alareunalle (pitkä reuna) tekstit ja viivat (alarivi, y < -threshold)
        for b in bottom_components:
            name = b['name']
            pname, w_p, h_p, t_p = block_param_map[name]
            
            x_rel = b['x_rel']
            y_rel = b['y_rel']
            cx = x_rel * w
            cy = y_rel * h
            
            # Tekstin paikka: SAMALLA X-TASOLLA kuin komponentti, Y vakio alhaalla
            text_x = cx  # Sama X-koordinaatti kuin komponentilla
            text_y = -h/2 - text_margin  # Y vakio alareunalla
            
            try:
                text_input = text_sk.sketchTexts.createInput(name, 0.4, adsk.core.Point3D.create(text_x, text_y, 0))
                text_obj = text_sk.sketchTexts.add(text_input)
                
                line_start = adsk.core.Point3D.create(text_x, text_y + 0.2, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)
            except:
                line_start = adsk.core.Point3D.create(text_x, text_y, 0)
                line_end = adsk.core.Point3D.create(cx, cy, 0)
                text_sk.sketchCurves.sketchLines.addByTwoPoints(line_start, line_end)

        # -------------------------
        # 6) Kytkentäkaavio (2D viivat levyllä)
        # -------------------------

        route_midpoints = []  # (mx, my) levyn pinnassa

        # Tarkistetaan onko wires vai routes käytössä
        wires_list = []
        if 'wires' in cfg:
            wires_list = cfg['wires']
        
        if wires_list:
            # Luodaan yksinkertainen 2D-kytkentäkaavio
            routes_sk = sketches.add(top_face)
            routes_sk.name = 'Kytkentäkaavio'
            route_lines = routes_sk.sketchCurves.sketchLines
            
            offset_step = 0.03  # 0.3mm offset johdoille
            
            for wire in wires_list:
                try:
                    n1 = wire['from']
                    n2 = wire['to']
                    wire_type = wire.get('type', 'power')
                    wire_name = wire.get('name', '')
                    
                    if n1 not in block_centers or n2 not in block_centers:
                        continue
                    x1, y1, _ = block_centers[n1]
                    x2, y2, _ = block_centers[n2]
                    
                    # Laske johdon suunta ja kohtisuora
                    dx = x2 - x1
                    dy = y2 - y1
                    length = (dx**2 + dy**2)**0.5
                    if length < 0.001:
                        continue
                    
                    # Kohtisuora vektori (normalisoitu)
                    perp_x = -dy / length
                    perp_y = dx / length
                    
                    if wire_type == 'power':
                        # Tehojohdoissa kaksi viivaa (+ ja -)
                        offset = offset_step
                        p1_plus = adsk.core.Point3D.create(x1 + perp_x * offset, y1 + perp_y * offset, 0)
                        p2_plus = adsk.core.Point3D.create(x2 + perp_x * offset, y2 + perp_y * offset, 0)
                        route_lines.addByTwoPoints(p1_plus, p2_plus)
                        
                        offset = -offset_step
                        p1_minus = adsk.core.Point3D.create(x1 + perp_x * offset, y1 + perp_y * offset, 0)
                        p2_minus = adsk.core.Point3D.create(x2 + perp_x * offset, y2 + perp_y * offset, 0)
                        route_lines.addByTwoPoints(p1_minus, p2_minus)
                        
                        # Läpivienti keskelle
                        mx = (x1 + x2) / 2.0
                        my = (y1 + y2) / 2.0
                        route_midpoints.append((mx, my))
                    else:
                        # Signaalijohdot - yksi viiva
                        p_start = adsk.core.Point3D.create(x1, y1, 0)
                        p_end = adsk.core.Point3D.create(x2, y2, 0)
                        route_lines.addByTwoPoints(p_start, p_end)
                        
                        mx = (x1 + x2) / 2.0
                        my = (y1 + y2) / 2.0
                        route_midpoints.append((mx, my))
                except:
                    pass

        # -------------------------
        # 7) Läpivientislotit reittien keskikohtiin
        # -------------------------

        sw = slot_w_param.value
        sh = slot_h_param.value

        slots_sk = sketches.add(top_face)
        slots_sk.name = 'Läpiviennit'
        slot_lines = slots_sk.sketchCurves.sketchLines

        for (mx, my) in route_midpoints:
            sp1 = adsk.core.Point3D.create(mx - sw/2, my - sh/2, 0)
            sp2 = adsk.core.Point3D.create(mx + sw/2, my - sh/2, 0)
            sp3 = adsk.core.Point3D.create(mx + sw/2, my + sh/2, 0)
            sp4 = adsk.core.Point3D.create(mx - sw/2, my + sh/2, 0)

            slot_lines.addByTwoPoints(sp1, sp2)
            slot_lines.addByTwoPoints(sp2, sp3)
            slot_lines.addByTwoPoints(sp3, sp4)
            slot_lines.addByTwoPoints(sp4, sp1)

        if slots_sk.profiles.count > 0:
            for i in range(slots_sk.profiles.count):
                try:
                    prof = slots_sk.profiles.item(i)
                    cut_in = extrudes.createInput(
                        prof,
                        adsk.fusion.FeatureOperations.CutFeatureOperation
                    )
                    # Leikkaus läpi (ThroughAll)
                    cut_in.setOneSideExtent(
                        adsk.fusion.ThroughAllExtentDefinition.create(),
                        adsk.fusion.ExtentDirections.PositiveExtentDirection
                    )
                    # Määritetään mihin bodyyn leikataan
                    cut_in.participantBodies = [plate_body]
                    cut = extrudes.add(cut_in)
                    cut.timelineObject.name = f'Läpivienti_{i+1}'
                except:
                    # Ohita leikkaus jos se on levyn ulkopuolella
                    pass

        # -------------------------
        # 8) Kiinnitysreiät kulmiin
        # -------------------------

        d = mh_d_param.value
        off = mh_o_param.value

        holes_sk = sketches.add(top_face)
        holes_sk.name = 'Kiinnitysreiät'
        circles = holes_sk.sketchCurves.sketchCircles

        # Neljä kulmaa
        hx = w/2 - off
        hy = h/2 - off

        pts = [
            adsk.core.Point3D.create( hx,  hy, 0),
            adsk.core.Point3D.create(-hx,  hy, 0),
            adsk.core.Point3D.create(-hx, -hy, 0),
            adsk.core.Point3D.create( hx, -hy, 0)
        ]

        for p in pts:
            circles.addByCenterRadius(p, d/2)

        if holes_sk.profiles.count > 0:
            for i in range(holes_sk.profiles.count):
                try:
                    prof = holes_sk.profiles.item(i)
                    cut_in = extrudes.createInput(
                        prof,
                        adsk.fusion.FeatureOperations.CutFeatureOperation
                    )
                    # Leikkaus läpi (ThroughAll)
                    cut_in.setOneSideExtent(
                        adsk.fusion.ThroughAllExtentDefinition.create(),
                        adsk.fusion.ExtentDirections.PositiveExtentDirection
                    )
                    # Määritetään mihin bodyyn leikataan
                    cut_in.participantBodies = [plate_body]
                    cut = extrudes.add(cut_in)
                    cut.timelineObject.name = f'Kiinnitysreikä_{i+1}'
                except:
                    # Ohita leikkaus jos se on levyn ulkopuolella
                    pass

        app.activeViewport.fit()
        ui.messageBox('Layout-automaatiotyökalu suoritettu.\nLevy, lohkot, reitit, läpiviennit ja kiinnitysreiät luotu.')

    except:
        ui.messageBox('Virhe run_layout():\n{}'.format(traceback.format_exc()))

# -------------------------------
# KOMENTOHANDLERIT
# -------------------------------

class LayoutCommandExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        run_layout()

class LayoutCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        try:
            cmd = args.command
            on_execute = LayoutCommandExecuteHandler()
            cmd.execute.add(on_execute)
            handlers.append(on_execute)
        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Virhe LayoutCommandCreatedHandler:\n{}'.format(traceback.format_exc()))

# -------------------------------
# ADD-ININ KÄYNNISTYS
# -------------------------------

def run(context):
    app = adsk.core.Application.get()
    ui  = app.userInterface

    try:
        cmd_def = ui.commandDefinitions.itemById('RauliLayoutCmd')
        if not cmd_def:
            cmd_def = ui.commandDefinitions.addButtonDefinition(
                'RauliLayoutCmd',
                'Aja layout-automaatiotyökalu',
                'Luo Testilevyn, lohkot, reitit ja läpiviennit layout_config.json-tiedoston mukaan.',
                ''  # Tyhjä string ikonille
            )

        on_created = LayoutCommandCreatedHandler()
        cmd_def.commandCreated.add(on_created)
        handlers.append(on_created)

        workspace = ui.workspaces.itemById('FusionSolidEnvironment')
        panel = workspace.toolbarPanels.itemById('SolidScriptsAddinsPanel')
        
        # Tarkista ettei komento ole jo paneelissa
        ctrl_check = panel.controls.itemById('RauliLayoutCmd')
        if not ctrl_check:
            panel.controls.addCommand(cmd_def)

    except:
        if ui:
            ui.messageBox('Virhe run():\n{}'.format(traceback.format_exc()))

# -------------------------------
# ADD-ININ SAMMUTUS
# -------------------------------

def stop(context):
    app = adsk.core.Application.get()
    ui  = app.userInterface

    try:
        cmd_def = ui.commandDefinitions.itemById('RauliLayoutCmd')
        if cmd_def:
            cmd_def.deleteMe()

        workspace = ui.workspaces.itemById('FusionSolidEnvironment')
        panel = workspace.toolbarPanels.itemById('SolidScriptsAddinsPanel')
        ctrl = panel.controls.itemById('RauliLayoutCmd')
        if ctrl:
            ctrl.deleteMe()

    except:
        ui.messageBox('Virhe stop():\n{}'.format(traceback.format_exc()))
