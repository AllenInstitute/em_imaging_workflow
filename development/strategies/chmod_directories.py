import os

def chmod_directory(chmod_dir):
    os.system(
        'find %s -type f -print -exec chmod go+r {} \;' % (
            chmod_dir))
    os.system(
        'find %s -type d -print -exec chmod go+rx {} \;' % (
            chmod_dir))

