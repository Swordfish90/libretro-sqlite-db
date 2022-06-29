#!/bin/bash

if [ ! -f  libretrodb_tool ];then
  git clone https://github.com/libretro/RetroArch
  cd RetroArch/libretro-db
  make
  cp ./libretrodb_tool ../..
  cd ../..
fi

if [ ! -d libretro-database ];then
  git clone https://github.com/libretro/libretro-database
else
  cd libretro-database
  git pull
  cd ..
fi

python3 libretro-sqlite-db.py