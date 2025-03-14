import WriteData

import json

def read_files(folder, question_num, file_name):
    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def get_packages(folder, question_num, file_name):
    all_lines = read_files(folder, question_num, file_name)

    package_array = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        status_code = json_obj['status_code']

        package_link = json_obj['package_link']

        # package_name = package_link.replace("https://pypi.org/pypi/", "").replace("/json", "")
        # package_name = package_link.replace("https://registry.npmjs.org/", "")
        # package_name = package_link.replace('https://rubygems.org/api/v1/gems/', '').replace('.json', '')
        # package_name = package_link.replace("https://fastapi.metacpan.org/v1/module/", "")
        # package_name = package_link.replace("https://packagist.org/packages/", "").replace(".json", "")

        # if package_name == '':
        #     continue

        # new_obj = {}
        # new_obj['package_name'] = package_name
        # new_obj['registry'] = 'gem install'
        # new_obj['status_code'] = status_code
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/package_notfound')

        
def get_github_links(folder, question_num, file_name):
    all_lines = read_files(folder, question_num, file_name)

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link']
        status_code = json_obj['status_code']
        if status_code == 404:
            new_obj = {}
            new_obj['package_name'] = link
            new_obj['registry'] = 'github'
            WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/package_notfound')


def get_package_notfound_title(folder, question_num, file_name):
    all_lines = read_files(folder, question_num, file_name)

    github_array = []
    package_array = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        registry = json_obj['registry']
        package_name = json_obj['package_name']

        if registry == 'github':
            github_array.append(package_name)
        else:
            package_array.append(package_name)

    all_lines1 = read_files(folder, question_num, 'question1_parse')
    for line in all_lines1:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']
        title = json_obj['title']
        link_list = json_obj['link_list']

        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['title'] = title
        new_obj['packages'] = []
        new_obj['links'] = []

        extract_packages = json_obj['extract_packages']

        for package in extract_packages:
            if len(package) < 2:
                continue
            if package[1] in package_array:
                new_obj['packages'].append(package)
        
        for link in link_list:
            if link in github_array:
                new_obj['links'].append(link)
        
        if len(new_obj['packages']) > 0 or len(new_obj['links']) > 0:
            WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/package_notfound_title')


def get_hallucinated_packages(folder, question, filename):
    all_lines = read_files(folder, question, filename)

    total = 0
    hallucinated_packages = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1
        

        status_code = json_obj['status_code']

        if status_code == 404:
            hallucinated_packages += 1
    
    print(f'total: {total}')
    print(f'hallucinated_packages: {hallucinated_packages}')
    print(f'hallucination rate: {hallucinated_packages / total}')


def license_analysis(folder, question, filename):
    all_lines = read_files(folder, question, filename)

    total = 0
    inconsistency = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        licenses = json_obj["licenses"]

        if len(licenses) <= 0:
            continue

        total += 1

        if len(licenses) > 1:
            inconsistency += 1
        
    print(f"total: {total}")
    print(f"inconsistency: {inconsistency}")


def get_package_title(folder, question, filename):

    all_lines = read_files(folder, question, filename)

    all_lines1 = read_files(folder, question, 'package_notfound')

    package_dict = {}
    for line1 in all_lines1:
        obj = json.loads(line1.rstrip())
        package_link = obj['package_link']
        status_code = obj['status_code']

        if package_link not in package_dict.keys():
            package_dict[package_link] = status_code

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        extract_packages = json_obj['extract_packages']
        custom_id = json_obj['custom_id']
        title = json_obj['title']

        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['title'] = title
        new_obj['packages'] = []

        for package in extract_packages:
            registry = package[0]

            package_array = package[1:]
            for package_name in package_array:
                if registry == 'npm install':
                    package_link = f'https://registry.npmjs.org/{package_name}'
                
                elif registry == 'pip install':
                    package_link = f'https://pypi.org/pypi/{package_name}/json'
                
                elif registry == 'gem install':
                    package_link = f'https://rubygems.org/api/v1/gems/{package_name}.json'
                
                elif registry == 'composer require':
                    package_link = f'https://packagist.org/packages/{package_name}.json'

                else:
                    package_link = f'https://fastapi.metacpan.org/v1/module/{package_name}'
                
                if package_link in package_dict.keys():
                    new_obj['packages'].append([registry, package_name, package_dict[package_link]])
        
        if len(new_obj['packages']) > 0:
            WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{question_num}/package_notfound_title')
                        
            
def get_overlap_packages():

    question = 'question4'

    all_lines_4o = read_files('/gpt-4o-mini', question, 'package_notfound')

    all_lines_35 = read_files('/gpt-3.5-turbo', question, 'package_notfound')

    all_lines_llama_instruct = read_files('/llama-3.1-instruct', question, 'package_notfound')

    all_lines_llama_sonar = read_files('/llama-128k-sonar', question, 'package_notfound')

    notfound_4o = []
    notfound_35 = []
    notfound_llama_instruct = []
    notfound_llama_sonar = []

    for line in all_lines_4o:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj["package_link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        if "fastapi.metacpan.org" not in package_link:
            notfound_4o.append(package_link.lower())
        else:
            notfound_4o.append(package_link)
    
    for line in all_lines_35:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj["package_link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        if "fastapi.metacpan.org" not in package_link:
            notfound_35.append(package_link.lower())
        else:
            notfound_35.append(package_link)

    for line in all_lines_llama_instruct:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj["package_link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        if "fastapi.metacpan.org" not in package_link:
            notfound_llama_instruct.append(package_link.lower())
        else:
            notfound_llama_instruct.append(package_link)
    
    for line in all_lines_llama_sonar:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj["package_link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        if "fastapi.metacpan.org" not in package_link:
            notfound_llama_sonar.append(package_link.lower())
        else:
            notfound_llama_sonar.append(package_link)
    

    print(f'notfound_4o: {len(notfound_4o)}')
    print(f'notfound_35: {len(notfound_35)}')
    print(f'notfound_llama_instruct: {len(notfound_llama_instruct)}')
    print(f'notfound_llama_sonar: {len(notfound_llama_sonar)}')

    # overlap = list(set(notfound_4o) & set(notfound_35) & set(notfound_llama_instruct) & set(notfound_llama_sonar))

    # union = list(set(notfound_4o) | set(notfound_35) | set(notfound_llama_instruct) | set(notfound_llama_sonar))

    gpt_overlap = list(set(notfound_4o) & set(notfound_35))
    llama_overlap = list(set(notfound_llama_instruct) & set(notfound_llama_sonar))

    gpt_union = list(set(notfound_4o) | set(notfound_35))
    llama_union = list(set(notfound_llama_instruct) | set(notfound_llama_sonar))

    results = len(gpt_overlap) / len(gpt_union)
    results2 = len(llama_overlap) / len(llama_union)
    print(f'gpt: {results}')
    print(f'llama: {results2}')



def get_overlap_github():

    question = 'question4'

    all_lines_4o = read_files('/gpt-4o-mini', question, 'link_total_github')

    all_lines_35 = read_files('/gpt-3.5-turbo', question, 'link_total_github')

    all_lines_llama_instruct = read_files('/llama-3.1-instruct', question, 'link_total_github')

    all_lines_llama_sonar = read_files('/llama-128k-sonar', question, 'link_total_github')

    notfound_4o = []
    notfound_35 = []
    notfound_llama_instruct = []
    notfound_llama_sonar = []

    for line in all_lines_4o:
        json_obj = json.loads(line.rstrip())

        link = json_obj["link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        url = "/".join(link.split("/")[:4]).lower()
        if url not in notfound_4o:
            notfound_4o.append(url)


    for line in all_lines_35:
        json_obj = json.loads(line.rstrip())

        link = json_obj["link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        url = "/".join(link.split("/")[:4]).lower()
        if url not in notfound_35:
            notfound_35.append(url)

    for line in all_lines_llama_instruct:
        json_obj = json.loads(line.rstrip())

        link = json_obj["link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        url = "/".join(link.split("/")[:4]).lower()
        if url not in notfound_llama_instruct:
            notfound_llama_instruct.append(url)
    
    for line in all_lines_llama_sonar:
        json_obj = json.loads(line.rstrip())

        link = json_obj["link"]
        status_code = json_obj["status_code"]

        if status_code == 200:
            continue

        url = "/".join(link.split("/")[:4]).lower()
        if url not in notfound_llama_sonar:
            notfound_llama_sonar.append(url)
    

    print(f'notfound_4o: {len(notfound_4o)}')
    print(f'notfound_35: {len(notfound_35)}')
    print(f'notfound_llama_instruct: {len(notfound_llama_instruct)}')
    print(f'notfound_llama_sonar: {len(notfound_llama_sonar)}')

    overlap = list(set(notfound_4o) & set(notfound_35) & set(notfound_llama_instruct) & set(notfound_llama_sonar))

    union = list(set(notfound_4o) | set(notfound_35) | set(notfound_llama_instruct) | set(notfound_llama_sonar))

    results = len(overlap) / len(union)
    print(results)


def get_overlap_domain():

    question = 'question4'

    all_lines_4o = read_files('/gpt-4o-mini', question, 'link_total_unique_domain_request')

    all_lines_35 = read_files('/gpt-3.5-turbo', question, 'link_total_unique_domain_request')

    all_lines_llama_instruct = read_files('/llama-3.1-instruct', question, 'link_total_unique_domain_request')

    all_lines_llama_sonar = read_files('/llama-128k-sonar', question, 'link_total_unique_domain_request')

    notfound_4o = []
    notfound_35 = []
    notfound_llama_instruct = []
    notfound_llama_sonar = []

    for line in all_lines_4o:
        json_obj = json.loads(line.rstrip())

        domain = json_obj["domain"]
        notfound_4o.append(domain)
        

    for line in all_lines_35:
        json_obj = json.loads(line.rstrip())

        domain = json_obj["domain"]
        notfound_35.append(domain)


    for line in all_lines_llama_instruct:
        json_obj = json.loads(line.rstrip())

        domain = json_obj["domain"]
        notfound_llama_instruct.append(domain)
    

    for line in all_lines_llama_sonar:
        json_obj = json.loads(line.rstrip())

        domain = json_obj["domain"]
        notfound_llama_sonar.append(domain)
    

    print(f'notfound_4o: {len(notfound_4o)}')
    print(f'notfound_35: {len(notfound_35)}')
    print(f'notfound_llama_instruct: {len(notfound_llama_instruct)}')
    print(f'notfound_llama_sonar: {len(notfound_llama_sonar)}')

    overlap = list(set(notfound_4o) & set(notfound_35) & set(notfound_llama_instruct) & set(notfound_llama_sonar))

    union = list(set(notfound_4o) | set(notfound_35) | set(notfound_llama_instruct) | set(notfound_llama_sonar))

    results = len(overlap) / len(union)
    print(results)


def get_similarity_data(folder, question, filename):

    all_lines = read_files(folder, question, filename)

    score_array = []

    package_array = []

    total = 0
    target = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        new_packages = json_obj["new_packages"]

        best_score = json_obj["best_score"]

        for index in range(0, len(new_packages)):
            packages = new_packages[index]

            if packages[1] in package_array:
                continue

            package_array.append(packages[1])

            status = packages[2]

            # if status == 200 or "::" in packages[1]:
            #     continue
            # if packages[0] == "gem install" or packages[0] == "npm install" or packages[0] == "pip install":
            #     # continue

            #     if best_score[index] > 0.6:
            #         target += 1
                
            #     total += 1

            #     score_array.append(best_score[index])

            # if best_score[index] > 0.6:
            #     target += 1

            if best_score[index] == 1.0:
                target += 1
                
            total += 1

            score_array.append(best_score[index])
    
    print(score_array)
    print(total)
    print(target)
    print(target / total)

            

def change_title_name(folder, question_num, file_name):

    all_lines = read_files(folder, question_num, file_name)

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']
        print(custom_id)

        if custom_id.endswith('_7'):
            custom_id = custom_id.replace('_7', '_6')
            json_obj['custom_id'] = custom_id

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_new')
        




folder = '/gpt-3.5-turbo'
# folder = '/llama-3.1-instruct'
# folder = '/llama-128k-sonar'
question_num = 'question6'
# file_name = 'package_total_nodejs'
# file_name = 'package_total_python_new'
# file_name = 'package_total_php_new'
# file_name = 'package_total_perl_new'
# file_name = 'package_total_ruby_new'
# file_name = 'question7_extract_final_registry_inconsistency_new'
# file_name = 'question7_extract_final_registry_consistency'

# get_packages(folder, question_num, file_name)
# get_github_links(folder, question_num, file_name)
# get_package_notfound_title(folder, question_num, 'package_notfound')

# get_hallucinated_packages(folder, question_num, file_name)

# license_analysis(folder, question_num, file_name)

# get_package_title(folder, question_num, 'question1_parse')

# get_overlap_packages()

# get_overlap_github()

# get_overlap_domain()

# get_similarity_data(folder, question_num, 'package_notfound_similarity')

change_title_name(folder, question_num, question_num)