import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import os

import json

import WriteData

import random


# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

def modify(input_str):

    input_str = input_str.lower()

    tokens = word_tokenize(input_str)

    tagged = pos_tag(tokens)

    # verbs = [word for word, pos in tagged if pos.startswith('VB')]

    auxiliary_verbs = [i for i, w in enumerate(tagged) if w[1].startswith('VB')]
    
    # print(auxiliary_verbs)
    if auxiliary_verbs:
        tagged.insert(0, tagged.pop(auxiliary_verbs[0]))
    # else:
    #     tagged.insert(0, ('to', 'VBD'))

    tagged.insert(0, ('how to', 'WRB'))

    return ' '.join([t[0] for t in tagged]) + '?'



def is_question(sentence):
    # Tokenize the sentence
    words = nltk.word_tokenize(sentence)
    
    # Perform POS tagging
    pos_tags = nltk.pos_tag(words)
    
    # Simple heuristic: check if the sentence starts with a Wh-word or an auxiliary verb
    wh_words = {'WDT', 'WP', 'WP$', 'WRB'}  # POS tags for Wh-words
    aux_verbs = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD'}  # POS tags for auxiliary/modal verbs
    
    # print(pos_tags)
    if pos_tags:
        first_word, first_tag = pos_tags[0]
        if first_tag in wh_words or first_tag in aux_verbs:
            return True
    
    # Another heuristic: check if the sentence ends with a question mark
    if sentence.strip().endswith('?'):
        return True
    
    return False


# result = is_question(question_three)
# print(result)

# steps
# check if a title is a question
# if not, change the title to a how-question
# check if a title contains a keyword from the array need_to_keep, then replace the detected keyword with node.js, python, php, perl, ruby

# then get the question dataset


def split_statement_and_question():

    folder = r"\checked_tag_files"

    need_to_keep = ['java', 'c#', 'typescript', 'scala', 'go', 'rust', 'kotlin']

    language_list = ['node.js', 'python', 'php', 'ruby', 'perl', 'nodejs', 'javascript', 'typescript']

    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        target_filename = os.path.join(file_path, f'{folder_name}_sort_tags')
        
        with open(f'{target_filename}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        for line in all_lines:

            obj = json.loads(line.rstrip())

            title = obj['title'].lower()

            result = is_question(title)

            # print(f'{result}: {title}')

            tags = obj['tags'].split('|')
            
            target_tag_flag = False
            tag_name = ''
            for tag in tags:
                if tag in language_list:
                    target_tag_flag = True
                    tag_name = tag
                    break
            
            need_to_keep_flag = False
            need_tag_name = ''
            for tag in tags:
                if tag in need_to_keep:
                    need_to_keep_flag = True
                    need_tag_name = tag
                    break
            
            
            if result is False:
                obj['title'] = modify(title).replace('c #', 'c#')
            
            new_title = obj['title'].lower()
            # print(new_title)

            new_title_array = new_title.split(' ')

            need_title_flag = False

            language_title_flag = False

            for item in new_title_array:
                item = item.replace('?', '').replace(':', '').replace(',', '')

                if item in language_list:
                    language_title_flag = True
                    break
            

            for item in new_title_array:
                item = item.replace('?', '').replace(':', '').replace(',', '')
                print(item)

                # print(item == 'java')

                if item == 'c#' or item == 'C#':
                    need_title_flag = True
                    break

                if item == 'java':
                    need_title_flag = True
                    break

                if item == 'scala':
                    need_title_flag = True
                    break

                if item == 'go' or item == 'golang':
                    need_title_flag = True
                    break

                if item == 'rust':
                    need_title_flag = True
                    break

                if item == 'kotlin':
                    need_title_flag = True
                    break
                
            if target_tag_flag is True and language_title_flag is False:
                obj['title'] = obj['title'].replace('?', f' in {tag_name}?')
                WriteData.write_in_path(json.dumps(obj), f'{target_filename}_questions_new')
            
            elif target_tag_flag is True and language_title_flag is True:
                WriteData.write_in_path(json.dumps(obj), f'{target_filename}_questions_new')
            
            elif need_to_keep_flag is True and need_title_flag is False:
                obj['title'] = obj['title'].replace('?', f' in {need_tag_name}?')
                WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic_new')

            else:
                WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic_new')    

            
            # if need_title_flag is True:
            #     WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic')
            # else:
            #     WriteData.write_in_path(json.dumps(obj), f'{target_filename}_questions')
                
            

# split_statement_and_question()



# question = "Java Component based vs Request based frameworks"

# question = modify(question).replace('c #', 'c#')
# print(question)

# print(is_question('Designing a fluent Javascript interface to abstract away the asynchronous nature of AJAX'))


def play_metamorphic():

    folder = r"\checked_tag_files"

    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        target_filename = os.path.join(file_path, f'{folder_name}_sort_tags_metamorphic_new')

        if not os.path.exists(f'{target_filename}.json'):
            continue
        
        with open(f'{target_filename}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        for line in all_lines:
            obj = json.loads(line.rstrip())

            title = obj["title"].lower()
            print(title)

            # title_array = title.split(' ')

            # for item in title_array:


            if 'c#' in title or 'C#' in title:
                # WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic')
                detail_metamorphic(obj, f'{target_filename}', 'c#')
            
            elif 'java' in title and 'javascript' not in title:
                # WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic')
                detail_metamorphic(obj, f'{target_filename}', 'java')
            
            elif 'scala' in title:
                # WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic')
                detail_metamorphic(obj, f'{target_filename}', 'scala')
            
            if 'go' in title or 'golang' in title:
                print(f'{folder_name}_sort_tags_questions')
                # WriteData.write_in_path(json.dumps(obj), os.path.join(file_path, f'{folder_name}_sort_tags_metamorphic'))
                detail_metamorphic(obj, f'{target_filename}', 'go')
            
            elif 'rust' in title:
                # WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic')
                detail_metamorphic(obj, f'{target_filename}', 'rust')
            
            elif 'kotlin' in title:
                # WriteData.write_in_path(json.dumps(obj), f'{target_filename}_metamorphic')
                detail_metamorphic(obj, f'{target_filename}', 'kotlin')




def delete_file():
    folder = r"\checked_tag_files"

    total = 0
    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        target_filename = os.path.join(file_path, f'{folder_name}_sort_tags_transformation_detail')

        target_filename_normal = os.path.join(file_path, f'{folder_name}_sort_tags_normal')

        if not os.path.exists(f'{target_filename}.json'):
            continue
        
        if not os.path.exists(f'{target_filename_normal}.json'):
            continue

        os.remove(f'{target_filename}.json') 
        os.remove(f'{target_filename_normal}.json')

# delete_file()


def detail_metamorphic(obj, path, keyword):

    new_obj = {}
    new_obj["id"] = f'{obj["id"]}_nodejs'
    new_obj["title"] = obj["title"].lower().replace('golang', 'node.js').replace(keyword, 'node.js').replace('C#', 'node.js')
    new_obj["tags"] = obj["tags"]
    new_obj["view_count"] = obj["view_count"]
    new_obj["answer_count"] = obj["answer_count"]
    new_obj["comment_count"] = obj["comment_count"]

    WriteData.write_in_path(json.dumps(new_obj), f'{path}_transformation_detail')

    new_obj1 = {}
    new_obj1["id"] = f'{obj["id"]}_python'
    new_obj1["title"] = obj["title"].lower().replace('golang', 'python').replace(keyword, 'python').replace('C#', 'python')
    new_obj1["tags"] = obj["tags"]
    new_obj1["view_count"] = obj["view_count"]
    new_obj1["answer_count"] = obj["answer_count"]
    new_obj1["comment_count"] = obj["comment_count"]

    WriteData.write_in_path(json.dumps(new_obj1), f'{path}_transformation_detail')

    new_obj2 = {}
    new_obj2["id"] = f'{obj["id"]}_php'
    new_obj2["title"] = obj["title"].lower().replace('golang', 'php').replace(keyword, 'php').replace('C#', 'php')
    new_obj2["tags"] = obj["tags"]
    new_obj2["view_count"] = obj["view_count"]
    new_obj2["answer_count"] = obj["answer_count"]
    new_obj2["comment_count"] = obj["comment_count"]

    WriteData.write_in_path(json.dumps(new_obj2), f'{path}_transformation_detail')

    new_obj3 = {}
    new_obj3["id"] = f'{obj["id"]}_perl'
    new_obj3["title"] = obj["title"].lower().replace('golang', 'perl').replace(keyword, 'perl').replace('C#', 'perl')
    new_obj3["tags"] = obj["tags"]
    new_obj3["view_count"] = obj["view_count"]
    new_obj3["answer_count"] = obj["answer_count"]
    new_obj3["comment_count"] = obj["comment_count"]

    WriteData.write_in_path(json.dumps(new_obj3), f'{path}_transformation_detail')

    new_obj4 = {}
    new_obj4["id"] = f'{obj["id"]}_ruby'
    new_obj4["title"] = obj["title"].lower().replace('golang', 'ruby').replace(keyword, 'ruby').replace('C#', 'ruby')
    new_obj4["tags"] = obj["tags"]
    new_obj4["view_count"] = obj["view_count"]
    new_obj4["answer_count"] = obj["answer_count"]
    new_obj4["comment_count"] = obj["comment_count"]

    WriteData.write_in_path(json.dumps(new_obj4), f'{path}_transformation_detail')


# play_metamorphic()


def play_transformation():

    folder = r"\checked_tag_files"

    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        target_filename = os.path.join(file_path, f'{folder_name}_sort_tags')

        if not os.path.exists(f'{target_filename}.json'):
            continue
        
        with open(f'{target_filename}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        for line in all_lines:

            flag = False

            obj = json.loads(line.rstrip())

            title = obj["title"].lower()
            
            title_array = title.split(' ')


            tags = obj['tags']

            tags_array = tags.split('|')
            for tag in tags_array:
                if tag == 'go' and ('golang' in title or 'go' in title):
                    flag = True
                    detail_metamorphic(obj, f'{target_filename}', 'go')

                if 'java' in title and 'javascript' not in title:
                    flag = True
                    detail_metamorphic(obj, f'{target_filename}', 'java')

            if 'c#' in title:
                flag = True
                detail_metamorphic(obj, f'{target_filename}', 'c#')
            
            if 'scala' in title:
                flag = True
                detail_metamorphic(obj, f'{target_filename}', 'scala')
            
            if 'rust' in title:
                flag = True
                detail_metamorphic(obj, f'{target_filename}', 'rust')
            
            if 'kotlin' in title:
                flag = True
                detail_metamorphic(obj, f'{target_filename}', 'kotlin')

            if flag is False:
                WriteData.write_in_path(json.dumps(obj), f'{target_filename}_normal')

# play_transformation()


def count():

    total = 0

    folder = r"\checked_tag_files"

    for folder_name in os.listdir(folder):
        
        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue

        file_path = os.path.join(folder, folder_name)

        metamorphic = os.path.join(file_path, f'{folder_name}_sort_tags_metamorphic')

        questions = os.path.join(file_path, f'{folder_name}_sort_tags_questions')
        
        with open(f'{metamorphic}.json', encoding='utf-8') as f:
            all_lines = f.readlines()
            f.close()

        with open(f'{questions}.json', encoding='utf-8') as f:
            all_lines1 = f.readlines()
            f.close()

        total += len(all_lines)
        total += len(all_lines1)
        print(f'{folder_name}_metamorphic: {len(all_lines)}')
        print(f'{folder_name}_questions: {len(all_lines1)}')
    
    print(total)

# count()


def random_license():

    licenses_array = ['Public Domain', 'MIT/X11', 'BSD-new', 'Apache 2.0', 'LGPLv2.1', 'LGPLv2.1+', 'LGPLv3', 'LGPLv3+', 'MPL 1.1', 'GPLv2', 'GPLv2+', 'GPLv3', 'GPLv3+', 'Affero GPLv3', 'Proprietary']
    random_value = random.choice(licenses_array)

    return random_value


def transformation_new_questions():

    custom_id_array = []
    chatgpt_model = 'gpt-4o-mini'
    write_path = '/data_again/top_50000'

    system_message = 'You are a helpful assistant skilled in generating, explaining, and optimizing code across multiple programming languages.'

    with open(f'/data_again/top_10000.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        obj = json.loads(line.rstrip())

        id = obj['id']
        title = obj['title'].lower()
        
        if id not in custom_id_array:
            custom_id_array.append(id)
        else:
            continue

        print(f'{id}: {title}')


        new_obj1 = {}
        new_obj1['custom_id'] = f'{id}_1'
        new_obj1['method'] = 'POST'
        new_obj1['url'] = '/v1/chat/completions'
        new_obj1['body'] = {}
        new_obj1['body']['model'] = chatgpt_model
        new_obj1['body']['messages'] = []
        new_obj1['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj1['body']['messages'].append({'role': 'user', 'content': f'{title}'})
        new_obj1['body']['max_tokens'] = 1000
        
        WriteData.write_in_path(json.dumps(new_obj1), write_path)

        license_value = random_license()

        prompt_2 = f'please give me a code example to solve or realize the following problem or task, {title}'

        new_obj2 = {}
        new_obj2['custom_id'] = f'{id}_2'
        new_obj2['method'] = 'POST'
        new_obj2['url'] = '/v1/chat/completions'
        new_obj2['body'] = {}
        new_obj2['body']['model'] = chatgpt_model
        new_obj2['body']['messages'] = []
        new_obj2['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj2['body']['messages'].append({'role': 'user', 'content': f'{prompt_2}'})
        new_obj2['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj2), write_path)


        prompt_3 = f'my software is under {license_value}, to maintain license compatibility with my software, please give me a code example to solve or realize the following problem or task, {title}'

        new_obj3 = {}
        new_obj3['custom_id'] = f'{id}_3'
        new_obj3['method'] = 'POST'
        new_obj3['url'] = '/v1/chat/completions'
        new_obj3['body'] = {}
        new_obj3['body']['model'] = chatgpt_model
        new_obj3['body']['messages'] = []
        new_obj3['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj3['body']['messages'].append({'role': 'user', 'content': f'{prompt_3}'})
        new_obj3['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj3), write_path)


        # new_title1 = f'please give me a package and its license, {title}'
        prompt_4 = f"please first give me a package, the package's registry, and its license in the fixed format (package-name, package-registry: package-license), and then show me how to use this package to solve or realize the following problem or task, {title}"

        new_obj4 = {}
        new_obj4['custom_id'] = f'{id}_4'
        new_obj4['method'] = 'POST'
        new_obj4['url'] = '/v1/chat/completions'
        new_obj4['body'] = {}
        new_obj4['body']['model'] = chatgpt_model
        new_obj4['body']['messages'] = []
        new_obj4['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj4['body']['messages'].append({'role': 'user', 'content': f'{prompt_4}'})
        new_obj4['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj4), write_path)

        prompt_5 = f"my software is under {license_value}, to maintain license compatibility with my software, please first give me a package, the package's registry, and its license in the fixed format (package-name, package-registry: package-license), and then show me how to use this package to solve or realize the following problem or task, {title}"

        new_obj5 = {}
        new_obj5['custom_id'] = f'{id}_5'
        new_obj5['method'] = 'POST'
        new_obj5['url'] = '/v1/chat/completions'
        new_obj5['body'] = {}
        new_obj5['body']['model'] = chatgpt_model
        new_obj5['body']['messages'] = []
        new_obj5['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj5['body']['messages'].append({'role': 'user', 'content': f'{prompt_5}'})
        new_obj5['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj5), write_path)



        # new_title = f'please give me five more packages and their licenses, {title}'
        prompt_6 = f"please further give me five more packages, the packages' registries, and their licenses in the fixed format (package-name, package-registry: package-license) to solve or realize the following problem or task (this time please don't show me the code detail), {title}"
        
        new_obj6 = {}

        new_obj6['custom_id'] = f'{id}_6'
        new_obj6['method'] = 'POST'
        new_obj6['url'] = '/v1/chat/completions'
        new_obj6['body'] = {}
        new_obj6['body']['model'] = chatgpt_model
        new_obj6['body']['messages'] = []
        new_obj6['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj6['body']['messages'].append({'role': 'user', 'content': f'{prompt_6}'})
        new_obj6['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj6), write_path)


        prompt_7 = f"my software is under {license_value}, to maintain license compatibility with my software, please only give me five more packages, the packages' registries, and their licenses in the fixed format (package-name, package-registry: package-license) to solve or realize the following problem or task (this time please don't show me the code detail), {title}"

        new_obj7 = {}
        new_obj7['custom_id'] = f'{id}_7'
        new_obj7['method'] = 'POST'
        new_obj7['url'] = '/v1/chat/completions'
        new_obj7['body'] = {}
        new_obj7['body']['model'] = chatgpt_model
        new_obj7['body']['messages'] = []
        new_obj7['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj7['body']['messages'].append({'role': 'user', 'content': f'{prompt_7}'})
        new_obj7['body']['max_tokens'] = 1000

        WriteData.write_in_path(json.dumps(new_obj7), write_path)

        
# transformation_new_questions()





