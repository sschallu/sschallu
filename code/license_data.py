import WriteData

import json

import requests

import time

import re

import numpy as np

import ast



def read_files(destination, suffix):

    with open(f'{destination}.{suffix}', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def is_2d_array(array):
    return (
        isinstance(array, list) and 
        all(isinstance(row, list) for row in array)
    )


def inconsistency_analysis_question5(folder, question, file_name):

    destination = f'{folder}/{question}/{file_name}'

    all_lines = read_files(destination, 'json')

    dic = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_information = json_obj['package_information']

        if len(package_information) <= 0:
            continue

        if is_2d_array(package_information):
            package_information = package_information[0]

        if len(package_information) == 2:
            print(f'{custom_id}')
            print(package_information)

        package_name = package_information[0]

        if package_name == "":
            continue

        package_registry = package_information[1]

        license = package_information[2].replace(',', '')

        key = f'{package_name}#{package_registry}'

        if key not in dic.keys():
            dic[key] = [license]
        
        else:
            if license not in dic[key]:
                dic[key].append(license)
    
    for key in dic.keys():
        obj = {}
        obj['package_name'] = key.split('#')[0]
        obj['registry'] = key.split('#')[1]
        obj['licenses'] = dic[key]

        if key.split('#')[0] == "":
            continue

        if len(dic[key]) > 1:
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question}/{file_name}_inconsistency')
        # else:
        #     WriteData.write_in_path(json.dumps(obj), f'{folder}/{question}/{file_name}_consistency')



def inconsistency_analysis_question7(folder, question, file_name):

    destination = f'{folder}/{question}/{file_name}'

    all_lines = read_files(destination, 'json')

    dic = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_information = json_obj['package_information']

        if len(package_information) <= 0:
            continue

        for packages in package_information:
            
            if len(packages) <= 0:
                continue

            if is_2d_array(packages):
                packages = packages[0]

            package_name = packages[0]

            if package_name == "":
                continue

            package_registry = packages[1]

            license = packages[2].replace(',', '')

            key = f'{package_name}#{package_registry}'

            if key not in dic.keys():
                dic[key] = [license]
            
            else:
                if license not in dic[key]:
                    dic[key].append(license)
    
    for key in dic.keys():
        obj = {}
        obj['package_name'] = key.split('#')[0]
        obj['registry'] = key.split('#')[1]
        obj['licenses'] = dic[key]

        if key.split('#')[0] == "":
            continue

        if len(dic[key]) > 1:
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question}/{file_name}_inconsistency')
        else:
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question}/{file_name}_consistency')


def count_license(folder, question, filename):

    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    count_obj = {}
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj['licenses']

        count = len(licenses)

        if count not in count_obj.keys():
            count_obj[count] = 1
        else:
            count_obj[count] += 1
    
    sorted_dict = {key: count_obj[key] for key in sorted(count_obj.keys())}

    new_dic = {}
    for key in sorted_dict.keys():
        key_str = f"{key}"
        new_dic[key_str] = sorted_dict[key]

    print(new_dic)



def get_accurate(folder, question, filename):

    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'jsonl')

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_name = custom_id.split('#')[0]

        registry = custom_id.split('#')[1]

        response = json_obj['response']['body']['choices'][0]['message']['content']

        obj = {}
            
        obj['package_name'] = package_name
        obj['registry'] = registry
        obj['response'] = response

        if response.startswith('Yes'):
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question}/{filename}_accurate')
        
        else:
            WriteData.write_in_path(json.dumps(obj), f'{folder}/{question}/{filename}_inaccurate')



def get_under_license(folder, question, filename):

    pattern = r"my software is under\s*(.+)"

    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    dic = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']
        title = json_obj['title']

        target = title.split(',')[0]

        under_license = re.findall(pattern, target)[0]

        dic[custom_id] = under_license

        print(f'{custom_id}, {under_license}')


    destination2 = f'{folder}/{question}/{question}_extract_final_registry'

    all_lines2 = read_files(destination2, 'json')

    for line in all_lines2:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_information = json_obj['package_information']

        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['under_license'] = dic[custom_id]
        new_obj['package_information'] = package_information

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question}/{filename}_pre_compatibility')


def is_2d_array(arr):
    return all(isinstance(i, list) for i in arr)

def get_under_license_question7(folder, question, filename, filename2):

    pattern = r"my software is under\s*(.+)"

    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    dic = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']
        title = json_obj['title']

        target = title.split(',')[0]

        under_license = re.findall(pattern, target)[0]

        dic[custom_id] = under_license

        print(f'{custom_id}, {under_license}')


    accurate_package = []
    destination2 = f'{folder}/{question}/{filename2}'

    all_lines2 = read_files(destination2, 'json')

    for line2 in all_lines2:
        obj = json.loads(line2.rstrip())

        package_name = obj['package_name']
        accurate_package.append(package_name)
    

    destination3 = f'{folder}/{question}/{question}_extract_final_registry'

    all_lines3 = read_files(destination3, 'json')
    
    for line3 in all_lines3:
        json_obj = json.loads(line3.rstrip())

        custom_id = json_obj['custom_id']

        package_information = json_obj['package_information']

        if len(package_information) <= 0:
            continue
        
        unique_license = []
        for package in package_information:

            if len(package) <= 0:
                continue
            
            if is_2d_array(package):
                package = package[0]

            print(package)
            package_name = package[0]
            license = package[2]

            if package_name in accurate_package:
                if license in unique_license:
                    continue

                unique_license.append(license)
            
                new_obj = {}
                new_obj['custom_id'] = f'{custom_id}_{license}'
                new_obj['under_license'] = dic[custom_id]
                new_obj['package_information'] = package

                WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question}/{filename}_pre_compatibility')


def arrange_inconsistency_license(folder, filename):
    
    destination = f'{folder}/{filename}'

    chatgpt_model = 'gpt-4o'

    # system_message = 'You are a helpful assistant skilled in understanding software licenses.'
    system_message = 'You are a helpful assistant skilled in understanding, explaining, and optimizing software licenses.'

    all_lines = read_files(destination, 'json')

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_name = json_obj['package_name']
        registry = json_obj['registry']
        licenses = json_obj['licenses']

        prompt = f'Please help me arrange the licenses array {licenses}. Do not alter any element. Remove the repeat elements, remove the non-license elements. Please output the arranged license array in JSON format, and only output the JSON format data. '
        
        new_obj = {}

        new_obj['custom_id'] = f'{package_name}#{registry}'
        new_obj['method'] = 'POST'
        new_obj['url'] = '/v1/chat/completions'
        new_obj['body'] = {}
        new_obj['body']['model'] = chatgpt_model
        new_obj['body']['messages'] = []
        new_obj['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj['body']['messages'].append({'role': 'user', 'content': f'{prompt}'})
        new_obj['body']['max_tokens'] = 2000

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_prompts')


def read_inconsistency_licenses_outputs(folder, filename):

    destination = f'{folder}/{filename}'

    all_lines = read_files(destination, 'jsonl')

    new_dict = {}

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        content = json_obj['response']['body']['choices'][0]['message']['content']

        pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
        result = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        if len(result) <= 0:
            continue

        new_array = ast.literal_eval(result[0])

        length = len(new_array)

        # if length == 1 or length == 0:
        #     continue

        if f"{length}" not in new_dict.keys():
            new_dict[f"{length}"] = 1
        else:
            new_dict[f"{length}"] += 1

        new_obj = {}
        new_obj['package_name'] = custom_id.split('#')[0]
        new_obj['registry'] = custom_id.split('#')[1]
        new_obj['licenses'] = new_array

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/question7_extract_final_registry_inconsistency_new')
    
    # sorted_dict = {key: new_dict[key] for key in sorted(new_dict, key=int)}
    # print(sorted_dict)


def read_incompatibility_results(folder, question, filename):

    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, "jsonl")

    incompatibility_count = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        content = json_obj['response']['body']['choices'][0]['message']['content']

        if content.startswith('No'):
            print(content)
            incompatibility_count += 1
    
    print(incompatibility_count)






# folder = r'\batches\gpt-4o-mini\data_total'
# folder = r'\batches\gpt-3.5-turbo\data_total'
# folder = r'\batches\llama-3.1-8b-instruct\data_total'
folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'
question = 'question7'
# inconsistency_analysis_question5(folder, 'question5', f'question5_extract_final_registry')
# inconsistency_analysis_question7(folder, 'question7', f'question7_extract_final_registry')
# count_license(folder, question, 'question5_extract_final_registry_inconsistency')


# get_accurate(folder, question, 'llama_question7_extract_final_registry_consistency_real_licenses_prompts_output')

# get_under_license(folder, question, question)

# get_under_license_question7(folder, question, question, 'question7_extract_final_registry_consistency_real_licenses_prompts_output_accurate')

# arrange_inconsistency_license(f'{folder}/{question}', 'question7_extract_final_registry_inconsistency')

# read_inconsistency_licenses_outputs(f'{folder}/{question}', 'llama_sonar_question7_extract_final_registry_inconsistency_prompts_output')

# read_incompatibility_results(folder, question, 'question5_llama_sonar_inaccuracy_prompts_output_accurate_compatibility_prompts_output')


