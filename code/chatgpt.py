import openai

import WriteData

import json

import os

import time

openai.api_key = ''



# messages = [{
#     "role": "system",
#     "content": "Your are a intelligent assistant."
# }]

def request_chatgpt(tag_name, message):

    messages = [{
        "role": "system",
        "content": "Your are a intelligent assistant."
    }]


    if message:
        messages.append(
            {"role": "user", "content": message}
        )

        chat = openai.chat.completions.create(
            # model = "gpt-3.5-turbo",
            model = "gpt-4-turbo",
            # model = "gpt-4o",
            messages = messages
        )
    
    print("waiting...")

    reply = chat.choices[0].message.content

    print(f"ChatGPT: {reply}")

    messages.append({"role": "assistant", "content": reply})

    WriteData.write_in_path(json.dumps(messages), f"/reply_language/{tag_name}")
    


def get_text(filename):

    file_path = f'/tags_split/{filename}.json'
    # print(f"{filename}: {os.path.exists(file_path)}")
    print(filename)

    with open(file_path, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    # question = "please give me a detailed specific list categorization of the words I provided, each word belongs to only one category, keep all the words lowercase"
    # question = "please provide a detailed format-specific list that categorizes the words I've provided, with each word belonging to only one category and all words remaining lowercase"
    # question = "please give me only a word list in plain text, each word takes up one line and belongs to software development and build technologies"

    question = "Which of the following words is a programming language, not a framework, put the answer in one line"

    word_list = ""

    for line in all_lines:
        word_list += f",{line.rstrip()}"
    
    message = f"{question}: {word_list[1:]}"

    print(message)

    request_chatgpt(filename, message)



def categorize_all_stackoverflow_tags():

    folder = r"\tags_split"

    for file_name in os.listdir(folder):

        file_path = os.path.join(folder, file_name)

        if os.path.isfile(file_path):
            only_file_name = file_name.split('.')[0]

            if only_file_name == "stackoverflow_tags_split_1":
                continue

            get_text(only_file_name)

            time.sleep(10)

            

def get_description(filename):

    file_path = f'/description/{filename}.json'
    
    print(filename)

    with open(file_path, encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    # question = "does this statement describe a technology (rather than a language) used in modern node.js, python, php, ruby, perl software application development and building"
    # question = "give me an answer of yes or no, does this statement describe a technology used in modern application development and building"    #q1
    # question = "give me an answer of yes or no, can this technology be used in node.js, python, php, ruby, perl applications development and building"  #q2
    # question = "give me an answer of yes or no, does this statement describe a technology that is not a fundamental language construct"   #q3
    question = "give me five keywords of this statement in one line"

    total = 0
    for line in all_lines:

        total += 1

        print(total)

        # if total < 1602:
        #     continue

        obj = json.loads(line.rstrip())

        tag_name = obj["tag_name"]

        print(f"{total}: {tag_name}")

        description = obj["description"]
    
        message = f'{question}: \n"{tag_name}, {description}"'
        
        time.sleep(0.2)

        request_chatgpt(tag_name, message)



# get_description('stackoverflow_tags_description_strip_1')
# get_description('stackoverflow_tags_description_strip_1_1')
# get_description('stackoverflow_tags_description_strip_2')
# get_description('stackoverflow_tags_description_strip_3')

# get_description('stackoverflow_tags_strip_1_q2_1')
# get_description('stackoverflow_tags_strip_1_q2_2')



# get_description('stackoverflow_tags_strip_1_q1_1')
# get_description('stackoverflow_tags_strip_1_q1_2')



# categorize_all_stackoverflow_tags()

# get_text('stackoverflow_tags_split_1')


# get_text('stackoverflow_tags_split_1')


for i in range(1, 11):

    folder = r"\tags_split"

    file_name = f"stackoverflow_tags_split_{i}"

    get_text(file_name)

    time.sleep(10)


