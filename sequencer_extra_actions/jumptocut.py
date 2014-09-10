# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy

from . import functions
from bpy.props import IntProperty, BoolProperty


class OBJECT_OT_Setinout(bpy.types.Operator):
    bl_label = "set IN and OUT to selected"
    bl_idname = "sequencerextra.setinout"
    bl_description = "set IN and OUT markers to the selected strips limits"

    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            return scn.sequence_editor.active_strip
        else:
            return False

    def execute(self, context):
        scn = context.scene
        markers =scn.timeline_markers
        seq = scn.sequence_editor
        
        meta_level = len(seq.meta_stack)
        if meta_level > 0:
            seq = seq.meta_stack[meta_level - 1]

        #search for timeline limits
        tl_start = 300000
        tl_end = -300000
        for i in context.selected_editable_sequences:
            #try:
            if i.select == True:
                start = i.frame_start + i.frame_offset_start - i.frame_still_start
                end = start + i.frame_final_duration + 1
                if start < tl_start:
                    tl_start = start
                print("eooooo")
                if end > tl_end:
                    tl_end = end - 1
                print(tl_start,tl_end)
            #except AttributeError as Error:
            #    print("##### ;-P  ", Error)

        if "IN" not in markers:
            mark=markers.new(name="IN")
            mark.frame=tl_start
        else:
            mark=markers["IN"]
            mark.frame=tl_start
        if "OUT" not in markers:
            mark= markers.new(name="OUT")
            mark.frame=tl_end
        else:
            mark=markers["OUT"]
            mark.frame=tl_end
        return {'FINISHED'}


class OBJECT_OT_Triminout(bpy.types.Operator):
    bl_label = "Trim to in & out"
    bl_idname = "sequencerextra.triminout"
    bl_description = "trim the selected strip to IN and OUT markers (if exists)"
    
    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            if scn.sequence_editor.active_strip:
                markers=scn.timeline_markers
                if "IN" and "OUT" in markers:
                    return True
        else:
            return False
   
    
    def execute(self, context):
        scene=context.scene
        seq=scene.sequence_editor
        markers=scene.timeline_markers
        sin=markers["IN"].frame
        sout=markers["OUT"].frame
        strips = context.selected_editable_sequences
        for strip in strips:
            #deselect all other strips 
            #(triminout function only works fine 
            # with one strip selected at a time)
            for i in strips: 
                try:
                    i.select = False
                except ReferenceError:
                    pass
            #select current strip
            strip.select = True
            remove=functions.triminout(strip,sin,sout)
            if remove == True:
                seq.sequences.remove(strip)
                #this strip should be deleted from strips list...
                #so i need some exceptions around
        
        #select all strips again
        for strip in strips:
            try: 
                strip.select=True
            except ReferenceError:
                pass
        bpy.ops.sequencer.reload()
        return {'FINISHED'}


#JUMP

class OBJECT_OT_Jumptocut(bpy.types.Operator):  #Operator jump previous edit point
    bl_label = "jump to edit points"
    bl_idname = "sequencerextra.jumptocut"
    bl_description = "jump to edit points"

    bl_options = {'REGISTER', 'UNDO'} 

    next = BoolProperty(
        name='next',
        description='jump to next cut',
        default=False)

    @classmethod
    def poll(self, context):
        return context.scene.sequence_editor

    def execute(self, context):
        scene=bpy.context.scene
        seq=scene.sequence_editor
        editpoints = functions.geteditpoints(context)
        
        if self.next == True:
            bpy.context.scene.frame_current = functions.searchnext(scene.frame_current, editpoints)
            last = 0
            for i in editpoints:
                if i > last: last = i
            if bpy.context.scene.frame_current == last:
                bpy.context.scene.frame_current = last
                #bpy.context.scene.frame_current = last-1
                self.report({'INFO'},'Last Frame')
        else:
            bpy.context.scene.frame_current = functions.searchprev(scene.frame_current, editpoints)
        return {'FINISHED'}       
        

# SOURCE IN OUT

class OBJECT_OT_Sourcein(bpy.types.Operator):  #Operator source in
    bl_label = "Source IN"
    bl_idname = "sequencerextra.sourcein"
    bl_description = "add or move a marker named IN"

    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn:
            return scn.sequence_editor
        else:
            return False

    def execute(self, context):
        scene=bpy.context.scene
        seq = scene.sequence_editor
        markers=scene.timeline_markers
        if "OUT" in markers:
            sout=markers["OUT"]
            if scene.frame_current <= sout.frame:
                if "IN" not in markers:
                    sin=markers.new(name="IN")
                    sin.frame=scene.frame_current
                else:
                    sin=markers["IN"]
                    sin.frame=scene.frame_current
            #trying to set in after out
            else:
                if "IN" not in markers:
                    sin=markers.new(name="IN")
                    sin.frame=sout.frame
                else:
                    sin=markers["IN"]
                    sin.frame=sout.frame
                self.report({'WARNING'},'IN after OUT')
        else:
            if "IN" not in markers:
                sin=markers.new(name="IN")
                sin.frame=scene.frame_current
            else:
                sin=markers["IN"]
                sin.frame=scene.frame_current
        if seq:
            bpy.ops.sequencer.reload()
        return {'FINISHED'}

class OBJECT_OT_Sourceout(bpy.types.Operator):  #Operator source out
    bl_label = "Source OUT"
    bl_idname = "sequencerextra.sourceout"
    bl_description = "add or move a marker named OUT"

    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn:
            return scn.sequence_editor
        else:
            return False

    def execute(self, context):
        scene=bpy.context.scene
        seq = scene.sequence_editor
        markers=scene.timeline_markers
        if "IN" in markers:
            sin=markers["IN"]
            if scene.frame_current >= sin.frame:
                if "OUT" not in markers:
                    sout= markers.new(name="OUT")
                    sout.frame=scene.frame_current
                else:
                    sout=markers["OUT"]
                    sout.frame=scene.frame_current
            #trying to set out before in
            else:
                if "OUT" not in markers:
                    sout= markers.new(name="OUT")
                    sout.frame = sin.frame
                else:
                    sout=markers["OUT"]
                    sout.frame = sin.frame
                self.report({'WARNING'}, "OUT before IN")
        else:
            sout= markers.new(name="OUT")
            sout.frame=scene.frame_current
        if seq:
            bpy.ops.sequencer.reload()
        return {'FINISHED'}

class OBJECT_OT_Setstartend(bpy.types.Operator):  #Operator set start & end
    bl_label = "set Start & End"
    bl_idname = "sequencerextra.setstartend"
    bl_description = "set Start and End to IN and OUT marker values"

    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(self, context):
        scn = context.scene
        markers=scn.timeline_markers
        if "IN" and "OUT" in markers:
            return True
        else:
            return False

    def execute(self, context):
        scn=context.scene
        markers=scn.timeline_markers
        sin=markers["IN"]
        sout=markers["OUT"]
        scn.frame_start = sin.frame
        scn.frame_end = sout.frame
        bpy.ops.sequencer.reload()
        return {'FINISHED'}


# COPY PASTE

class OBJECT_OT_Metacopy(bpy.types.Operator):  #Operator copy source in/out
    bl_label = "Trim & Meta-Copy"
    bl_idname = "sequencerextra.metacopy"
    bl_description = "make meta from selected strips, trim it to in/out (if available) and copy it to clipboard"

    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        # rehacer
        scene=bpy.context.scene
        seq = scene.sequence_editor
        markers=scene.timeline_markers
        strip1= seq.active_strip
        if strip1 != None:
            if "IN" and "OUT" in markers:
                sin=markers["IN"].frame
                sout=markers["OUT"].frame
                bpy.ops.sequencer.meta_make()
                strip2= seq.active_strip
                functions.triminout(strip2,sin,sout)
                bpy.ops.sequencer.copy()
                bpy.ops.sequencer.meta_separate()
                self.report({'INFO'}, "META2 has been trimed and copied")
            else:
                bpy.ops.sequencer.meta_make()
                bpy.ops.sequencer.copy()
                bpy.ops.sequencer.meta_separate()
                self.report({'WARNING'}, "No In & Out!! META has been copied")
        else:
            self.report({'ERROR'}, "No strip selected")
        return {'FINISHED'}

class OBJECT_OT_Metapaste(bpy.types.Operator):  #Operator paste source in/out
    bl_label = "Paste in current Frame"
    bl_idname = "sequencerextra.metapaste"
    bl_description = "paste source from clipboard to current frame"

    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        # rehacer
        scene=bpy.context.scene
        bpy.ops.sequencer.paste()
        bpy.ops.sequencer.snap(frame=scene.frame_current)
        strips = context.selected_editable_sequences
        context.scene.sequence_editor.active_strip=strips[0]
        context.scene.update()
        return {'FINISHED'}


class OBJECT_OT_Unmetatrim(bpy.types.Operator):  #Operator paste source in/out
    bl_label = "Paste in current Frame"
    bl_idname = "sequencerextra.meta_separate_trim"
    bl_description = "set in and out to meta, unmeta and trim the content"
    
    bl_options = {'REGISTER', 'UNDO'} 
    
    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            if scn.sequence_editor.active_strip:
                return scn.sequence_editor.active_strip.type == "META"
        else:
            return False

    def execute(self, context):
        scn=context.scene
        seq=scn.sequence_editor
        markers=scn.timeline_markers

        # setting in and out around meta
        # while keeping data to restore in and out positions
        strip = seq.active_strip
        sin = strip.frame_start + strip.frame_offset_start
        sout = sin + strip.frame_final_duration
        
        borrarin=False
        borrarout=False
        original_in = 0
        original_out = 0

        if "IN" in markers:
            original_in = markers["IN"].frame
            markers["IN"].frame = sin
        else:
            mark=markers.new(name="IN")
            mark.frame=sin
            borrarin=True

        if "OUT" in markers:
            original_out = markers["OUT"].frame
            markers["OUT"].frame=sout
        else:
            mark= markers.new(name="OUT")
            mark.frame=sout
            borrarout=True

        
        # here starts the operator...
        
        #get all META from selected strips
        strips=[]
        for i in context.selected_editable_sequences:
            if i.type == "META":
                strips.append(i) 
        
        for meta in strips:
            # deselect all strips 
            for i in strips:
                i.select = False

            print("### vuelta")

            #make active current meta
            meta.select = True
            seq.active_strip = meta
            bpy.ops.sequencer.reload()

            #set in and out to meta
            sin = meta.frame_start + meta.frame_offset_start
            sout = sin + meta.frame_final_duration
            print("meta: ", sin, sout)

            #grab meta content
            newstrips = []
            for i in meta.sequences:
                newstrips.append(i)
            
            #separate meta
            bpy.ops.sequencer.meta_separate()
            bpy.ops.sequencer.reload()
            #
            rmlist=[]
            for j in newstrips:
                j.select = False
            for i in newstrips:
                print(i)
                i.select = True
                remove = functions.triminout(i,sin,sout)
                if remove == True:
                    rmlist.append(i)
                i.select=False
        for i in rmlist:
            seq.sequences.remove(i)        

        bpy.ops.sequencer.reload()

        #restore original IN and OUT values
        if borrarin:
            markers.remove(markers['IN'])
        else:
            markers["IN"].frame = original_in
        if borrarout:
            markers.remove(markers['OUT'])
        else:
            markers["OUT"].frame = original_out
        scn.update()
    

        return {'FINISHED'}

class OBJECT_OT_Extrasnap(bpy.types.Operator):  #Operator paste source in/out
    bl_label = "extrasnap"
    bl_idname = "sequencerextra.extrasnap"
    bl_description = "snap the right, center or left of the strip to current frame"

    # align: 0 = left snap, 1 = center snap, 2= right snap
    align = IntProperty(
        name='align',
        min=0, max=2,
        default=1)

    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn and scn.sequence_editor:
            return scn.sequence_editor.active_strip
        else:
            return False

    def execute(self, context):
        scene=bpy.context.scene
        bpy.ops.sequencer.snap(frame=scene.frame_current)

        if self.align != 0:
            strips = context.selected_editable_sequences
            for strip in strips:
                if self.align == 1: #center snap
                    strip.frame_start-=strip.frame_final_duration/2
                else:               #right snap
                    strip.frame_start-=strip.frame_final_duration

        return {'FINISHED'}

class OBJECT_OT_Extrahandles(bpy.types.Operator):  #Operator paste source in/out
    bl_label = "extrahandles"
    bl_idname = "sequencerextra.extrahandles"
    bl_description = "snap the right, center or left of the strip to current frame"

    # side: 0 = left , 1 = both, 2= right
    side = IntProperty(
        name='side',
        min=0, max=2,
        default=1)

    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn and scn.sequence_editor:
            return scn.sequence_editor.active_strip
        else:
            return False

    def execute(self, context):
        scene=bpy.context.scene
        strips = context.selected_editable_sequences
        
        resetLeft = False
        resetRight = False
        changelistLeft = []
        changelistRight = []
        for strip in strips:
            if self.side == 0 or self.side == 1: 
                if strip.select_left_handle: 
                    resetLeft = True
                    changelistLeft.append(strip)
            if self.side == 1 or self.side == 2:
                if strip.select_right_handle: 
                    resetRight = True
                    changelistRight.append(strip)
        if len(changelistLeft) == len(strips):
            resetLeft = False
        if len(changelistRight) == len(strips):
            resetRight = False 
        if ((len(changelistRight) != len(strips)) \
            or (len(changelistRight) != len(strips))) \
            and self.side == 1:
            resetLeft = True
            resetRight = True    

        for strip in strips:
            if resetLeft:
                strip.select_left_handle = False
            if self.side == 0 or self.side == 1:
                print("uno", self.side, resetLeft, resetRight)
                if strip.select_left_handle:
                    strip.select_left_handle = False
                else:
                    strip.select_left_handle = True
            if resetRight:
                strip.select_right_handle = False
            if self.side == 1 or self.side == 2:
                print("otro", self.side, resetLeft, resetRight)
                if strip.select_right_handle:
                    strip.select_right_handle = False
                else:
                    strip.select_right_handle = True
               
        return {'FINISHED'}

#-----------------------------------------------------------------------------------------------------



class Jumptocut(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Jump to Cut"

    @staticmethod
    def has_sequencer(context):
        return (context.space_data.view_type\
        in {'SEQUENCER'})

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        preferences = bpy.context.user_preferences
        prefs = preferences.addons['sequencer_extra_actions'].preferences
        if scn and scn.sequence_editor:
            if prefs.use_jumptocut:
                return True
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="IPO_BOUNCE")

    def draw(self, context):
        
        preferences = bpy.context.user_preferences
        prefs = preferences.addons['sequencer_extra_actions'].preferences
        

        layout = self.layout

        row=layout.row(align=True)
        split=row.split()
        colR1 = split.column()
        row1=colR1.row(align=True)
        row1.operator("sequencerextra.jumptocut", icon="PLAY_REVERSE", text="cut").next=False
        row1.operator("sequencerextra.jumptocut", icon='PLAY', text="cut").next=True
        colR2 = split.column()
        row2=colR2.row(align=True)
        row2.operator("screen.marker_jump", icon="TRIA_LEFT", text="marker").next=False
        row2.operator("screen.marker_jump", icon='TRIA_RIGHT', text="marker").next=True

        row=layout.row(align=True)
        split=row.split()
        colR1 = split.column()
        row1=colR1.row(align=True)
        row1.operator("sequencerextra.sourcein", icon="MARKER_HLT", text="set IN")
        row1.operator("sequencerextra.sourceout", icon='MARKER_HLT', text="set OUT")
        colR2 = split.column()
        split=colR2.split(percentage=0.5)
        colR3 = split.column()
        colR4 = split.column()
        colR3.operator("sequencerextra.setinout", icon="ARROW_LEFTRIGHT", text="selected")
        colR4.operator("sequencerextra.triminout", icon="FULLSCREEN_EXIT", text="trim")
        
        row=layout.row(align=True)
        split=row.split(percentage=0.5)
        colR1 = split.column()
        sin=100
        sout=200
        row1=colR1.row(align=True)
        #row1.prop(prefs, "in_marker")
        #row1.prop(prefs, "out_marker")

        colR2 = split.column()
        row1=colR2.row(align=True)
        row1.operator("sequencerextra.metacopy", icon="COPYDOWN", text="meta")
        row1.operator("sequencerextra.metapaste", icon='PASTEDOWN', text="& snap")

        row=layout.row(align=True)
        split=row.split(percentage=0.5)
        colR1 = split.column()
        colR1.operator('sequencerextra.navigateup', icon='FILE_PARENT')
        colR2 = split.column()
        colR2.operator('sequencerextra.meta_separate_trim', text='unMeta & Trim', icon='ALIGN')
        

        row=layout.row(align=True)
        row.operator("sequencerextra.setstartend", icon="PREVIEW_RANGE", text="IN/OUT")
        row.operator('timeextra.trimtimelinetoselection', text='Selection', icon='PREVIEW_RANGE')
        row.operator('timeextra.trimtimeline', text='Content', icon='PREVIEW_RANGE')

        row=layout.row(align=True)
        row.operator('sequencerextra.extrasnap', text='left', icon='SNAP_ON').align=0
        row.operator('sequencerextra.extrasnap', text='center', icon='SNAP_ON').align=1
        row.operator('sequencerextra.extrasnap', text='right', icon='SNAP_ON').align=2

        row=layout.row(align=True)
        row.operator('sequencerextra.extrahandles', text='left H', icon='TRIA_LEFT').side=0
        row.operator('sequencerextra.extrahandles', text='both H', icon='PMARKER').side=1
        row.operator('sequencerextra.extrahandles', text='right H', icon='TRIA_RIGHT').side=2
