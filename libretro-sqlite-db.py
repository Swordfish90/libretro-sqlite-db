import contextlib
import json
import sqlite3
import subprocess


def main():
    entries = [
        {
            "filename": "libretro-database/rdb/Nintendo - Game Boy.rdb",
            "system": "gb",
        },
        {
            "filename": "libretro-database/rdb/Nintendo - Game Boy Color.rdb",
            "system": "gbc",
        },
        {
            "filename": "libretro-database/rdb/Nintendo - Game Boy Advance.rdb",
            "system": "gba",
        },
        {
            "filename": "libretro-database/rdb/Nintendo - Nintendo 64.rdb",
            "system": "n64",
        },
        {
            "filename": "libretro-database/rdb/Sega - Mega Drive - Genesis.rdb",
            "system": "md",
        },
        {
            "filename": "libretro-database/rdb/Nintendo - Nintendo Entertainment System.rdb",
            "system": "nes",
        },
        {
            "filename": "libretro-database/rdb/Nintendo - Super Nintendo Entertainment System.rdb",
            "system": "snes",
        },
        {
            "filename": "libretro-database/rdb/Sega - Master System - Mark III.rdb",
            "system": "sms",
        },
        {
            "filename": "libretro-database/rdb/FBNeo - Arcade Games.rdb",
            "system": "fbneo",
        },
        {
            "filename": "libretro-database/rdb/Sony - PlayStation Portable.rdb",
            "system": "psp",
        },
        {
            "filename": "libretro-database/rdb/Nintendo - Nintendo DS.rdb",
            "system": "nds",
        },
        {
            "filename": "libretro-database/rdb/Sega - Game Gear.rdb",
            "system": "gg",
        },
        {
            "filename": "libretro-database/rdb/Atari - 2600.rdb",
            "system": "atari2600",
        },
        {
            "filename": "libretro-database/rdb/Sony - PlayStation.rdb",
            "system": "psx",
        },
    ]

    connection = sqlite3.connect('./libretro-db.sqlite')
    connection.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, system TEXT, romName TEXT, developer TEXT, crc32 TEXT, serial TEXT)")

    for entry in entries:
        load_database(connection, entry['filename'], entry['system'])

    connection.execute("CREATE INDEX crc32Index ON games (crc32)")
    connection.execute("CREATE INDEX serialIndex ON games (serial)")
    connection.execute("CREATE INDEX romNameIndex ON games (romName)")

    connection.commit()
    connection.close()


def load_database(connection, filename, system):
    process = subprocess.run(['./libretrodb_tool', filename, 'list'], capture_output=True)
    values = []
    for line in process.stdout.decode().split('\n'):
        line = line.replace('\\', '\\\\')
        with contextlib.suppress(json.decoder.JSONDecodeError):
            game = json.loads(line)
            if 'serial' in game:
                game['serial'] = bytes.fromhex(game['serial'])
            game['system'] = system
            values.append(tuple(game.get(key, '') for key in ['name', 'rom_name', 'system', 'developer', 'crc', 'serial']))
    print(f"{system}: {len(values)} entries")
    connection.executemany("INSERT INTO games (name, romName, system, developer, crc32, serial) VALUES (?,?,?,?,?,?)", values)


if __name__ == '__main__':
    main()
