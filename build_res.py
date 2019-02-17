from sklearn.cluster import KMeans
import utils
import cv2
import os
import time
from colormap import hex2rgb
import sqlite3 as sqlite

res_folder = 'res'
list_dir = [f for f in os.listdir(res_folder) if not f.startswith('.')]

#read config file
defaul_color_dir = []
default_color = '#000000'
is_bound_dir = []
f_config = open('config.txt', 'r')
for line in f_config:
    line = line.strip()
    params = line.split(' ')
    if (len(params) == 0):
        break
    cmd = params[0]
    if cmd == 'default_color':
        default_color = params[1]
        defaul_color_dir = params[2:len(params)]
        print(f'default color = {default_color}')
        print(f'defaut color dir = {defaul_color_dir}')
    else: 
        if cmd == 'is_bound':
            is_bound_dir = params[1: len(params)]
            print(f'is bound dir = {is_bound_dir}')

f_config.close()

#find primary, secondary color and build db      
db_path = 'db/logo_maker.db'
conn = sqlite.connect(db_path)
cursor = conn.cursor()

#clear
cursor.execute('delete from sticker_model')
conn.commit()

for dir in list_dir:
    list_file = [f for f in os.listdir(res_folder + '/' + dir) if not f.startswith('.')]
    index = 0
    print(f'processing dir: {dir}\n')
    for f in list_file:

        res_path = f'{dir}/{f}'
        if dir in defaul_color_dir:
            sql = f'insert into sticker_model(res_id, res_boudary, primary_color, secondary_color) values("{res_path}", "{1 if dir in is_bound_dir else 0}", "{default_color}", "{default_color}")'
        else:
            if dir in is_bound_dir:
                sql = f'insert into sticker_model(res_id, res_boudary, primary_color, secondary_color) values("{res_path}", "1", "{default_color}", "{default_color}")'
            else:
                file_path = res_folder + '/' + dir + '/' + f
                image = cv2.imread(file_path)
                image = cv2.resize(image,None,fx=0.2,fy=0.2)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = image.reshape((image.shape[0] * image.shape[1], 3))
                clt = KMeans(n_clusters = 3)
                clt.fit(image)

                hist = utils.centroid_histogram(clt)
                try:
                    primaryColor, secondaryColor = utils.findPri_Sec(hist, clt.cluster_centers_)
                except:
                    print("error")
                    primaryColor, secondaryColor = '#000000', '#000000'
                sql = f'insert into sticker_model(res_id, res_boudary, primary_color, secondary_color) values("{res_path}", "0", "{primaryColor}", "{secondaryColor}")'
        cursor.execute(sql)
conn.commit()
print("Build finish!")