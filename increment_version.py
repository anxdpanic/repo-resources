# -*- coding: utf-8 -*-
import os
import re
import sys

GET_VERSION = re.compile(r'''<addon.+?version="(?P<version>[0-9.]+)"''', re.DOTALL)


def increment_version(version):
    version = version.split('.')
    version[2] = str(int(version[2]) + 1)
    return '.'.join(version)


def get_language_folders(chg_files):
    payload = []
    for chg_file in chg_files:
        if chg_file.startswith('resource.language') and \
                chg_file.endswith(('strings.po', 'langinfo.xml')):
            folder = os.path.split(chg_file)[0]
            payload.append(folder.split('/')[0])

    print('Files were modified in the following languages:')
    for language in payload:
        print('\t{language}'.format(language=language))

    return payload


def update_addon_xmls(lang_folders):
    addon_xmls = ['/'.join(['.', folder, 'addon.xml']) for folder in lang_folders]

    for addon_xml in addon_xmls:
        print('Reading {filename}'.format(filename=addon_xml))
        with open(addon_xml, 'r') as open_file:
            xml_content = open_file.read()

        version_match = GET_VERSION.search(xml_content)
        if not version_match:
            print('Unable to determine current version... skipping.', '')
            continue

        old_version = version_match.group('version')
        new_version = increment_version(old_version)
        print('\tOld Version: {version}'.format(version=old_version))
        print('\tNew Version: {version}'.format(version=new_version))

        new_xml_content = xml_content.replace(
            'version="{version}"'.format(version=old_version),
            'version="{version}"'.format(version=new_version),
        )

        if xml_content == new_xml_content:
            print('XML was unmodified... skipping.', '')
            continue

        print('Writing {filename}'.format(filename=addon_xml))
        with open(addon_xml, 'w') as open_file:
            open_file.write(new_xml_content)

        print('')


if __name__ == '__main__':
    changed_files = sys.argv
    if not changed_files:
        print('No changed files.')
        exit(0)

    language_folders = get_language_folders(changed_files)
    if not language_folders:
        print('No modified languages found.')
        exit(0)

    print('')

    update_addon_xmls(language_folders)

    print('')
