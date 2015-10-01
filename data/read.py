import os

os.chdir('recursive_example')

for case in os.listdir():
    print('%s'%case)
    os.chdir(case)

    for model in os.listdir():
        print('  %s'%model)
        os.chdir(model)

        for exp in os.listdir():
            print('    %s'%exp)
            os.chdir(exp)

            for ens in os.listdir():
                print('      %s'%ens)
                os.chdir(ens)

                for run in os.listdir():
                    print('        %s'%run)

                os.chdir('..')
            os.chdir('..')
        os.chdir('..')
    os.chdir('..')
os.chdir('..')





#for directory in os.walk('.'):
#    print(directory)

