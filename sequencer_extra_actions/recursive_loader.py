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

import random
import math
import os, sys

from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from bpy.props import StringProperty

from . import functions
from . import exiftool

        
# RECURSIVE LOADER

# TODO: add proxy options as addon properties

class Sequencer_Extra_RecursiveLoader(bpy.types.Operator):
    bl_idname = "sequencerextra.recursiveload"
    bl_label = "recursive load"
    bl_options = {'REGISTER', 'UNDO'}
    
    recursive = BoolProperty(
        name='recursive',
        description='Load in recursive folders',
        default=False)
        
    recursive_select_by_extension = BoolProperty(
        name='select by extension',
        description='Load only clips with selected extension',
        default=False)
        
    ext = EnumProperty(
        items=functions.movieextdict,
        name="extension",
        default="3")
        
    recursive_proxies = BoolProperty(
        name='use proxies',
        description='Load in recursive folders',
        default=False)
    build_25 = BoolProperty(name='default_build_25',
        description='build_25',
        default=True)
    build_50 = BoolProperty(name='default_build_50',
        description='build_50',
        default=False)
    build_75 = BoolProperty(name='default_build_75',
        description='build_75',
        default=False)
    build_100 = BoolProperty(name='default_build_100',
        description='build_100',
        default=False)
    proxy_suffix = StringProperty(
        name='proxy suffix',
        description='proxy filename suffix',
        default="-25")
    proxy_extension = StringProperty(
        name='proxy extension',
        description='proxy extension',
        default=".mkv")
    proxy_path = StringProperty(
        name='proxy path',
        description='proxy path',
        default="")
    
       
    
    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            return (scn.sequence_editor)
        else:
            return False
        
    def invoke(self, context, event):
        scn = context.scene
        try:
            self.build_25 = scn.default_build_25
            self.build_50 = scn.default_build_50
            self.build_75 = scn.default_build_75
            self.build_100 = scn.default_build_100
            self.proxy_suffix = scn.default_proxy_suffix
            self.proxy_extension = scn.default_proxy_extension
            self.proxy_path = scn.default_proxy_path
            self.recursive = scn.default_recursive
            self.recursive_select_by_extension = scn.default_recursive_select_by_extension
            self.recursive_proxies = scn.default_recursive_proxies
            self.ext = scn.default_ext 
        except AttributeError:
            functions.initSceneProperties(context, scn)
            self.build_25 = scn.default_build_25
            self.build_50 = scn.default_build_50
            self.build_75 = scn.default_build_75
            self.build_100 = scn.default_build_100
            self.proxy_suffix = scn.default_proxy_suffix
            self.proxy_extension = scn.default_proxy_extension
            self.proxy_path = scn.default_proxy_path
            self.recursive = scn.default_recursive
            self.recursive_select_by_extension = scn.default_recursive_select_by_extension
            self.recursive_proxies = scn.default_recursive_proxies
            self.ext = scn.default_ext 
                
        return context.window_manager.invoke_props_dialog(self)  
        
    def loader(self, context, filelist):
        scn = context.scene
        if filelist:
            for i in filelist:
                functions.setpathinbrowser(i[0], i[1])
                try:
                    if self.recursive_proxies:
                        bpy.ops.sequencerextra.placefromfilebrowserproxy(
                            proxy_suffix=self.proxy_suffix,
                            proxy_extension=self.proxy_extension,
                            proxy_path=self.proxy_path,
                            build_25=self.build_25,
                            build_50=self.build_50,
                            build_75=self.build_75,
                            build_100=self.build_100)
                    else:
                        bpy.ops.sequencerextra.placefromfilebrowser()
                except:
                    print("Error loading file (recursive loader error): ", i[1])
                    functions.add_marker(context, i[1])
                    self.report({'ERROR_INVALID_INPUT'}, 'Error loading file ')
                    pass


    def execute(self, context):
        scn = context.scene
        #functions.initSceneProperties(context, scn)
        if self.recursive == True:
            #recursive
            #print(functions.sortlist(functions.recursive(\
            #context, self.recursive_select_by_extension, self.ext)))
            self.loader(context, functions.sortlist(\
            functions.recursive(context, self.recursive_select_by_extension,\
            self.ext)))
        else:
            #non recursive
            #print(functions.sortlist(functions.onefolder(\
            #context, self.recursive_select_by_extension, self.ext)))
            self.loader(context, functions.sortlist(functions.onefolder(\
            context, self.recursive_select_by_extension, self.ext)))
        try:   
            scn.default_build_25 = self.build_25
            scn.default_build_50 = self.build_50
            scn.default_build_75 = self.build_75
            scn.default_build_100 = self.build_100 
            scn.default_proxy_suffix = self.proxy_suffix 
            scn.default_proxy_extension = self.proxy_extension 
            scn.default_proxy_path = self.proxy_path 
            scn.default_recursive = self.recursive 
            scn.default_recursive_select_by_extension = self.recursive_select_by_extension 
            scn.default_recursive_proxies = self.recursive_proxies
            scn.default_ext = self.ext 
        except AttributeError:
            functions.initSceneProperties(context, scn)
            self.build_25 = scn.default_build_25
            self.build_50 = scn.default_build_50
            self.build_75 = scn.default_build_75
            self.build_100 = scn.default_build_100
            self.proxy_suffix = scn.default_proxy_suffix
            self.proxy_extension = scn.default_proxy_extension
            self.proxy_path = scn.default_proxy_path
            self.recursive = scn.default_recursive
            self.recursive_select_by_extension = scn.default_recursive_select_by_extension
            self.recursive_proxies = scn.default_recursive_proxies
            self.ext = scn.default_ext
            
        return {'FINISHED'}


# READ EXIF DATA
class Sequencer_Extra_ReadExifData(bpy.types.Operator):
    # load exifdata from strip to scene['metadata'] property
    bl_label = 'Read EXIF Data'
    bl_idname = 'sequencerextra.read_exif'
    bl_description = 'Load exifdata from strip to metadata property in scene'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn and scn.sequence_editor and scn.sequence_editor.active_strip:
            return strip.type in ('IMAGE', 'MOVIE')
        else:
            return False


    def execute(self, context):
        try:
            exiftool.ExifTool().start()
        except:
            self.report({'ERROR_INVALID_INPUT'},
            'exiftool not found in PATH')
            return {'CANCELLED'}

        def getexifdata(strip):
            def getlist(lista):
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if "." + f.rpartition(".")[2].lower() \
                            in functions.imb_ext_image:
                            lista.append(f)
                        #if "."+f.rpartition(".")[2] in imb_ext_movie:
                        #    lista.append(f)
                strip.elements
                lista.sort()
                return lista

            def getexifvalues(lista):
                metadata = []
                with exiftool.ExifTool() as et:
                    try:
                        metadata = et.get_metadata_batch(lista)
                    except UnicodeDecodeError as Err:
                        print(Err)
                return metadata
            if strip.type == "IMAGE":
                path = bpy.path.abspath(strip.directory)
            if strip.type == "MOVIE":
                path = bpy.path.abspath(strip.filepath.rpartition("/")[0])
            os.chdir(path)
            #get a list of files
            lista = []
            for i in strip.elements:
                lista.append(i.filename)
            return getexifvalues(lista)

        sce = bpy.context.scene
        frame = sce.frame_current
        text = bpy.context.active_object
        strip = context.scene.sequence_editor.active_strip
        sce['metadata'] = getexifdata(strip)
        return {'FINISHED'}


class ExifInfoPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    """ TODO: fix poll to hide when unuseful"""
    bl_label = "EXIF Info Panel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    @staticmethod
    def has_sequencer(context):
        return (context.space_data.view_type\
        in {'SEQUENCER'})

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn and scn.sequence_editor and scn.sequence_editor.active_strip:
            return strip.type in ('MOVIE')
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="NLA")

    def draw(self, context):
        layout = self.layout
        sce = context.scene
        row = layout.row()
        row.operator("sequencerextra.read_exif")
        row = layout.row()
        row.label(text="Exif Data", icon='RENDER_REGION')
        row = layout.row()

        try:
            strip = context.scene.sequence_editor.active_strip

            f = strip.frame_start
            frame = sce.frame_current
            try:
                if len(sce['metadata']) == 1:
                    for d in sce['metadata'][0]:
                        split = layout.split(percentage=0.5)
                        col = split.column()
                        row = col.row()
                        col.label(text=d)
                        col = split.column()
                        col.label(str(sce['metadata'][0][d]))
                else:
                    for d in sce['metadata'][frame - f]:
                        split = layout.split(percentage=0.5)
                        col = split.column()
                        row = col.row()
                        col.label(text=d)
                        col = split.column()
                        col.label(str(sce['metadata'][frame - f][d]))
            except KeyError:
                pass
        except AttributeError:
            pass