import os

base_dir = os.getcwd()

for layers in [2, 3, 4, 5, 6]:
    for pw in [300, 400, 500, 600, 700]:
        for kpts in [3, 4, 5, 6, 7]:
            os.chdir('./runs/layers_{}/pw_{}/kpts{}_{}_1'.format(layers,
                                                                pw,
                                                                kpts,kpts))
            if not os.path.isfile('energy.txt'):
                print(layers, pw, kpts)
            os.chdir(base_dir)
