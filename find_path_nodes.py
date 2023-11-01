# %%
# Example node data for find_path_nodes.py
#     1,          -2.,           0.,        0.147
#     2,          -1.,          -1.,        0.147
#     3,           0.,           0.,        0.147
#     4,          -1.,           1.,        0.147
#     5,          -3.,           1.,        0.147
#     6,          -2.,           2.,        0.147
#     7,          -3.,          -1.,        0.147
#     8,          -2.,          -2.,        0.147

# commit - edit_find_path_nodes_2023_10_31_01

# import modules
import numpy as np

# Read in the node data from the file
# Node Data File name: Study_iter02_aligned1_1.12microsecond_nodal_coordinates.txt

# Open textfile
f = open('data_test.txt', 'r')

# Read textfile
data = f.readlines()

# Close textfile
f.close()

# create function to extract nodes and node co-ordinates from a line
#    1,           0.,           0.,        0.
def extract_node(line):
    node = line.split(',')[0]
    x = line.split(',')[1]
    y = line.split(',')[2]
    z = line.split(',')[3]
    return node, x, y, z

# Process each line of the data and extract the node number and node co-ordinates
# Create empty dictionary
node_dict = {}
# Loop through data
for line in data:
    line = line.strip()
    node, x, y, z = extract_node(line)
    node_dict[node] = [x, y, z]
        
# Find minimum and maximum x, y and z co-ordinates
x_min = 0
x_max = 0
y_min = 0
y_max = 0
z_min = 0
z_max = 0
for node in node_dict:
    x = float(node_dict[node][0])
    y = float(node_dict[node][1])
    z = float(node_dict[node][2])
    if x < x_min:
        x_min = x
    if x > x_max:
        x_max = x
    if y < y_min:
        y_min = y
    if y > y_max:
        y_max = y
    if z < z_min:
        z_min = z
    if z > z_max:
        z_max = z
        
# Calculate plate dimensions
# Plate dimensions are the dimensions of the plate which contains the nodes
# Plate_Length is the length of the plate in the x direction
# Plate_Width is the width of the plate in the y direction
# Plate_Height is the height of the plate in the z direction
Plate_Length = x_max - x_min
Plate_Width = y_max - y_min
Plate_Height = z_max - z_min        
        

# Find unique z co-ordinates
z_list = []
for node in node_dict:
    z = float(node_dict[node][2])
    if z not in z_list:
        z_list.append(z)
z_list.sort()
# Find unique number of z co-ordinates in z direction
num_unique_z_coord = len(z_list)

# Sort node_dict by z co-ordinate
# Example 9 unique nodes
#     1,           0.,           0.,        0.
#     2,           0.,           0.,        0.0735
#     3,           0.,           0.,        0.147
#     4,           1.,           0.,        0.
#     5,           1.,           0.,        0.0735
#     6,           1.,           0.,        0.147
#     7,           1.,           1.,        0.
#     8,           1.,           1.,        0.0735
#     9,           1.,           1.,        0.147
# Create empty Node_dict_sorted_z dictionary
node_dict_sorted_z = {}
# Loop through node_dict
# create num_unique_z_coord arrays
# Example 3 arrays
#     node_dict_sorted_z_array[0] = [1, 4, 7]
#     node_dict_sorted_z_array[1] = [2, 5, 8]
#     node_dict_sorted_z_array[2] = [3, 6, 9]
# Each array contains the node number which has the same z co-ordinate
node_dict_sorted_z_array = {}
for i in range(num_unique_z_coord):
    node_dict_sorted_z_array[i] = []
    for node in node_dict:
        z = float(node_dict[node][2])
        if z == z_list[i]:
            node_dict_sorted_z_array[i].append(node)
# Example node_dict_sorted_z_array
#     node_dict_sorted_z_array[0] = [1, 4, 7]

# Find unique y co-ordinates for each array in node_dict_sorted_z_array
y_list = {}
for i in range(num_unique_z_coord):
    y_list[i] = []
    for node in node_dict_sorted_z_array[i]:
        y = float(node_dict[node][1])
        if y not in y_list[i]:
            y_list[i].append(y)
    y_list[i].sort()
# Find unique number of y co-ordinates in y direction for each array in y_list
num_unique_y_coord = {}
for i in range(num_unique_z_coord):
    num_unique_y_coord[i] = len(y_list[i])
    
# Find unique x co-ordinates for each key in y_list
x_list = {}
for i in range(num_unique_z_coord):
    x_list[i] = {}
    for j in range(num_unique_y_coord[i]):
        x_list[i][j] = []
        for node in node_dict_sorted_z_array[i]:
            y = float(node_dict[node][1])
            if y == y_list[i][j]:
                x = float(node_dict[node][0])
                if x not in x_list[i][j]:
                    x_list[i][j].append(x)
        x_list[i][j].sort()
# Find unique number of x co-ordinates in x direction for each key in x_list
num_unique_x_coord = {}
for i in range(num_unique_z_coord):
    num_unique_x_coord[i] = {}
    for j in range(num_unique_y_coord[i]):
        num_unique_x_coord[i][j] = len(x_list[i][j])
        
# New node label is a list which contains node count in the x, y and z directions
# Create new node label for each node in node_dict
new_node_label = {}
for node in node_dict:
    new_node_label[node] = []
    z = float(node_dict[node][2])
    for i in range(num_unique_z_coord):
        if z == z_list[i]:
            new_node_label[node].append(i+1)
            y = float(node_dict[node][1])
            for j in range(num_unique_y_coord[i]):
                if y == y_list[i][j]:
                    new_node_label[node].append(j+1)
                    x = float(node_dict[node][0])
                    for k in range(num_unique_x_coord[i][j]):
                        if x == x_list[i][j][k]:
                            new_node_label[node].append(k+1)
                            # rearrange new_node_label as [k, j, i]
                            new_node_label[node] = new_node_label[node][::-1]
# Example new_node_label
#     new_node_label[1] = [1, 1, 1]
                            
# Create Node_dict_sorted dictionary based on new_node_label
# Loop through node_dict
# Create Node_dict_sorted dictionary
# Node number is the key
# Dictionaries contains New node label as key and Node co-ordinates as values are the values
# New node label is a list which contains node count in the x, y and z directions
# Node co-ordinates are a list which contains the x, y and z co-ordinates
# Example Node_dict_sorted dictionary
#     Node_dict_sorted[1] = [[1, 1, 1], [0, 0, 0]]
#     Node_dict_sorted[2] = [[1, 1, 2], [0, 0, 0.0735]]
#     Node_dict_sorted[3] = [[1, 1, 3], [0, 0, 0.147]]
#     Node_dict_sorted[4] = [[1, 2, 1], [0, 1, 0]]
#     Node_dict_sorted[5] = [[1, 2, 2], [0, 1, 0.0735]]
#     Node_dict_sorted[6] = [[1, 2, 3], [0, 1, 0.147]]
#     Node_dict_sorted[7] = [[2, 1, 1], [1, 0, 0]]
#     Node_dict_sorted[8] = [[2, 1, 2], [1, 0, 0.0735]]
#     Node_dict_sorted[9] = [[2, 1, 3], [1, 0, 0.147]]
Node_dict_sorted = {}
# Loop through node_dict
for node in node_dict:
    # Extract new node label
    new_node_label_list = new_node_label[node]
    # Extract node co-ordinates
    x = float(node_dict[node][0])
    y = float(node_dict[node][1])
    z = float(node_dict[node][2])
    node_coord = [x, y, z]
    # Add node to Node_dict_sorted dictionary
    Node_dict_sorted[node] = [new_node_label_list, node_coord]


# Print node_dict_sorted_z dictionary
print(Node_dict_sorted)


# Create a list of nodes

# Create a list of edges

# commit - edit_find_path_nodes_2023_10_31_02


# %%
