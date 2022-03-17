import sqlite3
import re
from pathlib import Path
import csv
import sys


def create_table(tables, db, connection):
    for _, query in tables.items():        
        connection.execute("".join(query))
    connection.commit


def get_columns(query):
    columns = []
    for _, column in enumerate(query[1:]):
        columns.append(column.split(' ')[0])
    return columns


def fill_table(query, values, connection):
    sub_values = ('?, ' * (len(query)-1))[0:-2]
    match = re.search(r"\w+(?=\()", query[0])
    if match:
        table_name = match.group(0)
        columns = ", ".join(get_columns(query))
        sql_code = f"INSERT INTO {table_name}({columns}) VALUES ({sub_values})"
        try:
            if len(values)>1:
                connection.executemany(sql_code, (values))
            else:
                connection.execute(sql_code, (values))
            connection.commit()
        except sqlite3.IntegrityError:
            print("Unexpected error:", sys.exc_info()[0])


def csv_to_db(csv_path_tables, db_name, delimiter=","):
    connection = sqlite3.connect(db_name)
    connection.execute("PRAGMA foreign_keys = ON;")
    create_table(csv_path_tables, db_name, connection)
    for csv_path, table_query in csv_path_tables.items():
        if Path(csv_path).is_file():
            with open(csv_path, 'r') as f:
                content = csv.reader(f, delimiter=delimiter)
                batch = []
                for i, row in enumerate(content):
                    if i:
                        batch.append(row)
                        if len(batch) == 50000:
                            fill_table(table_query, batch, connection)
                            batch = []
                if batch:
                    fill_table(table_query, batch, connection)
    connection.close()


def get_distinct_values(group_var, dist_var, table_name, connect):
    sql_code = f"SELECT {group_var}, COUNT(DISTINCT({dist_var})) FROM {table_name} GROUP BY {group_var}"
    res = connect.execute(sql_code).fetchall()
    return res


def update_table(table_name, col_id, val, condition, connection):
    sql_code = f"UPDATE {table_name} SET {col_id} = '{val}' WHERE {condition}"
    connection.execute(sql_code)
    connection.commit()


if __name__ == "__main__":
    # provide path to table locations
    base_path = "data/"
    csv_files_names = {
        f"{base_path}metadata.csv": ["CREATE TABLE IF NOT EXISTS meta(",
                "ind INTEGER,",
                "dna_chip_id TEXT PRIMARY KEY,",
                "breed TEXT,",
                "sex TEXT)"],
        f"{base_path}genstudio.csv": ["CREATE TABLE IF NOT EXISTS genstudio(",
                    "ind INTEGER PRIMARY KEY,",
                    "SNP_name TEXT,",
                    "SNP_Index INTEGER,",
                    "SNP_Aux INTEGER,",
                    "Sample_ID TEXT NOT NULL REFERENCES meta(dna_chip_id),",
                    "SNP TEXT,",
                    "Allele1_Top TEXT,",
                    "Allele2_Top TEXT,",
                    "Allele1_Forward TEXT,",
                    "Allele2_Forward TEXT,",
                    "Allele1_AB TEXT,",
                    "Allele2_AB TEXT,",
                    "Chr INTEGER,",
                    "Position INTEGER,",
                    "GC_Score REAL,",
                    "GT_Score REAL,",
                    "Theta REAL,",
                    "R REAL,",
                    "B_Allele_Freq REAL,",
                      "Log_R_Ratio REAL)",]
                    }
    csv_to_db(csv_files_names, "genlibrary.db")
    connect = sqlite3.connect("genlibrary.db")
    print("count distinct SNPs for all Sample_id")
    res = get_distinct_values("Sample_ID", "SNP", "genstudio", connect)
    print(res)
    print("update table meta - change sex for specific dna_chip_id")
    update_table("meta", "sex" , "Y", "dna_chip_id = '202341831127R04C02'", connect)
    print("check if updates are saved")
    sql_code = "SELECT * FROM meta WHERE sex = 'Y'"
    res = connect.execute(sql_code).fetchall()
    print(res)
    connect.close()
