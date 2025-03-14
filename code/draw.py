import matplotlib.pyplot as plt

# Sample data
# categories = ['function', 'method', 'multiprocessing', 'async', 'typeerror:', 'callback', 'possible', 'functions', 'within', 'performance']
# values = [0.121, 0.066, 0.044, 0.027, 0.026, 0.025, 0.025, 0.021, 0.020, 0.020]

# # Create a horizontal bar chart
# # plt.barh(categories, values, color=['red', 'green', 'blue', 'purple', 'orange'])
# plt.barh(categories, values)

# # Add labels and title
# plt.xlabel('Values')
# plt.ylabel('Categories')
# plt.title('Horizontal Bar Chart Example')

# # Add grid lines
# # plt.grid(True)

# # Annotate bars
# for index, value in enumerate(values):
#     plt.text(value, index, str(value))

# # Show the plot
# plt.show()



def draw_bar(categories, values):
    # Create a horizontal bar chart
    plt.barh(categories, values)

    # Add labels and title
    plt.xlabel('Values')
    plt.ylabel('Categories')
    plt.title('Horizontal Bar Chart Example')

    # Add grid lines
    # plt.grid(True)

    # Annotate bars
    for index, value in enumerate(values):
        plt.text(value, index, str(value))

    # Show the plot
    plt.show()




def extract_label_data(data_str):

    data_array = data_str.replace(' ', '').replace('"', '').split('+')

    categories = []
    values = []

    for data in data_array:
        items = data.split('*')

        categories.append(items[1])
        values.append(items[0])
        
    draw_bar(categories, values)


# data_str = '0.047*"route" + 0.043*"bootstrap" + 0.042*"string" + 0.042*"rails" + 0.038*"run" + 0.029*"inside" + 0.026*"list" + 0.025*"ruby" + 0.024*"nil" + 0.023*"convert"'

data_str = '0.091*"data" + 0.074*"space" + 0.048*"convert" + 0.046*"way" + 0.041*"3" + 0.038*"regex" + 0.030*"string" + 0.030*"particular" + 0.025*"count" + 0.022*"searching"'

extract_label_data(data_str)