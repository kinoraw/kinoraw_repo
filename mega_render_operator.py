# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Mega Render",
    "author": "Carlos Padial, Ferhoyo",
    "version": (0, 12),
    "blender": (2, 73, 0),
    "category": "Sequencer",
    "location": "Sequencer",
    "description": "mega render operator with log file",
    "warning": "",
    "wiki_url": "http://kinoraw.net",
    "tracker_url": "http://kinoraw.net",
    "support": "COMMUNITY"}



import bpy, os
from bpy.props import IntProperty, StringProperty

import os, subprocess


def generate_parts(s_frame, e_frame, number_of_threads):
    #lista de tramos que se han de renderizar
    tramos = []
    counter = s_frame

    duration = e_frame - s_frame

    part = int(duration/number_of_threads)

    print("-------------------------")
    
    for i in range(number_of_threads):
        if i < number_of_threads-1:
            #print(counter, counter+part, counter+part-counter)
            tramo = (counter, counter+part-1)
        else:
            #print(counter, e_frame, e_frame-counter)
            tramo = (counter, e_frame)
        counter = counter+part
        tramos.append(tramo)
        print("{} a {} ({} frames)".format(tramo[0],tramo[1], tramo[1]-tramo[0]+1))
    #print(tramos)

    return tramos


def generate_scripts():
    

    return {'FINISHED'}



class GenerateMegaRenderOperator(bpy.types.Operator):
    """ ______________ """
    bl_idname = "sequencer.generatemegarenderoperator"
    bl_label = "generate mega render"

    @classmethod
    def poll(self, context):
        return context.scene.sequence_editor

    def execute(self, context):
        
        preferences = context.user_preferences
        prefs = preferences.addons['mega_render_operator'].preferences

        blenderpath = prefs.blenderpath
        scriptfilename = bpy.path.abspath(prefs.scriptfilename)
        number_of_threads = prefs.number_of_threads

        # current .blend filename
        blendfile = bpy.data.filepath

        sce = context.scene
        s_frame = sce.frame_start
        e_frame = sce.frame_end
        duration = e_frame - s_frame
        part = int(duration / number_of_threads)

        tramos = generate_parts(s_frame, e_frame, number_of_threads)

        #generate_scripts(tra, blenderpath, blendfile, sce, scriptfilename)

        #tramos, blendfile, sce, scriptfilename

        # generate the script
        log_file = bpy.path.abspath("//render.log")
        text_file = open(bpy.path.abspath(scriptfilename), "w")
        text_file.write("#!/bin/bash\necho \"$(date +'%a %d %b %Y - %H:%M:%S'):\" > {}".format(log_file))
        for i, j in enumerate(tramos):
            text_file.write(("\n(\necho '#Rendering part {}'\nSTART_RENDER=$(date +'%s')\n").format(i))
            text_file.write("RESULT=$({} {} -b -S {} -s {} -e {} -a 2>&1".format(blenderpath, blendfile, sce.name, j[0], j[1]))
            text_file.write(" | grep 'Saved\|Append\|not an anim\|unknown fileformat') \nEND_RENDER=$(date +'%s')\nRENDERING_SECS=$(($END_RENDER-$START_RENDER))\nLINEAS=$(echo \"$RESULT\" | wc -l)\n")
            text_file.write("if [ $LINEAS -eq {} ];then\n".format(j[1]-j[0]+1))
            text_file.write("   echo \"#Finished frame {} to {} in $(printf '%dh:%dm:%ds' $(($RENDERING_SECS/3600)) $(($RENDERING_SECS%3600/60)) $(($RENDERING_SECS%60)))\"\nelse\n".format(j[0],j[1])) 
            text_file.write("   RESULT=$(echo \"$RESULT\" | sed -n '/\\(unknown fileformat\\|not an anim\\)/{N;p;}')\n")
            text_file.write("   RESULT=$(echo \"$RESULT\" | sed 's/Saved/Error on rendered image/;s/Append/Error on/;s/Time.*//;s/.*unknown fileformat/unknown fileformat/')\n")   
            text_file.write("   echo \"$RESULT\" | sed '/Error/G' >> {}\n".format(log_file))   

            text_file.write("   echo \"#One or more errors were found\\nplease see render.log for details\"\nfi\n )")
            text_file.write("| zenity --progress --pulsate --no-cancel --title='Part {}'".format(i))

            if i < len(tramos)-1:
                print(i, len(tramos)-1)
                text_file.write(" & \n")
        text_file.close()

        print("script done")        
       
        return {'FINISHED'}


class LaunchMegaRenderOperator(bpy.types.Operator):
    """ ______________ """
    bl_idname = "sequencer.launchmegarenderoperator"
    bl_label = "launch mega render"

    @classmethod
    def poll(self, context):
        preferences = context.user_preferences
        prefs = preferences.addons['mega_render_operator'].preferences
        return os.path.isfile(bpy.path.abspath(prefs.scriptfilename))

    def execute(self, context):
        preferences = context.user_preferences
        prefs = preferences.addons['mega_render_operator'].preferences
        scriptfilename = bpy.path.abspath(prefs.scriptfilename)
        command = "sh "+scriptfilename
        print("ejecutando {}".format(scriptfilename))
        subprocess.call(command,shell=True)

        return {'FINISHED'}


class MegaRenderPanel(bpy.types.Panel):
    """-_-_-"""
    bl_label = "Mega Render VSE"
    bl_idname = "OBJECT_PTMultiThread"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    
    @classmethod
    def poll(self, context):
        return context.scene.sequence_editor

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="FORCE_WIND")

    def draw(self, context):

        preferences = context.user_preferences
        prefs = preferences.addons['mega_render_operator'].preferences
        number_of_threads = prefs.number_of_threads

        layout = self.layout
        row = layout.row(align=True)
        row.label("______ megarender :)")    
        row.prop(prefs, "number_of_threads", text="threads")
        layout = self.layout
        layout.operator("sequencer.generatemegarenderoperator", text="generate")
        layout.operator("sequencer.launchmegarenderoperator", text="launch render")
        


class MegaRenderAddon(bpy.types.AddonPreferences):
    bl_idname = "mega_render_operator"
    bl_option = {'REGISTER'}

    blenderpath = StringProperty(
        name="blender executable path",
        description="blender executable path",
        default=bpy.app.binary_path)

    scriptfilename = StringProperty(
        name="script filename",
        description="script filename",
        default="//megarender.sh")

    number_of_threads = IntProperty(
        name="number of threads",
        description="number of threads",
        default=8,
        min = 1, max = 64)

    def draw(self, context):   
        layout = self.layout
        layout.prop(self, "blenderpath")
        layout.prop(self, "scriptfilename")
        layout.prop(self, "number_of_threads")
            

def register():
    bpy.utils.register_class(MegaRenderAddon)
    bpy.utils.register_class(LaunchMegaRenderOperator)
    bpy.utils.register_class(GenerateMegaRenderOperator)
    bpy.utils.register_class(MegaRenderPanel)
  

def unregister():
    bpy.utils.unregister_class(LaunchMegaRenderOperator)
    bpy.utils.unregister_class(GenerateMegaRenderOperator)
    bpy.utils.unregister_class(MegaRenderPanel)
    bpy.utils.unregister_class(MegaRenderAddon)


if __name__ == "__main__":
    register()