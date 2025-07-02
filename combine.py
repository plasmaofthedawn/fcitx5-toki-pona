import subprocess
import os
from collections import defaultdict




headers = defaultdict(lambda: """KeyCode=mnptkswljiueoaAR
Length=16
Prompt=
ConstructPhrase=
[Data]
""")

headers["UCSUR"] = """KeyCode=mnptkswljiueoa()[]{}^*.:"
Length=16
Prompt=
ConstructPhrase=
[Data]
"""

headers["nasin pi sitelen jelo"] = """KeyCode=mnptkswljiueoa[]"
Length=16
Prompt=
ConstructPhrase=
[Data]
"""


def make_conf(name, filepath):

    a = f"""[InputMethod]
Name=toki pona - {name}
LangCode=toki pona
Addon=table
Configurable=True

[Table]
File=table/{filepath}.dict
OrderPolicy=Fast
PageSize=10
ExactMatch={"True" if name != "UCSUR" else "False"}

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

        
try:
    os.mkdir("raw_tables")
    os.mkdir("table")
    os.mkdir("confs")
except FileExistsError as e:
    pass

names = [f"sitelen Kansi ({x})" for x in ["Tencent QQ", "sitelen munjan", "jan Josan", "jan Mato (jp)", "jan Mato (zh)", "jan U", "enervation", "jan lili", "StuleBackery", "sitelen Sonko pona", "WillBaneOfGods", "nasin pi kulupu Eko", "JoeStrout", "Evilkenevil77", "sitelen Sonwa", "sitelen Kanpun", "All"]] + ["UCSUR", "Toki Pona Script (dingbats)", "nasin pi sitelen jelo"]

filenames = ["toki_pona_" + x.replace(" ", "_").replace("(", "").replace(")", "").lower() for x in names]

data = open("data.txt").read()

for n, fn, d in zip(names, filenames, data.split("---")):

    print(n, fn)
    
    with open(f"raw_tables/{fn}.txt", "w") as f:
        f.write(headers[n])
        f.write(d.strip())

    subprocess.Popen(["libime_tabledict", f"raw_tables/{fn}.txt", f"table/{fn}.dict"])

    make_conf(n, fn)
