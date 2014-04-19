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

bl_info = {
    "name": "Extra Sequencer Actions",
    "author": "Turi Scandurra, Carlos Padial",
    "version": (3, 10),
    "blender": (2, 70, 0),
    "category": "Sequencer",
    "location": "Sequencer",
    "description": "Collection of extra operators to manipulate VSE strips",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
        "Scripts/Sequencer/Extra_Sequencer_Actions",
    "tracker_url": "https://developer.blender.org/T32532",
    "support": "COMMUNITY"}


if "bpy" in locals():
    import imp
    imp.reload(operators_extra_actions)
    imp.reload(audio_tools)
    imp.reload(proxy_tools)
    imp.reload(recursive_loader)
    imp.reload(jumptocut)
    imp.reload(eco)
    imp.reload(ui)
else:
    from . import operators_extra_actions
    from . import audio_tools
    from . import proxy_tools
    from . import recursive_loader
    from . import jumptocut
    from . import eco
    from . import ui

import bpy
import os.path
from bpy.types import Menu
from bpy.types import Header

from bpy.props import IntProperty, StringProperty, BoolProperty


class ProxyAddon(bpy.types.AddonPreferences):
    bl_idname = "sequencer_extra_actions"
    bl_option = {'REGISTER'}

    # Proxy Tools

    proxy_dir = StringProperty(
    name='directory to store proxies',
    default="//proxies/")

    proxy_scripts_path = StringProperty(
    name='directory to store proxy scripts',
    default="//proxy_scripts/")

    proxy_scripts = BoolProperty(
    name='generate ffmpeg scritps',
    default=False)

    # Audio Tools
    
    audio_dir = StringProperty(
    name='path to store extracted audio',
    default="//audio/")

    audio_scripts_path = StringProperty(
    name='path to store audio scripts',
    default="//audio_scripts/")

    audio_scripts = BoolProperty(
    name='generate ffmpeg scritps',
    default=False)

    # external links

    audio_use_external_links = BoolProperty(
        name='use external audio linked to movie strips',
        default=False)

    audio_external_filename = StringProperty(
    name='file to store info about linked audio',
    default="//external_audio_sync_info.txt")

    # eco

    eco_value = IntProperty(
        name = 'number of echoes',
        default = 5,
        min = 1, max = 25)

    eco_offset = IntProperty(
        name = 'Echo Offset',
        default = 1,
        min = -25000, max = 25000)

    eco_use_add_blend_mode = BoolProperty(
        name = 'use_add_blend_mode',
        default = False)

    def draw(self, context):

        # PROXY

        layout = self.layout
        layout.label("Proxy Tools default parameters")

        layout = self.layout
        layout.prop(self, "proxy_dir")

        layout = self.layout
        layout.prop(self, "proxy_scripts")

        if self.proxy_scripts:
            layout = self.layout
            layout.prop(self, "proxy_scripts_path")

        # AUDIO

        layout = self.layout
        layout.label("Audio Tools default parameters")
        
        layout = self.layout
        layout.prop(self, "audio_dir", text="path for audio files")


        if self.audio_scripts:
            layout = self.layout
            layout.prop(self, "audio_scripts_path", text="path for audio scripts")

        layout = self.layout
        layout.prop(self, "audio_use_external_links", text="external audio sync")

        layout = self.layout
        layout.prop(self, "audio_use_external_links")

        if self.audio_use_external_links:
            layout = self.layout
            layout.prop(self, "audio_external_filename")

        # ECO

        layout = self.layout
        layout.label("Eco default parameters")

        layout = self.layout
        layout.prop(self, "eco_value")

        layout = self.layout
        layout.prop(self, "eco_use_add_blend_mode")

        layout = self.layout
        layout.prop(self, "eco_offset")









# Registration
def register():
    bpy.utils.register_module(__name__)

    # Append menu entries
    bpy.types.SEQUENCER_MT_add.prepend(ui.sequencer_add_menu_func)
    bpy.types.SEQUENCER_MT_select.prepend(ui.sequencer_select_menu_func)
    bpy.types.SEQUENCER_MT_strip.prepend(ui.sequencer_strip_menu_func)
    bpy.types.SEQUENCER_HT_header.append(ui.sequencer_header_func)
    bpy.types.CLIP_HT_header.append(ui.clip_header_func)
    bpy.types.CLIP_MT_clip.prepend(ui.clip_clip_menu_func)
    bpy.types.TIME_MT_frame.prepend(ui.time_frame_menu_func)
    bpy.types.TIME_HT_header.append(ui.time_header_func)

    # Add keyboard shortcut configuration
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Frames')
    kmi = km.keymap_items.new('screenextra.frame_skip',
    'RIGHT_ARROW', 'PRESS', ctrl=True, shift=True)
    kmi.properties.back = False
    kmi = km.keymap_items.new('screenextra.frame_skip',
    'LEFT_ARROW', 'PRESS', ctrl=True, shift=True)
    kmi.properties.back = True

    # jumptocut shortcuts
    km = kc.keymaps.new(name='Jumptocut')
    kmi = km.keymap_items.new('sequencer.jumpprev',
    'Q', 'PRESS', ctrl=False, shift=False)
    kmi = km.keymap_items.new('sequencer.jumpnext',
    'W', 'PRESS', ctrl=False, shift=False)

    km = kc.keymaps.new(name='Jumptomark')
    kmi = km.keymap_items.new('sequencer.markprev',
    'Q', 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new('sequencer.marknext',
    'W', 'PRESS', ctrl=True, shift=True)



def unregister():
    bpy.utils.unregister_module(__name__)

    #  Remove menu entries
    bpy.types.SEQUENCER_MT_add.remove(ui.sequencer_add_menu_func)
    bpy.types.SEQUENCER_MT_select.remove(ui.sequencer_select_menu_func)
    bpy.types.SEQUENCER_MT_strip.remove(ui.sequencer_strip_menu_func)
    bpy.types.SEQUENCER_HT_header.remove(ui.sequencer_header_func)
    bpy.types.CLIP_HT_header.remove(ui.clip_header_func)
    bpy.types.CLIP_MT_clip.remove(ui.clip_clip_menu_func)
    bpy.types.TIME_MT_frame.remove(ui.time_frame_menu_func)
    bpy.types.TIME_HT_header.remove(ui.time_header_func)

    #  Remove keyboard shortcut configuration
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps['Frames']
    km.keymap_items.remove(km.keymap_items['screenextra.frame_skip'])
    km.keymap_items.remove(km.keymap_items['screenextra.frame_skip'])

    km = kc.keymaps['Jumptocut']
    km.keymap_items.remove(km.keymap_items['sequencer.jumpprev'])
    km.keymap_items.remove(km.keymap_items['sequencer.jumpnext'])

    km = kc.keymaps['Jumptomark']
    km.keymap_items.remove(km.keymap_items['sequencer.markprev'])
    km.keymap_items.remove(km.keymap_items['sequencer.marknext'])


if __name__ == '__main__':
    register()
