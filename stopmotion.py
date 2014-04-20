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


"""
README

this script only works with gnome linux systems...

it works by launching some command line applications from the blender gui.
If you don't have some of the following programs installed, the associated
button probably will give you an error message...


gstreamer-0.10
guvcview
mencoder

--------


"""


bl_info = {
    "name": "Stop Motion Tools",
    "author": "Carlos Padial",
    "version": (0, 1),
    "blender": (2, 70, 0),
    "category": "Sequencer",
    "location": "Sequencer",
    "description": "Collection of extra operators to manipulate VSE strips",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
        "Scripts/Sequencer/Extra_Sequencer_Actions",
    "tracker_url": "https://developer.blender.org/T32532",
    "support": "COMMUNITY"}


import bpy, os, sys, subprocess, time

from xml.dom.minidom import parseString

from bpy.props import IntProperty, BoolProperty, StringProperty



proxy_qualities = [  ( "1", "25%", "" ), ( "2", "50%", "" ), \
                    ( "3", "75%", "" ), ( "4", "100%", "" )]



# functions  (from sequencer_extra_tools/functions.py)

def setpathinbrowser(path, file):
    '''
    set path and file in the filebrowser
    '''
    scn = bpy.context.scene
    for a in bpy.context.window.screen.areas:
        if a.type == 'FILE_BROWSER':
            params = a.spaces[0].params
            break
    try:
        params
    except UnboundLocalError:
        #print("no browser")
        self.report({'ERROR_INVALID_INPUT'}, 'No visible File Browser')
        return {'CANCELLED'}

    params.directory = path
    params.filename = file
    return path, params


def create_folder(path):
    if not os.path.isdir(bpy.path.abspath(path)):
        folder = bpy.path.abspath(path)
        command = "mkdir "+folder
        subprocess.call(command,shell=True)


def triminout(strip, sin, sout):
    start = strip.frame_start + strip.frame_offset_start
    end = start + strip.frame_final_duration
    if end > sin:
        if start < sin:
            strip.select_right_handle = False
            strip.select_left_handle = True
            bpy.ops.sequencer.snap(frame=sin)
            strip.select_left_handle = False
    if start < sout:
        if end > sout:
            strip.select_left_handle = False
            strip.select_right_handle = True
            bpy.ops.sequencer.snap(frame=sout)
            strip.select_right_handle = False
    return {'FINISHED'}


def act_strip(context):
    try:
        return context.scene.sequence_editor.active_strip
    except AttributeError:
        return None


def add_strip_image(infile, context, strip=None):
    f, e = os.path.splitext(infile)

    if strip:
        if strip.type == 'IMAGE':
            image_file = []
            filename = {"name": infile.rpartition("/")[2]}
            image_file.append(filename)

            f_in = strip.frame_start
            f_out = f_in + strip.frame_final_duration

            channel = strip.channel + 1

            bpy.ops.sequencer.image_strip_add(files=image_file, \
            directory=f.rpartition("/")[0], frame_start=f_in, \
            frame_end=f_out, relative_path=False, channel = channel)

            # make new strip active
            newstrip = context.scene.sequence_editor.active_strip

            # deselect all other strips
            for i in context.selected_editable_sequences:
                if i.name != newstrip.name:
                    i.select=False

            # Update scene
            context.scene.update()

            print(newstrip.frame_final_duration, strip.frame_final_duration)
            newstrip.frame_final_duration = strip.frame_final_duration

            triminout(newstrip, strip.frame_start + strip.frame_offset_start, \
                strip.frame_start + strip.frame_offset_start + \
                strip.frame_final_duration)

            context.scene.update()
            return

        elif strip.type == 'MOVIE':
            bpy.ops.sequencer.movie_strip_add(filepath=path, \
            frame_start=frame, relative_path=False)
        elif strip.type == 'SOUND':
            bpy.ops.sequencer.sound_strip_add(filepath=path, \
            frame_start=frame, relative_path=False)

    elif strip == None:
        image_file = []
        filename = {"name": infile.rpartition("/")[2]}
        image_file.append(filename)

        f_in = context.scene.frame_current
        f_out = f_in

        print("cargando ", filename, f_in, f_out)

        bpy.ops.sequencer.image_strip_add(files=image_file, \
        directory=f.rpartition("/")[0], frame_start=f_in, \
        frame_end=f_out, relative_path=False)

        context.scene.frame_current = f_out + 1

    return {'FINISHED'}


# more functions

def kill_gstreamer():
    print("kill\n*\n*\n")
    command = "killall -9 gst-launch-0.10"
    p = subprocess.call(command,shell=True)


# elphel functions

def getsize(size_file):

    preferences = bpy.context.user_preferences
    elphelIP = preferences.addons['stopmotion'].preferences.elphelIP

    command = "wget -q 'http://{}/parsedit.php?immediate&WOI_WIDTH&WOI_HEIGHT' -O {}"\
        .format(elphelIP, size_file)
    print(command)
    subprocess.call(command, shell=True)


def readsize(size_file):
    try:
        file = open(size_file)
        data = file.read()
        file.close()
        dom = parseString(data)
        x = dom.getElementsByTagName("WOI_WIDTH")[0].childNodes[0]
        xxx = int(x.nodeValue)
        y = dom.getElementsByTagName("WOI_HEIGHT")[0].childNodes[0]
        yyy = int(y.nodeValue)
        command = "rm " + size_file
        subprocess.call(command, shell=True)
        return xxx, yyy
    except IOError:
        pass


# elphel or webcam functions

def get_image_from_camera(context, filepath):

    preferences = bpy.context.user_preferences
    prefs = preferences.addons['stopmotion'].preferences

    if prefs.elphel_on:
   
        elphelIP = prefs.elphelIP

        # get an image from elphel, and rename it with given filepath
        command = """wget http://{}:8081/bimg"""
        command = command.format(elphelIP)
        subprocess.call(command,shell=True)
        command = "mv bimg " + filepath
        subprocess.call(command,shell=True)

    else:
        device = prefs.device
        sce = context.scene
        res = str(sce.render.resolution_x) + "x" + str(sce.render.resolution_y)

        command = """gnome-terminal -e 'gst-launch-0.10 -e v4l2src device={} ! ffmpegcolorspace ! pngenc ! filesink location={} '""".format(device, filepath)

        subprocess.call(command,shell=True)

        print("-----------------capturado: ", filepath)


    return filepath


# stop motion tools operators


class CameraControlOperator(bpy.types.Operator):
    """ show controls for elphel camera or webcam"""
    bl_idname = "sequencer.elphel_control_operator"
    bl_label = "open controls"

    def execute(self, context):

        preferences = bpy.context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences
        elphel_on = prefs.elphel_on

        if elphel_on:
            preferences = bpy.context.user_preferences
            elphelIP = preferences.addons['stopmotion'].preferences.elphelIP

            command = """gnome-terminal -e 'midori http://{}/camvc.html?reload=0'"""
            command = command.format(elphelIP)
            subprocess.call(command,shell=True)
        else:
            command = """gnome-terminal -e 'guvcview -o {}'""".format(prefs.device)
            subprocess.call(command,shell=True)

        return {'FINISHED'}


class CameraSyncResOperator(bpy.types.Operator):
    """ set render resolution in blender according to elphel camera
    configuration (webcam not working)"""
    bl_idname = "sequencer.elphel_sync_res_operator"
    bl_label = " sync resolution  "

    @staticmethod
    def has_sequencer(context):
        return (context.space_data.view_type\
        in {'SEQUENCER', 'SEQUENCER_PREVIEW'})

    @classmethod
    def poll(self, context):
        preferences = bpy.context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences
        return prefs.elphel_on
        
    def execute(self, context):

        preferences = bpy.context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences

        if prefs.elphel_on:
            size_file = os.path.join(bpy.path.abspath("//"), "size.xml")
            getsize(size_file)
            xxx, yyy = readsize(size_file)
            context.scene.render.resolution_x = xxx
            context.scene.render.resolution_y = yyy
        else:
            print("oops")
        return {'FINISHED'}




class CameraPreviewOperator(bpy.types.Operator):
    """ preview a clip from elphel or webcam"""
    bl_idname = "sequencer.elphel_preview_operator"
    bl_label = " preview video stream "

    size = IntProperty(
    name='proxysize',
    default=1)
    bl_options = {'REGISTER', 'UNDO'}

    color = IntProperty(
    name='colormode',
    default=2)
    bl_options = {'REGISTER', 'UNDO'}

    #@classmethod
    #def poll(cls, context):
    #     return context.selected_editable_sequences

    def execute(self, context):
        preferences = bpy.context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences

        kill_gstreamer()

        if prefs.elphel_on:

            elphelIP = prefs.elphelIP

            if self.color != 2:

                command = "gnome-terminal -e 'mplayer rtsp://{}:554 -vo x11 "\
                 "-zoom'".format(elphelIP)

                #command = "gnome-terminal -e 'gst-launch rtspsrc " \
                #          "location=rtsp://{}:554 latency=100 " \
                #          "! rtpjpegdepay ! jpegdec ! autovideosink'".format(
                # elphelIP)

                print (command)

            else:
                size_file = os.path.join(bpy.path.abspath("//"), "size.xml")
                getsize(size_file)
                xxx, yyy = readsize(size_file)

                div = 4/self.size

                print(self.size)

                newres = (int(xxx/div),int(yyy/div))

                location = "rtsp://{}:554".format(elphelIP)

                command = """gnome-terminal -e 'gst-launch-0.10 rtspsrc \
                    location={} latency=100 ! rtpjpegdepay ! jpegdec ! queue ! \
                    jp462bayer ! "video/x-raw-bayer, width={}, height={}, format=grbg" ! \
                    queue ! bayer2rgb2 method=1 ! ffmpegcolorspace !\
                    queue ! xvimagesink'"""

                command = command.format(location, newres[0], newres[1])

            subprocess.call(command,shell=True)

        else:
            xxx = context.scene.render.resolution_x
            yyy = context.scene.render.resolution_y

            device = prefs.device
            onion_skin = prefs.onion_skin

            if onion_skin and act_strip(context):

                strip = act_strip(context)

                path = os.path.join(strip.directory,strip.elements[0]
                .filename)

                command = """gnome-terminal --geometry=10x10 -e ' gst-launch-0.10 \
                    videomixer name=mix sink_1::alpha=0.5 sink_1::zorder=3 !\
                    ffmpegcolorspace ! xvimagesink \
                    v4l2src device={} \
                    ! "video/x-raw-yuv,width={},height={},framerate=30/1" \
                    ! ffmpegcolorspace ! mix.sink_1 \
                    filesrc location={} ! pngdec ! imagefreeze \
                    ! ffmpegcolorspace ! mix.sink_0'""".format(device, xxx, yyy, path)


            else:
                command = """gnome-terminal --geometry=10x10 -e 'gst-launch-0.10 v4l2src \
                    device={} ! "video/x-raw-yuv,width={},height={},framerate=30/1" ! autovideosink'""".format(device, xxx, yyy)

                #command = """gst-launch-0.10 v4l2src device={} ! "video/x-raw-yuv,width={},height={},framerate=30/1" ! autovideosink""".format(device, xxx, yyy)

            print (command)
            p = subprocess.call(command,shell=True)

        return {'FINISHED'}


class CameraRecordOperator(bpy.types.Operator):
    """ record a clip from elphel or webcam"""
    bl_idname = "sequencer.elphel_record_operator"
    bl_label = " capture a video "

    #@classmethod
    #def poll(cls, context):
    #     return context.selected_editable_sequences

    def execute(self, context):

        filename = str(time.time()).rpartition(".")[0]
        dir =  bpy.path.abspath("//footage_" + context.scene.name)
        path = os.path.join(dir, filename)

        create_folder(dir)

        preferences = bpy.context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences

        if prefs.elphel_on:

            elphelIP = prefs.elphelIP

            create_folder("//footage")

            size_file = os.path.join(bpy.path.abspath("//"), "size.xml")
            getsize(size_file)
            xxx, yyy = readsize(size_file)

            factor = 2

            newres = (int(xxx/factor),int(yyy/factor))

            location = "rtsp://{}:554".format(elphelIP)



            get_image_from_camera(context, path + ".jpg")

            command = """gnome-terminal -e 'gst-launch-0.10 -e rtspsrc \
                location={} latency=100 ! rtpjpegdepay  ! \
                tee name=tee1 tee1. ! queue ! matroskamux ! filesink  \
                location={}.mkv tee1. ! queue ! jpegdec ! jp462bayer ! \
                "video/x-raw-bayer,width={},height={}, format=grbg"  ! \
                queue ! bayer2rgb2 method=1 ! ffmpegcolorspace ! xvimagesink'"""

            command = command.format(location, path, newres[0], newres[1])
            
            subprocess.call(command,shell=True)

        else:
            xxx = context.scene.render.resolution_x
            yyy = context.scene.render.resolution_y

            device = prefs.device

            prefs.recording = True

            kill_gstreamer()

            #timestamp_command="""gnome-terminal -e 'gst-launch-0.10 -e v4l2src device={} ! 'video/x-raw-yuv,width={},height={},framerate=30/1' ! timeoverlay halignment=right valignment=bottom shaded-background=true ! clockoverlay halignment=left valignment=bottom text="M/D/Y:" shaded-background=true time-format="%m/%d/%Y %H:%M:%S" ! tee name=t_vid ! queue ! xvimagesink sync=false t_vid. ! queue ! videorate ! 'video/x-raw-yuv,framerate=30/1' ! theoraenc ! queue ! oggmux ! filesink location={}.ogv'"""

            command="""gnome-terminal --geometry=10x10 -e 'gst-launch-0.10 -e v4l2src device={} ! 'video/x-raw-yuv,width={},height={},framerate=30/1' ! tee name=t_vid ! queue ! xvimagesink sync=false t_vid. ! queue ! videorate ! 'video/x-raw-yuv,framerate=30/1' ! jpegenc ! queue ! avimux ! filesink location={}.avi'"""

            command = command.format(device, xxx, yyy, path)
            

            print(command)
            subprocess.call(command,shell=True)

            prefs.captured_clip = path + ".avi"
            prefs.recording = True

        return {'FINISHED'}


class CameraStopRecordOperator(bpy.types.Operator):
    """mata el gstreamer, fixea el indice y carga el clip..."""
    bl_idname = "sequencer.elphel_stop_record_operator"
    bl_label = "stop recording"

    #@classmethod
    #def poll(cls, context):
    #     return context.selected_editable_sequences

    def execute(self, context):

        try:

            preferences = bpy.context.user_preferences
            prefs = preferences.addons['stopmotion'].preferences

            if prefs.recording:

                path = prefs.captured_clip
                filename = path.rpartition(".")[0]

                kill_gstreamer()

                prefs.recording = False
                
                command1 = "mencoder -idx {} -ovc copy -oac copy -o {}_fixed.avi".format(path, filename)

                command2 = "rm {}.avi && mv {}_fixed.avi {}.avi".format(filename, filename, filename)

                command = command1 + " && " + command2
                
                print(command)
                subprocess.call(command,shell=True)

                setpathinbrowser(path.rpartition("/")[0], path.rpartition("/")[2])
                
                bpy.ops.sequencerextra.placefromfilebrowser()


        except RuntimeError:
            return {'CANCELLED'}

        return {'FINISHED'}




class CameraGetImageOperator(bpy.types.Operator):
    """ record a clip with elphel or webcam"""
    bl_idname = "sequencer.elphel_get_image_operator"
    bl_label = " get an image "

    duration = IntProperty(
    name='frame_duration',
    default=1)
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        create_folder("//footage")

        #kill_gstreamer()

        preferences = bpy.context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences

        repeated_frames = prefs.repeated_frames

        preferences = bpy.context.user_preferences
        elphelIP = preferences.addons['stopmotion'].preferences.elphelIP

        location = bpy.path.abspath("//footage")

        if prefs.elphel_on:
            extension = ".jpg"
        else:
            extension = ".png"

        filename = str(time.time()).rpartition(".")[0] + extension
        filepath = os.path.join(location, filename)
        get_image_from_camera(context, filepath)

        # add the image strip

        for i in range(repeated_frames):
            add_strip_image(filepath, context)

        bpy.ops.sequencer.refresh_all()


        #bpy.ops.sequencer.elphel_preview_operator(color=1)


        
        return  {'FINISHED'}



class StopMotionPanel(bpy.types.Panel):
    bl_label = "Stop Motion Tools"
    bl_idname = "OBJECT_PT_elphel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    elphel_on = BoolProperty(
        name='elphel_on',
        default=False)


    @staticmethod
    def has_sequencer(context):
        return (context.space_data.view_type\
        in {'SEQUENCER', 'SEQUENCER_PREVIEW'})


    @classmethod
    def poll(cls, context):
        return cls.has_sequencer(context)


    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="NLA")


    def draw(self, context):

        preferences = context.user_preferences
        prefs = preferences.addons['stopmotion'].preferences


        layout = self.layout
        row = layout.row(align=True)
        #row.label("Use elphel camera:")
        row.prop(prefs, "elphel_on")

        if prefs.elphel_on:

            layout = self.layout
            layout.prop(prefs, "elphelIP")

            # LAUNCH ELPHEL WEB SERVICE
            row = layout.row(align=True)
            row.operator("sequencer.elphel_control_operator", \
                         icon='SETTINGS')
            # SYNC RENDER RESOLUTION with elphel
            row.operator("sequencer.elphel_sync_res_operator", \
                         icon='FILE_REFRESH')

            
        else:
            # LAUNCH WEBCAM interface
            layout = self.layout
            layout.prop(prefs, "device")

            row = layout.row(align=True)
            row.operator("sequencer.elphel_control_operator", \
                         icon='SETTINGS')
            # SYNC RENDER RESOLUTION with elphel
            row.operator("sequencer.elphel_sync_res_operator", \
                         icon='FILE_REFRESH')


        layout = self.layout

        onion_skin = preferences.addons['stopmotion'].preferences\
                .onion_skin

        layout = self.layout
        layout.prop(prefs, "onion_skin")

        layout.operator("sequencer.elphel_preview_operator",\
                     text="RGB preview", icon="COLOR").color=1

        if prefs.elphel_on:
        # PREVIEW
            layout.label(text="JP4 preview:", icon="CAMERA_DATA")
            row = layout.row(align=True)
            for i in range(4):
                proxysuffix = proxy_qualities[i][1]
                row.operator("sequencer.elphel_preview_operator", \
                         text= proxysuffix).size=i+1


        layout = self.layout
        layout.prop(prefs, "repeated_frames")

        # CAPTURE
        layout = self.layout
        layout.label(text="capture:")
        layout = layout.split(0.50)


        if prefs.recording:
            layout = self.layout
            layout.operator("sequencer.elphel_stop_record_operator", icon='MATPLANE')

        else:

            layout.operator("sequencer.elphel_record_operator", icon='REC')
            layout.operator("sequencer.elphel_get_image_operator",\
                            icon='RENDER_STILL')


            
class StopMotionAddon(bpy.types.AddonPreferences):
    bl_idname = "stopmotion"
    bl_option = {'REGISTER'}

    elphel_on = BoolProperty(
        name='use elphel camera',
        default=False)

    onion_skin = BoolProperty(
        name='use onion skin',
        default=False)

    elphelIP = StringProperty(
        name="elphel IP address",
        description="elphel ip address",
        subtype='NONE',
        default="192.168.5.9")

    device = StringProperty(
        name="video device",
        description="webcam device",
        subtype='NONE',
        default="/dev/video0")

    repeated_frames = IntProperty(
        name="repeated frames",
        description="repeated_frames",
        default=2,
        min = 1, max = 5)

    captured_clip = StringProperty(
        name="captured clip",
        description="path to last captured clip",
        subtype='NONE',
        default="")

    recording = BoolProperty(
        name='camera recording state',
        default=False)

    def draw(self, context):
    
        layout = self.layout
        layout.prop(self, "elphel_on")

        if self.elphel_on:

            layout.prop(self, "elphelIP")

        else:

            layout.prop(self, "device")


def register():
    
    bpy.utils.register_class(StopMotionAddon)
    bpy.utils.register_class(CameraGetImageOperator)
    bpy.utils.register_class(CameraSyncResOperator)
    bpy.utils.register_class(CameraControlOperator)
    bpy.utils.register_class(CameraPreviewOperator)
    bpy.utils.register_class(CameraRecordOperator)
    bpy.utils.register_class(CameraStopRecordOperator)
    bpy.utils.register_class(StopMotionPanel)


def unregister():
    bpy.utils.unregister_class(CameraGetImageOperator)
    bpy.utils.unregister_class(CameraSyncResOperator)
    bpy.utils.unregister_class(CameraControlOperator)
    bpy.utils.unregister_class(CameraPreviewOperator)
    bpy.utils.unregister_class(CameraRecordOperator)
    bpy.utils.unregister_class(CameraStopRecordOperator)
    bpy.utils.unregister_class(StopMotionPanel)
    bpy.utils.unregister_class(StopMotionAddon)


if __name__ == "__main__":
    register()


