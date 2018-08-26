import os


def showfile(path):
    import os
    for cpath in os.listdir(path):
        cpath = os.path.join(path, cpath)
        if os.path.isdir(cpath):
            showfile(cpath)
        else:
            print(cpath)

showfile('.')