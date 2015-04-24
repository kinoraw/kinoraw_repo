# Kinoraw Repository


A repository of tools to edit video with floss.

    In the external section i keep a copy of interesting addons to use in Blender VSE

##Instructions to install blender addons

* Download the zip file from this page and extract it somewhere or clone the repository with this command
 
    git clone https://github.com/kinoraw/kinoraw_repo.git

* Once in Blender, open the user preferences window (ctrl+alt+u) and load the zip file of each addon with the button 'install from file' you can find at the bottom of the window.

* After that, you should activate each addon by presing the checkbox next to the addon


## Kinoraw Tools (addon for blender 2.74)

(Tested with blender 2.74)

* Documentation here:
https://github.com/kinoraw/kinoraw_tools/blob/master/README.md

* The development version of the addon is: 
https://github.com/kinoraw/kinoraw_tools


## Mega_render_operator.py

it is mainly bash stuff, only tested in linux yet. It uses zenity to show info...

'Generate' operator divides the timeline in n pieces, being n the number of available cpu kernels, and create a bash script to launch as many background blenders as cpu threads. 

    Only works when exporting to frame sequences.

Be sure to save your project and setup your output location before press 'launch render'

in latests versions of blender VSE render uses multithread, so this script is not so necesary, but still it can improve your render times if you need to export to frames.

## Stop_motion / elphel_panel

you need to install some programs to use this addon...

for webcam you need:

    gstreamer-0.10
    guvcview
    mencoder

for elphel version you also need:

    exiftools


# External Addons

## VSE Transform Tool  (addon for blender 2.74)

http://blenderartists.org/forum/showthread.php?280731-VSE-Transform-tool

## VSE Quick Functions    (addon for blender 2.74)

http://blenderartists.org/forum/showthread.php?338598-Addon-WIP-VSE-Quick-functions-Snaps-Fades-Zoom-Parenting-Titling-Play-speed

## Copy Modifiers       (addon for blender 2.74)

in the repo there is a modified version with original UI hided  (commented lines)

http://blenderclan.tuxfamily.org/html/modules/newbb/viewtopic.php?post_id=458896#forumpost458896