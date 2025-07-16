#!/usr/bin/python3

import subprocess
import os
import csv 
import re
import shutil


KANSI_TABLE_HEADER = """KeyCode=mnptkswljiueoaAR
Length=16
Prompt=
ConstructPhrase=
[Data]
. 。
[ 「
] 」
"""

SITELEN_SELI_KIWEN_TABLE_HEADER = """KeyCode=mnptkswljiueoa()[]{}^*.:-_" 
Length=16
Prompt=
ConstructPhrase=
[Data]
_ 　
( 󱦗
) 󱦘
[ 󱦐 
] 󱦑
{ 󱦚 
} 󱦛 
^ 󱦕 
* 󱦖 
. 󱦜
: 󱦝　
- ‍
"""

def make_conf(name, filepath):

    a = f"""[InputMethod]
Name=toki pona - sitelen Kansi({name})
LangCode=toki pona
Addon=table
Configurable=True

[Table]
File=table/{filepath}.dict
OrderPolicy=Fast
PageSize=10
ExactMatch=True

[Table/PrevPage]
0=Page_Up

[Table/NextPage]
0=Page_Down

[Table/Selection]
0=F1
1=F2
2=F3
3=F4
4=F5
5=F6
6=F7
7=F8
8=F9
9=F10
"""
    with open(f"confs/{filepath}.conf", "w") as f:
        f.write(a)


# make the table dirs
for i in ["generated_tables", "confs", "table"]:
    try:
        os.mkdir(i)
    except FileExistsError as e:
        pass


print("Generating sitelen seli kiwen table...")

data = open("sitelen_seli_kiwen_glyph_data.txt").read().split("<!--")

with open("generated_tables/toki_pona_sitelen_seli_kiwen.txt", "w") as f:

    f.write(SITELEN_SELI_KIWEN_TABLE_HEADER)

    for i in data:
        name = re.search('class="gsn">(<div class="long..">)?([^<]+)<', i) # grab the name of this glyph
        if name: 
            name = name.group(2)
            
            # skip compounds and the colors
            if '+' in name or name == 'interpunct' or name == 'colon':
                continue 

            # grab the glyph
            glyph = re.search('class="gsg">([^<]*)<', i).group(1)

            # clean up the name 
            name = name.split(" ")[0]
            name = "".join(c for c in name if c not in "1234567890")

            f.write(f"{name} {glyph}\n")

print("Generating sitelen Kansi tables...")

# this creates chinese IME tables + confs
# pulls it from data.csv

# make stuff for all 
ALL_FILENAME = "toki_pona_sitelen_Kansi_All"
make_conf("All", ALL_FILENAME) 

all_table = open(f"generated_tables/{ALL_FILENAME}.txt", "w")
all_table.write(KANSI_TABLE_HEADER)


with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')

    words = next(reader) 

    for row in reader:
        
        name = row[0]
        filepath = "toki_pona_sitelen_Kansi_" + name.replace(" ", "_")

        make_conf(name, filepath)

        with open(f"generated_tables/{filepath}.txt", "w") as f:
            f.write(KANSI_TABLE_HEADER)

            for word, chars in zip(words[1:], row[1:]):
                if chars:
                    for char in chars.split(", "):
                        f.write(f"{word} {char}\n")
                        all_table.write(f"{word}, {char}\n")
                    #f.write("\n") 
        all_table.write("\n")

print("Building tables...")

for file in os.listdir("generated_tables"):
    fn = file[:-4]

    p = subprocess.Popen(["libime_tabledict", f"generated_tables/{fn}.txt", f"table/{fn}.dict"])
    p.wait()
    if p.returncode:
        print(f"{fn} failed to build")
        quit(1)

for file in os.listdir("static_tables"):
    fn = file[:-4]

    p = subprocess.Popen(["libime_tabledict", f"static_tables/{fn}.txt", f"table/{fn}.dict"])
    p.wait()
    if p.returncode:
        print(f"{fn} failed to build")
        quit(1)

print("Copying static confs...")

for file in os.listdir("static_confs"):
    shutil.copy(f"static_confs/{file}", f"confs/{file}")
