import os
import sqlite3 as sqlite

font_folder = 'font'
src_db_path = 'db/logomaker_db.db'
dst_db_path = 'db/logo_maker.db'

src_conn = sqlite.connect(src_db_path)
dst_conn = sqlite.connect(dst_db_path)

src_cur = src_conn.cursor()
dst_cur = dst_conn.cursor()

dst_cur.execute('select * from font_category') 
rows = dst_cur.fetchall()
font_cate = []
for row in rows:
    name = row[1]
    print(name)
    font_cate.append(name)
print(f'font category = {font_cate}')

#clear
dst_cur.execute('delete from font_info')

rows = src_cur.execute('select * from fontsmaster')
for row in rows:
    index = font_cate.index(row[4])
    if index == -1:
        print(f'font id = {row[0]} error')
    else:
        sql = f'insert into font_info(res_id, category_id, subtitle_font) values("{row[1]}", "{index}", "{1 if row[5] == "SubtitleFont" else 0}")'
        dst_cur.execute(sql)

dst_conn.commit()

src_cur.close()
del src_cur

dst_cur.close()
del dst_cur

src_conn.close()
dst_conn.close()

print('build font db finish!')





