import WriteData

import json

import os

import requests

import time


def init_request_dic(file_name):

    # folder = "/packages_request_status.json"
    folder = f"/{file_name}.json"

    with open(folder, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        url = obj['url']
        status_code = obj['status_code']

        dic[url] = status_code
    
    return dic


def request_packages(request_url):

    try:

        response = requests.get(request_url)

        history_list = response.history

        time.sleep(0.3)

        status_code = response.status_code

    except:

        status_code = "exception"
    
    return status_code


def write_request_package(file_name, request_url, status_code):
    request_obj = {}

    request_obj['url'] = request_url
    request_obj['status_code'] = status_code
    # WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')
    WriteData.write_in_path(json.dumps(request_obj), f'/{file_name}')


# For question1 and question2 and question3
def request_packages_123(folder, question_num, file):

    dic_registry = {
        'cpanm': 'https://metacpan.org/pod/',
        'cpan': 'https://metacpan.org/pod/',
        'pip install': 'https://pypi.org/project/',
        'composer require': 'https://packagist.org/packages/',
        'gem install': 'https://rubygems.org/gems/',
        'npm install': 'https://registry.npmjs.org/'
    }

    dic_array = ['cpanm ', 'cpan ', 'pip install', 'composer require', 'gem install', 'npm install']

    with open(f'{folder}/{question_num}/{file}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    # dic = init_request_dic('packages_request_status')
    dic = {}

    total = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        extract_packages = json_obj["extract_packages"]
        package_request = []

        custom_id = json_obj['custom_id']

        link_list = json_obj["link_list"]
        link_request = []

        if len(extract_packages) > 0:

            for package_array in extract_packages:
                install_command = package_array[0]
                packages = package_array[1:]
                
                install_command = install_command.strip()

                # registry = dic_registry[install_command]

                for package in packages:

                    if install_command == 'cpanm' or install_command == 'cpan':
                        request_url = f'https://fastapi.metacpan.org/v1/module/{package}'

                    elif install_command == 'pip install':
                        request_url = f'https://pypi.org/pypi/{package}/json'

                    elif install_command == 'composer require':
                        request_url = f'https://packagist.org/packages/{package}.json'

                    elif install_command == 'gem install':
                        request_url = f'https://rubygems.org/api/v1/gems/{package}.json'
                    
                    elif install_command == 'npm install':
                        request_url = f'https://registry.npmjs.org/{package}'

                    # request_url = f'{registry}{package}'

                    if request_url in dic.keys():
                        package_request.append([request_url, dic[request_url]])
                        print(f'{total}_already: {request_url}: {dic[request_url]}')

                    else:
                        status_code = request_packages(request_url)

                        dic[request_url] = status_code

                        # write_request_package('packages_request_status', request_url, status_code)

                        package_request.append([request_url, status_code])

                        print(f'{total}: {request_url}: {status_code}')

            

        # if len(link_list) > 0:
            
        #     for link in link_list:
        #         request_url = link

        #         if request_url in dic.keys():
        #             link_request.append([request_url, dic[request_url]])
        #             print(f'{total}_already: {request_url}: {dic[request_url]}')
                
        #         else:
        #             status_code = request_packages(request_url)

        #             dic[request_url] = status_code

        #             # write_request_package('packages_request_status', request_url, status_code)

        #             link_request.append([request_url, status_code])

        #             print(f'{total}: {request_url}: {status_code}')
        
        new_obj = {}
        new_obj['custom_id'] = json_obj['custom_id']
        new_obj['title'] = json_obj['title']
        new_obj['package_request'] = package_request
        new_obj['link_list'] = link_request

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{file}_request')



def re_request_nodejs(folder, filename):

    destination = f'{folder}/{filename}'

    dic = init_request_dic('packages_request_status_67')

    # new_request_template = f'https://pypi.org/pypi/{package_name}/json'

    total = 0

    with open(f'{destination}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    unique = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        package_link = json_obj['package_link'].replace('#', '').replace("'", "")


        if package_link in unique:
            continue

        unique.append(package_link)

        if package_link in dic.keys():
            print(f'{total}_already: {package_link}: {dic[package_link]}')

            status_code = dic[package_link]
        
        else:
            status_code = request_packages(package_link)

            dic[package_link] = status_code

            write_request_package('packages_request_status_67', package_link, status_code)

            print(f'{total}: {package_link}: {status_code}')

        new_obj = {}
        new_obj['package_link'] = package_link
        new_obj['status_code'] = status_code

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_new')


def re_request_python(folder, filename):

    destination = f'{folder}/{filename}'

    dic = init_request_dic('packages_request_status_python')

    # new_request_template = f'https://pypi.org/pypi/{package_name}/json'

    total = 0

    with open(f'{destination}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    unique = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        package_link = json_obj['package_link'].replace('#', '').replace("'", "")

        package_name = package_link.split('/')[-1]

        new_request_url = f'https://pypi.org/pypi/{package_name}/json'

        if new_request_url in unique:
            unique.append(new_request_url)

        if new_request_url in dic.keys():
            print(f'{total}_already: {new_request_url}: {dic[new_request_url]}')

            status_code = dic[new_request_url]
        
        else:
            status_code = request_packages(new_request_url)

            dic[new_request_url] = status_code

            write_request_package('packages_request_status_python', new_request_url, status_code)

            print(f'{total}: {new_request_url}: {status_code}')

        new_obj = {}
        new_obj['package_link'] = new_request_url
        new_obj['status_code'] = status_code

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_new')



def re_request_php(folder, filename):

    destination = f'{folder}/{filename}'

    dic = init_request_dic('packages_request_status_php')

    total = 0

    with open(f'{destination}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()


    unique = []
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        package_link = json_obj['package_link'].replace('#', '').replace("'", "")

        if package_link in unique:
            continue

        unique.append(package_link)

        package_name_array = package_link.split('/')[-2:]

        package_name = ('/').join(package_name_array)

        if package_name.startswith("packages/"):
            # new_request_url = f'https://packagist.org/{package_name}.json'
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_new_incomplete')
            continue
        else:
            new_request_url = f'https://packagist.org/packages/{package_name}.json'

        if new_request_url in dic.keys():
            print(f'{total}_already: {new_request_url}: {dic[new_request_url]}')

            status_code = dic[new_request_url]
        
        else:
            status_code = request_packages(new_request_url)

            dic[new_request_url] = status_code

            write_request_package('packages_request_status_php', new_request_url, status_code)

            print(f'{total}: {new_request_url}: {status_code}')

        new_obj = {}
        new_obj['package_link'] = new_request_url
        new_obj['status_code'] = status_code

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_new')


def re_request_ruby(folder, filename):

    destination = f'{folder}/{filename}'

    dic = init_request_dic('packages_request_status_ruby')

    total = 0

    with open(f'{destination}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    unique = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        package_link = json_obj['package_link'].replace('#', '').replace("'", "")

        package_name = package_link.split('/')[-1]

        new_request_url = f'https://rubygems.org/api/v1/gems/{package_name}.json'

        if new_request_url in unique:
            continue

        unique.append(new_request_url)

        if new_request_url in dic.keys():
            print(f'{total}_already: {new_request_url}: {dic[new_request_url]}')
            
            status_code = dic[new_request_url]
        
        else:
            status_code = request_packages(new_request_url)

            dic[new_request_url] = status_code

            write_request_package('packages_request_status_ruby', new_request_url, status_code)

            print(f'{total}: {new_request_url}: {status_code}')

        new_obj = {}
        new_obj['package_link'] = new_request_url
        new_obj['status_code'] = status_code

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_new')        


def re_request_perl(folder, filename):

    destination = f'{folder}/{filename}'

    dic = init_request_dic('packages_request_status_perl')

    total = 0

    with open(f'{destination}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()


    unique = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        package_link = json_obj['package_link'].replace('#', '').replace("'", "")

        package_name = package_link.split('/')[-1]

        new_request_url = f'https://fastapi.metacpan.org/v1/module/{package_name}'

        if new_request_url in unique:
            continue

        unique.append(new_request_url)

        if new_request_url in dic.keys():
            print(f'{total}_already: {new_request_url}: {dic[new_request_url]}')
            status_code = dic[new_request_url]
        
        else:
            status_code = request_packages(new_request_url)

            dic[new_request_url] = status_code

            write_request_package('packages_request_status_perl', new_request_url, status_code)

            print(f'{total}: {new_request_url}: {status_code}')

        new_obj = {}
        new_obj['package_link'] = new_request_url
        new_obj['status_code'] = status_code

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_new')        


def request_package_45(folder, question_num, file):

    dic_registry = {
        'cpan': 'https://metacpan.org/pod/',
        'pip': 'https://pypi.org/project/',
        'composer': 'https://packagist.org/packages/',
        'gem': 'https://rubygems.org/gems/',
        'npm': 'https://registry.npmjs.org/'
    }

    with open(f'{folder}/{question_num}/{file}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = init_request_dic('packages_request_status_45')

    total = 0

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        total += 1

        package_information = json_obj['package_information']

        package_request = []

        link_list = json_obj['link_list']

        link_request = []

        custom_id = json_obj['custom_id']

        if len(package_information) <= 0 and len(link_list) <= 0:
            continue
        
        if len(package_information) > 0:
            package_array = package_information

            if is_2d_array(package_information):
                package_array = package_information[0]
            
            registry = dic_registry[package_array[1]]

            request_url = f'{registry}{package_array[0]}'

            if package_array[1] == 'npm' or package_array[1] == 'gem' or package_array[1] == 'composer':
                request_url = request_url.lower()

            if request_url in dic.keys():
                package_request.append([request_url, dic[request_url]])

                print(f'{total}_already: {request_url}: {dic[request_url]}')
            
            else:

                status_code = request_packages(request_url)

                dic[request_url] = status_code

                write_request_package('packages_request_status_45', request_url, status_code)

                package_request.append([request_url, status_code])

                print(f'{total}: {request_url}: {status_code}')
        
        if len(link_list) > 0:

            for link in link_list:

                request_url = link

                if request_url in dic.keys():
                    link_request.append([request_url, dic[request_url]])
                    print(f'{total}_already: {request_url}: {dic[request_url]}')
                
                else:
                    status_code = request_packages(request_url)

                    dic[request_url] = status_code

                    write_request_package('packages_request_status_45', request_url, status_code)

                    link_request.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')

        new_obj = {}
        new_obj['custom_id'] = json_obj['custom_id']
        new_obj['package_request'] = package_request
        new_obj['link_list'] = link_request

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{file}_request')



def request_package_67(folder, question_num, file):

    dic_registry = {
        'cpan': 'https://metacpan.org/pod/',
        'pip': 'https://pypi.org/project/',
        'composer': 'https://packagist.org/packages/',
        'gem': 'https://rubygems.org/gems/',
        'npm': 'https://registry.npmjs.org/'
    }

    with open(f'{folder}/{question_num}/{file}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = init_request_dic('packages_request_status_67')

    total = 0

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        total += 1

        package_information = json_obj['package_information']

        package_request = []

        # link_list = json_obj['link_list']

        link_request = []

        custom_id = json_obj['custom_id']

        # if len(package_information) <= 0 and len(link_list) <= 0:
        #     continue

        if len(package_information) <= 0:
            continue
        
        if len(package_information) > 0:

            for package_array in package_information:
                temp_package_array = package_array

                if is_2d_array(package_array) and len(package_array) > 0:
                    temp_package_array = package_array[0]
                
                if len(temp_package_array) <= 0:
                    continue
                
                registry = dic_registry[temp_package_array[1]]

                request_url = f'{registry}{temp_package_array[0]}'

                if temp_package_array[1] == 'npm' or temp_package_array[1] == 'gem' or temp_package_array[1] == 'composer':
                    request_url = request_url.lower()

                if request_url in dic.keys():
                    package_request.append([request_url, dic[request_url]])

                    print(f'{total}_already: {request_url}: {dic[request_url]}')
                
                else:

                    status_code = request_packages(request_url)

                    dic[request_url] = status_code

                    write_request_package('packages_request_status_67', request_url, status_code)

                    package_request.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')
        

        # if len(link_list) > 0:

        #     for link in link_list:

        #         request_url = link

        #         if request_url in dic.keys():
        #             link_request.append([request_url, dic[request_url]])
        #             print(f'{total}_already: {request_url}: {dic[request_url]}')
                
        #         else:
        #             status_code = request_packages(request_url)

        #             dic[request_url] = status_code

        #             write_request_package('packages_request_status_67', request_url, status_code)

        #             link_request.append([request_url, status_code])

        #             print(f'{total}: {request_url}: {status_code}')

        new_obj = {}
        new_obj['custom_id'] = json_obj['custom_id']
        new_obj['package_request'] = package_request
        new_obj['link_list'] = link_request

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{file}_request')






def translate_registry(registry):
    target_registry = ''

    registry = registry.lower()

    if 'cpan' in registry or 'perl' in registry:
        target_registry = 'cpan'
    
    if 'pypi' in registry or 'pip' in registry or 'python' in registry:
        target_registry = 'pip'

    if 'gem' in registry or 'ruby' in registry:
        target_registry = 'gem'
    
    if 'packagist' in registry or 'composer' in registry or 'php' in registry:
        target_registry = 'composer'
    
    if 'npm' in registry or 'node' in registry:
        target_registry = 'npm'

    
    return target_registry


def is_2d_array(arr):
    return all(isinstance(i, list) for i in arr)


def registry_arrange_4and5(folder, question_num):

    # folder = '/gpt-4o-mini'
    # question_num = 'question4'
    suffix = '_extract_final'

    with open(f'{folder}/{question_num}/{question_num}{suffix}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    registry_array = []

    total = 0
    need = 0

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj['package_information']

        new_package_information = []

        if is_2d_array(package_information):
            for package_array in package_information:
                total += 1
                registry = package_array[1]

                target_registry = translate_registry(registry)
                if target_registry != '':
                    new_package_information.append([package_array[0], target_registry, package_array[2]])
                    need += 1

                if registry not in registry_array and 'https' not in registry:
                    registry_array.append(registry)
        
        else:

            total += 1
            registry = package_information[1]

            target_registry = translate_registry(registry)
            if target_registry != '':
                new_package_information = [package_information[0], target_registry, package_information[2]]
                need += 1

            if registry not in registry_array and 'https' not in registry:
                registry_array.append(registry)
        
        json_obj['package_information'] = new_package_information
        
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}{suffix}_registry')

    print(total)
    print(need)

    # print(registry_array)

    # for registry in registry_array:
    #     target_registry = translate_registry(registry)

    #     if target_registry == '':
    #         print(f'{registry}: {target_registry}')
            


def registry_arrange_6and7(folder, question_num):
     
    # folder = '/gpt-4o-mini'
    suffix = '_extract_final'

    with open(f'{folder}/{question_num}/{question_num}{suffix}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    registry_array = []

    total = 0
    need = 0

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj['package_information']

        custom_id = json_obj['custom_id']

        new_package_information = []

        for package in package_information:
            
            if is_2d_array(package):
                temp_package_array = []
                for package_array in package:
                    total += 1
                    registry = package_array[1]

                    target_registry = translate_registry(registry)
                    if target_registry != '':
                        temp_package_array.append([package_array[0], target_registry, package_array[2]])
                        need += 1

                    if registry not in registry_array and 'https' not in registry:
                        registry_array.append(registry)

                new_package_information.append(temp_package_array)
            
            else:

                total += 1
                registry = package[1]

                target_registry = translate_registry(registry)
                if target_registry != '':
                    new_package_information.append([package[0], target_registry, package[2]])
                    need += 1

                if registry not in registry_array and 'https' not in registry:
                    registry_array.append(registry)

        json_obj['package_information'] = new_package_information
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{question_num}{suffix}_registry')

    # for registry in registry_array:
    #     target_registry = translate_registry(registry)

    #     if target_registry == '':
    #         print(f'{registry}: {target_registry}')

    print(total)
    print(need)



# folder = '/batches/gpt-3.5-turbo/data_total/question4'
# folder = '/batches/gpt-4o-mini/data_total'
# folder = '/batches/llama-3.1-sonar-small-128k-chat/data_total/question7'
# folder = '/batches/llama-3.1-8b-instruct/data_total/question7'
# folder = '/gpt-4o-mini'
# folder = '/defense'
# folder = r'\defense\top_20000_question2_q3'
# folder = r'\batches\llama-3.1-8b-instruct\batches_prompts_14'

folder = r'\defense\real_useful\question2_avoid'

# registry_arrange_6and7(folder, 'question7')


# registry_arrange_4and5(folder, 'question5')
# request_package_45(folder, 'question5', 'question5_extract_final_registry')    


request_packages_123(f'{folder}', 'question2', 'question2_parse')

# re_request_nodejs(folder, 'package_total_nodejs')
# re_request_python(folder, 'package_total_python')
# re_request_php(f'{folder}', 'package_total_php')
# re_request_php(f'{folder}/question2', 'package_total_php')
# re_request_php(f'{folder}/question4', 'package_total_php')
# re_request_ruby(folder, 'package_total_ruby')
# re_request_perl(folder, 'package_total_perl')
        

# request_package_67(folder, 'question7', 'question7_extract_final_registry')


def registry_arrange_total():

    folder_template = 'batches_prompts_'
    for index in range(0, 15):

        file_name = f'{folder_template}{index}'

        print(f'{folder}{file_name}')

        # registry_arrange_4and5(f'{folder}{file_name}', 'question5')

        # registry_arrange_6and7(f'{folder}{file_name}', 'question7')

        request_packages_123(f'{folder}{file_name}', 'question2', 'question2_parse')

        # request_package_45(f'{folder}{file_name}', 'question5', 'question5_extract_final_registry') 
        # request_package_67(f'{folder}{file_name}', 'question7', 'question7_extract_final_registry')


# registry_arrange_total()


def merge_two_files():

    with open(f'/packages_request_status_67.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    url_array = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        url = json_obj['url']
        status_code = json_obj['status_code']

        if url not in url_array:
            url_array.append(url)
        
    
    with open(f'/packages_request_status_67_1.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()
    
    for line in all_lines1:
        obj = json.loads(line.rstrip())

        url = obj['url']

        if url not in url_array:
            url_array.append(url)
            print(url)
            WriteData.write_in_path(json.dumps(obj), f'/packages_request_status_67')



# merge_two_files()



def detect_redirection(folder, question_num, file_name):

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        link_list = json_obj['link_list']

        total += 1

        for link in link_list:

            if 'github' not in link and 'gitlab' not in link:
                continue
            
            if link.endswith('.git'):
                link = link.rstrip('.git')

            if link in dic.keys():
                print(f'{total}_already: {link}')
                continue

            try:

                response = requests.get(link)
                
                history_list = response.history

                if len(history_list) > 0:
                    new_obj = {}
                    new_obj['original_url'] = link
                    new_obj['redirected_url'] = []
                    for history in history_list:
                        print(f'{custom_id}: {link}: {history.headers["Location"]}')
                        new_obj["redirected_url"].append(history.headers['Location'])

                    WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{file_name}_redirection')

                    dic[link] = new_obj['redirected_url']

                time.sleep(0.2)


            except:

                status_code = "exception"

# detect_redirection(folder, 'question7' ,'question7_extract')


# response = requests.get('http://www.freecharset.com/')
# print(response.status_code)

