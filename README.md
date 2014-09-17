addons_kinoraw (blender 2.71)
===================================



sequencer_extra_actions
-----------------------

1.- ZIP the sequencer_extra_actions folder

2.- open the user preferences window (ctrl+alt+u) and load the zip file with the button 'install from file' you can find at the bottom of the window.

3.- now in the addons window, you should activate the addon by presing the checkbox next to the addon 


There are some spreaded documentation. Main functions are described here:

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

it is suposed to work fine with windows and mac. Some feedback with steps to acomplish this will be apreciated.

mega_render_operator.py
-------------------------------

"Generate" operator divides the timeline in n pieces, being n the number of available cpu kernels, and generate a bash script to launch as many background blenders as cpu threads.


stop_motion / elphel_panel
------------------------

you need to install some programs to use this addon...

for webcam you need:

    gstreamer-0.10
    guvcview
    mencoder

for elphel version you also need:

    exiftools

