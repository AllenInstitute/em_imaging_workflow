import os

def chmod_directory(chmod_dir, dir_only=True):
    if dir_only is False:
        os.system(
            'find %s -type f -print -exec chmod go+r {} \;' % (
                chmod_dir))
    os.system(
        'find %s -type d -print -exec chmod go+rx {} \;' % (
            chmod_dir))

