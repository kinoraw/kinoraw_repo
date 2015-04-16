import bpy, time
from bpy.app.handlers import persistent

def act_strip(context):
    try:
        return context.scene.sequence_editor.active_strip
    except AttributeError:
        return None

def find_parent(child):
    if (type(child) == str):
        childname = child
    else:
        childname = child.name
    scene = bpy.context.scene
    for relationship in scene.parenting:
        if (relationship.child == childname):
            return relationship.parent
    return "None"

def find_children(parent):
    if (type(parent) == str):
        parentname = parent
    else:
        parentname = parent.name
    scene = bpy.context.scene
    childrennames = []
    for relationship in scene.parenting:
        if (relationship.parent == parentname):
            childrennames.append(relationship.child)
    return childrennames

@persistent
def load_handler(dummy):
    scn = bpy.context.scene
    strips = scn.sequence_editor.sequences_all
    strip = act_strip(bpy.context)
    if scn.parenting:
        childrennames = find_children(strip.name)
        parentname = find_parent(strip.name)
        print(childrennames)
        for i in strips:
            if i.name in childrennames:
                i.select = True
    
    
    
bpy.app.handlers.scene_update_post.append(load_handler)