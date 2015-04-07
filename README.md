#Addons Kinoraw

a compilation of addons to improve video editing with blender's VSE


##Kinoraw Tools addon

* Download the zip file from this page https://github.com/kinoraw/kinoraw_repo

* Open Blender

* Open the user preferences window (ctrl+alt+u) and load the zip file named *kinoraw_tools_Vxxx.zip* with the button 'install from file' you can find at the bottom of the window.

* After that, you should activate the addon by presing the checkbox next to the addon

(Tested with blender 2.74)

* Documentation here:
https://github.com/kinoraw/kinoraw_tools/blob/master/README.md

* The development version of the addon is: 
https://github.com/kinoraw/kinoraw_tools


## Mega_render_operator.py

it is mainly bash stuff, only tested in linux yet. It uses zenity to show info...

'Generate' operator divides the timeline in n pieces, being n the number of available cpu kernels, and create a bash script to launch as many background blenders as cpu threads. 

Be sure to save your project and setup your output location before press 'launch render'

## Stop_motion / elphel_panel

you need to install some programs to use this addon...

for webcam you need:

    gstreamer-0.10
    guvcview
    mencoder

for elphel version you also need:

    exiftools


# External Addons

## VSE Transform Tool

Mod version working in 2.74  (source: somewhere in Blenderartist...)
