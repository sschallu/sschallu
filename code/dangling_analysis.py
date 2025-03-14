import WriteData

import json

import os


def get_useful_items(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total_package = 0
    total_link = 0

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        # package_request = json_obj['package_request']

        link_list = json_obj['link_list']

        # if len(package_request) > 0:
        #     total_package += 1
            # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_package')
        
        if len(link_list) > 0:
            total_link += 1
            # WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_link')
    
    print(f"package: {total_package}")
    print(f"link: {total_link}")


def extract_404(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_request = json_obj['package_request']

        link_list = json_obj['link_list']

        new_package_request = []
        new_link_request = []

        if len(package_request) > 0:

            for package_array in package_request:
                status_code = package_array[1]

                if status_code != 200:
                    print(f'{custom_id}: {package_array[0]}')
                    new_package_request.append(package_array)
        

        if len(link_list) > 0:
            for link_array in link_list:

                status_code = link_array[1]

                if status_code != 200:
                    print(f'{custom_id}: {link_array[0]}')
                    new_link_request.append(link_array)
        
        if len(new_package_request) > 0 or len(new_link_request) > 0:
            json_obj['package_request'] = new_package_request
            json_obj['link_list'] = new_link_request

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_404')


def extract_404_overview(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    request_array = []

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_request = json_obj['package_request']

        link_list = json_obj['link_list']

        if len(package_request) > 0:

            for package_array in package_request:
                status_code = package_array[1]

                # if package_array[0] not in request_array:
                #     request_array.append(package_array[0])
                #     total += 1

                if status_code == 404 or status_code == 'exception':
                    if package_array[0] not in request_array:
                        request_array.append(package_array[0])
                        url_obj = {}
                        url_obj['url'] = package_array[0]
                        url_obj['status_code'] = status_code
                        WriteData.write_in_path(json.dumps(url_obj), f'{folder}/{file_name}_404_overview')
        

        if len(link_list) > 0:
            for link_array in link_list:

                status_code = link_array[1]

                if status_code == 404 or status_code == 'exception':
                    if link_array[0] not in request_array:
                        request_array.append(link_array[0])
                        url_obj = {}
                        url_obj['url'] = link_array[0]
                        url_obj['status_code'] = status_code
                        WriteData.write_in_path(json.dumps(url_obj), f'{folder}/{file_name}_404_overview_url')
    
    print(total)


# folder = r'\defense\question2'
# folder = r'\batches\llama-3.1-8b-instruct\batches_prompts_14\question4'
# folder = r'\gpt-4o-mini\question2'
folder = r'\defense\top_20000_question2_q3\question2'
# folder = r'\defense\real_useful\question2_do_not_recommend\question2'
# file_name = 'question3_parse_request'
# file_name = 'question7_extract_final_registry_request'
# file_name = 'question2_parse_request'
file_name = 'question2_parse_request'

# extract_404_overview(folder, file_name)

# folder = r'\batches\gpt-4o-mini'


# extract_404(folder, f'{file_name}_useful')

# get_useful_items(folder, file_name)


def parse_question_total(folder):

    folder_template = 'batches_prompts_'
    for index in range(0, 14):
        
        file_name = f'{folder_template}{index}'

        print(f'{folder}\{file_name}')

        for sub_index in range(1, 8):
            
            sub_template = f'question{sub_index}'
            print(sub_template)

            if sub_index == 1 or sub_index == 2 or sub_index == 3:
                target_file = f'{sub_template}_parse_request'

            else:
                target_file = f'{sub_template}_extract_final_registry_request'    

            get_useful_items(f'{folder}\{file_name}\{sub_template}', target_file)

            extract_404(f'{folder}\{file_name}\{sub_template}', f'{target_file}_useful')


# parse_question_total(folder)


def category_packages(folder, file_name):

    # dic_array = ['cpanm ', 'cpan ', 'pip install', 'composer require', 'gem install', 'npm install']

    # dic_registry = {
    #     'cpanm': 'https://metacpan.org/pod/',
    #     'cpan': 'https://metacpan.org/pod/',
    #     'pip install': 'https://pypi.org/project/',
    #     'composer require': 'https://packagist.org/packages/',
    #     'gem install': 'https://rubygems.org/gems/',
    #     'npm install': 'https://registry.npmjs.org/'
    # }

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()


    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_request = json_obj['package_request']

        if len(package_request) <= 0:
            continue

        for package_array in package_request:
            registry = package_array[0]
            status_code = package_array[1]

            if status_code != 200:
                continue

            obj = {}
            if registry.startswith('https://metacpan.org/pod/'):
                # print('perl')
                package_name = registry.split('https://metacpan.org/pod/')[1]
                obj['registry'] = 'perl'
                obj['package_name'] = package_name
                obj['package_link'] = registry

                WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_perl')

            
            elif registry.startswith('https://pypi.org/project/'):
                # print('python')
                package_name = registry.split('https://pypi.org/project/')[1]
                obj['registry'] = 'python'
                obj['package_name'] = package_name
                obj['package_link'] = registry

                WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_python')

            
            elif registry.startswith('https://packagist.org/packages/'):
                # print('php')
                package_name = registry.split('https://packagist.org/packages/')[1]
                obj['registry'] = 'php'
                obj['package_name'] = package_name
                obj['package_link'] = registry
                
                WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_php')
                
            
            elif registry.startswith('https://rubygems.org/gems/'):
                # print('rugy')
                package_name = registry.split('https://rubygems.org/gems/')[1]
                obj['registry'] = 'ruby'
                obj['package_name'] = package_name
                obj['package_link'] = registry

                WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_ruby')

            
            elif registry.startswith('https://registry.npmjs.org/'):
                # print('nodejs')
                package_name = registry.split('https://registry.npmjs.org/')[1]
                obj['registry'] = 'nodejs'
                obj['package_name'] = package_name
                obj['package_link'] = registry

                WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_nodejs')
            
            else:
                print('danger')


# folder = 'D:/Code/LLM/exported_files/data_again/batches/gpt-3.5-turbo/'

def category_packages_total():

    question_num = 'question7'

    folder_template = 'batches_prompts_'
    for index in range(0, 15):

        file_name = f'{folder_template}{index}'

        print(f'{folder}{file_name}/{question_num}')

        target_folder = f'{folder}{file_name}/{question_num}'
        
        category_packages(target_folder, f'{question_num}_extract_final_registry_request')

        # extract_404_overview(target_folder, f'{question_num}_parse_request')

        # extract_404_overview(target_folder, f'{question_num}_extract_final_registry_request')


# category_packages_total()

# category_packages(folder, 'question4_extract_final_registry_request')        
        
    


# two things    1. php packages 2. lowercase or 





