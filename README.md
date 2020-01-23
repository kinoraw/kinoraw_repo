# Kinoraw Repository (VSE addons for blender 2.76b)


A repository of tools to edit video with floss.

    In the external section i keep a copy of interesting addons to use in Blender VSE

##Instructions to install blender addons

* Download the zip file from this page and extract it somewhere or clone the repository with this command
 
    git clone https://github.com/kinoraw/kinoraw_repo.git

* Once in Blender, open the user preferences window (ctrl+alt+u) and load the zip file of each addon with the button 'install from file' you can find at the bottom of the window.

* After that, you should activate each addon by presing the checkbox next to the addon


## Kinoraw Tools

* Documentation here:
https://github.com/kinoraw/kinoraw_tools/blob/master/README.md

* The development version of the addon is: 
https://github.com/kinoraw/kinoraw_tools


## Mega_render_operator.py

Updated for Blender 2.80
 
It is mainly bash stuff, only tested in linux yet. It uses zenity to show info...

The operator "generate" divides the timeline in n pieces, being n the number of available cores, and generates a bash script to launch as many blenders as cores are indicated, executing blender processes in background.

It works with video and image sequences.

If the output is set to video (at the moment only mp4 and mkv), once the video parts are finished it uses ffmpeg to concatenate them into the final output video file.


FFMPEG required.


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

http://blenderartists.org/forum/showthread.php?280731-VSE-Transform-tool

## VSE Quick Functions  

http://blenderartists.org/forum/showthread.php?338598-Addon-WIP-VSE-Quick-functions-Snaps-Fades-Zoom-Parenting-Titling-Play-speed

## Copy Modifiers    

in the repo there is a modified version with original UI hided  (commented lines)

http://blenderclan.tuxfamily.org/html/modules/newbb/viewtopic.php?post_id=458896#forumpost458896