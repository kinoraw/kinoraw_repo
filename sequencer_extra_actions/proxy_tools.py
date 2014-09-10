import bpy, os
from bpy.props import IntProperty, StringProperty, BoolProperty
import subprocess

from . import functions


proxy_qualities = [  ( "1", "25%", "" ), ( "2", "50%", "" ),
                    ( "3", "75%", "" ), ( "4", "100%", "" )]
                    
# TODO
# generate megarender.sh
#  ls *.sh | parallel -j 8 sh {}
#





# functions


def create_proxy(strip, size, res):
    # calculate proxy resolution
    div = 4/size
    newres = (int(int(res[0])/div), int(int(res[1])/div))

    preferences = bpy.context.user_preferences
    proxy_dir = preferences.addons['sequencer_extra_actions'].preferences.proxy_dir
    scripts = preferences.addons['sequencer_extra_actions'].preferences.proxy_scripts

    functions.create_folder(proxy_dir)

    if scripts:
        commands = []

    # get filename
    if strip.type == "MOVIE":
        filename = bpy.path.abspath(strip.filepath)
        proxysuffix = proxy_qualities[size-1][1].split("%")[0]
        proxy_dir = bpy.path.abspath(proxy_dir)
        newfilename = os.path.join(proxy_dir,filename.rpartition("/")[2])
        fileoutput = newfilename.rpartition(".")[0]+"-"+proxysuffix+".avi"

        command = '''ffmpeg -i {} -vcodec mjpeg -qscale 1 -s {}x{} -y {}'''

        command = command.format(filename, newres[0], newres[1], fileoutput)
        #print(command)

        if scripts:
            commands.append(command)
        else:
            # check for existing file
            if not os.path.isfile(fileoutput):
                subprocess.call(command, shell=True)
            else:
                print("ya existe")

        # set up proxy settings
        strip.use_proxy = True
        strip.use_proxy_custom_file = True
        strip.proxy.filepath = bpy.path.relpath(fileoutput)
        if (proxysuffix == "25"):
            strip.proxy.build_25 = True
        if (proxysuffix == "50"):
            strip.proxy.build_50 = True
        if (proxysuffix == "75"):
            strip.proxy.build_75 = True
        if (proxysuffix == "100"):
            strip.proxy.build_100 = True

    if scripts:
        return commands
    else:
        return None


def create_proxy_scripts(scripts_dir, commands, strip_name = None):

    functions.create_folder(bpy.path.abspath(scripts_dir))

    for i in commands:
        #print(i)
        filename = "{}/proxy_script_{}.sh".format(scripts_dir, strip_name)
        text_file = open(bpy.path.abspath(filename), "w")
        #print(filename)
        text_file.write(i)
        text_file.close()



# classes

class CreateProxyOperator(bpy.types.Operator):
    """ Use ffmpeg to create a proxy from video and setup proxies \
    for selected strip"""
    bl_idname = "sequencer.create_proxy_operator"
    bl_label = " Create proxy"

    size = IntProperty(
    name='proxysize',
    default=1)
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        if scn and scn.sequence_editor and scn.sequence_editor.active_strip:
            return strip.type in ('MOVIE')
        else:
            return False

    def execute(self, context):

        preferences = bpy.context.user_preferences
        proxy_dir = preferences.addons['sequencer_extra_actions'].preferences.proxy_dir
        scripts = preferences.addons['sequencer_extra_actions'].preferences.proxy_scripts
        proxy_scripts_path = preferences.addons['sequencer_extra_actions'].preferences.proxy_scripts_path
        for strip in context.selected_editable_sequences:

            # get resolution from active strip
            bpy.ops.sequencerextra.read_exif()
            sce = context.scene
            try:
                res = sce['metadata'][0]['Composite:ImageSize'].split("x")
            except:
                res=(sce.render.resolution_x, sce.render.resolution_y)
                #print(res)

            commands = create_proxy(strip, self.size, res)

            if commands == None:
                # Update scene
                context.scene.update()
                newstrip = context.scene.sequence_editor.active_strip

                # deselect all other strips
                for i in context.selected_editable_sequences:
                    if i.name != newstrip.name:
                        i.select=False

                # Update scene
                context.scene.update()
            else:
                create_proxy_scripts(proxy_scripts_path, commands, strip.name)


        return {'FINISHED'}


class CreateProxyToolPanel(bpy.types.Panel):
    """  """
    bl_label = "Proxy Tools"
    bl_idname = "OBJECT_PT_ProxyTool"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    @staticmethod
    def has_sequencer(context):
        return (context.space_data.view_type\
        in {'SEQUENCER', 'SEQUENCER_PREVIEW'})

    @classmethod
    def poll(self, context):
        strip = functions.act_strip(context)
        scn = context.scene
        preferences = bpy.context.user_preferences
        prefs = preferences.addons['sequencer_extra_actions'].preferences
        if scn and scn.sequence_editor and scn.sequence_editor.active_strip:
            if prefs.use_proxy_tools:
                return strip.type in ('MOVIE')
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="IPO_BOUNCE")

    def draw(self, context):

        preferences = bpy.context.user_preferences
        prefs = preferences.addons['sequencer_extra_actions'].preferences

        layout = self.layout
        layout.prop(prefs, "proxy_dir", text="path for proxies")

        layout = self.layout
        layout.label("create and import proxy from clip:")
        row = layout.row(align=True)

        for i in range(4):
            proxysuffix = proxy_qualities[i][1]
            row.operator("sequencer.create_proxy_operator",text=proxysuffix).size=i+1

        layout = self.layout
        layout.prop(prefs, "proxy_scripts")

        if prefs.proxy_scripts:
            layout = self.layout
            layout.prop(prefs, "proxy_scripts_path", text="path for scripts")
