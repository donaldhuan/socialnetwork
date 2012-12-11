# -*- coding: UTF-8 -*- 
import MySQLdb



conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='weibo', port=3306, charset='utf8')
cur = conn.cursor()
cur.execute('select address, count(*) as num from user where address <> "其他" group by address order by num desc limit 0,10;')
res = cur.fetchall()
for i in res:
    a = i[0]
    b = i[1]
    print a,b

cur.close()
conn.close()
