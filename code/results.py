import WriteData

import json

import os

import re

import requests

import time

from urllib.parse import urlparse
from packaging import version



def read_files(destination, suffix):

    with open(f'{destination}.{suffix}', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def category_files(folder, filename):

    target_file = f'{folder}/{filename}'

    all_lines = read_files(target_file, 'json')

    package_dic = {}
    link_dic = {}

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_request = json_obj['package_request']

        # link_list = json_obj['link_list']

        for package in package_request:
            package_link = package[0]
            status_code = package[1]

            if package_link not in package_dic.keys():
                package_dic[package_link] = status_code

                obj = {}
                obj['package_link'] = package_link
                obj['status_code'] = status_code

                WriteData.write_in_path(json.dumps(obj), f'{folder}/package_total')

                # if status_code == 404 or status_code == 'exception':
                #     WriteData.write_in_path(json.dumps(obj), f'{folder}/package_total_404')
        
        # for item in link_list:
        #     link = item[0]
        #     status_code = item[1]

        #     if link not in link_dic.keys():
        #         link_dic[link] = status_code

        #         obj = {}
        #         obj['link'] = link
        #         obj['status_code'] = status_code

        #         WriteData.write_in_path(json.dumps(obj), f'{folder}/link_total')

                # if status_code == 404 or status_code == 'exception':
                #     WriteData.write_in_path(json.dumps(obj), f'{folder}/link_total_404')


def category_package(folder, filename):

    target_file = f'{folder}/{filename}'

    all_lines = read_files(target_file, 'json')

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']

        if package_link.startswith("https://metacpan.org/pod/"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_perl')

        elif package_link.startswith("https://pypi.org/project/"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_python')
            
        elif package_link.startswith("https://packagist.org/packages/"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_php')

        elif package_link.startswith("https://rubygems.org/gems/"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_ruby')

        elif package_link.startswith("https://registry.npmjs.org/"):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_nodejs')
            

def get_404(folder, filename):
    destination = f"{folder}/{filename}"

    all_lines = read_files(destination, "json")

    total = 0
    non_existent = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        status_code = json_obj['status_code']

        total += 1

        if status_code == 404:
            non_existent += 1
    
    print(non_existent)
    print(total)
    print(non_existent / total)


def extract_link(folder, filename):

    destination = f"{folder}/{filename}"

    all_lines = read_files(destination, "json")

    unique_domainname = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        status_code = json_obj['status_code']

        domain = urlparse(link).netloc

        if domain in unique_domainname:
            continue

        unique_domainname.append(domain)
            
        new_obj = {}
        new_obj['domain'] = domain
        new_obj['status'] = status_code
        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_unique_domain')


        # if status_code == 'exception' and not link.startswith('https://github.com'):
        #     WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_exception')
        
        # if status_code == 404 and not link.startswith('https://github.com'):
        #     if link.endswith('.js'):
        #         WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_404_js')

        #     elif link.endswith('.css'):
        #         WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_404_css')
            
        #     else:
        #         WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_404_rest')
        
        # if link.startswith('https://github.com'):
        #     WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_github')


def init_request_dic(file_name):

    folder = f"/{file_name}.json"

    with open(folder, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        domain = obj['domain']
        res = obj['res']

        dic[domain] = res
    
    return dic

            

def godaddy_api(folder, filename):

    godaddy_api_key_ote = ''
    godaddy_secret_ote = ''

    destination = f"{folder}/{filename}"

    all_lines = read_files(destination, "json")

    dic = init_request_dic('domain_request_godaddy')

    total = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        status_code = json_obj['status']
        domain = json_obj['domain']

        if 'www.' in domain:
            domain = domain.replace('www.', '')

        if status_code == 200:
            continue

        if domain not in dic.keys():
            url = f"https://api.ote-godaddy.com/v1/domains/available?domain={domain}"

            headers = {
                    "Authorization": f"sso-key {godaddy_api_key_ote}:{godaddy_secret_ote}"
                }

            response = requests.get(url, headers=headers)
            data = response.json()

            dic[domain] = data
            new_obj = {}
            new_obj['domain'] = domain
            new_obj['res'] = data

            print(f'{total}: {domain}, {data}')
            WriteData.write_in_path(json.dumps(new_obj), f'/domain_request_godaddy')

            time.sleep(2)

            if 'code' in data:
                continue

            json_obj['available'] = data['available']
        
        else:
            res = dic[domain]

            print(f'{total}: {domain}, {res}')

            if 'code' in res:
                continue

            ava = res['available']
            json_obj['available'] = ava

        ava = json_obj['available']
        print(f'{total}: {domain}, {ava}')
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_request')


def github_redirection_check(folder, filename):

    destination = f"{folder}/{filename}"

    all_lines = read_files(destination, "json")

    total = 0

    for line in all_lines:

        total += 1

        # if total <= 1189:
        #     continue

        json_obj = json.loads(line.rstrip())

        link = json_obj["link"]

        status_code = json_obj["status_code"]

        if status_code == 200:

            response = requests.get(link)

            time.sleep(0.5)

            print(f'{total}, {link}: {response.url}')

            if link != response.url:
                json_obj["redirected_url"] = response.url

                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_redirected')
        
        else:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_redirected')


            
def github_account_check(folder, file_name):

    if not os.path.exists(f'{folder}/{file_name}.json'):
        return

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    token = ''

    headers = {
        "Authorization": f"Bearer {token}"
    }

    account_array = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        url = json_obj['link']

        url = url.replace("https://github.com/", "")

        account = url.split('/')[0]

        if account in account_array:
            continue

        account_array.append(account)

        request_url = f'https://api.github.com/users/{account}'

        response = requests.get(request_url, headers=headers)

        status_code = response.status_code

        if status_code == 404:
            # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_hijacking')
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/link_total_404_cdn_github_hijacking')

        print(f'{request_url}: {status_code}')

        time.sleep(0.2)



def data_arrange(folder, filename):

    destination = f"{folder}/{filename}"

    all_lines = read_files(destination, "json")

    total = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        license = json_obj['license']

        deprecated = json_obj['deprecated']

        if license == 'exception':
            continue

        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_new')


def read_package_404(folder, filename):

    print(filename)

    destination = f'{folder}/{filename}'
    all_lines = read_files(destination, 'json')

    total = 0
    hallucination = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())
        
        status_code = json_obj['status_code']

        total += 1

        if status_code == 404:
            hallucination += 1
        
    
    print(hallucination)
    print(total)
    print(hallucination / total)



def link_arrange(folder, filename):

    print(filename)

    destination = f'{folder}/{filename}'
    all_lines = read_files(destination, 'json')

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        if '(' in link or '<' in link or 'x.' in link or '.x' in link:
            continue
        
        if link.endswith('.'):
            continue
        
        if link.startswith('https://metacpan.org/pod/') or link.startswith('https://pypi.org/project/') or link.startswith('https://packagist.org/packages/') or link.startswith('https://rubygems.org/gems/') or link.startswith('https://registry.npmjs.org/'):
            continue

        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_new')



def read_jsrepository(folder, filename):
    
    destination = f'/jsrepository-v4'

    with open(f'{destination}.json', encoding='utf-8') as f:
        content = f.read()
        f.close()

    json_obj = json.loads(content)

    print(len(json_obj.keys()))

    target_destination = f'{folder}/{filename}'

    all_line = read_files(target_destination, 'json')

    result_dict = {}
    
    for line in all_line:
        obj = json.loads(line.rstrip())

        link = obj['link']

        status_code = obj['status_code']

        if status_code != 200:
            continue

        if not link.endswith('.js'):
            continue

        match = re.search(r'/(\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9]+)?)/', link)
        if match:
            ver = match.group(1)
        else:
            continue
        

        for key in json_obj.keys():
            if key.lower() in link.lower():

                print(key)

                vulber = []
                vulnerabilities = json_obj[key]['vulnerabilities']

                for vul in vulnerabilities:
                    if 'below' in vul and 'atOrAbove' in vul:
                        if version.parse(ver) >= version.parse(vul['atOrAbove']) and version.parse(ver) < version.parse(vul['below']):

                            vulber.append([ver, vul['severity']])
                    
                    elif 'below' in vul:
                        if version.parse(ver) < version.parse(vul['below']):
                            vulber.append([ver, vul['severity']])

                if len(vulber) > 0:
                    new_obj = {}
                    new_obj['link'] = link
                    new_obj['key'] = key
                    new_obj['versions'] = vulber
                    WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_outdated_version')
                            

def read_files_count(folder, question, filename):

    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    print(filename)

    print(len(all_lines))


def get_cdn_domains(folder, question, filename):


    pre_defind_dict = {
        'npm': ['unpkg.com', 'cdn.jsdelivr.net'],
        'github': ['cdn.rawgit.com', 'cdn.jsdelivr.net', 'rawgit.com']
    }


    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')


    npm_unique = []
    github_unique = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        domain = urlparse(link).netloc

        if domain in pre_defind_dict['npm']:

            package_name = ''

            if link.startswith(f'https://unpkg.com'):

                link = link.replace('https://unpkg.com/', '')
                link_array = link.split('/')

                if link_array[0].startswith('@'):
                    package_name = f"{link_array[0]}/{link_array[1].split('@')[0]}"
                else:
                    package_name = link_array[0].split('@')[0]
            
            elif link.startswith('https://cdn.jsdelivr.net/npm/'):
                link = link.replace('https://cdn.jsdelivr.net/npm/', '')

                link_array = link.split('/')

                if link_array[0].startswith('@'):
                    package_name = f"{link_array[0]}/{link_array[1].split('@')[0]}"
                else:
                    package_name = link_array[0].split('@')[0]
            
            elif link.startswith('https://cdn.jsdelivr.net/gh/'):

                link = link.replace('https://cdn.jsdelivr.net/gh/', '')
                link_array = link.split('/')
                github = f'{link_array[0]}/{link_array[1].split("@")[0]}'
                
                if github not in github_unique:
                    github_unique.append(github)
                
            if package_name not in npm_unique:
                npm_unique.append(package_name)
    
        
        elif domain in pre_defind_dict['github']:

            github = ''

            if link.startswith(f'https://cdn.rawgit.com/'):

                link = link.replace('https://cdn.rawgit.com/', '')
                link_array = link.split('/')
                github = f'{link_array[0]}/{link_array[1]}'

            elif link.startswith('https://rawgit.com'):

                link = link.replace('https://rawgit.com/', '')
                link_array = link.split('/')
                github = f'{link_array[0]}/{link_array[1]}'
            
            if github not in github_unique:
                github_unique.append(github)
    
    for npm in npm_unique:
        new_obj = {}
        new_obj['link'] = f'https://registry.npmjs.org/{npm}'

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question}/{filename}_cdn_npm')
    
    for github in github_unique:
        new_obj = {}
        new_obj['link'] = f'https://github.com/{github}'

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question}/{filename}_cdn_github')


def request_cdn_npm_package(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    if not os.path.exists(f'{destination}.json'):
        return

    all_lines = read_files(destination, 'json')

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        response = requests.get(link)
        
        status_code = response.status_code

        if status_code == 404:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/link_total_404_cdn_npm_hijacking')
        
        print(f'{link}: {status_code}')

        time.sleep(0.2)


def get_packages_count_total(folder, question):

    destination_nodejs = f'{folder}/{question}/package_total_nodejs'
    # destination_nodejs = f'{folder}/{question}/package_total_nodejs_new'
    all_lines_nodejs = read_files(destination_nodejs, 'json')

    destination_python = f'{folder}/{question}/package_total_python_new'
    all_lines_python = read_files(destination_python, 'json')

    destination_ruby = f'{folder}/{question}/package_total_ruby_new'
    all_lines_ruby = read_files(destination_ruby, 'json')

    destination_perl = f'{folder}/{question}/package_total_perl_new'
    all_lines_perl = read_files(destination_perl, 'json')

    destinatino_php_incomplete = f'{folder}/{question}/package_total_php_new_incomplete'
    all_lines_php_incomplete = read_files(destinatino_php_incomplete, 'json')

    destination_php = f'{folder}/{question}/package_total_php_new'
    all_lines_php = read_files(destination_php, 'json')

    print(f'all_lines_nodejs: {len(all_lines_nodejs)}')
    print(f'all_lines_python: {len(all_lines_python)}')
    print(f'all_lines_ruby: {len(all_lines_ruby)}')
    print(f'all_lines_perl: {len(all_lines_perl)}')
    print(f'all_lines_php_incomplete: {len(all_lines_php_incomplete)}')
    print(f'all_lines_php: {len(all_lines_php)}')

    total = len(all_lines_nodejs) + len(all_lines_python) + len(all_lines_ruby) + len(all_lines_perl) + len(all_lines_php_incomplete) + len(all_lines_php)

    print(f'total: {total}')
    

def get_php_incomplete_range(folder, question):
    
    destination_incomplete = f'{folder}/{question}/package_total_php_new_incomplete'
    all_lines_incomplete = read_files(destination_incomplete, 'json')

    destination_php = f'{folder}/{question}/package_total_php_new'
    all_lines_php = read_files(destination_php, 'json')

    total = len(all_lines_incomplete) + len(all_lines_php)

    percentage = (len(all_lines_incomplete) / total) * 100

    print(f'incomplete: {len(all_lines_incomplete)}')
    print(f'php: {len(all_lines_php)}')
    print(f'percentage: {percentage}')


def get_rest_link_count(folder, question):
    
    destination_link_total = f'{folder}/{question}/link_total'
    all_lines_total = read_files(destination_link_total, 'json')

    destination_link_github = f'{folder}/{question}/link_total_github'
    all_lines_github = read_files(destination_link_github, 'json')

    total = len(all_lines_total) - len(all_lines_github)

    precentage = (1115 / total) * 100

    print(f'total: {total}')
    print(f'precentage: {precentage}')


def get_js_count(folder, question):

    destination = f'{folder}/{question}/link_total'

    all_lines = read_files(destination, 'json')

    count = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        if not link.endswith('.js'):
            continue

        count += 1
    
    precentage = (62 / count) * 100
    print(count)
    print(precentage)

folder = r'\batches\gpt-4o-mini\data_total'
# folder = r'\batches\gpt-3.5-turbo\data_total'
# folder = r'\batches\llama-3.1-8b-instruct\data_total'
# folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'
# folder = r''
question = 'question4'

# get_packages_count_total(folder, question)
# get_php_incomplete_range(folder, question)
# get_rest_link_count(folder, question)
get_js_count(folder, question)

# data_arrange(folder, 'package_nodejs_infor')

# category_files(folder, 'question7_extract_final_registry_request')

# category_package(folder, 'package_total')

# get_404(folder, 'package_total_nodejs')

# extract_link(folder, 'link_total')


# godaddy_api(folder, 'link_total_unique_domain')
# godaddy_api_auction(folder, 'link_total_unique_domain_request')


# github_redirection_check(folder, "link_total_github")


# get_cdn_domains(folder, question, 'link_total_404_js_new')
# get_cdn_domains(folder, question, 'link_total_404_css_new')

# github_account_check(f'{folder}/{question}', "link_total_404_css_new_cdn_github")
# request_cdn_npm_package(folder, question, 'link_total_404_css_new_cdn_npm')
# github_account_check(f'{folder}/{question}', "link_total_404_js_new_cdn_github")
# request_cdn_npm_package(folder, question, 'link_total_404_js_new_cdn_npm')


# read_package_404(folder, 'package_total_nodejs_new')
# read_package_404(folder, 'package_total_nodejs')
# read_package_404(folder, 'package_total_python_new')
# read_package_404(folder, 'package_total_ruby_new')
# read_package_404(folder, 'package_total_perl_new')
# read_package_404(folder, 'package_total_php_new')


# link_arrange(folder, 'link_total_404_rest')
# link_arrange(folder, 'link_total_404_js')
# link_arrange(folder, 'link_total_404_css')

# read_jsrepository(folder, 'link_total')

# question = 'question4'
# read_files_count(folder, question, 'link_total_404_js_new')
# read_files_count(folder, question, 'link_total_404_css_new')
# read_files_count(folder, question, 'link_total_404_rest_new')





