import matplotlib.pyplot as plt
import numpy as np


# category_names = ['original question', 'code example', 'single package', 'five packages']
# results = {
#     'Nodejs': [9.60, 9.87, 35.88, 48.91],
#     'Python': [8.36, 8.45, 37.09, 48.65],
#     'Ruby': [24.13, 25.32, 51.15, 63.14],
#     'Perl': [33.09, 36.28, 67.43, 71.24],
#     'PHP': [44.16, 45.07, 60.21, 82.89]
# }

# def survey(results, category_names):
    
#     labels = list(results.keys())
#     data = np.array(list(results.values()))
    
#     # Normalize data to make each row sum to 1
#     normalized_data = data / data.sum(axis=1, keepdims=True)
    
#     data_cum = normalized_data.cumsum(axis=1)
#     category_colors = plt.colormaps['RdYlGn'](
#         np.linspace(0.15, 0.85, normalized_data.shape[1]))
    
#     fig, ax = plt.subplots(figsize=(9.2, 5))
#     ax.invert_yaxis()
#     ax.xaxis.set_visible(False)
#     ax.set_xlim(0, 1)  # Set max to 1 since all rows are normalized

#     for i, (colname, color) in enumerate(zip(category_names, category_colors)):
#         widths = normalized_data[:, i]
#         starts = data_cum[:, i] - widths
#         rects = ax.barh(labels, widths, left=starts, height=0.5,
#                         label=colname, color=color)

#         # Display original data as labels
#         ax.bar_label(rects, labels=[f'{orig:.2f}%' for orig in data[:, i]], label_type='center', color='white')
#     ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
#               loc='lower left', fontsize='small')
    
#     plt.savefig("package-gpt-4o-mini.eps", format="eps",bbox_inches = "tight")
#     return fig, ax


# survey(results, category_names)
# plt.show()


x_labels = ['original question', 'code example', 'single package', 'five packages']
x = range(len(x_labels))  

# --------------gpt-4o-mini-------------------------
# nodejs = [9.60, 9.87, 35.88, 48.91]      
# python = [8.36, 8.45, 37.09, 48.65]      
# ruby = [24.13, 25.32, 51.15, 63.14]       
# perl = [33.09, 36.28, 67.43, 71.24]      
# php = [44.16, 45.07, 60.21, 82.89]       
# --------------gpt-4o-mini-------------------------

# # --------------gpt-3.5-turbo-------------------------
# nodejs = [13.80, 13.38, 35.37, 47.30]      
# python = [14.69, 14.31, 36.56, 46.58]      
# ruby = [24.28, 27.08, 45.03, 61.19]       
# perl = [26.68, 28.03, 49.94, 52.37]      
# php = [38.90, 37.67, 53.64, 69.28]       
# # --------------gpt-3.5-turbo-------------------------

# # --------------llama-3.1-8b-instruct-------------------------
nodejs = [24.58, 27.25, 56.99, 64.23]      
python = [26.59, 30.86, 61.09, 68.83]      
ruby = [38.62, 47.73, 67.88, 77.97]       
perl = [49.63, 54.45, 80.31, 81.87]      
php = [74.45, 79.54, 72.42, 87.27]       
# # --------------llama-3.1-8b-instruct-------------------------

# --------------llama-3.1-sonar-small-128k-chat-------------------------
# nodejs = [28.81, 26.70, 33.70, 59.89]      
# python = [28.80, 28.33, 40.15, 61.16]      
# ruby = [43.72, 41.32, 49.31, 74.67]       
# perl = [49.55, 49.08, 59.58, 77.05]      
# php = [73.00, 72.07, 57.35, 86.08]       
# --------------llama-3.1-sonar-small-128k-chat-------------------------


plt.figure(figsize=(8, 6))

plt.plot(x, nodejs, label='Nodejs', linestyle='-', marker='o')
plt.plot(x, python, label='Python', linestyle='--', marker='s')
plt.plot(x, ruby, label='Ruby', linestyle='-.', marker='^')
plt.plot(x, perl, label='Perl', linestyle=':', marker='d')
plt.plot(x, php, label='PHP', linestyle='-', marker='x')


plt.xticks(ticks=x, labels=x_labels, fontsize=16)  


plt.xlabel('Prompt Sets', fontsize=18)  
plt.ylabel('Hallucination Rates', fontsize=18)            
# plt.title('Five Lines with Custom X-Axis Labels', fontsize=16)  
plt.legend(fontsize=18)  


plt.grid(True)

# plt.savefig("package-gpt-4o-mini.eps", format="eps",bbox_inches = "tight")
# plt.savefig("package-gpt-3.5-turbo.eps", format="eps",bbox_inches = "tight")
plt.savefig("package-llama-3.1-8b-instruct.eps", format="eps",bbox_inches = "tight")
# plt.savefig("package-llama-3.1-sonar-small-128k-chat.eps", format="eps",bbox_inches = "tight")
plt.show()






