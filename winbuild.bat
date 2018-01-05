
pyinstaller --workpath ../laitbuild/build --distpath ../laitbuild -y --clean --onedir --add-data Config;Config  --add-data data;data -i data/winicon/lait.ico --noconsole lait lait_editor

copy settings.yml ..\laitbuild\lait
