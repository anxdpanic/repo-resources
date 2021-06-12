# -*- coding: utf-8 -*-
import os
import sys

if __name__ == '__main__':
    changed_files = sys.argv
    if not changed_files:
        exit(0)

    language_folders = []
    for changed_file in changed_files:
        if changed_file.startswith('resource.language') and \
                changed_file.endswith(('strings.po', 'langinfo.xml')):
            folder = os.path.split(changed_file)[0]
            language_folders.append(folder.split(os.sep)[0])

    print('a' * 10, language_folders)
