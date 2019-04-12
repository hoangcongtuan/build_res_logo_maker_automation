import os
from os.path import isfile, join
layout_folder = 'layout'
layout_out_folder = 'out_layout'
list_file = [f for f in os.listdir(layout_folder) if (not f.startswith('.')) and isfile(join(layout_folder, f))]

for f in list_file:
    print(f)
    with open(join(layout_folder, f), 'rt') as fin:
        with open(join(layout_out_folder, f), 'wt') as fout:
            for line in fin:
                line = line.replace('android.support.v7.widget.RecyclerView', 'androidx.recyclerview.widget.RecyclerView')
                fout.write(line.replace('androidx.constraintlayout.ConstraintLayout', 'androidx.constraintlayout.widget.ConstraintLayout'))
print('rename all file finish!!')
    
