addons_kinoraw (blender 2.72)
===================================

kinoraw_tools
=============

a compilation of addons to improve video editing with blender's VSE

(Tested with blender 2.72)



Kinoraw Tools addon
-----------------------

sequencer_extra_actions now is part of kinoraw tools addon.

I removed the buttons in the VSE header, also create a panel to host all working functions. All menu entries are in the original place in the UI. Distribute, ripples and inserts doesn't work, needs some check...

I removed many old proxy functions in the recursive loader and extra operators. The proxy tool module is better and easier to use...

Every panel can be switched visible/invisible in the addon preferences panel.

in blender 2.73 there is an option to jump to edit points, so jump to cut original feature, and also a slide function like the one in sequencer extra tools (Turi Scandurra) so both have been merged into blender code!!! =) 

Todo: keep the buttons in the panel but remove old operator to launch the internal feature

Todo: remove slide operator and change the shortcut to internal feature

(((((kinoraw tools will be developed in a separate repository)))))

The development version of the addon is here: https://github.com/kinoraw/kinoraw_tools

You can clone the addon directly in the blender addons folder, i.e: in my ubuntu
computer i had to do:

cd ~/.config/blender/2.72/scripts/addons

git clone https://github.com/kinoraw/kinoraw_tools

then you can start blender and activate the addon in the user preferences
window.

* zip versions in this repo should be latest stable version, ready to install.



1.- open the user preferences window (ctrl+alt+u) and load the zip file with the button 'install from file' you can find at the bottom of the window.

2.- after that, you should activate the addon by presing the checkbox next to the addon 


There are some old and spreaded documentation. Main functions are described here:

http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Sequencer/Extra_Sequencer_Actions

for audio and proxy tools check this old explanation:

http://kinoraw.net/wordpress/herramientas-para-la-produccion-de-cine-libre/addons-para-blender/proxy-and-audio-tools/extractimport-wav/

http://kinoraw.net/wordpress/herramientas-para-la-produccion-de-cine-libre/addons-para-blender/proxy-and-audio-tools/createset-proxy/

for jump to cut check this, but many things changed since this docs...

http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Sequencer/Jump_to_cut

for eco tools check:

http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Sequencer/Eco

to get exif info panel you need to install exiftools:

    sudo apt-get install libimage-exiftool-perl



mega_render_operator.py
-------------------------------

it is mainly bash stuff, only tested in linux yet. It uses zenity to show info...

'Generate' operator divides the timeline in n pieces, being n the number of available cpu kernels, and create a bash script to launch as many background blenders as cpu threads. 

Be sure to save your project and setup your output location before press 'launch render'





stop_motion / elphel_panel
------------------------

you need to install some programs to use this addon...

for webcam you need:

    gstreamer-0.10
    guvcview
    mencoder

for elphel version you also need:

    exiftools

