import gzip
import sqlite3
from tqdm import tqdm

DB_FILE = "imdb.db"

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            nconst TEXT PRIMARY KEY,
            primaryName TEXT,
            birthYear INTEGER,
            deathYear INTEGER,
            primaryProfession TEXT,
            knownForTitles TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS titles (
            tconst TEXT PRIMARY KEY,
            titleType TEXT,
            primaryTitle TEXT,
            originalTitle TEXT,
            isAdult INTEGER,
            startYear INTEGER,
            endYear INTEGER,
            runtimeMinutes INTEGER,
            genres TEXT
        );
    ''')

    conn.commit()

def parse_int(value):
    return int(value) if value.isdigit() else None

def import_name_basics(conn, file_path):
    cursor = conn.cursor()
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        next(file)  # Skip header
        for line in tqdm(file, desc="Importing names"):
            parts = line.strip().split('\t')
            if len(parts) != 6:
                continue
            nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles = parts
            cursor.execute('''
                INSERT OR IGNORE INTO persons (nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                nconst, primaryName,
                parse_int(birthYear),
                parse_int(deathYear),
                primaryProfession,
                knownForTitles
            ))
    conn.commit()

def import_title_basics(conn, file_path):
    cursor = conn.cursor()
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        next(file)  # Skip header
        for line in tqdm(file, desc="Importing titles"):
            parts = line.strip().split('\t')
            if len(parts) != 9:
                continue
            tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres = parts
            cursor.execute('''
                INSERT OR IGNORE INTO titles (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tconst, titleType, primaryTitle, originalTitle,
                int(isAdult) if isAdult.isdigit() else 0,
                parse_int(startYear),
                parse_int(endYear),
                parse_int(runtimeMinutes),
                genres
            ))
    conn.commit()

def main():
    conn = sqlite3.connect(DB_FILE)
    create_tables(conn)

    import_name_basics(conn, "backend/datasets/name.basics.tsv.gz")
    import_title_basics(conn, "backend/datasets/title.basics.tsv.gz")

    conn.close()

if __name__ == "__main__":
    main()
