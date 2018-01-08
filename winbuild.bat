
pyinstaller --workpath ../laitbuild/build --distpath ../laitbuild -y --clean --onedir --add-data Config;Config  --add-data data;data -i data/winicon/lait.ico --noupx --noconsole lait lait_editor

copy settings.yml ..\laitbuild\lait
mkdir ..\laitbuild\lait\thorpy
mkdir ..\laitbuild\lait\thorpy\data

copy C:\Python36\Lib\site-packages\thorpy\data  ..\laitbuild\lait\thorpy\data\
