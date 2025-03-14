import WriteData

import json


def read_files(destination, suffix):

    with open(f'{destination}.{suffix}', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def rearrange_license_inconsistency(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_name = json_obj['package_name']

        licenses = json_obj['licenses']

        if len(licenses) <= 0:
            continue
        
        if len(licenses) == 1:
            print(f'{package_name}: {licenses}')
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/question7_extract_final_registry_consistency')
            continue

        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_final')


def get_license_information(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    dict_license = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']

        license = json_obj['license']

        dict_license[package_link] = license
    
    return dict_license
        

def get_real_license(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    if question == 'question5':
        dict_nodejs = get_license_information(folder, question, 'package_total_nodejs_request')
    else:
        dict_nodejs = get_license_information(folder, question, 'package_total_nodejs_new_request')

    dict_python = get_license_information(folder, question, 'package_total_python_new_request')
    dict_php = get_license_information(folder, question, 'package_total_php_new_request')
    dict_ruby = get_license_information(folder, question, 'package_total_ruby_new_request')
    dict_perl = get_license_information(folder, question, 'package_total_perl_new_request')

    print(f'nodejs: {len(dict_nodejs)}')
    print(f'python: {len(dict_python)}')
    print(f'php: {len(dict_php)}')
    print(f'ruby: {len(dict_ruby)}')
    print(f'perl: {len(dict_perl)}')

    count = len(dict_nodejs) + len(dict_python) + len(dict_php) + len(dict_ruby) + len(dict_perl)
    print(f'total: {count}')

    total = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_name = json_obj['package_name']

        registry = json_obj['registry']

        licenses = json_obj['licenses']
        

        if registry == 'npm':
            link = f'https://registry.npmjs.org/{package_name}'
            if link in dict_nodejs.keys():
                json_obj['real_license'] = dict_nodejs[link]
                total += 1
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_real_licenses')

        elif registry == 'pip':
            link = f'https://pypi.org/pypi/{package_name}/json'
            if link in dict_python.keys():
                json_obj['real_license'] = dict_python[link]
                total += 1
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_real_licenses')

        elif registry == 'gem':
            link = f'https://rubygems.org/api/v1/gems/{package_name}.json'
            if link in dict_ruby.keys():
                json_obj['real_license'] = dict_ruby[link]
                total += 1
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_real_licenses')

        elif registry == 'composer':
            link = f'https://packagist.org/packages/{package_name}.json'
            if link in dict_php.keys():
                json_obj['real_license'] = dict_php[link]
                total += 1
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_real_licenses')

        elif registry == 'cpan':
            link = f'https://fastapi.metacpan.org/v1/module/{package_name}'
            if link in dict_perl.keys():
                json_obj['real_license'] = dict_perl[link]
                total += 1
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_real_licenses')
                
        
    print(total)


def translate_license(license):
    dict_license = {
        'MIT': 'MIT/X11',
        "[MIT]https://github.com/Azure/MachineLearningNotebooks/blob/master/LICENSE": "MIT/X11",
        "[MIT]https://github.com/jezdez/collectfast/blob/master/LICENSE": "MIT/X11", 
        "[MIT]https://github.com/pmndrs/react-three-fiber/blob/master/LICENSE": "MIT/X11", 
        "[MIT]https://github.com/ipdata-co/ipdata/blob/master/LICENSE": "MIT/X11", 
        "[MIT]https://opensource.org/licenses/MIT": "MIT/X11", 
        "[MIT]https://github.com/PyYAML/pyyaml/blob/master/LICENSE": "MIT/X11", 
        "[MIT]https://github.com/locativejs/location-api/blob/master/LICENSE": "MIT/X11", 
        "Apache-2.0": "Apache 2.0", 
        "MPL-1.1": "MPL 1.1", 
        "GPLv3+": "GPLv3 or GPLv3+", 
        "LGPLv2.1": "LGPLv2.1", 
        "BSD-3-Clause": "BSD-new", 
        "LGPLv2.1+": "LGPLv2.1+", 
        "GPL-3.0-or-later": "GPLv3 or GPLv3+", 
        "GPLv2": "GPLv2", 
        "LGPL-2.1-or-later": "LGPLv2.1+", 
        "GPLv2+": "GPLv2+", 
        "GPLv3": "GPLv3 or GPLv3+", 
        "LGPL-2.1": "LGPLv2.1", 
        "GPL-3.0": "GPLv3 or GPLv3+", 
        "LGPL-3.0": "LGPLv3 or LGPLv3+", 
        "GPL-2.0-or-later": "GPLv2+", 
        "${Apache-2.0}": "Apache 2.0", 
        "GPL-2.0": "GPLv2", 
        "public": "Public Domain", 
        "LGPLv3+": "LGPLv3 or LGPLv3+", 
        "LGPL-2.1+": "LGPLv2.1+", 
        "LGPLv3": "LGPLv3 or LGPLv3+", 
        "Public-Domain": "Public Domain", 
        "mit": "MIT/X11", 
        "public-domain": "Public Domain", 
        "apache-2.0": "Public Domain", 
        "GNU-General-Public-v3.0": "GPLv3 or GPLv3+", 
        "LGPL-3.0-or-later": "LGPLv3 or LGPLv3+", 
        "GPL-3": "GPLv3 or GPLv3+", 
        "BSD-3": "BSD-new", 
        "LGPLv2+": "LGPLv2.1+",
        "Public": "Public Domain",
        "GPL-3.0+": "GPLv3 or GPLv3+",
        "LGPL-3": "LGPLv3 or LGPLv3+",
        "GPL-2": "GPLv2",
        "GPL-v3+": "GPLv3 or GPLv3+",
        "GPL-2.0+": "GPLv2+",
        "BSD-3-Clause*": "BSD-new",
        "GNU-General-Public-v2.0": "GPLv2",
        "BSD-new": "BSD-new",
        "GPL-v3": "GPLv3 or GPLv3+",
        "GPL-3.0-only": "GPLv3 or GPLv3+",
        "MIT/X11": "MIT/X11",
        "GPL-2.0-only": "GPLv2",
        "LGPL-2.1-only": "LGPLv2.1",
        "GPL-v3.0": "GPLv3 or GPLv3+",
        "GPL-2+": "GPLv2+",
        "Apache_2_0": "Apache 2.0",
        "LGPL-3.0-only": "LGPLv3 or LGPLv3+",
        "LGPL-v3": "LGPLv3 or LGPLv3+",
        "Apache_2.0": "Apache 2.0",
        "GPL_2": "GPLv2",
        "LGPL-2.2": "LGPLv2.1+", 
        "LGPL_2_1": "LGPLv2.1", 
        "GPL_3": "GPLv3 or GPLv3+", 
        "Apache-2_0": "Apache 2.0", 
        "GPL3": "GPLv3 or GPLv3+", 
        "LGPL-3.0+": "LGPLv3 or LGPLv3+", 
        "GPL2": "GPLv2", 
        "LGPL_3": "LGPLv3 or LGPLv3+", 
        "bsd-3-clause": "BSD-new", 
        "MIT.": "MIT/X11", 
        "BSD-3-Clause.": "BSD-new", 
        "gplv3": "GPLv3 or GPLv3+", 
        "GPLv2+.": "GPLv2", 
        "Apache-2.0.": "Apache 2.0", 
        "GPLv2.": "GPLv2", 
        "GPL-3+": "GPLv3 or GPLv3+"
    }

    if license in dict_license.keys():
        return dict_license[license]
    else:
        return ""


def translate_real_license(license):
    dict_license = {
        'MIT/X11': 'MIT/X11',
        "Apache 2.0": "Apache 2.0", 
        "GPL-3.0": "GPLv3 or GPLv3+", 
        "BSD-3-Clause": "BSD-new",
        "Public Domain": "Public Domain", 
        "GPLv3": "GPLv3 or GPLv3+", 
        "GPLv3+": "GPLv3 or GPLv3+", 
        "mit": "MIT/X11",
        "BSD-2-Clause,GPL-3.0-only,icalendar": "GPLv3 or GPLv3+", 
        "GPL-2.0": "GPLv2", 
        "LGPLv3": "LGPLv3 or LGPLv3+", 
        "GPL-3.0+": "GPLv3 or GPLv3+", 
        "apache_2_0": "Apache 2.0", 
        "(GPL-2.0 OR LGPL-2.1 OR MPL-1.1)": "GPLv2", 
        "BSD 3-Clause License": "BSD-new", 
        "GPL-2.0-or-later": "GPLv2+", 
        "3-clause BSD": "BSD-new",
        "BSD3": "BSD-new",
        "LGPL 3": "LGPLv3 or LGPLv3+",
        "LGPL-2.1-or-later": "LGPLv2.1+",
        "unknown,lgpl_2_1": "LGPLv2.1", 
        "unknown,artistic_1,gpl_2": "GPLv2", 
        "Ruby's,GPLv2 or later": "GPLv2+", 
        "GPLv2": "GPLv2", 
        "apache": "Apache 2.0", 
        "New BSD": "BSD-new", 
        "LGPL-3.0-only": "LGPLv3 or LGPLv3+", 
        "GPL3": "GPLv3 or GPLv3+", 
        "BSD 3-Clause": "BSD-new", 
        "GPL-2.0+,Ruby": "GPLv2+", 
        "APACHE2": "Apache 2.0", 
        "GPL-3.0-or-later": "GPLv3 or GPLv3+", 
        "LGPL-2.1+": "LGPLv2.1+", 
        "LGPLv3+": "LGPLv3 or LGPLv3+", 
        "LGPL-3.0": "LGPLv3 or LGPLv3+", 
        "public domain": "Public Domain", 
        "apache-2.0": "Apache 2.0", 
        "GPL-2.0+,Ruby-1.8": "Apache 2.0", 
        "GNU GPLv3+": "GPLv3 or GPLv3+", 
        "LGPL 2.1+": "LGPLv2.1+", 
        "Public domain": "Public Domain", 
        "New BSD License": "BSD-new", 
        "GNU GPL v3": "GPLv3 or GPLv3+", 
        "GPL v3 or later": "GPLv3 or GPLv3+", 
        "LGPLv2+": "LGPLv2.1+", 
        "GNU General Public License v3": "GPLv3 or GPLv3+", 
        "GNU GPLv3": "GPLv3 or GPLv3+", 
        "Ruby,LGPLv3+": "GPLv3 or GPLv3+", 
        "GPL v2": "GPLv2", 
        "GPL2": "GPLv2", 
        "3-Clause BSD License": "BSD-new", 
        "LGPL-3.0-or-later": "LGPLv3 or LGPLv3+", 
        "GNU LESSER GENERAL PUBLIC LICENSE Version 3": "GPLv3 or GPLv3+", 
        "BSD 3-clause": "BSD-new", 
        "gpl_2": "GPLv2", 
        "LGPL v3": "LGPLv3 or LGPLv3+", 
        "GNUv3": "GPLv3 or GPLv3+", 
        "GPL v3.0": "GPLv3 or GPLv3+", 
        "BSD-3": "BSD-new", 
        "Ruby,GPL2": "GPLv2", 
        "lgpl_2_1": "LGPLv2.1", 
        "GPL-2": "GPLv2", 
        "LGPL-3": "LGPLv3 or LGPLv3+", 
        "APACHE-2.0": "Apache 2.0", 
        "GNU GPL 3": "GPLv3 or GPLv3+", 
        "GPL v3": "GPLv3 or GPLv3+", 
        "(LGPL-2.1+ OR GPL-2.0)": "GPLv2", 
        "LGPL 2.1": "LGPLv2.1", 
        "LGPL-2.1-only": "LGPLv2.1",
        "GNU General Public License v3 or later (GPLv3+)": "GPLv3 or GPLv3+",
        "New-BSD": "BSD-new", 
        "(BSD-2-Clause OR GPL-2.0-only)": "GPLv2", 
        "EPL-2.0 OR BSD-3-Clause": "BSD-new",
        "APLv2": "Apache 2.0",
        "APACHE2_0": "Apache 2.0",
        "GNU LGPL v2.1": "LGPLv2.1",
        "BSD-3-Clause,GPL-2.0-only,GPL-3.0-only": "GPLv3 or GPLv3+",
        "LGPL-3.0+": "LGPLv3 or LGPLv3+",
        "GPL-3.0-only": "GPLv3 or GPLv3+", 
        "LGPL version 2.1": "LGPLv2.1",
        "LGPL-2.1": "LGPLv2.1",
        "GPL-2.0+,Nonstandard": "GPLv2+",
        "LGPL-3.0-only,Commercial": "LGPLv3 or LGPLv3+",
        "GPL-2.0+": "GPLv2+",
        "LGPL3": "LGPLv3 or LGPLv3+",
        "GPL 3": "GPLv3 or GPLv3+",
        "LGPL 2.1 or later": "LGPLv2.1+",
        "GPLv3 License": "GPLv3 or GPLv3+",
        "LGPLv2.1": "LGPLv2.1",
        "GNU LGPL 3.0": "LGPLv3 or LGPLv3+",
        "GNU LGPL v3+": "LGPLv3 or LGPLv3+",
        "GNU General Public License v3.0": "GPLv3 or GPLv3+",
        "GPL-3": "GPLv3 or GPLv3+",
        "GNU GPLv2 or any later version": "GPLv2+",
        "GNU v3": "GPLv3 or GPLv3+",
        "GPL 2.0": "GPLv2",
        "gpl-3.0": "GPLv3 or GPLv3+",
        "GNU GPL3": "GPLv3 or GPLv3+",
        "GNU GENERAL PUBLIC LICENSE Version 3": "GPLv3 or GPLv3+",
        "LGPLv2.1+": "LGPLv2.1+",
        "License :: GNU GPLv3": "GPLv3 or GPLv3+",
        "GNU Lesser General Public License v3 (LGPLv3)": "LGPLv3 or LGPLv3+",
        "GPL V3+": "GPLv3 or GPLv3+",
        "(BSD-3-Clause OR GPL-2.0)": "GPLv2",
        "GNU General Public License v3 (GPLv3)": "GPLv3 or GPLv3+",
        "GNU Lesser General Public License v3+": "GPLv3 or GPLv3+",
        "GUN V3": "GPLv3 or GPLv3+",
        "GNU GENERAL PUBLIC LICENSE Version 2": "GPLv2", 
        "GPL-3.0 License": "GPLv3 or GPLv3+",
        "GPL-2.0-only": "GPLv2",
        "BSD-3-Clause-Clear": "BSD-new",
        "BSD (3-clause)": "BSD-new",
        "GPL 2": "GPLv2",
        "new BSD": "BSD-new",
        "LGPL Version 3": "LGPLv3 or LGPLv3+", 
        "LGPL 3.0": "LGPLv3 or LGPLv3+",
        "GPLv2+": "GPLv2+",
        "gpl_3": "GPLv3 or GPLv3+",
        "BSD-3-Clause OR AFL-2.1": "BSD-new",
        "GNU AFFERO GENERAL PUBLIC LICENSE (v3)": "GPLv3 or GPLv3+",
        "New BSD license": "BSD-new",
        "GNU3": "GPLv3 or GPLv3+",
        "GNU General Public License v2 or later (GPLv2+)": "GPLv2+",
        "GNU General Public License v3 or greater": "GPLv3 or GPLv3+",
        "GNU GPL version 3": "GPLv3 or GPLv3+",
        "BSD-3  Copyright 2022 Matthew Newville": "BSD-new",
        "GNU General Public License (GPL) v3": "GPLv3 or GPLv3+",
        "three-clause BSD": "BSD-new",
        "GLPv3": "GPLv3 or GPLv3+",
        "lgplv3+": "LGPLv3 or LGPLv3+",
        "LGPL 3.0 or later": "LGPLv3 or LGPLv3+",
        "GNU GPL (3.0)": "GPLv3 or GPLv3+",
        "BSD-3-Clause-Attribution": "BSD-new",
        "GPL 3.0": "GPLv3 or GPLv3+",
        "GPL-2.0 License": "GPLv2",
        "LGPL-3.0-or-newer": "LGPLv3 or LGPLv3+", 
        "GNUGPL-v3": "GPLv3 or GPLv3+",
        "LGPL 2.1 License": "LGPLv2.1",
        "GPL 2+": "GPLv2+",
        "BSD New": "BSD-new",
        "Ruby,GPL-2.0": "GPLv2",
        "new BSD License": "BSD-new",
        "BSD 3-clause license": "BSD-new",
        "GNU GPL-3 or later": "GPLv3 or GPLv3+",
        "[{'type': 'GPL v3', 'url': 'http://www.gnu.org/licenses/gpl.html'}]": "GPLv3 or GPLv3+",
        "BSD 3.0": "GPLv3 or GPLv3+", 
        "apache2.0 (http://www.apache.org/licenses/LICENSE-2.0)": "Apache 2.0", 
        "LGPL3+": "LGPLv3 or LGPLv3+", 
        "GPLV3": "GPLv3 or GPLv3+",
        "BSD 3 clause": "BSD-new", 
        'BSD 3-clause "New" or "Revised" License': "BSD-new",
        "GNU Lesser General Public License v3 or later (LGPLv3+)": "LGPLv3 or LGPLv3+", 
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)": "GPLv3 or GPLv3+", 
        "BDS-3-Clause": "BSD-new", 
        "GPL V3": "GPLv3 or GPLv3+", 
        "BSD 3": "BSD-new", 
        "GNU/LGPLv3": "LGPLv3 or LGPLv3+", 
        "GPL-v3": "GPLv3 or GPLv3+", 
        "Ruby,GPL-2.0-or-later": "GPLv2+", 
        "(new) BSD": "BSD-new", 
        "LGPL2.1+ (the library)": "LGPLv2.1+", 
        "http://www.gnu.org/licenses/gpl-3.0.html": "GPLv3 or GPLv3+", 
        "New BSD License (http://www.opensource.org/licenses/bsd-license.php)": "BSD-new", 
        "# GNU GENERAL PUBLIC LICENSE ## Version 3": "GPLv3 or GPLv3+", 
        "Ruby,GPL-3.0": "GPLv3 or GPLv3+", 
        "GNU GENERAL PUBLIC LICENSE  Version 2": "GPLv2", 
        "https://www.apache.org/licenses/LICENSE-2.0": "Apache 2.0", 
        "http://opensource.org/licenses/apache2.0.php": "Apache 2.0", 
        "BSD License (3-Clause)": "BSD-new", 
        "GNU GPLv3.0": "GPLv3 or GPLv3+", 
        "GNU General Public License version 3.0 (GPLv3)": "GPLv3 or GPLv3+", 
        "https://opensource.org/licenses/LGPL-3.0": "LGPLv3 or LGPLv3+", 
        "APACHE 2.0": "Apache 2.0", 
        "GPL/V3": "GPLv3 or GPLv3+", 
        "GPLv3 or later": "GPLv3 or GPLv3+", 
        "BSD-3-Clause-Modification": "BSD-new", 
        "Mit": "MIT/X11", 
        "GNU General Public License Version 3": "GPLv3 or GPLv3+",
        "3-clause BSD License": "BSD-new", 
        "BSD-3-Clause License": "BSD-new", 
        "GNU Public License version 3": "GPLv3 or GPLv3+", 
        "GPL-2+": "GPLv2", 
        "{'license': 'GPL-3.0'}": "GPLv3 or GPLv3+", 
        "http://www.apache.org/licenses/LICENSE-2.0": "Apache 2.0", 
        "Public domain(unlicense)": "Public Domain", 
        "http://www.apache.org/licenses/LICENSE-2.0.html": "Apache 2.0", 
        "BSD-3.0": "BSD-new", 
        '3-Clause ("New") BSD license': "BSD-new", 
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)": "GPLv3 or GPLv3+", 
        "LGPL v2.1": "LGPLv2.1", 
        "GNU GPL v2 or later": "GPLv2+", 
        "GPL2+": "GPLv2+", 
        "GNU GPL v2": "GPLv2", 
        "LGPL (version 3 or later)": "LGPLv3 or LGPLv3+", 
        "GPLv3.0": "GPLv3 or GPLv3+", 
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)": "GPLv2+", 
        "3-Clause BSD": "BSD-new", 
        "GNU Lesser General Public License v2.1 (LGPLv2.1)": "LGPLv2.1", 
        "GPL-3.0 license": "GPLv3 or GPLv3+", 
        "lgpl_3_0": "GPLv3 or GPLv3+", 
        "http://opensource.org/licenses/GPL-3.0": "GPLv3 or GPLv3+", 
        "GNU LESSER GENERAL PUBLIC LICENSE Version 2.1": "LGPLv2.1", 
        "GPL v 3": 'GPLv3 or GPLv3+', 
        "NEW BSD LICENSE: http://www.opensource.org/licenses/bsd-license.php": "BSD-new", 
        "3-clause BSD <https://opensource.org/licenses/bsd-license.php>": "BSD-new",
        "X11": "MIT/X11", 
        "GNU GPL v2+": "GPLv2+", 
        "bsd-3-clause": "BSD-new", 
        "LGPLv2.1 or later": "LGPLv2.1+", 
        "gpl3": "GPLv3 or GPLv3+", 
        "LGPL v3 or later": "LGPLv3 or LGPLv3+", 
        "GNU GPL v2.0": "GPLv2", 
        "apache license 2.0": "Apache 2.0", 
        "GNU Lesser General Public License v3 or late": "LGPLv3 or LGPLv3+",
        "GNU Public License v3.0": "GPLv3 or GPLv3+"
    }

    if license in dict_license.keys():
        return dict_license[license]
    else:
        return ""


def get_unique_license(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    obtain_license = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj['licenses'][0]

        real_license = json_obj['real_license']

        if real_license is None:
            continue

        real_license = str(real_license).replace('\t', '')

        if "Apache" in real_license and "MIT" in real_license:
            real_license = "Apache 2.0"
        elif "Apache" in real_license:
            real_license = "Apache 2.0"
        elif "MIT" in real_license:
            real_license = 'MIT/X11'
        elif 'BSD 3-Clause' in real_license: 
            real_license = "BSD 3-Clause"
        elif "Public Domain" in real_license:
            real_license = "Public Domain"


        # if real_license not in obtain_license:
        #     obtain_license.append(real_license)

    # print(len(obtain_license))
    # for license in obtain_license:
    #     translate_real = translate_real_license(license)
    #     if translate_real == "":
    #         print(license)

        translate_obtain = translate_license(licenses)
        translate_real = translate_real_license(real_license)

        if translate_obtain == translate_real and translate_obtain != "":
            json_obj['translate_license'] = translate_obtain
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_accurate')
        else:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_inaccurate')


def get_unique_license_filter(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    unique_license = []
    

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj['licenses'][0]

        if licenses not in unique_license:
            unique_license.append(licenses)

        # if licenses in filter_license:
        #     continue

        # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/{filename}_filter')

    total = 0
    add = []
    rest = len(unique_license)
    for license in unique_license:
        total += 1
        add.append(license)
        

        if  total % 300 == 0 and rest > 300:
            print(rest)
            rest = rest - 300
            print(add)
            add = []
        
    print(add)
    # print(unique_license)
            




def read_count(folder, question):
    destination = f'{folder}/{question}/{question}_extract_final_registry_inconsistency_new_final'

    all_lines = read_files(destination, 'json')

    destination2 = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter'

    all_lines2 = read_files(destination2, 'json')

    print(len(all_lines))

    print(len(all_lines2))

    total = len(all_lines) + len(all_lines2)

    count = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj['licenses']

        if len(licenses) >= 5:
            count += 1


    # precentage = (len(all_lines2) / total) * 100
    # precentage = (len(all_lines) / total) * 100

    precentage = (count / total) * 100

    # print(f'total: {total}')
    print(f'precentage: {precentage}')



def read_inaccurate_count(folder, question):
    destination = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter_real_licenses_inaccurate'

    all_lines = read_files(destination, 'json')

    # destination2 = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter_real_licenses_accurate'

    # all_lines2 = read_files(destination2, 'json')

    destination2 = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter_real_licenses'

    all_lines2 = read_files(destination2, 'json')

    destination3 = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter'

    all_lines3 = read_files(destination3, 'json')

    print(f'inaccurate: {len(all_lines)}')

    print(f'real_licenses: {len(all_lines2)}')

    print(f'consistency: {len(all_lines3)}')

    valid_precentage = (len(all_lines2) / len(all_lines3)) * 100

    inaccuracy_precentage = (len(all_lines) / len(all_lines2)) * 100

    print(f'valid_precentage: {valid_precentage}')

    print(f'inaccuracy_precentage: {inaccuracy_precentage}')


def calculate_inaccurate_license(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    license_obj = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj['licenses'][0]

        if licenses not in license_obj.keys():
            license_obj[licenses] = 1
        else:
            license_obj[licenses] += 1
    
    sorted_dict = dict(sorted(license_obj.items(), key=lambda item: item[1], reverse=True))

    print(sorted_dict)


def get_prompts_accurate_packages(folder, question):
    destination = f'{folder}/{question}/{question}'

    all_lines = read_files(destination, 'json')

    destination1 = f'{folder}/{question}/{question}_extract_final_registry'

    all_lines1 = read_files(destination1, 'json')

    destination2 = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter_real_licenses_accurate'

    all_lines2 = read_files(destination2, 'json')

    accurate_license = {}
    for line in all_lines2:
        json_obj = json.loads(line.rstrip())
        package_name = json_obj['package_name']
        translate_license = json_obj['translate_license']

        accurate_license[package_name] = translate_license
    

    specified_license = {}
    for line in all_lines:
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']
        title = obj['title']
        specified = title.split(',')[0].replace('my software is under ', '')

        specified_license[custom_id] = specified
    
    for line in all_lines1:
        new_obj = json.loads(line.rstrip())
        custom_id = new_obj['custom_id']

        package_information = new_obj['package_information']

        if len(package_information) <= 0:
            continue

        package_name = package_information[0]

        if isinstance(package_name, list):
            package_name = package_name[0]

        if package_name in accurate_license.keys():
            obj1 = {}
            obj1['custom_id'] = custom_id
            obj1['package_name'] = package_name
            obj1['specified_license'] = specified_license[custom_id]
            obj1['license'] = accurate_license[package_name]

            WriteData.write_in_path(json.dumps(obj1), f'{folder}/{question}/{question}_accurate_precompatibility')


def get_prompts_accurate_packages_q7(folder, question):
    destination = f'{folder}/{question}/{question}'

    all_lines = read_files(destination, 'json')

    destination1 = f'{folder}/{question}/{question}_extract_final_registry'

    all_lines1 = read_files(destination1, 'json')

    destination2 = f'{folder}/{question}/{question}_extract_final_registry_consistency_filter_real_licenses_accurate'

    all_lines2 = read_files(destination2, 'json')

    accurate_license = {}
    for line in all_lines2:
        json_obj = json.loads(line.rstrip())
        package_name = json_obj['package_name']
        translate_license = json_obj['translate_license']

        accurate_license[package_name] = translate_license
    

    specified_license = {}
    for line in all_lines:
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']
        title = obj['title']
        specified = title.split(',')[0].replace('my software is under ', '')

        specified_license[custom_id] = specified
    
    for line in all_lines1:
        new_obj = json.loads(line.rstrip())
        custom_id = new_obj['custom_id']

        package_information = new_obj['package_information']

        new_package_array = []

        if len(package_information) <= 0:
            continue

        for package_array in package_information:

            if len(package_array) <= 0:
                continue

            package_name = package_array[0]

            if isinstance(package_name, list):
                package_name = package_name[0]

            if package_name in accurate_license.keys():
                new_package_array.append([package_name, accurate_license[package_name]])
                
        if len(new_package_array) <= 0:
            continue

        obj1 = {}
        obj1['custom_id'] = custom_id
        obj1['specified_license'] = specified_license[custom_id]
        obj1['packages_licenses'] = new_package_array
        WriteData.write_in_path(json.dumps(obj1), f'{folder}/{question}/{question}_accurate_precompatibility')


def incompatibility_license_check(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    strongly_protective = ["GPLv2", "GPLv2+", "GPLv3 or GPLv3+", "GPLv3", "GPLv3+"]

    incompatibility = {
        "Apache 2.0": ["MPL 1.1", "LGPLv2.1", "GPLv2", "LGPLv2.1+"],
        "GPLv2": ["Apache 2.0"], 
        "LGPLv2.1": ["Apache 2.0"], 
        "MPL 1.1": ["Apache 2.0"], 
        "LGPLv2.1+": ["Apache 2.0"] 
        # "GPLv2+": ["Apache 2.0"]
    }

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        specified_license = json_obj['specified_license']
        license = json_obj['license']

        if license in strongly_protective and specified_license not in strongly_protective:
            total += 1
            print(f'{specified_license}, {license}')

        elif specified_license in incompatibility.keys() and license in incompatibility[specified_license]:
            total += 1
            print(f'{specified_license}, {license}')

    print(total)


def incompatibility_license_check_q7(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    strongly_protective = ["GPLv2", "GPLv2+", "GPLv3 or GPLv3+", "GPLv3", "GPLv3+"]

    incompatibility = {
        "Apache 2.0": ["MPL 1.1", "LGPLv2.1", "GPLv2", "LGPLv2.1+"],
        "GPLv2": ["Apache 2.0"], 
        "LGPLv2.1": ["Apache 2.0"], 
        "MPL 1.1": ["Apache 2.0"], 
        "LGPLv2.1+": ["Apache 2.0"] 
        # "GPLv2+": ["Apache 2.0"]
    }

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        specified_license = json_obj['specified_license']
        packages_licenses = json_obj['packages_licenses']

        new_package_array = []

        for package_array in packages_licenses:
            license = package_array[1]

            if license in strongly_protective and specified_license not in strongly_protective:
                new_package_array.append([specified_license, license])

            elif specified_license in incompatibility.keys() and license in incompatibility[specified_license]:
                new_package_array.append([specified_license, license])

            if license in incompatibility.keys():
                print(f"{specified_license}, {license}")

        if len(new_package_array) > 0:
            print(new_package_array)
            total += 1
    
    print(total)


def apache_check(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    unique_apache = []
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj['licenses'][0]
        
        if 'apache' in licenses.lower() and licenses not in unique_apache:
            unique_apache.append(licenses)
    
    print(unique_apache)
        


# folder = r'\batches\gpt-4o-mini\data_total'
# folder = r'\batches\gpt-3.5-turbo\data_total'
# folder = r'\batches\llama-3.1-8b-instruct\data_total'
folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'
question = 'question5'
# filename = 'question7_extract_final_registry_inconsistency_new'
filename = 'question7_extract_final_registry_consistency_filter'

# rearrange_license_inconsistency(folder, question, filename)

# get_real_license(folder, question, filename)

# get_unique_license(folder, question, f"{filename}_real_licenses")

read_count(folder, question)

# get_unique_license_filter(folder, question, filename)

# read_inaccurate_count(folder, question)

# calculate_inaccurate_license(folder, question, f'{question}_extract_final_registry_consistency_filter_real_licenses_inaccurate')

# get_prompts_accurate_packages(folder, question)
# get_prompts_accurate_packages_q7(folder, question)

# incompatibility_license_check(folder, question, f'{question}_accurate_precompatibility')

# incompatibility_license_check_q7(folder, question, f'{question}_accurate_precompatibility')

# apache_check(folder, question, f'{question}_extract_final_registry_consistency')


