#!/bin/python3
import hashlib, os, json, shutil
from multiprocessing import Pool
from time import time


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

current_time = int(time())
print("Aegis")
file_list = []


for (dirpath, dirs, files) in os.walk("world"):
   for name in files:
      file_list.append(os.path.join(dirpath, name))

results = []
with Pool(5) as p:
    results = p.map(md5, file_list)


hash_table = {}

for index, filename in enumerate(file_list):
    hash_table[filename] = results[index]

#print(hash_table)

previous_hash_table = {}
try:
    with open('backup_db.json', 'r') as data:
        previous_hash_table = json.load(data)
except Exception as err:
    print(err)

for backup_entry in hash_table:
    if backup_entry in previous_hash_table:
        if hash_table[backup_entry] == previous_hash_table[backup_entry]:
            continue
        else:
            print("File " + str(backup_entry) + " has changed.")
    else:
        print("File " + str(backup_entry) + " is new.")

try:
    with open('backup_db.json', 'w') as data:
        json.dump(hash_table, data)
except Exception as err:
    print(err)