import bpy
strips = bpy.context.selected_sequences
for strip in strips:
    if strip.type != "SOUND":
        mod = strip.modifiers.new("invert","CURVES")
        points = mod.curve_mapping.curves[3].points
        points[0].location=(0,1)
        points[1].location=(1,0)