import WriteData

import json

import random

import re

import hashlib


def random_license():

    licenses_array = ['Public Domain', 'MIT/X11', 'BSD-new', 'Apache 2.0', 'LGPLv2.1', 'LGPLv2.1+', 'LGPLv3', 'LGPLv3+', 'MPL 1.1', 'GPLv2', 'GPLv2+', 'GPLv3', 'GPLv3+', 'Affero GPLv3', 'Proprietary']
    random_value = random.choice(licenses_array)

    return random_value


def get_defense_id():

    id_dic = {}

    target_folder = r'\defense'

    with open(f'{target_folder}/top_20000.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        # custom_id = json_obj['custom_id']

        # custom_id = custom_id.replace('_2', '')

        custom_id = f'{json_obj["id"]}'

        id_dic[custom_id] = json_obj
    
    return id_dic



def prompt_based_defense():

    custom_id_array = []

    chatgpt_model = 'gpt-4o-mini'

    system_message = 'You are a helpful assistant skilled in generating, explaining, optimizing code across multiple programming languages.'

    write_path = '/defense/top_20000_prompts_new3'

    # id_dic = get_defense_id()

    with open(f'/defense/top_20000.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        obj = json.loads(line.rstrip())

        id = obj['id']
        title = obj['title'].lower()

        custom_id = f'{id}_1'
        
        if id not in custom_id_array:
            custom_id_array.append(id)
        else:
            continue

        # if custom_id not in id_dic.keys():
        #     continue

        print(f'{id}: {title}')

        # license_value = random_license()

        # prompt = f"{title}, please give me a code example to solve or realize the above question or task. Do not hallucinate. Do not fabricate factual information. Ensure every link and every package must exist, and the software licenses of the packages must be accurate and consistent."

        # prompt = f"do not hallucinate, do not fabricate factual information, and ensure that every recommended package and link exists: {title}."

        # prompt = f"{title}, please give me a code example to solve or realize the above question or task. Please avoid recommending URLs and packages."

        prompt = f"{title}, please give me a code example to solve or realize the above question or task. Do not recommend URLs and packages that can not be successfully requested."

        prompt_original = f"{title}, please give me a code example to solve or realize the above question or task. Recommended URLs and packages must be successfully requested."

        # prompt_license = f"{title}, my software is under {license_value}, please give me a code example to solve or realize the above question or task. Do not hallucinate. Do not fabricate factual information. Ensure every link and every package must exist, and the software licenses of the packages must be accurate and consistent while being compatible with my software."
        
        new_obj1 = {}
        new_obj1['custom_id'] = f'{id}_1'
        new_obj1['method'] = 'POST'
        new_obj1['url'] = '/v1/chat/completions'
        new_obj1['body'] = {}
        new_obj1['body']['model'] = chatgpt_model
        new_obj1['body']['messages'] = []
        new_obj1['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj1['body']['messages'].append({'role': 'user', 'content': f'{prompt_original}'})
        new_obj1['body']['max_tokens'] = 2000
        
        WriteData.write_in_path(json.dumps(new_obj1), write_path)

        # new_obj2 = {}
        # new_obj2['custom_id'] = f'{id}_2'
        # new_obj2['method'] = 'POST'
        # new_obj2['url'] = '/v1/chat/completions'
        # new_obj2['body'] = {}
        # new_obj2['body']['model'] = chatgpt_model
        # new_obj2['body']['messages'] = []
        # new_obj2['body']['messages'].append({'role': 'system', 'content': system_message})
        # new_obj2['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        # new_obj2['body']['max_tokens'] = 2000

        # WriteData.write_in_path(json.dumps(new_obj2), write_path)


# prompt_based_defense()





def get_original_top_20000():

    target_folder = r'\batches\gpt-4o-mini'

    write_path = r'\defense'

    batch_folder_template = 'batches_prompts_'

    id_dic = get_defense_id()

    total = 0
    for index in range(0, 15):

        combine_folder = f'{target_folder}/{batch_folder_template}{index}'

        with open(f'{combine_folder}/question2/question2.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()
        
        for line in all_lines:
            json_obj = json.loads(line.rstrip())

            custom_id = json_obj['custom_id']

            custom_id = custom_id.replace('_2', '')

            if custom_id in id_dic.keys():
                total += 1
                
                WriteData.write_in_path(json.dumps(json_obj), f'{write_path}/original_4o_mini_question2')

                # WriteData.write_in_path(json.dumps(id_dic[custom_id]), f'{write_path}/comparison_4o_mini')

    print(total)


# get_original_top_20000()


def count_number(file_name):

    print(file_name)

    # target_folder = r'\defense\top_20000_question2'
    target_folder = r'\defense\top_20000_question2_q3\question2'

    # original_ids = get_defense_id()

    with open(f'{target_folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    package_num = 0
    package_404 = 0
    link_num = 0
    link_404 = 0

    total_count = 0

    package_unique = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        total_count += 1

        extract_packages = json_obj['extract_packages']
        
        # link_list = json_obj['link_list']

        if len(extract_packages) > 0:

            for packages in extract_packages:
                
                package_array = packages[1:]

                for package in package_array:
                    if package not in package_unique:
                        package_unique.append(package)
                        WriteData.write_in_path(json.dumps({'package': package}), f'{target_folder}/question2_parse_unique_packages')

        # if len(link_list) > 0:
        #     for link in link_list:
        #         link_num += 1

        #         if link[1] == 404 or link[1] == 'exception':
        #             link_404 += 1
        
    print(f'package count: {len(package_unique)}')
    # print(f'package 404: {package_404}')
    # print(f'link count: {link_num}')
    # print(f'link 404: {link_404}')

    # print(f'total count: {total_count}')


# count_number('question2_parse')


def generate_prompt():

    # target_folder = r'\gpt-4o-mini\question2'

    target_folder = r'\defense'

    chatgpt_model = 'gpt-4o-mini'

    system_message = 'You are a helpful assistant skilled in generating, explaining, optimizing code across multiple programming languages.'

    write_path = '/defense/top_20000_question2_q1_url'

    with open(f'{target_folder}/top_20000_question2.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        output = json_obj['output']   #q1

        # extracted_package = json_obj['extracted_package']   #q2

        # q2
        # if len(extracted_package) <= 0:
        #     continue

        # title = json_obj['title']

        # packages = json_obj['packages']

        # prompt = f"{output} Are there any packages installed using commands in the content above? If yes, please extract all the packages and their registries from the content above. Do not alter package names, and output packages and registries in JSON array format. This JSON format should only contain the keys package-name and registry; only output this JSON data. If no, simply output 'no'."

        prompt = f"{output} Are there any external URLs used in the content above? If yes, please extract all the URLs from the content above. Do not alter URLs, and output URLs in JSON array format. This JSON format should only contain the key url; only output this JSON data. If no, simply output 'no'."

        # prompt_q2 = f"{extracted_package}. Please check if the packages in the above json data, which are the values corresponding to the key package-name, exist in their corresponding registry (returning true or false), which are the values corresponding to the key registry. If the package does not exist, provide a package with the same functionality, which must exist in the corresponding registry. Please output them in JSON format. This JSON format should only contains four keys package-name, registry, existence, and similar-package; only output this JSON data."

        # prompt_q3 = f"Please use the following packages, {packages}, and give me a code example to solve or realize the following problem or task, {title}"

        new_obj1 = {}
        new_obj1['custom_id'] = f'{custom_id}'
        new_obj1['method'] = 'POST'
        new_obj1['url'] = '/v1/chat/completions'
        new_obj1['body'] = {}
        new_obj1['body']['model'] = chatgpt_model
        new_obj1['body']['messages'] = []
        new_obj1['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj1['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        new_obj1['body']['max_tokens'] = 5000
        
        WriteData.write_in_path(json.dumps(new_obj1), write_path)


# generate_prompt()

def md5(url):

    md5_hash = hashlib.md5()

    md5_hash.update(url.encode('utf-8'))

    md5_value = md5_hash.hexdigest()

    return md5_value



def generate_prompt_q2():

    # target_folder = r'\batches\gpt-4o-mini\batches_prompts_14\question2'

    target_folder = r'\defense'

    chatgpt_model = 'gpt-4o-mini'

    # system_message = 'You are a helpful assistant skilled in generating, explaining, optimizing code across multiple programming languages.'
    system_message = 'You are an assistant skilled in making HTTP requests.'

    write_path = '/defense/top_20000_question2_q2_url'

    with open(f'{target_folder}/top_20000_question2_q1_url_output_parse.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()


    package_array = []


    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        # extracted_package = json_obj['extracted_package']   #q1

        extracted_package = json_obj['extract_urls']   #q1

        if len(extracted_package) <= 0:
            continue
        
        
        for package in extracted_package:

            #--------------------q1----------------------------------
            # try:
            #     package_name = package['package-name']
            #     registry = package['registry']
            #     key = f'{package_name}#{registry}'
            # except:
            #     print(package)

            # if key in package_array:
            #     continue
            # else:
            #     package_array.append(key)
            #--------------------q1----------------------------------

            key = md5(package)

            if key in package_array:
                continue

            package_array.append(key)

            
            # prompt_q2 = f"Please only provide a yes or no answer to whether the package '{package_name}' exists in the '{registry}' registry. Ensure that you check for the existence of the exact package name. Do not alter the package name, and do not mark it as existing based on similar package names."

            # prompt_q2 = f"Please check the status of the url, {package}, and output it in JSON format. This JSON format should only contain the keys url and the status-code; only output this JSON data. Ensure that you check for the status of the exact url. Do not alter the url."

            prompt_q2 = f"{package}, please check whether the url above can be accessible, and output it in JSON format. This JSON format should only contain the keys url and the status-code; only output this JSON data. Ensure that you check for the status of the exact url. Do not alter the url."

            new_obj1 = {}
            new_obj1['custom_id'] = f'{key}'
            new_obj1['method'] = 'POST'
            new_obj1['url'] = '/v1/chat/completions'
            new_obj1['body'] = {}
            new_obj1['body']['model'] = chatgpt_model
            new_obj1['body']['messages'] = []
            new_obj1['body']['messages'].append({'role': 'system', 'content': system_message})
            new_obj1['body']['messages'].append({'role': 'user', 'content': f'{prompt_q2}'})
            new_obj1['body']['max_tokens'] = 5000
            
            WriteData.write_in_path(json.dumps(new_obj1), write_path)


# generate_prompt_q2()


def extract_json():

    pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'

    write_path = '/defense'

    with open(f'{write_path}/top_20000_question2_q1_output.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    registry_array = []

    registry_dic = {
        'npm': ['npmjs.com', 'npx', 'npm', 'npmjs', 'NPM', 'https://nodejs.org/', 'https://registry.npmjs.org/', 'https://nodejs.org', 'Node.js standard library', 'Node.js'], 
        'PyPI': ['Pypi', 'pip3', 'Python', 'Standard Library (Python)', 'Python Standard Library', 'PyPI', 'pypi', 'pip', 'Python Package Index (PyPI)', 'python', 'Python Package Index', 'https://www.python.org/', 'getcomposer.org'], 
        'Packagist': ['Packagist', 'packagist.org', 'PHP', 'https://getcomposer.org', 'composer', 'Composer', 'packagist', 'https://www.php.net/'],
        'RubyGems': ['gem', 'rubygems', 'Gemfile', 'RubyGems', 'rubygems.org', 'ruby', 'RubyGem', 'ruby standard library', 'standard Ruby library', 'Ruby Standard Library', 'Ruby standard library', 'Rubygems', 'Ruby Gem'],
        'CPAN': ['CPAN', 'cpan', 'Perl Standard Library', 'cpanm', 'Perl', 'perl']
    }

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        content = json_obj['response']['body']['choices'][0]['message']['content']

        if content == 'no':
            continue

        result = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        length = len(result)

        if length <= 0:
            continue
        
        extracted_packages = []
        
        for jsonstr in result:

            try:
                obj_array = json.loads(jsonstr)

                for obj in obj_array:
                    package_name = obj['package-name']
                    old_registry = obj['registry']

                    registry = ''

                    if old_registry in registry_dic['npm'] or old_registry.startswith('https://www.npmjs.com'):
                        registry = 'npm'
                    
                    elif old_registry in registry_dic['PyPI'] or old_registry.startswith('pip install') or old_registry.startswith('https://pypi.org'):
                        registry = 'PyPI'
                    
                    elif old_registry in registry_dic['Packagist'] or old_registry.startswith('composer require') or old_registry.startswith('https://packagist.org') or old_registry.startswith('https://getcomposer.org'):
                        registry = 'Packagist'
                    
                    elif old_registry in registry_dic['RubyGems'] or old_registry.startswith('gem install') or old_registry.startswith('gem command') or old_registry.startswith('https://rubygems.org'):
                        registry = 'RubyGems'
                    
                    elif old_registry in registry_dic['CPAN'] or old_registry.startswith('https://metacpan.org'):
                        registry = 'CPAN'
                    
                    if registry == '':
                        continue
                    
                    obj['registry'] = registry

                    extracted_packages.append(obj)

            except:
                # print(jsonstr)
                a=1
        if len(extracted_packages) <= 0:
            continue

        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['extracted_package'] = extracted_packages

        WriteData.write_in_path(json.dumps(new_obj), f'{write_path}/top_20000_question2_q1_output_parse')
                    
# extract_json()


def get_question():

    write_path = '/gpt-4o-mini/question2'

    questino_dic = {}

    with open(f'{write_path}/question2_parse.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        title = json_obj['title'].replace('please give me a code example to solve or realize the following problem or task, ', '')

        questino_dic[custom_id] = title
    
    return questino_dic



def extract_json_q2():

    write_path = '/defense'

    with open(f'{write_path}/top_20000_question2_q2_output.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        content = json_obj['response']['body']['choices'][0]['message']['content']

        print(f'{custom_id}: {content}')

        if content.startswith('Yes'):
            existence = True
        else:
            existence = False

        custom_array = custom_id.split('#')
        package_name = custom_array[0]
        registry = custom_array[1]

        new_obj = {}
        new_obj['package-name'] = package_name
        new_obj['registry'] = registry
        new_obj['existence'] = existence

        WriteData.write_in_path(json.dumps(new_obj), f'{write_path}/top_20000_question2_q2_output_parse')


       
# extract_json_q2()   


def verification():

    question_folder = r'\defense\top_20000_question2'

    another_folder = r'\defense'

    registry_obj = {
        'pip install': 'PyPI', 
        'npm install': 'npm', 
        'gem install': 'RubyGems', 
        'composer require': 'Packagist', 
        'cpan ': 'CPAN', 
        'cpanm ': 'CPAN'
    }

    package_defense = []

    with open(f'{another_folder}/top_20000_question2_q2_output_parse.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()

    for line in all_lines1:
        json_obj = json.loads(line.rstrip())

        package_name = json_obj['package-name']
        registry = json_obj['registry']
        existence = json_obj['existence']
        key = f'{package_name}#{registry}'
        
        if existence is False and key not in package_defense:
            package_defense.append(key)


    with open(f'{question_folder}/top_20000_question2_parse.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        extract_packages = json_obj['extract_packages']

        new_extract_packages = []

        for packages in extract_packages:
            
            install_command = packages[0]

            registry = registry_obj[install_command]

            sub_packages = []

            package_array = packages[1:]

            for package in package_array:
                temp_key = f'{package}#{registry}'

                if temp_key in package_defense:
                    continue
                
                sub_packages.append(package)
            
            if len(sub_packages) <= 0:
                continue
            
            sub_packages.insert(0, install_command)
            new_extract_packages.append(sub_packages)
        
        json_obj['extract_packages'] = new_extract_packages
            
        WriteData.write_in_path(json.dumps(json_obj), f'{question_folder}/question2_verfication_parse')

       
# verification()


def arrange_url(url):

    if not url.startswith('http') and not url.startswith('github'):
        return ''
    
    if url.startswith('github'):
        return f'https://{url}'
    
    if 'example.' in url or '127.0.0.1' in url or 'localhost' in url or '/example' in url:
        return ''
    
    if '//YOUR' in url or '//<' in url or '/user/' in url or '/users/' in url or '//123.' in url:
        return ''
    
    if 'username' in url or 'your' in url or 'account_name.' in url or 'USERNAME' in url:
        return ''
    
    return url
        

        
def extract_json_q1_url():

    pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'

    write_path = '/defense'

    with open(f'{write_path}/top_20000_question2_q1_url_output.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        content = json_obj['response']['body']['choices'][0]['message']['content']

        extract_urls = []

        if content == 'no':
            continue

        result = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        length = len(result)

        if length <= 0:
            continue
        
        for jsonstr in result:

            try:
                obj_array = json.loads(jsonstr)

                if isinstance(obj_array, list):
                    
                    if len(obj_array) <= 0:
                        continue

                    for obj in obj_array:
                        if 'url' in obj:
                            new_url = arrange_url(obj['url'])
                        else:
                            new_url = arrange_url(obj)
                        
                        if new_url != '' and new_url not in extract_urls:
                            extract_urls.append(new_url)

                else:
                    url_list = obj_array['url']

                    for url in url_list:
                        new_url = arrange_url(url)

                        if new_url != '' and new_url not in extract_urls:
                            extract_urls.append(new_url)

            except:
                # print(jsonstr)
                a=1
        
        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['extract_urls'] = extract_urls
        WriteData.write_in_path(json.dumps(new_obj), f'{write_path}/top_20000_question2_q1_url_output_parse')


# extract_json_q1_url()


def generate_prompt_q3():

    target_folder = r'\defense\top_20000_question2'

    chatgpt_model = 'gpt-4o-mini'

    registry_obj = {
        'pip install': 'PyPI', 
        'npm install': 'npm', 
        'gem install': 'RubyGems', 
        'composer require': 'Packagist', 
        'cpan ': 'CPAN', 
        'cpanm ': 'CPAN'
    }

    system_message = 'You are a helpful assistant skilled in generating, explaining, optimizing code across multiple programming languages.'

    write_path = '/defense/top_20000_question2_q3'

    with open(f'{target_folder}/question2_verfication_parse.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        extract_packages = json_obj['extract_packages']

        title = json_obj['title'].replace('please give me a code example to solve or realize the following problem or task, ', '')

        new_packages = []

        temp_prompt = ""
        
        if len(extract_packages) <= 0:
            continue

        for packages in extract_packages:
            install_commad = packages[0]

            registry = registry_obj[install_commad]

            temp_prompt += f" packages, {packages[1:]} in the registry {registry},"
        
        prompt = f"Please use the {temp_prompt} to solve or realize the following problem or task: {title}. Only use the provided packages. Do not alter package names, and do not add additional packages."

        new_obj1 = {}
        new_obj1['custom_id'] = f'{custom_id}'
        new_obj1['method'] = 'POST'
        new_obj1['url'] = '/v1/chat/completions'
        new_obj1['body'] = {}
        new_obj1['body']['model'] = chatgpt_model
        new_obj1['body']['messages'] = []
        new_obj1['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj1['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        new_obj1['body']['max_tokens'] = 5000

        WriteData.write_in_path(json.dumps(new_obj1), write_path)


# generate_prompt_q3()

folder = r'\defense\real_useful\question2_avoid\question2'

def get_unique_packages(folder, filename):

    with open(f'{folder}/{filename}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    unique_package = {}
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_request = json_obj['package_request']

        for package in package_request:
            link = package[0]
            status_code = package[1]

            if link in unique_package.keys():
                continue

            unique_package[link] = status_code

            new_obj = {}
            new_obj['package'] = link
            new_obj['status'] = status_code

            WriteData.write_in_path(json.dumps(new_obj), f'{folder}/question2_parse_unique_packages')
    
    # for package in unique_package.keys():
    #     print(package)

    #     if package.startswith('https://fastapi.metacpan.org/v1/module'):
    #         package = package.replace('https://fastapi.metacpan.org/v1/module/', '')

    #     elif package.startswith('https://pypi.org/pypi/'):
    #         package = package.replace('https://pypi.org/pypi/', '')

    #     elif package.startswith('https://packagist.org/packages/'):
    #         package = package.replace('https://packagist.org/packages/', '')

    #     elif package.startswith('https://rubygems.org/api/v1/gems/'):
    #         package = package.replace('https://rubygems.org/api/v1/gems/', '')
        
    #     elif package.startswith('https://registry.npmjs.org/'):
    #         package = package.replace('https://registry.npmjs.org/', '')

    #     new_obj = {}
    #     new_obj['package'] = package
    #     new_obj['status'] = status_code

    #     WriteData.write_in_path(json.dumps(new_obj), f'{folder}/question2_parse_unique_packages')

# get_unique_packages(folder, 'question2_parse_request')
