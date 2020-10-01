# libretro-db-sqlite

This is a tiny script I used to pack a bunch of libretro rdb files into a single sqlite database.

# Usage

From within this folder:

```
go get github.com/mattn/go-sqlite3
go get github.com/libretro/ludo/rdb

git clone https://github.com/libretro/libretro-database

# If needed, customize the list of entries in libretro-sqlite-db.go

go run libretro-sqlite-db.go
```

# Usage (Python version)

From within this folder:

```
git clone https://github.com/libretro/libretro-database
git clone https://github.com/libretro/RetroArch
cd RetroArch/libretro-db
make
cp ./libretrodb_tool ../..

# If needed, customize the list of entries in libretro-sqlite-db.py
cd ../..
python3 libretro-sqlite-db.py
```
