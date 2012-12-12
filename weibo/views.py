# -*- coding: UTF-8 -*- 
# Create your views here.
from __future__ import division #true division
from django.shortcuts import render_to_response
import time
import mysqlconn

def home(request):
    return render_to_response('index.html')

#get the status of the fans, do some simple analysis
def status_fans(request):
    #connect to the mysql db
    conn = mysqlconn.dbconn()
    cursor = conn.cursor()

    #get sum of the fans
    sql = 'select count(*) from user;'
    cursor.execute(sql)
    sum = cursor.fetchone()[0]
    #get the female num
    sql = 'select count(*) from user where sex="f";'
    cursor.execute(sql)
    fnum = cursor.fetchone()[0]
    #the percentage of female
    fperc = round(fnum / sum, 4) * 100
    mperc = round((sum - fnum) / sum, 4) * 100
   
    #get the top10 area
    sql = 'select address, count(*) as num from user where address <> "其他" group by address order by num desc limit 0,10;'
    cursor.execute(sql)
    areadic = cursor.fetchall()
    areaname = []
    areanum = []
    for area in areadic:
        areaname.append(area[0].encode('utf8'))
        areanum.append(int(area[1]))

    thisyear = time.strftime('%Y',time.localtime(time.time())) #this year, like '2012'
    #get the num of each age interval
    sql = 'select count(*) from user where birthday > ' + thisyear + '-18;'
    cursor.execute(sql)
    age1 = cursor.fetchone()[0]
    sql = 'select count(*) from user where birthday <= ' + thisyear + '-18 and birthday >= ' + thisyear + '-24;'
    cursor.execute(sql)
    age2 = cursor.fetchone()[0]
    sql = 'select count(*) from user where birthday < ' + thisyear + '-24 and birthday >= ' + thisyear + '-34;'
    cursor.execute(sql)
    age3 = cursor.fetchone()[0]
    sql = 'select count(*) from user where birthday < ' + thisyear + '-34;'
    cursor.execute(sql)
    age4 = cursor.fetchone()[0]
    sum = age1 + age2 + age3 + age4
    age = []
    age.append(round(age1 / sum, 4) * 100)
    age.append(round(age2 / sum, 4) * 100)
    age.append(round(age3 / sum, 4) * 100)
    age.append(round(age4 / sum, 4) * 100)

    #get the last weibo sent from where
    sql = 'select count(*) from user_source;'
    cursor.execute(sql)
    sum = cursor.fetchone()[0]
    sql = 'select source, count(*) as num from user_source group by source order by num desc limit 12;'
    cursor.execute(sql)
    sentfrom = []
    for source, num in cursor.fetchall():
        sentfrom.append((source, round(num / sum, 4) * 100))

    #the distribution of the fans' tag
    sql = 'select count(*) from user_tag;'
    cursor.execute(sql)
    sum = cursor.fetchone()[0]
    sql = 'select tag, count(*) as num from user_tag group by tag order by num desc limit 10;'
    cursor.execute(sql)
    tagdic = cursor.fetchall()
    tag = []
    for t in tagdic:
        tag.append((t[0].encode('utf8'), round(t[1] / sum, 4) * 100))

    #close the cursor
    cursor.close()
    #disconnet the link to mysql db
    mysqlconn.dbclose(conn)


    return render_to_response('status.html', {'male':mperc, 'female':fperc, 'areaname':areaname, 'areanum':areanum, 'age':age, 'source':sentfrom, 'tag':tag})

#have a global look at the fans
def management_fans(request):
    p = 0
    type = 'null'
    if request.GET.has_key('p'):
        p = request.GET['p']
    if request.GET.has_key('type'):
        type = request.GET['type']
    #connect to the mysql
    conn = mysqlconn.dbconn()
    cursor = conn.cursor()
    sql = 'select user.screenname, user.sex, user.address, user.fansnumber, user.id from user, user_vector where user.id = user_vector.uid order by '+type+' desc limit '+str(int(p)*20)+',20;'
    cursor.execute(sql)
    fans = cursor.fetchall()
    print fans

    #close the cursor
    cursor.close()
    #disconnet the link to mysql db
    mysqlconn.dbclose(conn)
    

    return render_to_response('management_fans.html', {'fans':fans, 'page':int(p), 'type':type})
