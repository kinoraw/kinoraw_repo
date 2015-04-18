import bpy

bl_info = {
    "name": "Copie des modifiers sous VSE",
    "author": "DoubleZ",
    "version": (0, 35),
    "blender": (2, 6, 5),
    "api": 40779,
    "location": "VSE > Properties > Copier modifiers",
    "description": "Copier modifiers",
    "warning": "Non pris en compte : keyframe",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"}

modifStrip = ""

class CopierModifiers(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sequencer.copier_modifiers"
    bl_label = "Copier Modifiers"
    
    def execute(self, context):
        global modifStrip
        modifStrip = bpy.context.selected_sequences[0]  ##Un "pointeur" pointe sur ce strip
        return {'FINISHED'}
    
class CollerModifiers(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sequencer.coller_modifiers"
    bl_label = "Coller Modifiers"
    
    def execute(self, context):
        global modifStrip
        for sequence in bpy.context.selected_sequences:
            for i in modifStrip.modifiers :
                last = sequence.modifiers.new(i.name,i.type)
                
                #Recopie des masks/strips
                last.input_mask_id = i.input_mask_id
                last.input_mask_strip = i.input_mask_strip
                last.input_mask_type = i.input_mask_type
                
                #Simple recopie des paramètres
                if i.type == "COLOR_BALANCE":
                    last.color_multiply = i.color_multiply
                    #lift
                    last.color_balance.lift = i.color_balance.lift
                    last.color_balance.invert_lift = i.color_balance.invert_lift
                    #gamma
                    last.color_balance.gamma = i.color_balance.gamma
                    last.color_balance.invert_gamma = i.color_balance.invert_gamma
                    #gain
                    last.color_balance.gain = i.color_balance.gain
                    last.color_balance.invert_gain = i.color_balance.invert_gain
                
                #Simple recopie des paramètres    
                if i.type == "BRIGHT_CONTRAST" :
                    last.bright = i.bright
                    last.contrast = i.contrast
                
                #Courbes... plus complexe pour la recopie
                if i.type == "HUE_CORRECT" or i.type == "CURVES" :
                    for curve in range(len(i.curve_mapping.curves)):
                        #Nettoie la courbe dans le cas d'une utilisation de HUE_CORRECT
                        aDetruire = last.curve_mapping.curves[curve].points
                        while len(aDetruire) > 2 :
                            aDetruire.remove(aDetruire[1])
                        
                        #Recopie de la position des points sur la courbe    
                        for point in range(len(i.curve_mapping.curves[curve].points)):
                            lct = i.curve_mapping.curves[curve].points[point].location
                            if point == 0 or point == len(i.curve_mapping.curves[curve].points)-1 : #Premier et dernier point non supprimable
                                last.curve_mapping.curves[curve].points[point].location = lct
                            else :                                                                  #Les autres points sont crées sur la courbe
                                last.curve_mapping.curves[curve].points.new(lct[0],lct[1])

                            #Type de vector (trait droit ou courbe)
                            last.curve_mapping.curves[curve].points[point].handle_type = i.curve_mapping.curves[curve].points[point].handle_type
                    
                    #Simple recopie des paramètres
                    last.curve_mapping.clip_max_x = i.curve_mapping.clip_max_x
                    last.curve_mapping.clip_max_y = i.curve_mapping.clip_max_y
                    last.curve_mapping.clip_min_x = i.curve_mapping.clip_min_x
                    last.curve_mapping.clip_min_y = i.curve_mapping.clip_min_y
                    
                    
        return {'FINISHED'}

#Génére les 2 boutons à partir de la barre du bas du VSE
def import_copieModifiers_buttons(self,context):
    row = self.layout.row(align=True)
    row.operator("sequencer.copier_modifiers", text="Copier modifier", icon='COPYDOWN')
    row.operator("sequencer.coller_modifiers", text="Coller modifier", icon='PASTEDOWN')

def register():
    bpy.utils.register_class(CopierModifiers)
    bpy.utils.register_class(CollerModifiers)
    bpy.types.SEQUENCER_HT_header.append(import_copieModifiers_buttons)

def unregister():
    bpy.utils.unregister_class(CopierModifiers)
    bpy.utils.unregister_class(CollerModifiers)
    bpy.types.SEQUENCER_HT_header.remove(import_copieModifiers_buttons)
    

if __name__ == "__main__":
    register()