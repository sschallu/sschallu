
import json

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def cdf_license_count():


    # gpt_4o_mini = "{"2": 1362, "3": 414, "4": 168, "5": 102, "6": 64, "7": 35, "8": 34, "9": 20, "10": 16, "11": 15, "12": 9, "13": 5, "14": 5, "15": 3, "16": 3, "17": 2, "19": 1, "21": 3, "22": 1, "24": 1, "25": 1, "28": 1, "29": 2, "30": 1, "33": 1}"
    # gpt_35_turbo = "{"2": 1266, "3": 395, "4": 153, "5": 76, "6": 46, "7": 27, "8": 16, "9": 11, "10": 13, "11": 5, "12": 5, "13": 4, "14": 2, "15": 1, "16": 1, "18": 2, "24": 1}"
    # llama_31_8b = "{"2": 1627, "3": 340, "4": 138, "5": 61, "6": 36, "7": 22, "8": 7, "9": 6, "10": 6, "11": 2, "12": 3, "13": 1, "15": 1, "16": 1, "18": 1, "20": 1, "21": 1}"
    # llama_sonar = "{"2": 972, "3": 352, "4": 152, "5": 85, "6": 67, "7": 41, "8": 34, "9": 33, "10": 22, "11": 13, "12": 8, "13": 3, "14": 7, "15": 3, "16": 4, "17": 2, "18": 2, "19": 1, "21": 1, "22": 1, "23": 1}"

    gpt_4o_mini = '{"2": 3724, "3": 1124, "4": 528, "5": 279, "6": 177, "7": 115, "8": 84, "9": 62, "10": 48, "11": 40, "12": 29, "13": 23, "14": 28, "15": 18, "16": 17, "17": 17, "18": 15, "19": 13, "20": 4, "21": 10, "22": 6, "23": 4, "24": 1, "26": 5, "27": 1, "28": 2, "29": 3, "30": 4, "31": 3, "32": 1, "33": 1, "34": 1, "35": 1, "38": 1, "40": 1, "42": 1, "43": 1, "50": 1}'
    gpt_35_turbo = '{"2": 4629, "3": 1335, "4": 582, "5": 284, "6": 163, "7": 82, "8": 54, "9": 37, "10": 20, "11": 14, "12": 10, "13": 12, "14": 9, "15": 6, "16": 8, "17": 4, "18": 2, "19": 2, "20": 5, "22": 4, "24": 1, "28": 2, "30": 2, "35": 1}'
    llama_31_8b = '{"2": 9832, "3": 3058, "4": 915, "5": 415, "6": 157, "7": 85, "8": 30, "9": 24, "10": 17, "11": 13, "12": 9, "13": 2, "14": 3, "15": 5, "16": 3, "17": 2}'
    llama_sonar = '{"2": 5629, "3": 1545, "4": 510, "5": 267, "6": 107, "7": 88, "8": 50, "9": 29, "10": 24, "11": 13, "12": 13, "13": 11, "14": 6, "15": 8, "16": 3, "17": 6, "18": 1, "19": 2, "21": 1, "23": 1, "24": 1, "25": 2, "26": 2, "28": 1, "31": 2, "39": 1, "46": 1, "48": 1, "51": 1}'


    gpt_4o_mini_obj = json.loads(gpt_4o_mini)
    gpt_4o_mini_y = []

    gpt_35_turbo_obj = json.loads(gpt_35_turbo.strip())
    gpt_35_turbo_y = []

    llama_31_8b_obj = json.loads(llama_31_8b.strip())
    llama_31_8b_y = []

    llama_sonar_obj = json.loads(llama_sonar.strip())
    llama_sonar_y = []

    x_label = []
    list = range(1, 55)
    for i in list:
        index = str(i)
        x_label.append(index)
        if index in gpt_4o_mini_obj.keys():
            gpt_4o_mini_y.append(gpt_4o_mini_obj[index])
        else:
            gpt_4o_mini_y.append(0)

        if index in gpt_35_turbo_obj.keys():
            gpt_35_turbo_y.append(gpt_35_turbo_obj[index])
        else:
            gpt_35_turbo_y.append(0)
        
        if index in llama_31_8b_obj.keys():
            llama_31_8b_y.append(llama_31_8b_obj[index])
        else:
            llama_31_8b_y.append(0)
        
        if index in llama_sonar_obj.keys():
            llama_sonar_y.append(llama_sonar_obj[index])
        else:
            llama_sonar_y.append(0)
        
        
    # ------------- cdf start -----------------
    cdf_gpt_4o_mini = np.cumsum(gpt_4o_mini_y) / np.sum(gpt_4o_mini_y)
    cdf_gpt_35_turbo = np.cumsum(gpt_35_turbo_y) / np.sum(gpt_35_turbo_y)
    cdf_llama_31_8b = np.cumsum(llama_31_8b_y) / np.sum(llama_31_8b_y)
    cdf_sonar_y = np.cumsum(llama_sonar_y) / np.sum(llama_sonar_y)


    plt.plot(list, cdf_gpt_4o_mini, label="GPT-4o-mini",color="dodgerblue")
    plt.plot(list, cdf_gpt_35_turbo, label="GPT-3.5-turbo",color="lawngreen")
    plt.plot(list, cdf_llama_31_8b, label="Llama-3.1-8b-instruct",color="grey")
    plt.plot(list, cdf_sonar_y, label="Llama-3.1-sonar-small-128k-chat",color="darkorange")
    plt.xlabel("Same Package Multiple Licenses", fontsize=16)
    plt.ylabel("CDF", fontsize=16)
#    plt.title("CDF for USCs upgrade times")
    plt.grid(True)
    plt.xlim([1, 55])
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # plt.yscale("log")
    plt.legend(prop ={"size": 16},loc="lower right")
    plt.savefig("license-count-cdf.eps", format="eps",bbox_inches = "tight")
    plt.show()
    # ------------- cdf end -----------------

    


cdf_license_count()



