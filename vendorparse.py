import sqlite3

f = open("vendors.txt", "r", encoding="utf-8")
lines = f.readlines()
f.close()
con = sqlite3.connect("database.db")
cur = con.cursor()
rc = 0
for line in lines:
    line = line.split('\t')
    for i in range(len(line)):
        line[i] = line[i].replace("\"", "")
    if(len(line)==3):
        con.execute(
            "INSERT INTO vendors (mac, vendor) VALUES (?, ?)",(line[0],line[2])
        )
        pass
    else:
        con.execute(
            "INSERT INTO vendors (mac, vendor) VALUES (?, ?)",(line[0],line[1])
        )
        pass
    con.commit()
    print(rc)
    rc+=1
con.close()    
