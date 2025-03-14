import WriteData

import json

import re

import hashlib

def read_real_license(folder, file_name):

    dic = {}

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        link = json_obj['link']

        license = json_obj['license']

        dic[link] = license
    
    return dic


def is_2d_array(arr):
    return all(isinstance(i, list) for i in arr)


def read_request_file(folder, question_num, file_name):

    parent_folder = 's/data_again'

    # write_path = r'\batches\gpt-4o-mini\data_total\licenses'


    dic_nodejs = read_real_license(parent_folder, 'package_nodejs_infor')
    dic_python = read_real_license(parent_folder, 'package_python_infor')
    dic_perl = read_real_license(parent_folder, 'package_perl_info')
    dic_php = read_real_license(parent_folder, 'package_php_info')
    dic_ruby = read_real_license(parent_folder, 'package_ruby_infor')

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        # package_information = json_obj['package_information']

        # if len(package_information) <= 0:
        #     continue

        # if is_2d_array(package_information):
        #     new_package_information = [package_information[0][0], package_information[0][1], f'{package_information[0][2]} or {package_information[1][2]}']
        #     package_information = new_package_information

        package_name = json_obj['package_name']

        registry = json_obj['registry']

        license = json_obj['licenses'][0]

        # link = f'{dic_registry[registry]}{package_name}'
        if registry == 'npm':
            link = f'https://registry.npmjs.org/{package_name}'
        
        if registry == 'pip':
            link = f'https://pypi.org/pypi/{package_name}/json'
        
        if registry == 'gem': 
            link = f'https://rubygems.org/api/v1/gems/{package_name}.json'
        
        if registry == 'cpan':
            link = f'https://fastapi.metacpan.org/v1/module/{package_name}'

        if registry == 'composer':
            link = f'https://packagist.org/packages/{package_name}.json'


        if registry == 'composer':
            if '/' not in package_name:
                # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_package_incomplete')
                # WriteData.write_in_path(json.dumps(json_obj), f'{write_path}/{question_num}_package_incomplete')
                continue

        real_license = ''

        if registry == 'npm':
            if link in dic_nodejs.keys():
                real_license = dic_nodejs[link]
        
        elif registry == 'pip':
            if link in dic_python.keys():
                real_license = dic_python[link]
        
        elif registry == 'composer':
            if link in dic_php.keys() and dic_php[link] != 'exception':
                real_license = dic_php[link]
            # else:
            #     # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_package_notfound')
            #     WriteData.write_in_path(json.dumps(json_obj), f'{write_path}/{question_num}_package_notfound')
            #     continue
        
        elif registry == 'gem':
            if link in dic_ruby.keys():
                real_license = dic_ruby[link]
        
        elif registry == 'cpan':
            if link in dic_perl.keys():
                real_license = dic_perl[link]
        
        if real_license != '':
            obj = {}
            obj['custom_id'] = f'{package_name}#{registry}'
            obj['registry'] = registry
            obj['packages_name'] = package_name
            obj['link'] = link
            obj['obtained_license'] = license
            obj['real_license'] = real_license

            # WriteData.write_in_path(json.dumps(obj), f'{folder}/{question_num}/{file_name}_licenses')
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question_num}/{file_name}_real_licenses')


        
    
    # print(license_array)

        

def formulate_prompts(folder, question_num, file_name):

    chatgpt_model = 'gpt-4o'

    system_message = 'You are a helpful assistant skilled in understanding software licenses.'

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj["custom_id"]
        obtained_license = json_obj["obtained_license"]
        real_license = json_obj["real_license"]

        prompt = f'please give me an answer of yes or no, do the following two licenses refer to the same license: \'{obtained_license}\' and \'{real_license}\''
        
        new_obj = {}

        new_obj['custom_id'] = custom_id
        new_obj['method'] = 'POST'
        new_obj['url'] = '/v1/chat/completions'
        new_obj['body'] = {}
        new_obj['body']['model'] = chatgpt_model
        new_obj['body']['messages'] = []
        new_obj['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        new_obj['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{file_name}_prompts')


def prompts_result_analysis(folder, question_num, file_name):

    with open(f'{folder}/{question_num}/{file_name}_prompts_output.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        result = json_obj['response']['body']['choices'][0]['message']['content']

        dic[custom_id] = result
    

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()

    total_yes = 0
    total_no = 0
    for line in all_lines1:

        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        result = dic[custom_id]

        if 'yes' in result.lower():
            total_yes += 1
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question_num}/{file_name}_yes')
        else:
            total_no += 1
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question_num}/{file_name}_no')
    
    print(total_yes)
    print(total_no)



def formulate_prompts_compatibility(folder, question_num, file_name):


    chatgpt_model = 'gpt-4o'

    system_message = 'You are a helpful assistant skilled in understanding software licenses.'

    # with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
    #     all_lines = f.readlines()
    #     f.close()

    # dic = []

    # for line in all_lines:
        
    #     json_obj = json.loads(line.rstrip())

    #     package_name = json_obj['package_name']

    #     dic.append(package_name)
    
    unique_id = []

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()

    for line1 in all_lines1:
        obj = json.loads(line1.rstrip())

        custom_id = obj["custom_id"]
        under_license = obj["under_license"]

        if custom_id in unique_id:
            continue

        unique_id.append(custom_id)

        package_information = obj['package_information']

        if len(package_information) <= 0:
            continue
        
        print(package_information)
        package_name = package_information[0]

        # if package_name not in dic:
        #     continue

        obtained_license = package_information[2]

        prompt = f'Please give me an answer of yes or no, my software\'s license is under \'{under_license}\', to maintain my software license compatibility, can I use a package with a license under \'{obtained_license}\''
        
        new_obj = {}

        new_obj['custom_id'] = custom_id
        new_obj['method'] = 'POST'
        new_obj['url'] = '/v1/chat/completions'
        new_obj['body'] = {}
        new_obj['body']['model'] = chatgpt_model
        new_obj['body']['messages'] = []
        new_obj['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        new_obj['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/{file_name}_prompts')



def read_request_file7(folder, question_num, file_name):

    parent_folder = 's/data_again'

    write_path = r'\batches\gpt-4o-mini\data_total\licenses'

    dic_registry = {
        'cpan': 'https://metacpan.org/pod/',
        'pip': 'https://pypi.org/project/',
        'composer': 'https://packagist.org/packages/',
        'gem': 'https://rubygems.org/gems/',
        'npm': 'https://registry.npmjs.org/'
    }

    dic_nodejs = read_real_license(parent_folder, 'packages_license_nodejs')
    # dic_python = read_real_license(parent_folder, 'packages_license_python')
    # dic_perl = read_real_license(parent_folder, 'packages_license_perl')
    # dic_php = read_real_license(parent_folder, 'packages_license_php')
    # dic_ruby = read_real_license(parent_folder, 'packages_license_ruby')

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_information = json_obj['package_information']

        new_incomplete = []

        new_notfound = []

        if len(package_information) <= 0:
            continue
        
        for index in range(0, len(package_information)):

            package_array = package_information[index]

            if len(package_array) <= 0:
                continue

            if is_2d_array(package_array):
                new_package_array = [package_array[0][0], package_array[0][1], f'{package_array[0][2]} or {package_array[1][2]}']
                package_array = new_package_array

            custom_id = json_obj['custom_id']

            package_name = package_array[0]
            
            registry = package_array[1]
            
            license = package_array[2]

            link = f'{dic_registry[registry]}{package_name}'

            real_license = ''

            if registry == 'composer' and '/' not in package_name:
                # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_package_incomplete')
                new_incomplete.append(package_array)
                continue

            if registry == 'npm':
                if link in dic_nodejs.keys():
                    real_license = dic_nodejs[link]
            
            # elif registry == 'pip':
            #     if link in dic_python.keys():
            #         real_license = dic_python[link]
            
            # elif registry == 'composer':
            #     # if link in dic_php.keys():
            #     #     real_license = dic_php[link]
                
            #     if link in dic_php.keys() and dic_php[link] != 'exception':
            #         real_license = dic_php[link]
            #     else:
            #         # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_package_notfound')
            #         new_notfound.append(package_array)
            #         continue
            
            # elif registry == 'gem':
            #     if link in dic_ruby.keys():
            #         real_license = dic_ruby[link]
            
            # elif registry == 'cpan':
            #     if link in dic_perl.keys():
            #         real_license = dic_perl[link]
            
            if real_license != '':
                obj = {}
                obj['custom_id'] = f'{custom_id}_{index}'
                obj['registry'] = registry
                obj['package_name'] = package_name
                obj['link'] = link
                obj['obtained_license'] = license
                obj['real_license'] = real_license

                # WriteData.write_in_path(json.dumps(obj), f'{folder}/{question_num}/{file_name}_licenses')
                WriteData.write_in_path(json.dumps(obj), f'{write_path}/{question_num}_licenses')

        if len(new_incomplete) > 0:
            json_obj['package_information'] = new_incomplete
            # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_package_incomplete')
            WriteData.write_in_path(json.dumps(json_obj), f'{write_path}/{question_num}_package_incomplete')

        if len(new_notfound) > 0:
            json_obj['package_information'] = new_notfound
            # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_package_notfound')
            WriteData.write_in_path(json.dumps(json_obj), f'{write_path}/{question_num}_package_notfound')


def compare_license_accurate(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        obtained_license = json_obj['obtained_license']

        real_license = json_obj['real_license']

        if obtained_license != real_license:

            if not real_license or obtained_license not in real_license:
                print(f'{custom_id}: {obtained_license}, {real_license}')
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_inaccurate')
            else:
                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_accurate')
        
        else:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_accurate')

            


# folder = 's/data_again/gpt-4o-mini'

# folder = r'\batches\gpt-3.5-turbo\data_total'
# folder = r'\batches\llama-3.1-8b-instruct\data_total'
# folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'
folder = r'\batches\gpt-4o-mini\data_total'
question = 'question5'


# compare_license_accurate(f'{folder}/{question}', 'question5_extract_final_registry_consistency_real_licenses')

# read_real_license('s/data_again', 'packages_license_nodejs')

# read_request_file(folder, question, f'{question}_extract_final_registry_consistency')

# read_request_file(folder, 'question4', 'question4_extract_final_registry')

# formulate_prompts(folder, question, f'{question}_extract_final_registry_consistency_real_licenses')

# prompts_result_analysis(folder, 'question7', 'question7_extract_final_registry_licenses')


# formulate_prompts_compatibility(folder, question, 'question7_pre_compatibility')


# read_request_file7(folder, 'question6', 'question6_extract_final_registry')


def license_compare_total_5(folder, question_num, file_name):
    
    read_request_file(folder, question_num, file_name)

    formulate_prompts(folder, question_num, f'{file_name}_licenses')


# license_compare_total_5(folder, 'question4', 'question4_extract_final_registry')

def license_compare_total():

    folder_template = 'batches_prompts_'

    question_num = 'question5'

    for index in range(0, 1):

        file_name = f'{folder_template}{index}'

        target_folder = f'{folder}/{file_name}'

        print(f'{target_folder}/{question_num}')

        read_request_file(target_folder, question_num, f'{question_num}_extract_final_registry')

        formulate_prompts(target_folder, question_num, f'{question_num}_extract_final_registry_licenses')

        # read_request_file7(target_folder, question_num, f'{question_num}_extract_final_registry')

        # formulate_prompts(target_folder, question_num, f'{question_num}_extract_final_registry_licenses')

     
# license_compare_total()



def md5_hash(temp_str):

    md5_hash = hashlib.md5()

    md5_hash.update(temp_str.encode('utf-8'))

    hash_result = md5_hash.hexdigest()

    return hash_result


def get_unique_compare_licenses():

    chatgpt_model = 'gpt-4o'

    system_message = 'You are a helpful assistant skilled in understanding software licenses.'

    folder_template = 'batches_prompts_'

    question_num_array = ['question4', 'question5', 'question6', 'question7']

    dic = {}

    for question_num in question_num_array:
        target_folder = 's/data_again/gpt-4o-mini'

        print(target_folder)

        file_name = f'{question_num}_extract_final_registry_licenses'

        with open(f'{target_folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        for line in all_lines:

            json_obj = json.loads(line.rstrip())

            obtained_license = json_obj['obtained_license']

            real_license = json_obj['real_license']

            key = f'{obtained_license}#{real_license}'

            hash_key = md5_hash(key)

            if hash_key not in dic:
                dic[hash_key] = [obtained_license, real_license]



    for index in range(0, 14):

        target_folder = f'{folder}/{folder_template}{index}'

        for question_num in question_num_array:

            print(f'{target_folder}/{question_num}')

            file_name = f'{question_num}_extract_final_registry_licenses'

            with open(f'{target_folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
                all_lines = f.readlines()
                f.close()

            for line in all_lines:

                json_obj = json.loads(line.rstrip())

                obtained_license = json_obj['obtained_license']

                real_license = json_obj['real_license']

                key = f'{obtained_license}#{real_license}'

                hash_key = md5_hash(key)

                if hash_key not in dic:
                    dic[hash_key] = [obtained_license, real_license]
    
    WriteData.write_in_path(json.dumps(dic), f's/data_again/package_license_unique')

    for key in dic.keys():

        obtained_license = dic[key][0]
        real_license = dic[key][1]

        prompt = f'please give me an answer of yes or no, does the following two phrases refer to the same license: \'{obtained_license}\' and \'{real_license}\''
        
        new_obj = {}

        new_obj['custom_id'] = key
        new_obj['method'] = 'POST'
        new_obj['url'] = '/v1/chat/completions'
        new_obj['body'] = {}
        new_obj['body']['model'] = chatgpt_model
        new_obj['body']['messages'] = []
        new_obj['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        new_obj['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj), f's/data_again/package_license_unique_prompts')



def get_total_packages_question():

    question_num = 'question6'

    folder_template = 'batches_prompts_'

    for index in range(0, 15):

        batch_folder = f'{folder_template}{index}'

        print(f'{folder}/{batch_folder}/{question_num}')

        target_folder = f'{folder}/{batch_folder}'
        
        # read_request_file(target_folder, question_num, f'{question_num}_extract_final_registry')
        read_request_file7(target_folder, question_num, f'{question_num}_extract_final_registry')



# get_unique_compare_licenses()

# get_total_packages_question()


def same_package_different_license():

    folder = r'\batches\llama-3.1-8b-instruct\batches_prompts_14\question4'

    file_name = 'question7_licenses'

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic_package_name = {}

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_name = json_obj['package_name']

        obtained_license = json_obj['obtained_license']

        registry = json_obj['registry']

        real_license = json_obj['real_license']

        unique = f'{package_name}#{registry}'

        if unique not in dic_package_name.keys():
            dic_package_name[unique] = []
        
        else:
            if obtained_license not in dic_package_name[unique]:
                dic_package_name[unique].append(obtained_license)
    
    total = 0
    for key in dic_package_name.keys():
        obtained_license_list = dic_package_name[key]

        if len(obtained_license_list) > 1:
            total += 1
            print(f'{key}: {obtained_license_list}')

            obj = {}
            obj['package_name'] = key
            # obj['registry'] = registry
            # obj['real_license'] = real_license
            obj['obtained_license'] = obtained_license_list

            WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_obtained_conflict')


    print(total)


# same_package_different_license()

def get_same_package_difference_license():

    folder = r'\batches\llama-3.1-8b-instruct\batches_prompts_14\question4'

    file_name = 'question4_extract_final_registry'

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic_package_name = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_information = json_obj['package_information']

        if len(package_information) <= 0:
            continue

        package_name = package_information[0]

        package_registry = package_information[1]

        package_license = package_information[2]

        unique = f'{package_name}#{package_registry}'

        if unique not in dic_package_name.keys():
            dic_package_name[unique] = []
        
        else:
            if package_license not in dic_package_name[unique]:
                dic_package_name[unique].append(package_license)
        

    total = 0
    for key in dic_package_name.keys():
        obtained_license_list = dic_package_name[key]

        if len(obtained_license_list) > 1:
            total += 1
            print(f'{key}: {obtained_license_list}')


# get_same_package_difference_license()



