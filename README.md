addons_kinoraw (para blender 2.70)
===================================

cada addon o script puede tener unas instrucciones diferentes de instalacion y uso:


sequencer_extra_actions
-----------------------

1.- comprimir la carpeta sequencer_extra_actions en un zip

2.- abrir la ventana de preferencias del usuario, en la pestana de addons, abajo de la ventana hay un boton que dice 'install from file'. Seleccionar el zip y cargarlo.

3.- en la ventana de addons hay que activar el cuadradito que aparece a la derecha.

El script incluye diversas utilidades, para la mayoria consultar:

http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Sequencer/Extra_Sequencer_Actions

para audio y proxy tools consultar (por el momento es la explicacion de la versión antigua):

http://kinoraw.net/wordpress/herramientas-para-la-produccion-de-cine-libre/addons-para-blender/proxy-and-audio-tools/extractimport-wav/

http://kinoraw.net/wordpress/herramientas-para-la-produccion-de-cine-libre/addons-para-blender/proxy-and-audio-tools/createset-proxy/

para jump to cut consultar:

http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Sequencer/Jump_to_cut

para eco tools consultar:

http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Sequencer/Eco

para que funcione exif info panel hay que instalar exiftools:

    sudo apt-get install libimage-exiftool-perl

multi_thread_vse.py
-------------------------------

Esto no es un addon, sino un script que hay que correr desde el editor de textos de blender. 

El script divide el timeline en n trozos, siendo n el numero de nucleos disponibles, y genera varios scripts para lanzar tantos blenders como nucleos, desde un terminal.

Editar la linea 11 con el numero de nucleos a usar, y la linea 14 con la ruta al ejecutable blender.

Tras ejecutar el script se crea una carpeta con los scripts de cada trozos, por defecto en la carpeta //scripts_render y un script megarender.sh en la carpeta //

desde un terminal, en //, ejecutar:

    sh megarender.sh

En la version multi_thread_vse_solo.py, se utiliza un solo script y mejora la compatibilidad con otras distros de linux, pero aun no indica los frames fallidos en caso de error.


stop_motion / elphel_panel
------------------------

hay que instalar varios programas para usar este addon...

para la webcam hay que instalar:

    gstreamer-0.10
    guvcview
    mencoder

para la elphel tambien hace falta

    exiftools

