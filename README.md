#Addons Kinoraw

a compilation of addons to improve video editing with blender's VSE


##Kinoraw Tools addon

(Tested with blender 2.74)

* Instructions here:
https://github.com/kinoraw/kinoraw_tools/blob/master/README.md

* The development version of the addon is: 
https://github.com/kinoraw/kinoraw_tools

You can clone the addon directly in the blender addons folder, i.e: in my ubuntu
computer i had to do:

cd ~/.config/blender/2.74/scripts/addons

git clone https://github.com/kinoraw/kinoraw_tools

then you can start blender and activate the addon in the user preferences
window.

* zip versions in this repo should be latest stable version, ready to install.


1.- open the user preferences window (ctrl+alt+u) and load the zip file with the button 'install from file' you can find at the bottom of the window.

2.- after that, you should activate the addon by presing the checkbox next to the addon 


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

