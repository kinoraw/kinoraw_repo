'''
               LICENCE PUBLIQUE RIEN À BRANLER
                     Version 1, Mars 2009

Copyright (C) 2009 Sam Hocevar
 14 rue de Plaisance, 75014 Paris, France

La copie et la distribution de copies exactes de cette licence sont
autorisées, et toute modification est permise à condition de changer
le nom. 

        CONDITIONS DE COPIE, DISTRIBUTON ET MODIFICATION
              DE LA LICENCE PUBLIQUE RIEN À BRANLER

 0. Faites ce que vous voulez, j’en ai RIEN À BRANLER.
'''

import bpy

bl_info = {
    "name": "Copy modifier(s) in VSE",
    "author": "DoubleZ",
    "version": (0, 5),
    "blender": (2, 7, 4),
    "api": 40779,
    "location": "VSE > Properties > Copier modifiers",
    "description": "Copy modifier(s)",
    "warning": "Non pris en compte : keyframe",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"}

modifStrip = ""

class CopyModifiers(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sequencer.copy_modifiers"
    bl_label = "Copy Modifier(s)"
    
    def execute(self, context):
        global modifStrip
        modifStrip = bpy.context.selected_sequences[0]  ##Un "pointeur" pointe sur ce strip
        return {'FINISHED'}
    
class PasteModifiers(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sequencer.paste_modifiers"
    bl_label = "Paste Modifier(s)"
    
    def execute(self, context):
        global modifStrip
        try :       #Dans le cas ou aucun "copier" n'a été effectué
            for sequence in bpy.context.selected_sequences:
                #copie de l'utilisation de "linear modifiers"
                sequence.use_linear_modifiers = modifStrip.use_linear_modifiers
                
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
                        
                    #Recopie des keyframes (action)
                    #TODO
                        
        except :
            pass
                    
        return {'FINISHED'}

#Génére les 2 boutons à partir de la barre du bas du VSE

# def import_copyModifiers_buttons(self,context):
#     row = self.layout.row(align=True)
#     row.operator("sequencer.copy_modifiers", text="Copy modifier(s)", icon='COPYDOWN')
#     row.operator("sequencer.paste_modifiers", text="Paste modifier(s)", icon='PASTEDOWN')

def register():
    bpy.utils.register_class(CopyModifiers)
    bpy.utils.register_class(PasteModifiers)
    #bpy.types.SEQUENCER_HT_header.append(import_copyModifiers_buttons)

def unregister():
    bpy.utils.unregister_class(CopyModifiers)
    bpy.utils.unregister_class(PasteModifiers)
    #bpy.types.SEQUENCER_HT_header.remove(import_copyModifiers_buttons)
    

if __name__ == "__main__":
    register()