#!/bin/bash
rm -fr ../lait
pyinstaller --workpath ../lait/build --distpath ../lait -y --clean --onefile --icon=data/winicon/lait.ico --noconsole lait
cp -rfv data ../lait/
cp -rfv Config ../lait/
cp settings.yml ../lait/
rm -fr ../lait/build ../lait/lait.app
cd ..
zip -r lait_MacOS_64bit.zip lait/
rm -fr lait
