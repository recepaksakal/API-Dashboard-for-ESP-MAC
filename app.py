from flask import Flask, redirect, request, render_template
import datetime
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dash/')


@app.route('/dash/', defaults={"typ": "day"})
@app.route('/dash/<typ>/', methods=['GET', 'POST'])
def dash(typ):
    typ = str(typ)
    if typ == "day":
        tdt = datetime.date.today()
        #tdt = '2020-08-18'
        title = str(tdt).split(' ')[0]
        dt = str(tdt).split("-")
        epochList = []
        for i in range(24):
            ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), i, 0, 0).timestamp()))
            epochList.append(ep)
        ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 23, 59, 59).timestamp()))
        epochList.append(ep)
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        counts = []
        hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        for i in range(24):
            sql = 'SELECT mr_id, epoch FROM timestamps WHERE epoch>' + epochList[i] + ' AND epoch<' + epochList[
                i + 1] + ' GROUP BY mr_id'
            cur.execute(sql)
            res = cur.fetchall()
            counts.append(len(res))

        # hangi vendordan kaç cihaz yakalandı?
        sql = 'SELECT vendor, COUNT(vendor) FROM mac_records WHERE id IN (SELECT mr_id FROM timestamps WHERE epoch>' + epochList[0] + ' AND epoch<' + epochList[-1] + ') GROUP BY(vendor)'
        cur.execute(sql)
        countvendor = cur.fetchall()
        cvx = []
        cvy = []
        for cv in countvendor:
            cv = list(cv)
            cvx.append(cv[0])
            cvy.append(cv[1])

        data = {"sec": 0, "title": title, "counts": counts, "hours": hours, "cvx": cvx, "cvy": cvy}
        con.close()
        return render_template("dashboard.html", data=data)

    elif typ == "week":
        stpoint = datetime.date.today() - datetime.timedelta(6)
        epochList = []
        days = []
        counts = []
        for i in range(8):
            dt = str(stpoint).split('-')
            ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0).timestamp()))
            epochList.append(ep)
            days.append(str(stpoint))
            stpoint = stpoint + datetime.timedelta(1)
        days = days[:-1]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        for i in range(7):
            sql = 'SELECT mr_id, epoch FROM timestamps WHERE epoch>' + epochList[i] + ' AND epoch<' + epochList[
                i + 1] + ' GROUP BY mr_id'
            cur.execute(sql)
            res = cur.fetchall()
            counts.append(len(res))
        title = "Son 1 Hafta"

        # hangi vendordan kaç cihaz yakalandı?
        sql = 'SELECT vendor, COUNT(vendor) FROM mac_records WHERE id IN (SELECT mr_id FROM timestamps WHERE epoch>' + epochList[0] + ' AND epoch<' + epochList[-1] + ') GROUP BY(vendor)'
        cur.execute(sql)
        countvendor = cur.fetchall()
        cvx = []
        cvy = []
        for cv in countvendor:
            cv = list(cv)
            cvx.append(cv[0])
            cvy.append(cv[1])


        data = {"sec": 1, "title": title, "counts": counts, "days": days, "cvx": cvx, "cvy": cvy}
        con.close()
        return render_template("dashboard.html", data=data)

    elif typ == "month":
        stpoint = datetime.date.today() - datetime.timedelta(30)
        epochList = []
        days = []
        counts = []
        for i in range(32):
            dt = str(stpoint).split('-')
            ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0).timestamp()))
            epochList.append(ep)
            days.append(str(stpoint))
            stpoint = stpoint + datetime.timedelta(1)
        days = days[:-1]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        for i in range(31):
            sql = 'SELECT mr_id, epoch FROM timestamps WHERE epoch>' + epochList[i] + ' AND epoch<' + epochList[
                i + 1] + ' GROUP BY mr_id'
            cur.execute(sql)
            res = cur.fetchall()
            counts.append(len(res))
        title = "Son 1 Ay"

        # hangi vendordan kaç cihaz yakalandı?
        sql = 'SELECT vendor, COUNT(vendor) FROM mac_records WHERE id IN (SELECT mr_id FROM timestamps WHERE epoch>' + epochList[0] + ' AND epoch<' + epochList[-1] + ') GROUP BY(vendor)'
        cur.execute(sql)
        countvendor = cur.fetchall()
        cvx = []
        cvy = []
        for cv in countvendor:
            cv = list(cv)
            cvx.append(cv[0])
            cvy.append(cv[1])

        data = {"sec": 1, "title": title, "counts": counts, "days": days, "cvx": cvx, "cvy": cvy}

        con.close()
        return render_template("dashboard.html", data=data)

    elif typ == "custom":
        if request.method == 'POST':
            date1 = request.form.get('date1').split('-')
            date2 = request.form.get('date2').split('-')
            date1 = datetime.datetime(int(date1[0]), int(date1[1]), int(date1[2]), 0, 0, 0)
            date2 = datetime.datetime(int(date2[0]), int(date2[1]), int(date2[2]), 0, 0, 0)
            stpoint = ""
            fark = 0
            title = ""
            if date1 == date2:
                tdt = str(date1).split(' ')[0]
                dt = str(tdt).split("-")
                title = str(tdt).split(' ')[0]
                epochList = []
                for i in range(24):
                    ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), i, 0, 0).timestamp()))
                    epochList.append(ep)
                ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 23, 59, 59).timestamp()))
                epochList.append(ep)
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                counts = []
                hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
                for i in range(24):
                    sql = 'SELECT mr_id, epoch FROM timestamps WHERE epoch>' + epochList[i] + ' AND epoch<' + epochList[
                        i + 1] + ' GROUP BY mr_id'
                    cur.execute(sql)
                    res = cur.fetchall()
                    counts.append(len(res))

                # hangi vendordan kaç cihaz yakalandı?
                sql = 'SELECT vendor, COUNT(vendor) FROM mac_records WHERE id IN (SELECT mr_id FROM timestamps WHERE epoch>' + \
                      epochList[0] + ' AND epoch<' + epochList[-1] + ') GROUP BY(vendor)'
                cur.execute(sql)
                countvendor = cur.fetchall()
                cvx = []
                cvy = []
                for cv in countvendor:
                    cv = list(cv)
                    cvx.append(cv[0])
                    cvy.append(cv[1])

                data = {"sec": 0, "title": title, "counts": counts, "hours": hours, "cvx": cvx, "cvy": cvy}

                con.close()
                return render_template("dashboard.html", data=data)

            elif date1 > date2:
                fark = str(date1 - date2)
                fark = int(fark.split(' ')[0])
                stpoint = date2
                title = str(date2).split(' ')[0] + " <-> " + str(date1).split(' ')[0]

            elif date2 > date1:
                fark = str(date2 - date1)
                fark = int(fark.split(' ')[0])
                stpoint = date1
                title = str(date1).split(' ')[0] + " <-> " + str(date2).split(' ')[0]

            stpoint = str(stpoint).split(' ')[0].split('-')
            stpoint = datetime.date(int(stpoint[0]), int(stpoint[1]), int(stpoint[2]))
            epochList = []
            days = []
            counts = []
            for i in range(fark + 1):
                dt = str(stpoint).split('-')
                ep = str(int(datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0).timestamp()))
                epochList.append(ep)
                days.append(str(stpoint))
                stpoint = stpoint + datetime.timedelta(1)
            days = days[:-1]
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            for i in range(fark):
                sql = 'SELECT mr_id, epoch FROM timestamps WHERE epoch>' + epochList[i] + ' AND epoch<' + epochList[
                    i + 1] + ' GROUP BY mr_id'
                cur.execute(sql)
                res = cur.fetchall()
                counts.append(len(res))

                # hangi vendordan kaç cihaz yakalandı?
                sql = 'SELECT vendor, COUNT(vendor) FROM mac_records WHERE id IN (SELECT mr_id FROM timestamps WHERE epoch>' + \
                      epochList[0] + ' AND epoch<' + epochList[-1] + ') GROUP BY(vendor)'
                cur.execute(sql)
                countvendor = cur.fetchall()
                cvx = []
                cvy = []
                for cv in countvendor:
                    cv = list(cv)
                    cvx.append(cv[0])
                    cvy.append(cv[1])

                data = {"sec": 1, "title": title, "counts": counts, "days": days, "cvx": cvx, "cvy": cvy}
            con.close()
            return render_template("dashboard.html", data=data)

    else:
        return "404"


@app.route('/api/', methods=['POST'])
def api():
    if request.method == 'POST':
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            icdata = request.get_data().decode("utf-8").strip()
            count = icdata.count(".txt")
            if count == 2:
                if icdata[-3:] == "---":
                    print("son req")
                    #print(icdata)
                    icdata = icdata.split('+')
                    icdata = icdata[1:]
                    icdata[-1] = icdata[-1].split('---')[0]
                else:
                    print("ilk req")
                    #print(icdata)
                    icdata = icdata.split('+')
                    icdata = icdata[1:]

            else:
                print("ara req")
                #print(icdata)
                icdata = icdata.split("+")
                icdata = icdata[1:]

            for line in icdata:
                line = line.split(" -> ")
                mac = line[0].upper()
                date = line[1].split(" *-* ")
                time = date[1].split(':')
                date = date[0].split('.')
                epoch = int(datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]),
                                              int(time[2])).timestamp())
                vendor = findVendor(mac)

                sql = 'SELECT id FROM mac_records WHERE mac = "' + mac + '"'
                cur.execute(sql)
                sres = cur.fetchall()
                if not sres:
                    err = False
                    try:
                        sql = 'INSERT INTO mac_records (mac, vendor) VALUES ("' + mac + '", "' + vendor + '")'
                        con.execute(sql)
                        con.commit()
                    except:
                        err = True
                        print("Yeni MAC eklenirken hata oluştu.")
                    if not err:
                        try:
                            sql = 'SELECT id FROM mac_records WHERE mac = "' + mac + '"'
                            cur.execute(sql)
                            id = cur.fetchall()
                            id = list(id[0])[0]
                            sql = 'INSERT INTO timestamps (mr_id, epoch) VALUES (' + str(id) + ', ' + str(epoch) + ')'
                            con.execute(sql)
                            con.commit()
                        except:
                            print("Yeni MAC timestamp eklenirken hata oluştu.")
                else:
                    try:
                        id = list(sres[0])[0]
                        sql = 'INSERT INTO timestamps (mr_id, epoch) VALUES (' + str(id) + ', ' + str(epoch) + ')'
                        con.execute(sql)
                        con.commit()
                    except:
                        print("MAC timestamp eklenirken hata oluştu.")
            return "success"
        except:
            return "fail"


def findVendor(mac):
    qmac = mac[0:8]
    sql = "SELECT mac,vendor FROM vendors WHERE mac LIKE '" + qmac + "%'"
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(sql)
    vendor = cur.fetchall()
    con.close()
    if (len(vendor) == 0):
        vendor = "Bulunamadı."
    elif (len(vendor) == 1):
        vendor = list(vendor[0])[1].strip()
    else:
        venDict = {}
        bit = int(list(vendor[1])[0].split('/')[1]) // 4
        tmp = bit // 2
        bit += tmp
        mainVendor = list(vendor[0])[1].strip()
        vendor = vendor[1:]
        for ven in vendor:
            ven = list(ven)
            venDict[ven[0][0:bit]] = ven[1].strip()
        vendor = venDict[mac[0:bit]]
        vendor = mainVendor + " -> " + vendor
    return vendor


if __name__ == '__main__':
    app.run(debug=True)
