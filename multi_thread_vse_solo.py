import bpy, os, subprocess

# current scene
sce = bpy.context.scene

#start and end frame
s_frame = sce.frame_start
e_frame = sce.frame_end

# number of threads
nucleos = 8

# path to blender executable
#blender = "~/blender/blender-2.70a-linux-glibc211-x86_64/blender"
blender = "~/soft/blender-2.70a-linux-glibc211-x86_64/blender"
#blender = "c:/Users/carlos/soft/blender-2.69-testbuild1-windows64/blender.exe"

# current filename
file = bpy.data.filepath

duration = e_frame - s_frame

part = int(duration / nucleos)

#lista de tramos que se han de renderizar
tramos = []
counter = s_frame

print("-------------------------")
for i in range(nucleos):
    if i < nucleos-1:
        print(counter, counter+part, counter+part-counter)
        tramo = (counter, counter+part)
    else:
        print(counter, e_frame, e_frame-counter)
        tramo = (counter, e_frame)
    counter = counter+part+1
    tramos.append(tramo)
print(tramos)

# generate the script

text_file = open(bpy.path.abspath("//megarender-solo.sh"), "w")
text_file.write("#!/bin/bash")
for i, j in enumerate(tramos):
    text_file.write( ("\n(\necho '#Rendering part {}' ;\nSTART_RENDER=$(date +'%s');\nRENDERED=$(").format(i))
    command = "{} {} -b -S {} -s {} -e {} -a".format(blender, file, sce.name, j[0], j[1])
    text_file.write(command)
    text_file.write(" | grep -c Saved) \nEND_RENDER=$(date +'%s');\nRENDERING_SECS=$(($END_RENDER-$START_RENDER))\n")
    command = """if [ $RENDERED -eq {} ]\nthen\n   echo \"#Finished frame {} to {} in $(printf '%dh:%dm:%ds' $(($RENDERING_SECS/3600)) $(($RENDERING_SECS%3600/60)) $(($RENDERING_SECS%60)))\"\nelse\n   echo \"#Errors in script {}\"\nfi\n ) | zenity --progress --pulsate --no-cancel --title='Part {}'""".format(j[1]-j[0]+1, j[0],j[1], i, i)
    text_file.write(command)
    if i < len(tramos)-1:
        print(i, len(tramos)-1)
        text_file.write(" & \n")
text_file.close()

