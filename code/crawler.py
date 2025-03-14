import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import json
import secrets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import WriteData

import re
import requests

from bs4 import BeautifulSoup



url = 'https://stackoverflow.com/questions/tagged/'


def init(tag_array):

    options = uc.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.set_capability("detach", True)

    options.add_argument("--window-size=1920,1050")

    chrome_path = r'D:\Code\LLM\code\chromedriver.exe'

    driver = uc.Chrome(options=options, driver_executable_path=chrome_path)

    total = 0
    for tag in tag_array:

        total += 1

        # if total < 21778:
        #     continue

        tag_name = tag["tag_name"]

        time.sleep(0.5)

        try:

            driver.get(f"{url}{tag_name}")

            time.sleep(0.5)

            print(f"{total}: {tag_name}")

            mainbar = driver.find_element(by=By.ID, value='mainbar')

            p = mainbar.find_element(by=By.TAG_NAME, value='p')

            text = p.text
            tag["description"] = text
        
        except:
            print(f"{total}: {tag_name}, fail...")

        WriteData.write_in_path(json.dumps(tag), "/stackoverflow_tags_2_description")


    driver.quit()


def get_tags():

    tag_array = []

    with open(r'/stackoverflow_tags_2.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        obj = json.loads(line.rstrip())

        tag_name = obj["tag_name"]

        count = obj["count"]

        if count >= 50:
            tag_array.append(obj)
    
    return tag_array




# tag_array = get_tags()

# init(tag_array)




def init_request_dic(file_name):

    # folder = "/data_again/packages_request_status.json"
    folder = f"/data_again/{file_name}.json"

    with open(folder, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        link = obj['link']
        license = obj['license']

        dic[link] = license
    
    return dic


def init_request_dic_nodejs(file_name):

    folder = f"/data_again/{file_name}.json"

    with open(folder, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        link = obj['link']
        license = obj['license']
        deprecated = obj['deprecated']

        dic[link] = [license, deprecated]
    
    return dic


def write_request_package_nodejs(file_name, request_url, license, deprecated):
    request_obj = {}

    request_obj['link'] = request_url
    request_obj['license'] = license
    request_obj['deprecated'] = deprecated
    WriteData.write_in_path(json.dumps(request_obj), f'/data_again/{file_name}')


def request_packages(request_url):

    try:

        response = requests.get(request_url)

        response_obj = json.loads(response.text)

        license = response_obj['license']

        time.sleep(0.3)

    except:

        license = "exception"
    
    return license


def write_request_package(file_name, request_url, license):
    request_obj = {}

    request_obj['link'] = request_url
    request_obj['license'] = license
    WriteData.write_in_path(json.dumps(request_obj), f'/data_again/{file_name}')



def registry_crawler_nodejs(folder, file_name):

    dic = init_request_dic_nodejs('package_nodejs_infor')

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']
        status_code = json_obj['status_code']

        total += 1

        if status_code != 200:
            continue

        package_link = package_link.replace('#', '').replace("'", "")

        if package_link not in dic.keys():

            # try:

            response = requests.get(package_link)

            response_obj = json.loads(response.text)
            # print(package_link)

            # print(response_obj)

            if 'license' in response_obj:
                license = response_obj['license']

            else:
                license = 'unknown'

            deprecated = False

            if 'dist-tags' in response_obj and 'latest' in response_obj['dist-tags']:

                last_tags = response_obj['dist-tags']['latest']

                version = response_obj['versions'][last_tags]

                if 'deprecated' in version:
                    deprecated = True
                
                if license == 'unknown':
                    if 'license' in version:
                        license = version['license']
                    
                    if 'licenses' in version and isinstance(version['licenses'], list):

                        if len(version['licenses']) <= 0:
                            continue
                        
                        if isinstance(version['licenses'][0], dict) and 'type' in version['licenses'][0]:
                            license = version['licenses'][0]['type']
                        else:
                            license = version['licenses'][0]
                    
                    if 'liceses' in version:
                        license = version['licenses']
                
            
            if 'time' in response_obj and 'unpublished' in response_obj['time']:
                deprecated = "unpublished"

            # except:
            #     license = "exception"
            #     deprecated = False
            
            time.sleep(0.3)

            json_obj['license'] = license
            json_obj['deprecated'] = deprecated
            
            dic[package_link] = [license, deprecated]

            write_request_package_nodejs('package_nodejs_infor', package_link, license, deprecated)

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

            print(f'{total}: {package_link}: {license}, {deprecated}')

        else:
            print(f'{total}_already: {package_link}')

            json_obj['license'] = dic[package_link][0]
            json_obj['deprecated'] = dic[package_link][1]

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')


    


def registry_crawler_perl(folder, file_name):

    dic = init_request_dic_nodejs('package_perl_info')

    total = 0

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']

        status_code = json_obj['status_code']

        total += 1

        if status_code != 200:
            continue

        if package_link not in dic.keys():

            package_link = package_link.replace('#', '')
            print(package_link)

            response = requests.get(package_link)

            if response.status_code == 404:
                continue

            response_obj = json.loads(response.text)

            if 'distribution' not in response_obj:
                continue

            distribution = response_obj['distribution']

            json_obj['distribution'] = distribution

            time.sleep(0.3)


            new_request_url = f'https://fastapi.metacpan.org/v1/release/{distribution}'

            print(new_request_url)

            new_response = requests.get(new_request_url)

            if new_response.status_code == 404:
                continue

            new_response_obj = json.loads(new_response.text)

            deprecated = new_response_obj['deprecated']

            if 'license' in new_response_obj:
                license = new_response_obj["license"]

                if isinstance(new_response_obj["license"], list):
                    license = ','.join(new_response_obj["license"])
            else:
                license = 'unknown'

            json_obj['license'] = license

            json_obj['deprecated'] = deprecated

            dic[package_link] = [license, deprecated]

            write_request_package_nodejs('package_perl_info', package_link, license, deprecated)

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

            print(f'{total}: {package_link}: {license}, {deprecated}')

            time.sleep(0.3)

        else:

            print(f'{total}_already: {package_link}, {dic[package_link][1]}')

            json_obj['license'] = dic[package_link][0]
            json_obj['deprecated'] = dic[package_link][1]

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')



def registry_crawler_python(folder, file_name):

    dic = init_request_dic('package_python_infor')

    total = 0

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']

        status_code = json_obj['status_code']

        total += 1

        if status_code != 200:
            continue

        if package_link not in dic.keys():

            package_link = package_link.replace('#', '')
            print(package_link)

            response = requests.get(package_link)

            response_obj = json.loads(response.text)

            if 'info' not in response_obj:
                continue

            license = response_obj["info"]["license"]

            if license and ',' in license:
                license = license.split(',')[0]

            json_obj['license'] = license
            write_request_package('package_python_infor', package_link, license)

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

            dic[package_link] = license

            print(f'{total}: {package_link}: {license}')

            time.sleep(0.5)

        else:
            print(f'{total}_already: {package_link}')

            json_obj['license'] = dic[package_link]

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')



def registry_crawler_ruby(folder, file_name):

    dic = init_request_dic('package_ruby_infor')

    total = 0

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']

        status_code = json_obj['status_code']

        total += 1

        if status_code != 200:
            continue

        if package_link not in dic.keys():

            package_link = package_link.replace('#', '')
            print(package_link)

            response = requests.get(package_link)

            if response.status_code == 404:
                continue

            response_obj = json.loads(response.text)

            if 'licenses' in response_obj:
                license = response_obj["licenses"]

                if isinstance(response_obj["licenses"], list):
                    license = ','.join(response_obj["licenses"])
            else:
                license = 'unknown'

            json_obj['license'] = license

            write_request_package('package_ruby_infor', package_link, license)

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

            dic[package_link] = license

            print(f'{total}: {package_link}: {license}')

            time.sleep(0.5)

        else:

            print(f'{total}_already: {package_link}')

            json_obj['license'] = dic[package_link]

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')



def registry_crawler_php(folder, file_name):

    
    dic = init_request_dic_nodejs('package_php_info')

    total = 0

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        package_link = json_obj['package_link']

        status_code = json_obj['status_code']

        total += 1

        if status_code != 200:
            continue

        if package_link not in dic.keys():

            package_link = package_link.replace('#', '')

            if package_link.endswith('/.json'):
                continue

            print(package_link)

            response = requests.get(package_link)

            if response.status_code == 404:
                continue

            response_obj = json.loads(response.text)

            if 'dev-master' in response_obj['package']['versions']:
                license = response_obj['package']["versions"]['dev-master']['license']

                if isinstance(response_obj['package']["versions"]['dev-master']['license'], list):
                    license = ','.join(response_obj['package']["versions"]['dev-master']['license'])

            else:
                key = next(iter(response_obj['package']["versions"]))
                print(key)
                license = response_obj['package']["versions"][key]['license']

                if isinstance(response_obj['package']["versions"][key]['license'], list):
                    license = ','.join(response_obj['package']["versions"][key]['license'])

            
            if 'abandoned' in response_obj['package']:
                deprecated = response_obj['package']['abandoned']
            else:
                deprecated = False

            json_obj['license'] = license
            json_obj['deprecated'] = deprecated

            write_request_package_nodejs('package_php_info', package_link, license, deprecated)

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

            dic[package_link] = license

            print(f'{total}: {package_link}: {license}, {deprecated}')

            time.sleep(0.3)

        else:
            print(f'{total}_already: {package_link}, {dic[package_link][1]}')

            json_obj['license'] = dic[package_link][0]
            json_obj['deprecated'] = dic[package_link][1]

            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')




        
        
# folder = r'/data_again/gpt-4o-mini'

# folder = '/data_again/batches/gpt-4o-mini'

# folder = '/data_again/batches/gpt-3.5-turbo'

# folder = '/data_again/batches/llama-3.1-8b-instruct/batches_prompts_14'

# folder = r'\batches\gpt-4o-mini\data_total'
# folder = r'\batches\gpt-3.5-turbo\data_total'
folder = r'\batches\llama-3.1-8b-instruct\data_total'
# folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'

# registry_crawler_nodejs(folder, 'question4', 'question4_extract_final_registry_request_nodejs')

# registry_crawler_perl(folder, 'question6', 'question6_extract_final_registry_request_perl')

# registry_crawler_python(folder, 'question6', 'question6_extract_final_registry_request_python')

# registry_crawler_ruby(folder, 'question6', 'question6_extract_final_registry_request_ruby')

# registry_crawler_php(folder, 'question6', 'question6_extract_final_registry_request_php')


def registry_crawler_nodejs_total():

    # folder_template = 'batches_prompts_'

    question_num = 'question'

    for index in range(6, 8):

        file_name = f'{question_num}{index}'

        target_folder = f'{folder}/{file_name}'

        print(f'{target_folder}/{question_num}')

        registry_crawler_nodejs(target_folder, question_num, f'{question_num}_extract_final_registry_request_nodejs')

        # registry_crawler_python(target_folder, question_num, f'{question_num}_extract_final_registry_request_python')

        # registry_crawler_perl(target_folder, question_num, f'{question_num}_extract_final_registry_request_perl')

        # registry_crawler_ruby(target_folder, question_num, f'{question_num}_extract_final_registry_request_ruby')

        # registry_crawler_php(target_folder, question_num, f'{question_num}_extract_final_registry_request_php')



# registry_crawler_nodejs_total()
# registry_crawler_nodejs(f'{folder}/question1', 'package_total_nodejs')
# registry_crawler_nodejs(f'{folder}/question2', 'package_total_nodejs')
# registry_crawler_nodejs(f'{folder}/question4', 'package_total_nodejs')
# registry_crawler_nodejs(f'{folder}/question5', 'package_total_nodejs')

# registry_crawler_nodejs(f'{folder}/question6', 'package_total_nodejs_new')
# registry_crawler_nodejs(f'{folder}/question7', 'package_total_nodejs_new')

# registry_crawler_python(f'{folder}/question5', 'package_total_python_new')
# registry_crawler_python(f'{folder}/question7', 'package_total_python_new')

# registry_crawler_ruby(f'{folder}/question5', 'package_total_ruby_new')
# registry_crawler_ruby(f'{folder}/question7', 'package_total_ruby_new')

# registry_crawler_perl(f'{folder}/question1', 'package_total_perl_new')
# registry_crawler_perl(f'{folder}/question2', 'package_total_perl_new')
# registry_crawler_perl(f'{folder}/question4', 'package_total_perl_new')
# registry_crawler_perl(f'{folder}/question5', 'package_total_perl_new')
# registry_crawler_perl(f'{folder}/question6', 'package_total_perl_new')
# registry_crawler_perl(f'{folder}/question7', 'package_total_perl_new')

# registry_crawler_php(f'{folder}/question1', 'package_total_php_new')
# registry_crawler_php(f'{folder}/question2', 'package_total_php_new')
# registry_crawler_php(f'{folder}/question4', 'package_total_php_new')
# registry_crawler_php(f'{folder}/question5', 'package_total_php_new')
# registry_crawler_php(f'{folder}/question6', 'package_total_php_new')
# registry_crawler_php(f'{folder}/question7', 'package_total_php_new')


# folder_list = [r'\batches\llama-3.1-8b-instruct\data_total', r'\batches\llama-3.1-sonar-small-128k-chat\data_total']

# for folder in folder_list:
#     print(folder)
#     registry_crawler_perl(f'{folder}/question1', 'package_total_perl_new')
#     registry_crawler_perl(f'{folder}/question2', 'package_total_perl_new')
#     registry_crawler_perl(f'{folder}/question4', 'package_total_perl_new')
#     registry_crawler_perl(f'{folder}/question5', 'package_total_perl_new')
#     registry_crawler_perl(f'{folder}/question6', 'package_total_perl_new')
#     registry_crawler_perl(f'{folder}/question7', 'package_total_perl_new')


# folder_list = [r'\batches\gpt-3.5-turbo\data_total', r'\batches\gpt-4o-mini\data_total', r'\batches\llama-3.1-8b-instruct\data_total', r'\batches\llama-3.1-sonar-small-128k-chat\data_total']

# for folder in folder_list:
#     print(folder)
#     registry_crawler_php(f'{folder}/question1', 'package_total_php_new')
#     registry_crawler_php(f'{folder}/question2', 'package_total_php_new')
#     registry_crawler_php(f'{folder}/question4', 'package_total_php_new')
#     registry_crawler_php(f'{folder}/question5', 'package_total_php_new')
#     registry_crawler_php(f'{folder}/question6', 'package_total_php_new')
#     registry_crawler_php(f'{folder}/question7', 'package_total_php_new')




def init_request_godaddy(file_name):

    folder = f"/data_again/{file_name}.json"

    with open(folder, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        domain = obj["domain"]
        available = obj["available"]

        dic[domain] = available
    
    return dic



def write_request_godaddy(file_name, domain, available):
    request_obj = {}

    request_obj['domain'] = domain
    request_obj['available'] = available
    WriteData.write_in_path(json.dumps(request_obj), f'/data_again/{file_name}')


def init_request_deprecated(file_name):

    folder = f"/data_again/{file_name}.json"

    with open(folder, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        package_link = obj["package_link"]
        deprecated = obj["deprecated"]

        dic[package_link] = deprecated
    
    return dic


def write_request_deprecated(file_name, package_link, deprecated):
    request_obj = {}

    request_obj['package_link'] = package_link
    request_obj['deprecated'] = deprecated
    WriteData.write_in_path(json.dumps(request_obj), f'/data_again/{file_name}')


def godaddy_check_domain(folder, file_name):

    options = uc.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--lang=en')
    options.set_capability("detach", True)

    options.add_argument("--window-size=1920,1050")

    chrome_path = r'D:\Code\LLM\code\chromedriver.exe'

    driver = uc.Chrome(options=options, driver_executable_path=chrome_path)

    dic = init_request_godaddy('domain_request_godaddy_status')

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0

    count = 0

    driver.get(f"https://www.godaddy.com/domainsearch/find?domainToCheck=slproweb.com")

    time.sleep(5)

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        domain = json_obj["domain"]

        status = json_obj["status"]

        total += 1

        # if total % 200 == 0 and total != 0:
        #     print('sleeping...')
        #     time.sleep(30 * 60)

        # if count % 30 == 0 and count != 0:
        #     print('sleep...')
        #     time.sleep(30 * 60)


        if status == 200 or status == 403 or status == 404:
            continue

        domain = domain.replace("www.", "")

        if len(domain.split(".")) <= 2:
            
            flag = False

            if domain not in dic.keys():

                count += 1

                # url = f'https://www.godaddy.com/domainsearch/find?domainToCheck={domain}'

                try:

                    input_ele = driver.find_element(by=By.ID, value='domain-search-box')

                    # input_ele.clear()

                    input_ele.send_keys(Keys.CONTROL + "a")
                    input_ele.send_keys(Keys.DELETE)

                    time.sleep(2)

                    input_ele.click()
                    
                    time.sleep(2)

                    input_ele.send_keys(domain)

                    time.sleep(2)

                    input_ele.send_keys(Keys.ENTER)

                    time.sleep(5)

                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    items = soup.select('span[data-cy="availableCard-tag"]')

                    for item in items:
                        if "EXACT MATCH" in item.text.strip():
                            flag = True

                    pre_items = soup.select('span[data-cy="ExactMatchPremium-tag"]')
                    
                    if len(pre_items) > 0:
                        flag = True
                    
                    json_obj["available"] = flag

                    dic[domain] = flag

                    print(f'{total}: {domain}, {flag}')

                    write_request_godaddy('domain_request_godaddy_status', domain, flag)

                    WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

                except:
                    json_obj["available"] = "exception"
                    
                    print(f'{total}: {domain}, exception')
                    
                    WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')

            else:
                json_obj["available"] = dic[domain]

                print(f'{total}_already: {domain}, {dic[domain]}')

                WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_request')





# folder = r"\batches\gpt-4o-mini\data_total\question1"
# folder = r"\batches\gpt-3.5-turbo\data_total\question4"
# folder = r"\batches\llama-3.1-8b-instruct\data_total\question1"
folder = r"\batches\llama-3.1-sonar-small-128k-chat\data_total\question4"
# godaddy_check_domain(folder, "link_total_unique_domain")


