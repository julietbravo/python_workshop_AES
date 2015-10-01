import os

os.mkdir('recursive_example')
os.chdir('recursive_example')

names  = ('case_1','case_2','case_3','case_4')
models = ('model_1','model_2','model_3','model_4')
runs   = ('exp_1','exp_2','exp_3','exp_4')
ens    = ('ens_1','ens_2','ens_3','ens_4')

for name in names:
    os.mkdir(name)
    os.chdir(name)

    for model in models:
        os.mkdir(model)
        os.chdir(model)

        for run in runs:
            os.mkdir(run)
            os.chdir(run)

            for en in ens:
                os.mkdir(en)
                os.chdir(en)

                f = open('data.txt', 'w')
                f.write('this is data')
                f.close()

                os.chdir('..')
            os.chdir('..')
        os.chdir('..')
    os.chdir('..')
os.chdir('..')
