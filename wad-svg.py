import os
import sys
import json
import config
from omg import *
import drawsvg as draw

def map_to_svg(wad, map_name, width, out_dir):
    xsize = width - 8
    
    try:
        edit = UMapEditor(wad.udmfmaps[map_name])
    except KeyError:
        edit = UMapEditor(wad.maps[map_name])

    xmin = ymin = float('inf')
    xmax = ymax = float('-inf')
    for v in edit.vertexes:
        xmin = min(xmin, v.x)
        xmax = max(xmax, v.x)
        ymin = min(ymin, -v.y)
        ymax = max(ymax, -v.y)

    scale = xsize / float(xmax - xmin)
    xmax = xmax * scale
    xmin = xmin * scale
    ymax = ymax * scale
    ymin = ymin * scale

    for v in edit.vertexes:
        v.x = v.x * scale
        v.y = -v.y * scale
        
    d = draw.Drawing(int(xmax - xmin) + 8, int(ymax - ymin) + 8, origin=(0, 0))
    
    edit.linedefs.sort(key=lambda a: not a.twosided)
    for line in edit.linedefs:
        p1x = edit.vertexes[line.v1].x - xmin + 4
        p1y = edit.vertexes[line.v1].y - ymin + 4
        p2x = edit.vertexes[line.v2].x - xmin + 4
        p2y = edit.vertexes[line.v2].y - ymin + 4

        color = "red"
        if line.twosided:
            color = "yellow"
        if line.special:
            color = "lavender"
                
        d.append(draw.Line(p1x, p1y, p2x, p2y, stroke=color, stroke_width=1, fill='none'))
    
    d.save_svg(os.path.join(out_dir, f"{map_name.lower()}.svg"))
    del edit

wad_index = []
for wad in config.wads:
    iwad = WAD()
    iwad.from_file(wad["file"])

    wad_out_dir = os.path.join(config.out_dir, wad["slug"].lower())
    if not os.path.exists(wad_out_dir):
        os.makedirs(wad_out_dir)
    
    map_index = []
    for map in iwad.maps:
        print(f"- {wad["name"]} > {map}")
        map_to_svg(iwad, map, config.max_width, wad_out_dir)
        map_index.append(map.lower())
    del iwad

    wad["maps"] = map_index
    wad_index.append(wad)

with open(os.path.join(config.out_dir, "index.json"), "w") as f:
    json.dump(wad_index, f)
    
