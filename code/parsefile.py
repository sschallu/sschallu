import pandas

import json

import WriteData

import os

import re


def read_stackoverflow_tags():

    csv = pandas.read_csv('/stackoverflow_tags.csv')

    for index, row in csv.iterrows():

        id, tag_name, count, excerpt_post_id, wiki_post_id = row["id"], row["tag_name"], row["count"], row["excerpt_post_id"], row["wiki_post_id"]

        json_obj = {}
        json_obj["id"] = id
        json_obj["tag_name"] = tag_name
        json_obj["count"] = count
        # json_obj["excerpt_post_id"] = excerpt_post_id
        # json_obj["wiki_post_id"] = wiki_post_id

        WriteData.write_in_path(json.dumps(json_obj), "/stackoverflow_tags")

        print(f"{tag_name} done...")



# read_stackoverflow_tags()



# First, I need to define some keywords for the tags
# For libraries, javascript, js, css
# For packages, node.js, npm, python, pip, php, packagist, ruby, rubygems, perl, cpan
# For configuration files, node.js: package.json, python: setup.py, requirements.txt, Pipfile, pyproject.toml, conda.yml  php: composer.json, ruby: gemfile, perl: cpanfile, Makefile.PL, Build.PL
# For docker, docker, docker-image
# For dependency, dependen
# For infrastructure as code, infrastructure
# For CI pipeline, pipeline, workflow, github, configuration 

def selected_stackoverflow_tags():

    with open(r'/stackoverflow_tags.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    num = 0
    for line in all_lines:

        obj = json.loads(line.rstrip())
        
        tag_name = obj["tag_name"]
        count = obj["count"]

        if "pyproject" in str(tag_name):
            num += 1
            print(f"{tag_name} {count}")
            # WriteData.write_in_path(json.dumps(obj), "/tags_python")
    
    print(num)


# selected_stackoverflow_tags()


def read_stackoverflow_javascript(tag_name, file):

    print(file)
    csv = pandas.read_csv(f'/{file}.csv')

    count = 0
    for index, row in csv.iterrows():

        id, title, body, accepted_answer_id, answer_count, comment_count, community_owned_date, creation_date, favorite_count, last_activity_date, last_edit_date, last_editor_display_name, last_editor_user_id, owner_user_id, parent_id, post_type_id, score, tags, view_count = row["id"], row["title"], row["body"], row["accepted_answer_id"], row["answer_count"], row["comment_count"], row["community_owned_date"], row["creation_date"], row["favorite_count"], row["last_activity_date"], row["last_edit_date"], row["last_editor_display_name"], row["last_editor_user_id"], row["owner_user_id"], row["parent_id"], row["post_type_id"], row["score"], row["tags"], row["view_count"]


        # if "node.js" in tags or "python" in tags or "php" in tags or "ruby" in tags or "perl" in tags:
        if True:

            json_obj = {}
            json_obj["id"] = id
            json_obj["title"] = title
            json_obj["body"] = body
            json_obj["accepted_answer_id"] = accepted_answer_id
            json_obj["answer_count"] = answer_count
            json_obj["comment_count"] = comment_count
            # json_obj["community_owned_date"] = community_owned_date
            # json_obj["creation_date"] = creation_date
            # json_obj["favorite_count"] = favorite_count
            # json_obj["last_activity_date"] = last_activity_date
            # json_obj["last_edit_date"] = last_edit_date
            # json_obj["last_editor_display_name"] = last_editor_display_name
            # json_obj["last_editor_user_id"] = last_editor_user_id
            # json_obj["accepted_answer_id"] = accepted_answer_id
            # json_obj["owner_user_id"] = owner_user_id
            # json_obj["parent_id"] = parent_id
            # json_obj["post_type_id"] = post_type_id
            json_obj["score"] = score
            json_obj["tags"] = tags
            json_obj["view_count"] = view_count


            WriteData.write_in_path(json.dumps(json_obj), f"/{file}")
            # WriteData.write_in_path(json.dumps(json_obj), f"/checked_tag_files/mysql_1")

            print(f"{id} saved...")

        else:
            print(f"{id} done...")
        

# read_stackoverflow_javascript('licensing', 'licensing')
    



# read_stackoverflow_javascript('stackoverflow_nodejs_without_javascript')
# read_stackoverflow_javascript('stackoverflow_javascript_1')

# files = ['stackoverflow_javascript_1', 'stackoverflow_javascript_2', 'stackoverflow_javascript_3', 'stackoverflow_javascript_4', 'stackoverflow_javascript_5']

# for file in files:
#     read_stackoverflow_javascript(file)


def get_order_tags():

    default_tag = "node.js"

    # files = ['stackoverflow_javascript_11', 'stackoverflow_javascript_2', 'stackoverflow_javascript_3', 'stackoverflow_javascript_4', 'stackoverflow_javascript_5']

    files = ['stackoverflow_nodejs_without_javascript']

    dic_obj = {}

    tags_arr = []

    for file in files:

        with open(f'/{file}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()
        
        for line in all_lines:

            obj = json.loads(line.rstrip())

            tags = obj["tags"]

            tag_array = tags.split('|')

            for tag in tag_array:

                if tag != default_tag and tag not in tags_arr:
                    tags_arr.append(tag)

                if tag != default_tag:
                    key = f"{default_tag}_{tag}"

                    if key in dic_obj.keys():
                        dic_obj[key] += 1
                    else:
                        dic_obj[key] = 1

            print(tags)

    sorted_dic = sorted(dic_obj.items(), key=lambda item:item[1], reverse=True)
    WriteData.write_in_path(json.dumps(dict(sorted_dic)), f"/stackoverflow_nodejs_without_javascript_sort")
    WriteData.write_in_path(json.dumps(tags_arr), f"/stackoverflow_nodejs_without_javascript_sort_tags")


# get_order_tags()


def extract_only_tag_names():

    with open(f'/stackoverflow_tags.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    index = 1
    for line in all_lines:
        obj = json.loads(line.rstrip())

        tag_name = obj["tag_name"]
        id = obj["id"]
        count = obj["count"]

        if count <= 10:
            continue

        if id == 9745 or id == 694:
            continue
        
        total += 1
        WriteData.write_in_path(tag_name, f"/tags_split/stackoverflow_tags_split_{index}")

        if total % 120 == 0:
            total = 0
            index += 1

            print(index)
            

    
# extract_only_tag_names()





def read_file(file_name):
    
    with open(f'/reply/{file_name}.json', encoding='utf-8') as f:
        content = f.read()
        f.close()
    
    obj = json.loads(content)

    question = obj[1]["content"].split(':')[-1].replace('\n', '').replace(' ', '')
    question_words = question.split(',')

    reply = obj[-1]["content"].replace('\n\n', '')

    reply_words = reply.split('\n')

    for item in reply_words:
        item = item.replace(' ', '')
        if item in question_words:
            WriteData.write_in_path(json.dumps(item), f"/stackoverflow_tags_technologies")

    # print(reply)
    



def extract_first_line():

    folder = r"\reply"

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        if os.path.isfile(file_path):
            
            only_file_name = file_name.split('.')[0]
            
            read_file(only_file_name)

            # if only_file_name == "reply_102":

            #     read_file(only_file_name)
            #     break




# category_file_parse('reply_46')
# category_file_parse('reply_1')


# extract_first_line()


def filter_tag_files():

    technologies_not = []

    with open(f'/stackoverflow_tags_technologies_not.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        line = line.rstrip()

        if line not in technologies_not:
            technologies_not.append(line)

    # with open(f'/stackoverflow_tags.json', encoding='utf-8') as f:
    #     all_lines1 = f.readlines()
    #     f.close()

    # for line in all_lines1:
    #     obj = json.loads(line.rstrip())
        
    #     tag_name = obj["tag_name"]

    #     if tag_name not in technologies:
    #         WriteData.write_in_path(tag_name, f"/stackoverflow_tags_technologies_not")

    total = 0
    with open(f'/stackoverflow_javascript_tags/stackoverflow_javascript_5.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()

    for line in all_lines1:
        obj = json.loads(line.rstrip())
        
        tags = obj["tags"]

        tag_array = tags.split('|')

        for tag in tag_array:
            if tag != "javascript" and tag in technologies_not:
                total += 1
                break

    print(total)


# filter_tag_files()


def filter_no_usage_guidance():

    with open(f'/stackoverflow_tags_description.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        obj = json.loads(line.rstrip())

        if "description" not in obj:
            continue

        description = obj["description"]

        if "no usage guidance" in description:
            continue

        WriteData.write_in_path(json.dumps(obj), f'/stackoverflow_tags_description_strip.json')

# filter_no_usage_guidance()


def check_Q_result():

    with open(f'/description/stackoverflow_tags_strip_1_q2.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    count = 0
    for line in all_lines:

        total += 1

        # if total > 8411:
        #     continue

        obj = json.loads(line.rstrip())

        new_obj = {}

        new_obj["id"] = obj["id"]
        new_obj["tag_name"] = obj["tag_name"]
        new_obj["count"] = obj["count"]

        tag_name = obj["tag_name"]

        # file_path = f'/reply/{tag_name}.json'
        # file_path = f'/reply_q2/{tag_name}.json'
        file_path = f'/reply_q3/{tag_name}.json'

        if os.path.isfile(file_path):
            print(tag_name)
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
                f.close()

            json_obj = json.loads(content)

            reply_content = json_obj[-1]["content"].lower()

            new_obj["keywords"] = reply_content
            new_obj["description"] = obj["description"]

            print(reply_content)            
            WriteData.write_in_path(json.dumps(new_obj), f"/description/stackoverflow_tags_strip_1_q3_keywords")

            
            # if reply_content.startswith("yes"):
            #     # print(tag_name)

            #     # if tag_name == "parsing":
            #     #     print(tag_name)

            #     WriteData.write_in_path(json.dumps(obj), f"/description/stackoverflow_tags_strip_1_q3")

            #     count += 1

    


# check_Q_result()


def sort_class_file(tag_name, file_name):

    print(file_name)

    with open(f'/checked_tag_files/{tag_name}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    files_array = []

    for line in all_lines:
        obj = json.loads(line.rstrip())

        # view_count = obj["view_count"]
        # comment_count = obj["comment_count"]
        # answer_count = obj["answer_count"]

        files_array.append(obj)

    sorted_items = sorted(files_array, key=lambda x: (x['view_count'], x['answer_count'], x['comment_count']), reverse=True)

    for item in sorted_items:
        print(item["id"])

        WriteData.write_in_path(json.dumps(item), f"/checked_tag_files/{tag_name}/{file_name}_sort")


# sort_class_file('ruby-on-rails', 'ruby-on-rails')


def get_title(tag_name, file_name):

    print(file_name)

    with open(f'/checked_tag_files/{tag_name}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    languages = ['javascript', 'python', 'java', 'c#', 'php', 'ruby', 'typescript', 'scala', 'perl', 'go', 'rust', 'kotlin', 'node.js']

    need_to_keep = ['java', 'c#', 'typescript', 'scala', 'go', 'rust', 'kotlin']

    keywords = ['string', 'date', 'datetime', 'char', 'boolean', 'int', 'byte', 'decimal', 'float', 'double', 'integer', 'floating-point', 'decimal-point', 'numeric', 'long-integer']

    skip_words = ['error', 'exception', 'failed', 'failure', 'warning', 'denied', 'forbidden', 'not found', 'not working', 'unable', 'visual studio', 'wpf', 'linux', 'java_home', 'eclipse', '.csproj', 'intellij', 'jar', 'can\'t', '.net']

    for line in all_lines:

        obj = json.loads(line.rstrip())

        json_obj = {}

        json_obj["id"] = obj["id"]
        json_obj["title"] = obj["title"]
        json_obj["tags"] = obj["tags"]
        json_obj["view_count"] = obj["view_count"]
        json_obj["answer_count"] = obj["answer_count"]
        json_obj["comment_count"] = obj["comment_count"]

        title = obj["title"].lower()

        skip_flag = False
        for word in skip_words:
            if word in title:
                skip_flag = True
                break

        if skip_flag is True:
            continue

        need_to_keep_flag = False
        for need in need_to_keep:
            if need in title:
                need_to_keep_flag = True
                break

        tags = obj["tags"].split('|')

        if len(tags) <= 2 or 'android' in tags:
            continue

        keywords_flag = False
        for tag in tags:
            if tag in keywords:
                keywords_flag = True
                break

        flag = False
        for tag in tags:
            print(tag)
            if tag in languages:
                flag = True
                break

        tag_flag = False
        for tag in tags:
            if tag == tag_name:
                tag_flag = True
                break
        
        if flag is True and keywords_flag is False and tag_flag is True and need_to_keep_flag is True:
            WriteData.write_in_path(json.dumps(json_obj), f'/checked_tag_files/{tag_name}/{file_name}_tags')

        # print(title)



# read_stackoverflow_javascript('validation', 'validation')
# sort_class_file('validation', 'validation')
# get_title('validation', 'validation_sort')



def parse_top_tags():

    top_folder = r"\checked_tag_files"


    total = 0
    for folder_name in os.listdir(top_folder):
        # print(folder_name)

        file_path = os.path.join(top_folder, folder_name)

        # get_title(folder_name, f'{folder_name}_sort')


        # target_filename = os.path.join(file_path, f'{folder_name}_sort_tags')

        # with open(f'{target_filename}.json', encoding='utf-8') as f:
        #     all_lines = f.readlines()
        #     f.close()

        # total += len(all_lines)
        
        # print(f'{folder_name}: {len(all_lines)}')

        for file_name in os.listdir(file_path):

            if file_name.endswith('metamorphic_new_detail.json'):
                flag = False
                tagfile_name = f'{file_path}\{file_name}'
                print(tagfile_name)
                os.remove(tagfile_name)
                break
        
        # if flag is True:
        #     read_stackoverflow_javascript(folder_name, folder_name)
        #     sort_class_file(folder_name, folder_name)
        #     get_title(folder_name, f'{folder_name}_sort')

    print(total)
            
# parse_top_tags()



def print_lda_data():

    str_data = '0.090*"group" + 0.076*"values" + 0.072*"time" + 0.066*"field" + 0.060*"order" + 0.054*"way" + 0.041*"form" + 0.033*"date" + 0.030*"value" + 0.023*"format"'

    str_data = str_data.replace(' ', '')

    str_array = str_data.split('+')


    str_array.reverse()


    for item in str_array:
        
        item = item.replace('"', '')
        
        item_array = item.split('*')

        print(f"{item_array[1]}     {item_array[0]}")
        

# print_lda_data()


def get_top_count_tags():

    with open(f'/description/stackoverflow_tags_strip_1_q3_keywords_check.json', encoding='utf-8') as f:
        content = f.read()
        f.close()

    tag_array = json.loads(content)

    total = 0
    for item in tag_array:
        tag_name = item["tag_name"]
        count = item["count"]
        if count > 10000:
            print(tag_name)
            total += 1
    
    print(total)

# get_top_count_tags()


def extract_first_50_questions():

    folder = r"\checked_tag_files"

    id_collection = []

    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        questions = os.path.join(file_path, f'{folder_name}_sort_tags_normal')
        
        with open(f'{questions}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        take_number = 150
        question_number = len(all_lines)

        if question_number < 150:
            take_number = question_number
        
        for i in range(0, take_number):
            obj = json.loads(all_lines[i].rstrip())

            id = obj['id']

            if id in id_collection:
                continue
            else:
                id_collection.append(id)

            title = obj['title'].lower()
            print(title)

            if title.startswith('can') or title.startswith('cannot') or title.startswith('can not') or title.startswith('is') or title.startswith('does'):
                continue

            if title.startswith('which') or title.startswith('why') or title.startswith('what'):
                continue
            
            WriteData.write_in_path(all_lines[i].rstrip(), '/data_again/top_20000')

# extract_first_50_questions()


def extract_first_50_questions_metamorphic():

    folder = r"\checked_tag_files"

    id_collection = []

    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        questions = os.path.join(file_path, f'{folder_name}_sort_tags_transformation_detail')

        if not os.path.exists(f'{questions}.json'):
            continue
        
        with open(f'{questions}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        take_number = 150
        question_number = len(all_lines)

        if question_number < 150:
            take_number = question_number
        
        for i in range(0, take_number):
            obj = json.loads(all_lines[i].rstrip())

            id = obj['id']

            if id in id_collection:
                continue
            else:
                id_collection.append(id)

            title = obj['title'].lower()
            print(title)

            if title.startswith('can') or title.startswith('cannot') or title.startswith('can not') or title.startswith('is') or title.startswith('does'):
                continue

            if title.startswith('which') or title.startswith('why') or title.startswith('what'):
                continue
            
            WriteData.write_in_path(all_lines[i].rstrip(), '/data_again/top_20000')


# extract_first_50_questions_metamorphic()

