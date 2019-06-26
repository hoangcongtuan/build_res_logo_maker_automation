import os
import json
import re

def get_label(dir):
    return ''.join(i for i in dir if not i.isdigit()).strip()

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


art_folder = 'art'
list_dir = [f for f in os.listdir(art_folder) if not f.startswith('.')]
list_dir = sorted_aphanumeric(list_dir)
#print(list_dir)
art_dict = {}
for dir in list_dir:
    art_dict[dir] = get_label(dir)
json_art = json.dumps(art_dict)

print(json_art)
with open('art_info.json', 'w') as f_art:
    json.dump(json_art, f_art, ensure_ascii=False)

print('rename all file finish!!')


