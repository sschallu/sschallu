import WriteData

import json

import requests

from markdown import markdown

from bs4 import BeautifulSoup

import re

import requests

import time


def get_custom_id(folder, file_name):

    with open(f'{folder}/{file_name}.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dictionary = {}

    for line in all_lines:
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        content = obj['body']['messages'][1]['content']

        dictionary[custom_id] = content
    
    return dictionary



def category_outputs(folder, file_name):

    dic = get_custom_id(folder, file_name)

    # folder = "/gpt-4o-mini"

    with open(f'{folder}/{file_name}_output.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:

        obj = json.loads(line.rstrip())

        # custom_id = obj["custom_id"]


        custom_id = obj['custom_id']

        
        json_obj = {}
        json_obj['custom_id'] = custom_id
        json_obj['title'] = dic[custom_id]

        choices = obj['response']['body']['choices']

        content = choices[0]['message']['content']

        json_obj['output'] = content


        # if 'outputs' in obj:
        #     json_obj['output'] = 'exceptions'

        # else:
        #     choices = obj['choices']

        #     content = choices[0]['message']['content']

        #     json_obj['output'] = content
         

        if custom_id.endswith("_1"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question1/question1')

        elif custom_id.endswith("_2"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question2/question2')
        
        elif custom_id.endswith("_3"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question3/question3')

        elif custom_id.endswith("_4"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question4/question4')

        elif custom_id.endswith("_5"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question5/question5')
        
        elif custom_id.endswith("_6"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question6/question6')
        
        elif custom_id.endswith("_7"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/question7/question7')
        
        else:
            print(f"{custom_id} error...")


def special_character(sub_item):
    flag = False

    character_array = ['{', '(', '=', '&', '<', ':^', ',', ')', 'install', '}}', '|', '5.0.0', 'true']

    for character in character_array:
        if character in sub_item:
            flag = True
            break

    return flag


def start_with_character(sub_item):
    flag = False

    character_array = ['', '.', 'requirements.txt', '\\', '`', './', 'pip']

    for character in character_array:
        if character == sub_item:
            flag = True
            break
    
    return flag


def arrang_package(pending_str_array):

    new_str_array = []
    for item in pending_str_array:
        
        if item.startswith('-') or item.startswith('https:') or item.startswith('http:') or item.startswith('git') or item.startswith('github') or item.startswith('~') or item.startswith('.'):
            continue

        elif not item.startswith('@') and '@' in item:
            temp_str = item.split('@')[0]
            new_str_array.append(temp_str)

        elif '==' in item:
            temp_str = item.split('==')[0]
            new_str_array.append(temp_str)
        else:
            item = item.replace("'", "").replace('\"', '').replace(',', '').replace(';', '')
            new_str_array.append(item)
    
    return new_str_array
        



def extract_install(code_list):

    # install_array = ['npm install', 'pip install', 'composer require', 'gem install', 'cpanm ', 'cpan ']

    packages = []

    for item in code_list:
        # item = item.replace('-r', '').replace('--save-dev', '').replace('--no-binary', '').replace('--upgrade', '').replace('--save', '').replace(':all:', '').replace('-g', '').replace('--dev', '').replace('--save', '').replace('-v', '').replace('--user', '')
        
        if '#' in item:
            item = item.split('#')[0]

        item = item.strip()

        if item.startswith('npm install'):
            temp_array = ['npm install']
            pending_str = item.strip().split('npm install')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)
            
        elif item.startswith('pip install'):
            temp_array = ['pip install']
            pending_str = item.strip().split('pip install')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)
            
        elif item.startswith('composer require'):
            temp_array = ['composer require']
            pending_str = item.strip().split('composer require')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)
            
        elif item.startswith('gem install'):
            temp_array = ['gem install']
            pending_str = item.strip().split('gem install')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)
        
        elif item.startswith('gem '):
            item = item.replace('gem ', 'gem install ')
            temp_array = ['gem install']
            pending_str = item.strip().split('gem install')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)
            
        elif item.startswith('cpanm '):
            temp_array = ['cpanm ']
            pending_str = item.strip().split('cpanm ')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)

        elif item.startswith('cpan '):
            temp_array = ['cpan ']
            pending_str = item.strip().split('cpan ')[1].strip()
            pending_str_array = arrang_package(pending_str.split(' ')) 
            temp_array.extend(pending_str_array)
            print(temp_array)
            packages.append(temp_array)
        
    return packages



def parse_output(folder, question_num):
    
    # folder = "/gpt-4o-mini"
    # question_num = 'question1'
    # question_num = 'question2'
    # question_num = 'question3'

    pattern = r'github\.com\/[a-zA-Z0-9\-]+\/[a-zA-Z0-9_\-]+'

    http_pattern = r'https:\/\/(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(?:\/[^\s]*)?'

    with open(f'{folder}/{question_num}/{question_num}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj["custom_id"]

        output = json_obj["output"]

        link_list = []

        content_array = output.split('\n')
        filtered_array = list(filter(lambda x: x.strip(), content_array))

        for item in filtered_array:
            if 'github.com' in item and 'user' not in item:
                links = re.findall(pattern, item)
                if len(links) > 0:
                    for link in links:
                        github_link = f'https://{link}'
                        if github_link not in link_list:
                            link_list.append(github_link)

        


        # pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
        # result = re.findall(pattern, output, re.DOTALL | re.MULTILINE)

        json_obj["extract_packages"] = extract_install(filtered_array)

        html = markdown(output, output_format='html5')

        soup = BeautifulSoup(html, 'html.parser')

        for a in soup.findAll('a'):
            if a.get('href') is not None:
                href = a.get('href')

                if href.startswith('http') and 'example.com' not in href:
                    if href not in link_list:
                        link_list.append(href)
        
        for item in filtered_array:
            if 'https://' in item and 'localhost' not in item and 'endpoint.com' not in item and 'example' not in item and 'YOUR_PARSE_SERVER_URL' not in item and 'YOUR_DOMAIN' not in item and 'user' not in item and 'your' not in item and '{' not in item and 'name' not in item and 'YOUR' not in item and '$' not in item and 'external' not in item and 'USER' not in item:
                https = re.findall(http_pattern, item)
                if len(https) > 0:
                    for http in https:
                        http = http.replace(').', '').replace(',', '').replace(')', '').replace(';', '').replace("'", '').replace('></script>', '').replace('"', '').replace('>', '').replace(']', '').replace('`', '').replace('</url', '').replace('/:', '')
                        if http.endswith(':'):
                            http = http[:-1]
                            
                        if http not in link_list:
                            print(http)
                            link_list.append(http)

        json_obj['link_list'] = link_list
        json_obj['output'] = ''

        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}_parse')


# step 1 - question4 and question5
def parse_outputs4and5_extract(folder, question_num):
    # folder = "/gpt-4o-mini"
    # # question_num = 'question4'
    # question_num = 'question5'

    pattern = r'github\.com\/[a-zA-Z0-9\-]+\/[a-zA-Z0-9_\-]+'
    http_pattern = r'https:\/\/(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(?:\/[^\s]*)?'

    with open(f'{folder}/{question_num}/{question_num}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:

        new_obj = {}

        json_obj = json.loads(line.rstrip())

        output = json_obj["output"]
        custom_id = json_obj["custom_id"]

        new_obj['custom_id'] = custom_id
        # new_obj['title'] = json_obj['title']
        new_obj['package_information'] = []

        output_array = output.split('\n\n')

        link_list = []

        content_array = output.split('\n')
        filtered_array = list(filter(lambda x: x.strip(), content_array))

        # --------------------------------------------------------
        for item in filtered_array:
            if 'github.com' in item and 'user' not in item:
                links = re.findall(pattern, item)
                if len(links) > 0:
                    for link in links:
                        github_link = f'https://{link}'
                        if github_link not in link_list:
                            link_list.append(github_link)
        

        html = markdown(output, output_format='html5')

        soup = BeautifulSoup(html, 'html.parser')

        for a in soup.findAll('a'):
            if a.get('href') is not None:
                href = a.get('href')

                if href.startswith('http') and 'example.com' not in href:
                    if href not in link_list:
                        link_list.append(href)
        
        for item in filtered_array:
            if 'https://' in item and 'localhost' not in item and 'endpoint.com' not in item and 'EXAMPLE' not in item and 'example' not in item and 'YOUR_PARSE_SERVER_URL' not in item and 'YOUR_DOMAIN' not in item and 'user' not in item and 'your' not in item and '{' not in item and 'name' not in item and 'YOUR' not in item and '$' not in item and 'external' not in item and 'USER' not in item:
                https = re.findall(http_pattern, item)
                if len(https) > 0:
                    for http in https:
                        http = http.replace(').', '').replace(',', '').replace(')', '').replace(';', '').replace("'", '').replace('></script>', '').replace('"', '').replace('>', '').replace(']', '').replace('`', '').replace('</url', '').replace('/:', '').replace("\\", "").replace('</iframe>', '')
                        if http.endswith(':'):
                            http = http[:-1]

                        if http not in link_list:
                            # print(http)
                            link_list.append(http)
        # ----------------------------------------------------------

        length = 4
        if len(output_array) < length:
            length = len(output_array)

        detect_flag = True
        for index in range(0, length):
            item = output_array[index].replace('\n', ' ')

            if ':' not in item:
                continue
        
            first_letter = item[0]
            if not first_letter.isalpha() or item.lower().startswith('package') or ('package' in item.lower() and 'name' in item.lower()):
                total += 1
                new_obj['package_information'].append(item)
                print(f"{custom_id}: {item}")

        new_obj['link_list'] = link_list

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{question_num}_extract')

    print(total)


def replace_unuse_information(package):
    unusable_array = ['### Package Information', '### Package Info', '### Package Details', '### Suggested Package Information', 'Package Information', '### Library Information', '### Suggested Package', '### Package Description', '### Selected Package', '### Recommended Package']

    for item in unusable_array:

        if item in package:
            package = package.replace(item, '')

    return package


def replace_special_characters(new_str):
    
    new_str = new_str.replace("- ", "").replace(" -", "").replace(": ", " ").replace(" :", " ").replace('`', '').replace('*', '').replace(',', '').replace('1. ', '').replace('2. ', '').replace('3. ', '').replace(' .', '').strip().replace('"', '').replace("'", "").replace("\"", "")
    new_str = new_str.replace('[', '').replace(']', '')

    return new_str




# step 2 - question4 and question5
def parse_outputs4and5_filter(folder, question_num):
    
    # folder = "/gpt-4o-mini"
    # # question_num = 'question4'
    # question_num = 'question5'

    with open(f'{folder}/{question_num}/{question_num}_extract.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj["package_information"]

        custom_id = json_obj["custom_id"]
        new_package = []
        new_package_filter = []

        for package in package_information:
            
            # step 1
            matches = re.findall(r"\*\*.*?\*\*", package)

            for match in matches:
                if 'package' in match.lower() or 'registry' in match.lower() or 'license' in match.lower():
                    package = package.replace(match, "")
            
            matches2 = re.findall(r'\(.*?\)', package)

            for match2 in matches2:
                package = package.replace(match2, "")
            
            # step 2
            package = replace_unuse_information(package)

            # if package.startswith('###'):
            #     continue

            new_package.append(package)
        
        for new_str in new_package:
            # new_str = new_str.replace("- ", "").replace(" -", "").replace(": ", " ").replace(" :", " ").replace('`', '').replace('*', '').replace(',', '').replace('1. ', '').replace('2. ', '').replace('3. ', '').strip()
            new_str = replace_special_characters(new_str)
            result = re.sub(r'\s+', ' ', new_str)
            result = result.replace('package-name', '').replace('package-registry', '').replace('package-license', '').replace('package', '').replace("\\", '').replace('Package Name', '').replace('Package Registry', '').replace('License', '').replace('Package', '').replace(' name', '').replace('registry ', '').replace('license ', '').replace("Registry", "")
            result = re.sub(r'\s+', ' ', result)
            new_package_filter.append(result)
        
        
        json_obj['package_information'] = new_package_filter
        print(f"{custom_id}, {new_package_filter}")
            
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}_extract_filter')
        
    
    print(total)



def replace_license_space(package):

    package = package.replace("Apache 2.0", "Apache-2.0").replace("Artistic 2.0", "Artistic-2.0").replace('BSD 3-Clause', 'BSD-3-Clause').replace('Docker Hub', 'Docker-Hub').replace('docker hub', 'docker-hub').replace('GPL v2', 'GPL-v2').replace('MIT license', 'MIT')

    package = package.replace('GPL v3', 'GPL-v3').replace('LGPL v3', 'LGPL-v3').replace('BSD 2-Clause', 'BSD-2-Clause').replace('LGPL 3.0', 'LGPL-3.0').replace('Open Source', 'Open-Source')

    package = package.replace('# ', '').replace('Public Domain', 'Public-Domain').replace('MPL 2.0', 'MPL-2.0').replace('MPL 1.1', 'MPL-1.1').replace('GNU General Public v3.0', 'GNU-General-Public-v3.0').replace('GNU General Public v2.0', 'GNU-General-Public-v2.0')

    package = package.replace('GPL 1.0+', 'GPL-1.0+').replace('GPL 1+', 'GPL-1+').replace("GPL 1.0", "GPL-1.0").replace('GPL 1', 'GPL-1').replace('Perl 5', 'Perl-5')

    return package


# step3 - question4 and question5
def parse_outputs4and5_final(folder, question_num):

    # folder = "/gpt-4o-mini"
    # # question_num = 'question4'
    # question_num = 'question5'

    with open(f'{folder}/{question_num}/{question_num}_extract_filter.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj["custom_id"]

        package_information = json_obj["package_information"]

        new_package = []

        for package in package_information:
            package = package.strip()

            if package == "":
                continue

            package = package.replace('GitHub', '').replace('plaintext', '').replace('Fixed Format:', '').replace('Format:', '').replace('Format', '').replace('details', '').replace('license', '').replace('Fixed', '')

            package = replace_license_space(package)

            package = replace_special_characters(package)

            package = re.sub(r'\s+', ' ', package).strip()
            
            package_array = package.split(' ')
            
            length = len(package_array)

            if length < 3:
                continue
            
            if package.startswith('##'):
                continue
            
            if 'maven' in package.lower():
                continue

            if package_array[0].lower() == package_array[1].lower():
                package_array = package_array[1:]
            
            length = len(package_array)

            if length > 3 and 'https:' not in package:
                
                tt = []

                for split in [' or ', ' OR ', ' / ']:

                    temp_array = package.split(split)
                    if len(temp_array[0].split(' ')) == 3:
                        tt.append(temp_array[0].split(' '))

                        for index in range(1, len(temp_array)):
                            tt.append([temp_array[0].split(' ')[0], temp_array[0].split(' ')[1], temp_array[index]])
                
                        new_package = tt

                if len(new_package) <= 0:
                    new_package = [package_array[0], package_array[1], package_array[2]]

            if length == 3:
                total += 1
                # print(f"{custom_id}: {package}")
                new_package = [package_array[0], package_array[1], package_array[2]]
        
        print(f"{custom_id}, {new_package}")
        json_obj["package_information"] = new_package
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}_extract_final')

    
    print(total)





# step 1
def parse_output6and7_extract(folder, question_num):

    # folder = "/gpt-4o-mini"
    # # question_num = 'question6'
    # question_num = 'question7'

    pattern = r'github\.com\/[a-zA-Z0-9\-]+\/[a-zA-Z0-9_\-]+'
    http_pattern = r'https:\/\/(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(?:\/[^\s]*)?'

    with open(f'{folder}/{question_num}/{question_num}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        new_obj = {}
        json_obj = json.loads(line.rstrip())

        output = json_obj['output'].replace('\n \n', '\n\n').replace('\n  \n', '')

        custom_id = json_obj['custom_id']

        output_array = output.split('\n\n')

        link_list = []

        content_array = output.split('\n')
        filtered_array = list(filter(lambda x: x.strip(), content_array))

        # --------------------------------------------------------
        for item in filtered_array:
            if 'github.com' in item and 'user' not in item:
                links = re.findall(pattern, item)
                if len(links) > 0:
                    for link in links:
                        github_link = f'https://{link}'
                        if github_link not in link_list:
                            link_list.append(github_link)
        

        html = markdown(output, output_format='html5')

        soup = BeautifulSoup(html, 'html.parser')

        for a in soup.findAll('a'):
            if a.get('href') is not None:
                href = a.get('href')

                if href.startswith('http') and 'example.com' not in href:
                    if href not in link_list:
                        link_list.append(href)
        
        for item in filtered_array:
            if 'https://' in item and 'localhost' not in item and 'endpoint.com' not in item and 'EXAMPLE' not in item and 'example' not in item and 'YOUR_PARSE_SERVER_URL' not in item and 'YOUR_DOMAIN' not in item and 'user' not in item and 'your' not in item and '{' not in item and 'name' not in item and 'YOUR' not in item and '$' not in item and 'external' not in item and 'USER' not in item:
                https = re.findall(http_pattern, item)
                if len(https) > 0:
                    for http in https:
                        http = http.replace(').', '').replace(',', '').replace(')', '').replace(';', '').replace("'", '').replace('></script>', '').replace('"', '').replace('>', '').replace(']', '').replace('`', '').replace('</url', '').replace('/:', '').replace("\\", "").replace('</iframe>', '')
                        if http not in link_list:
                            if http.endswith(':'):
                                http = http.rstrip(':')

                            print(http)
                            link_list.append(http)
        # ----------------------------------------------------------

        package_information = ""

        # for gpt-4o-mini
        # ----------------------------------------------------------------
        # if len(output_array) <= 1:
        #     continue
        # -----------------------------------------------------------------
        

        # for gpt-3.5-turbo
        # ----------------------------------------------------------------------------
        if '1. ' in output_array[0] and len(output_array) > 4:
            package_information = '\n'.join(output_array)

        elif "1. " in output_array[0] or len(output_array) <= 1:
            package_information = output_array[0]

        elif "1. " not in output_array[1] and len(output_array) > 2:
            package_information = output_array[2]

        elif len(output_array) > 4:
            package_information = '\n'.join(output_array[1:])

        else:
            package_information = output_array[1]
        # -----------------------------------------------------------------------------

        # for gpt-4o-mini
        # ------------------------------------------------------------------
        # if "1. " not in output_array[1] and len(output_array) > 2:
        #     package_information = output_array[2]
        #     # print(f"{custom_id}: {output_array[2]}")

        # elif len(output_array) > 4:
        #     package_information = '\n'.join(output_array[1:])

        # else:
        #     # print(f"{custom_id}: {output_array[1]}")
        #     package_information = output_array[1]
        # ---------------------------------------------------------------------

        print(package_information)

        new_obj['custom_id'] = custom_id
        new_obj['package_information'] = package_information
        new_obj['link_list'] = link_list

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{question_num}_extract')
    


# step 2
def parse_output6and7_filter(folder, question_num):

    # folder = "/gpt-4o-mini"
    # # question_num = 'question6'
    # question_num = 'question7'

    with open(f'{folder}/{question_num}/{question_num}_extract.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj["package_information"].replace('\n\n', '\n')

        custom_id = json_obj["custom_id"]

        package_array = package_information.split('\n')

        new_array = []

        for package in package_array:
            package = package.strip()

            if package == '':
                continue

            first_letter = package[0]

            if not first_letter.isdigit() and ": " not in package:
                continue
        
            new_array.append(package)
        
        json_obj["package_information"] = "\n".join(new_array)

        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}_extract_filter')


# step 3
def parse_output6and7_arrange(folder, question_num):

    # folder = "/gpt-4o-mini"
    # question_num = 'question6'
    # question_num = 'question7'

    with open(f'{folder}/{question_num}/{question_num}_extract_filter.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        flag = False

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj["custom_id"]

        package_information = json_obj['package_information'].replace('\\n', '\n').replace('alert(\"', '')

        package_array = package_information.split('\n')
        new_pack_array = []

        for package in package_array:
            package = package.strip()

            if package == "":
                continue
            
            temp_array = package.split(' ')
            if len(temp_array) > 6:
                continue

            first_letter = package[0]

            new_pack_array.append(package)

            if not first_letter.isdigit() and ': ' in package and ', ' not in package:
                total += 1
                flag = True
                # print(f"{custom_id}: {package}")
            # else:
                # print(f"{custom_id}: {package}")
        
        if flag is True:
            combinations = []

            if len(new_pack_array) % 2 == 0:
                combinations = [new_pack_array[i] + ', ' + new_pack_array[i + 1] for i in range(0, len(new_pack_array), 2)]
                print(f"{custom_id}: {combinations}")

            elif len(new_pack_array) % 3 == 0:
                combinations = [new_pack_array[i] + ', ' + new_pack_array[i + 1] + ', ' + new_pack_array[i + 2] for i in range(0, len(new_pack_array), 3)]
            
            json_obj['package_information'] = '\n'.join(combinations)
        
        else:
            json_obj['package_information'] = '\n'.join(new_pack_array)

        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}_extract_arrange')
                
    
    print(total)


# step 4
def parse_output6and7_final(folder, question_num):

    # folder = "/gpt-4o-mini"
    # question_num = 'question6'
    # question_num = 'question7'

    with open(f'{folder}/{question_num}/{question_num}_extract_arrange.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        flag = False

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj["custom_id"]

        package_information = json_obj['package_information']

        package_array = package_information.split('\n')

        new_package = []

        for package in package_array:
            package = package.strip()

            if package == "":
                continue
            
            if 'maven' in package.lower() or 'microsoft' in package.lower():
                continue

            package = package.replace('1. ', '').replace('2. ', '').replace('3. ', '').replace('4. ', '').replace('5. ', '').replace('  ', ' ')

            # gpt-3.5-turbo
            package = package.replace('Package-name:', '').replace('Package-registry:', '').replace('Package-license:', '').replace('from ', '').replace('on ', '').replace('package:', '').replace('package-license:', '').replace('**Package**', '').replace('**Registry**', '').replace('**License**', '')

            package = package.replace('package-name:', '').replace('package-registry: ', '').replace('license: ', '').replace('Package Name:', '').replace('Package Registry', '').replace('Package License', '').replace('Registry: ', '').replace('License: ', '').replace('registry: ', '').replace('License', '').replace('Package:', '').replace('registry,', '')

            # gpt-3.5-turbo
            package = package.replace('name:', '').replace('Registry ', '').replace('- ', '')

            package = package.replace('**', '').replace('`', '').replace(', ', ' ').replace(': ', ' ').replace(' - ', ' ').replace(')', '').replace('(', '').replace('[', ' ').replace(']', ' ').replace(' | ', ' ').replace('\"', '')

            package = re.sub(r'\s+', ' ', package).strip()

            package = replace_license_space(package)

            package = package.replace('CPAN Perl;', 'CPAN').replace('CPAN Perl', 'CPAN')

            item_array = package.split(' ')

            # gpt-3.5-turbo
            if len(item_array) > 3 and item_array[0] == item_array[2]:
                del item_array[2]
            if len(item_array) > 3 and item_array[0] == item_array[1]:
                del item_array[1]

            if len(item_array) > 3:
                total += 1

                tt = []

                for split in [' or ', ' OR ', ' / ']:

                    temp_array = package.split(split)
                    if len(temp_array[0].split(' ')) == 3:
                        tt.append(temp_array[0].split(' '))
                        flag = True
                        for index in range(1, len(temp_array)):
                            tt.append([temp_array[0].split(' ')[0], temp_array[0].split(' ')[1], temp_array[index]])
                
                        new_package.append(tt)

                if item_array[3].startswith('https'):
                    new_package.append([item_array[0], item_array[1], item_array[2]])
            
            if len(item_array) == 3:
                new_package.append([item_array[0], item_array[1], item_array[2]])
        
        json_obj['package_information'] = new_package
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}_extract_final')

    
    print(total)





# folder = '/batches/gpt-3.5-turbo/data_total'
# folder = '/batches/gpt-4o-mini/data_total'
# folder = '/batches/llama-3.1-sonar-small-128k-chat/data_total'
# folder = '/batches/llama-3.1-8b-instruct/data_total'
# folder = '/gpt-4o-mini/'
# folder = '/defense'
# folder = '/batches/llama-3.1-8b-instruct/'
# file_name = 'batches_prompts_14'

folder = r'\defense\real_useful\question2_new2_ensure'

# folder = r'\defense'
# folder = r'\gpt-4o-mini'
# folder = r'\defense\top_20000_question2_q3'
# file_name = 'top_20000_question2_q3'



def parse_output6and7_total(folder, question_num):

    parse_output6and7_extract(folder, question_num)

    parse_output6and7_filter(folder, question_num)

    parse_output6and7_arrange(folder, question_num)

    parse_output6and7_final(folder, question_num)


def parse_output4and5_total(folder, question_num):

    parse_outputs4and5_extract(folder, question_num)

    parse_outputs4and5_filter(folder, question_num)

    parse_outputs4and5_final(folder, question_num)


# parse_output4and5_total(folder, 'question5')
# parse_outputs4and5_final(folder, 'question4')


# parse_output6and7_total(f'{folder}', 'question7')

# parse_output6and7_final(f'{folder}{file_name}', 'question6')

# parse_output6and7_arrange(f'{folder}{file_name}', 'question6')

# parse_output6and7_filter(f'{folder}{file_name}', 'question6')

# parse_output6and7_extract(f'{folder}', 'question6')


# parse_outputs4and5_final(f'{folder}{file_name}', 'question4')

# parse_outputs4and5_filter(f'{folder}{file_name}', 'question4')

# parse_outputs4and5_extract(f'{folder}{file_name}', 'question4')


# parse_output(folder, 'question2')


# category_outputs(folder, file_name)

# parse_output(folder, 'question3')


def outputs_total():

    folder_template = 'batches_prompts_'
    for index in range(0, 15):

        file_name = f'{folder_template}{index}'

        print(f'{folder}{file_name}')

        # category_outputs(f'{folder}{file_name}', file_name)

        parse_output(f'{folder}{file_name}', 'question2')

        # parse_output4and5_total(f'{folder}{file_name}', 'question5')

        # parse_output6and7_total(f'{folder}{file_name}', 'question7')



# outputs_total()







