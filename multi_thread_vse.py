import bpy, os, subprocess

# current scene
sce = bpy.context.scene

#start and end frame
s_frame = sce.frame_start
e_frame = sce.frame_end

# number of threads
nucleos = 8

# path to blender executable
blender = "~/soft/blender-2.70a-linux-glibc211-x86_64/blender"
#blender = "c:/Users/carlos/soft/blender-2.69-testbuild1-windows64/blender.exe"

# current filename
file = bpy.data.filepath

# output folder for the scripts
folder = bpy.path.abspath("//scripts_render")
os.system("mkdir "+folder)
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

#generate one script for each part

for i, j in enumerate(tramos):
    command = "{} {} -b -S {} -s {} -e {} -a".format(blender, file, sce.name, j[0], j[1])
    text_file = open(bpy.path.abspath("{}/render_part_{}.sh".format(folder,str(i))), "w")
    text_file.write(command)
    command = """zenity --info --text='render {} finished. from frame {} to {}'""".format(i, j[0],j[1])
    text_file.write("\n")
    text_file.write(command)
    text_file.close()
    
# generate main script

text_file = open(bpy.path.abspath("//megarender.sh".format(folder,str(i))), "w")
for i, j in enumerate(tramos):
    command = """gnome-terminal -e 'sh scripts_render/render_part_{}.sh'""".format(i)
    text_file.write(command)
    if i < len(tramos)-1:
        print(i, len(tramos)-1)
        text_file.write(" && ")
text_file.close()
