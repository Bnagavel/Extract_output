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
        
# Find number of nodes in z direction
# Example 3 nodes in z direction
#     1,           0.,           0.,        0.
#     2,           0.,           0.,        0.0735
#     3,           0.,           0.,        0.147
# Find unique z co-ordinates
z_list = []
for node in node_dict:
    z = float(node_dict[node][2])
    if z not in z_list:
        z_list.append(z)
z_list.sort()
# Find unique number of z co-ordinates in z direction
num_unique_z_coord = len(z_list)

# Calculate plate dimensions
# Plate dimensions are the dimensions of the plate which contains the nodes
# Plate_Length is the length of the plate in the x direction
# Plate_Width is the width of the plate in the y direction
# Plate_Height is the height of the plate in the z direction
Plate_Length = x_max - x_min
Plate_Width = y_max - y_min
Plate_Height = z_max - z_min

# Create node_dict_3D dictionary
# Node number is the key
# New node label and Node co-ordinates are the values
# New node label is a list which contains node count in the x, y and z directions
# Node co-ordinates are a list which contains the x, y and z co-ordinates
node_dict_3D = {}
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
#     node_dict_sorted_z_array[0] = [1, 2, 3]
#     node_dict_sorted_z_array[1] = [4, 5, 6]
#     node_dict_sorted_z_array[2] = [7, 8, 9]
# Each array contains the node number which has the same z co-ordinate
node_dict_sorted_z_array = {}
for i in range(num_unique_z_coord):
    node_dict_sorted_z_array[i] = []
    for node in node_dict:
        z = float(node_dict[node][2])
        if z == z_list[i]:
            node_dict_sorted_z_array[i].append(node)
# Loop through node_dict
# Create Node_dict_sorted_z dictionary
for i in range(num_unique_z_coord):
    for node in node_dict:
        z = float(node_dict[node][2])
        if z == z_list[i]:
            node_dict_sorted_z[node] = node_dict[node]
# Print node_dict_sorted_z dictionary
print(node_dict_sorted_z)


# Create a list of nodes

# Create a list of edges

# commit - edit_find_path_nodes_2023_10_31_02


# %%
