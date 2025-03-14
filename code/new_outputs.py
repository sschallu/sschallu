import WriteData

import json

import requests

from markdown import markdown

from bs4 import BeautifulSoup

import re

import requests

import time

import numpy as np


# step 2
def parse_output6and7_filter_sonar(folder, question_num):


    with open(f'{folder}/{question_num}/{question_num}_extract.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj["package_information"].replace('\n\n', '\n').replace('\n   ', ' ')

        custom_id = json_obj["custom_id"]

        package_array = package_information.split('\n')

        new_package = []

        for package in package_array:
            if package.startswith('1.'):
                new_package.append(package)

            elif package.startswith('2.'):
                new_package.append(package)
            
            elif package.startswith('3.'):
                new_package.append(package)
            
            elif package.startswith('4.'):
                new_package.append(package)
            
            elif package.startswith('5.'):
                new_package.append(package)
        
        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['package_information'] = new_package

        print(f'{custom_id}')

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{question_num}_extract_filter')


# step 3
def parse_output6and7_arrange_sonar(folder, question_num):


    with open(f'{folder}/{question_num}/{question_num}_extract_filter.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj["package_information"]

        custom_id = json_obj["custom_id"]

        new_package_information = []

        for package in package_information:

            package = package.replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').strip()

            # package = package.replace('`', '').replace(' - ', ' ').replace('**', '').replace('Package Name:', '').replace('Package Registry:', '').replace('License:', '').strip()

            package = package.replace('`', '').replace(' - ', ' ').replace('**', '').strip()

            # package = package.replace('package-name:', '').replace('package-registry:', '').replace('package-license:', '').strip().replace('Registry:', '').replace('(', '').replace(')', '').replace('registry:', '').replace('license:', '')

            package = package.replace('(', '').replace(')', '')

            package_name = ''
            package_registry = ''
            license = ''

            if 'Package Name:' in package and 'Package Registry:' in package and 'License:' in package:
                package_name = package.split("Package Name:")[1].split("Package Registry:")[0].strip().replace(',', '')

                package_name = package_name.split(' ')[0]

                package_registry = package.split("Package Registry:")[1].split("License:")[0].strip().replace(',', '')

                if 'Note:' in package_registry:
                    package_registry = package_registry.split('Note:')[0]

                license = package.split("License:")[1].strip()

                license = license.split(' ')[0]

                print(f'{package_name}, {package_registry}, {license}')

            elif 'package-name:' in package and 'package-registry:' in package and 'package-license:' in package:
                package_name = package.split("package-name:")[1].split("package-registry:")[0].strip().replace(',', '')

                package_name = package_name.split(' ')[0]

                package_registry = package.split("package-registry:")[1].split("package-license:")[0].strip().replace(',', '')

                if 'Note:' in package_registry:
                    package_registry = package_registry.split('Note:')[0]

                license = package.split("package-license:")[1].strip()

                license = license.split(' ')[0]

                print(f'{package_name}, {package_registry}, {license}')
                
            elif 'Registry:' in package and 'License:' in package:
                package_name = package.split("Registry:")[0].strip().replace(',', '')

                package_name = package_name.split(' ')[0]

                package_registry = package.split("Registry:")[1].split("License:")[0].strip().replace(',', '')

                if 'Note:' in package_registry:
                    package_registry = package_registry.split('Note:')[0]

                license = package.split("License:")[1].strip()

                license = license.split(' ')[0]

                print(f'{package_name}, {package_registry}, {license}')
            
            elif 'registry:' in package and 'License:' in package: 
                package_name = package.split("registry:")[0].strip().replace(',', '')

                package_name = package_name.split(' ')[0]

                package_registry = package.split("registry:")[1].split("License:")[0].strip().replace(',', '')

                if 'Note:' in package_registry:
                    package_registry = package_registry.split('Note:')[0]

                license = package.split("License:")[1].strip()

                license = license.split(' ')[0]

                print(f'{package_name}, {package_registry}, {license}')

            elif 'package-name:' in package and 'registry:' in package and 'license:' in package: 
                package_name = package.split("package-name:")[1].split("registry:")[0].strip().replace(',', '')

                package_name = package_name.split(' ')[0]

                package_registry = package.split("registry:")[1].split("license:")[0].strip().replace(',', '')

                if 'Note:' in package_registry:
                    package_registry = package_registry.split('Note:')[0]

                license = package.split("license:")[1].strip()

                license = license.split(' ')[0]

                print(f'{package_name}, {package_registry}, {license}')
            
            elif 'registry:' in package and 'license:' in package: 
                package_name = package.split("license:")[0].strip().replace(',', '')

                package_name = package_name.split(' ')[0]

                package_registry = package.split("registry:")[1].split("license:")[0].strip().replace(',', '')

                if 'Note:' in package_registry:
                    package_registry = package_registry.split('Note:')[0]

                license = package.split("license:")[1].strip()

                license = license.split(' ')[0]

                print(f'{package_name}, {package_registry}, {license}')

            else:
                package = package.replace(',', '').replace('registry:', '').replace('License:', '')

                if 'Packagist:' in package:
                    package = package.split('Packagist:')[1]
                
                package = re.sub(r'\s+', ' ', package).strip()
                package = package.replace(': ', ' ')

                package_array = package.split(' ')

                unique_package = list(dict.fromkeys(package_array))

                if len(unique_package) < 3:
                    continue

                package_name = unique_package[0]
                package_registry = unique_package[1]
                license = unique_package[2]

            if package_name != '' and package_registry != '' and license != '':
                new_package_information.append([package_name, package_registry, license])

        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['package_information'] = new_package_information

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{question_num}_extract_final')

 


# step 2
def parse_output6and7_filter_llama(folder, question_num):

    with open(f'{folder}/{question_num}/{question_num}_extract.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj["package_information"]

        custom_id = json_obj["custom_id"]

        package_array = package_information.split('\n')

        new_package = []

        for package in package_array:
            if package.startswith('1.'):
                new_package.append(package)

            elif package.startswith('2.'):
                new_package.append(package)
            
            elif package.startswith('3.'):
                new_package.append(package)
            
            elif package.startswith('4.'):
                new_package.append(package)
            
            elif package.startswith('5.'):
                new_package.append(package)
        
        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['package_information'] = new_package

        print(f'{new_package}')

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{question_num}_extract_filter')



def parse_output6and7_arrange_llama(folder, question_num):


    with open(f'{folder}/{question_num}/{question_num}_extract_filter.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj["package_information"]

        custom_id = json_obj["custom_id"]

        new_package_information = []

        for package in package_information:
            
            if 'Go Package' in package or 'Maven Central' in package or 'NuGet' in package or 'Maven:' in package: 
                continue

            package = package.replace('Ruby Gems', 'RubyGems').replace('registry:', '').replace('pip install', 'pip')

            match = re.search(r"\*\*(.+?)\*\*", package)
            
            package_name = ' '

            if match:
                result = match.group(1)

                package_name = result.replace('`', '')

                if ' ' in package_name:
                    continue
            else:
                continue

            package = package.replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').strip()

            package = package.replace('`', '').replace(' - ', ' ').replace('**', '').replace('License', '').strip()

            package = package.replace('(', '').replace(')', '').replace(': ', ' ').replace(', ', ' ')

            package_array = package.split(' ')

            unique_package = list(dict.fromkeys(package_array))

            package_registry = ''
            license = ''

            if len(unique_package) < 3:
                continue
            
            if unique_package[0] != package_name:
                continue
            
            package_registry = unique_package[1]

            license = unique_package[2]

            if package_name != '' and package_registry != '' and license != '':
                new_package_information.append([package_name, package_registry, license])

            
        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['package_information'] = new_package_information

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{question_num}_extract_final')



# folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'
folder = r'\batches\llama-3.1-8b-instruct\data_total'

# parse_output6and7_filter_sonar(folder, 'question7')

# parse_output6and7_arrange_sonar(folder, 'question7')

# parse_output6and7_filter_llama(folder, 'question7')

# parse_output6and7_arrange_llama(folder, 'question7')

