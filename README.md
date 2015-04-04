#Addons Kinoraw

a compilation of addons to improve video editing with blender's VSE


##Kinoraw Tools addon

(Tested with blender 2.74)

* Instructions here:
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


## External Addons

### Transform Tools
