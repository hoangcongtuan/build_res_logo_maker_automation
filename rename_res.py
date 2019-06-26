import os
res_folder = 'res'
list_dir = [f for f in os.listdir(res_folder) if not f.startswith('.')]

for dir in list_dir:
    list_file = [f for f in os.listdir(res_folder + '/' + dir) if not f.startswith('.')]
    index = 0
    print(f'processing dir: {dir}\n')
    for f in list_file:
        file_name, file_extension = os.path.splitext(f)
        old_name = res_folder + '/' + dir + '/' + f
        new_name =  f'{res_folder}/{dir}/{dir}_{index}{file_extension}'
        #res_folder + '/' + dir + '/' + dir + '_' + index + file_extension
        index = index + 1
        os.rename(old_name, new_name)
        print(f'\t{old_name} -> {new_name}\n')

print('rename all file finish!!')
    
