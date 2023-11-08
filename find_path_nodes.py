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

# import modules
import numpy as np

def create_node_dict(node_data_file_name, aligned_angle):
    # Read in the node data from the file

    # Open textfile
    f = open(node_data_file_name, 'r')

    # Read textfile
    data = f.readlines()

    # Close textfile
    f.close()

    # Process each line of the data and extract the node number and node co-ordinates
    # Create empty dictionary
    node_dict = {}
    # Loop through data
    for line in data:
        line = line.strip()
        node = line.split(',')[0]
        x = line.split(',')[1]
        y = line.split(',')[2]
        z = line.split(',')[3]
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
            
    # Transform node co-ordinates x and y based on aligned_angle
    # aligned_angle is the angle of node alignment in degrees
    # aligned_angle could be 0, 15, 30 or 45 degrees
    # Loop through node_dict
    for node in node_dict:
        # Extract x and y co-ordinates
        x = float(node_dict[node][0])
        y = float(node_dict[node][1])
        # Transform x and y co-ordinates and round to 3 decimal places
        x_transformed = x*np.cos(np.deg2rad(aligned_angle)) - y*np.sin(np.deg2rad(aligned_angle))
        y_transformed = x*np.sin(np.deg2rad(aligned_angle)) + y*np.cos(np.deg2rad(aligned_angle))
        x_transformed = round(x_transformed, 3)
        y_transformed = round(y_transformed, 3)
        # Update node_dict
        node_dict[node][0] = x_transformed
        node_dict[node][1] = y_transformed
        
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
    
    # Find maximum and minimum new node label in the x, y and z directions
    new_node_label_x_max = 0
    new_node_label_x_min = 0
    new_node_label_y_max = 0
    new_node_label_y_min = 0
    new_node_label_z_max = 0
    new_node_label_z_min = 0
    for node in new_node_label:
        new_node_label_x = new_node_label[node][0]
        new_node_label_y = new_node_label[node][1]
        new_node_label_z = new_node_label[node][2]
        if new_node_label_x > new_node_label_x_max:
            new_node_label_x_max = new_node_label_x
        if new_node_label_x < new_node_label_x_min:
            new_node_label_x_min = new_node_label_x
        if new_node_label_y > new_node_label_y_max:
            new_node_label_y_max = new_node_label_y
        if new_node_label_y < new_node_label_y_min:
            new_node_label_y_min = new_node_label_y
        if new_node_label_z > new_node_label_z_max:
            new_node_label_z_max = new_node_label_z
        if new_node_label_z < new_node_label_z_min:
            new_node_label_z_min = new_node_label_z
            
    # Create a list of new node label for x,1,1
    # Example
    #     new_node_label_x_list = [[1, 1, 1], [2, 1, 1], [3, 1, 1]]
    new_node_label_x_list = []
    for i in range(new_node_label_x_min, new_node_label_x_max+1):
        new_node_label_x_list.append([i, 1, 1])
    # Create a list of new node label for 1,y,1
    # Example
    #     new_node_label_y_list = [[1, 1, 1], [1, 2, 1], [1, 3, 1]]
    new_node_label_y_list = []
    for i in range(new_node_label_y_min, new_node_label_y_max+1):
        new_node_label_y_list.append([1, i, 1])
                                
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

    # Return Node_dict_sorted dictionary
    return Node_dict_sorted, new_node_label_x_list, new_node_label_y_list


def find_path_nodes(node_dict_sorted, node_start_label, angle):

    find_path_nodes_list = []
    find_path_node_label_list = []

    if angle == 0:
        # Find path nodes
        # Find path nodes in the x direction
        # Find maximum and minimum node label in the x direction for a specific y and z direction of node_start_lable 
        # Start node label is first label of node_start_label in the x direction
        # End node label is maximum node label in the x direction
        # Example
        #     node_start_label = [1, 1, 1]
        #     node_start_label[0] = 1
        #     maximum_node_label_x = 100
        #     minimum_node_label_x = 1
        #     node_start_label_x = 1
        #     node_end_label_x = 100
        # node_label_list is a list which contains the node label starting from node_start_label_x to node_end_label_x
        # Example
        #     node_label_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        # Find maximum and minimum node label in the x direction
        maximum_node_label_x = 1
        minimum_node_label_x = 1
        for node in node_dict_sorted:
            node_label_x = node_dict_sorted[node][0][0]
            node_label_y = node_start_label[1]
            node_label_z = node_start_label[2]
            if node_label_x > maximum_node_label_x and node_label_y == node_start_label[1] and node_label_z == node_start_label[2]:
                maximum_node_label_x = node_label_x
            if node_label_x < minimum_node_label_x and node_label_y == node_start_label[1] and node_label_z == node_start_label[2]:
                minimum_node_label_x = node_label_x
        # Find node label x list in the x direction which is for angle 0
        node_label_x_list = []
        for i in range(minimum_node_label_x, maximum_node_label_x+1):
            node_label_x_list.append(i)
        # Find path nodes
        # Loop through node_dict_sorted
        for node in node_dict_sorted:
            node_label_x = node_dict_sorted[node][0][0]
            node_label_y = node_start_label[1]
            node_label_z = node_start_label[2]
            if node_label_x in node_label_x_list:
                if int(node_label_y) == int(node_dict_sorted[node][0][1]):
                    if int(node_label_z) == int(node_dict_sorted[node][0][2]):
                        find_path_nodes_list.append(node)
                        find_path_node_label_list.append(node_dict_sorted[node][0])
        # Sort find_path_nodes_list and find_path_node_label_list
        # Sort find_path_node_label_list
        # Example
        #     find_path_node_label_list = [[1, 1, 1], [1, 1, 2], [1, 1, 3]]
        for i in range(len(find_path_node_label_list)):
            for j in range(len(find_path_node_label_list)-1):
                if find_path_node_label_list[j][0] > find_path_node_label_list[j+1][0]:
                    temp = find_path_node_label_list[j]
                    find_path_node_label_list[j] = find_path_node_label_list[j+1]
                    find_path_node_label_list[j+1] = temp
        # Sort find_path_nodes_list based on find_path_node_label_list
        # Example
        #     find_path_nodes_list = [1, 2, 3]
        #    find_path_node_label_list = [[1, 1, 1], [1, 1, 2], [1, 1, 3]]
        find_path_nodes_list_temp = []
        for i in range(len(find_path_node_label_list)):
            for node in node_dict_sorted:
                if node_dict_sorted[node][0] == find_path_node_label_list[i]:
                    find_path_nodes_list_temp.append(node)
        find_path_nodes_list = find_path_nodes_list_temp
        
    if angle == 90:
        # Find path nodes
        # Find path nodes in the y direction
        # Find maximum and minimum node label in the y direction for a specific x and z direction of node_start_lable 
        # Start node label is first label of node_start_label in the y direction
        # End node label is maximum node label in the y direction
        # Example
        #     node_start_label = [1, 1, 1]
        #     node_start_label[1] = 1
        #     maximum_node_label_y = 100
        #     minimum_node_label_y = 1
        #     node_start_label_y = 1
        #     node_end_label_y = 100
        # node_label_list is a list which contains the node label starting from node_start_label_y to node_end_label_y
        # Example
        #     node_label_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        # Find maximum and minimum node label in the y direction
        maximum_node_label_y = 1
        minimum_node_label_y = 1
        
        for node in node_dict_sorted:
            node_label_x = node_start_label[0]
            node_label_y = node_dict_sorted[node][0][1]
            node_label_z = node_start_label[2]
            if node_label_y > maximum_node_label_y and node_label_x == node_start_label[0] and node_label_z == node_start_label[2]:
                maximum_node_label_y = node_label_y
            if node_label_y < minimum_node_label_y and node_label_x == node_start_label[0] and node_label_z == node_start_label[2]:
                minimum_node_label_y = node_label_y
        # Find node label y list along the y direction which is for angle 90
        node_label_y_list = []
        for i in range(minimum_node_label_y, maximum_node_label_y+1):
            node_label_y_list.append(i)
        # print(node_label_y_list)
        # Find path nodes
        # Loop through node_dict_sorted
        for node in node_dict_sorted:
            node_label_x = node_start_label[0]
            node_label_y = node_dict_sorted[node][0][1]
            node_label_z = node_start_label[2]
            if node_label_y in node_label_y_list:
                if int(node_label_x) == int(node_dict_sorted[node][0][0]):
                    if int(node_label_z) == int(node_dict_sorted[node][0][2]):
                        # Example
                        # node = 10248
                        # node_start_label = [2, 1, 1]
                        # node_dict_sorted[node][0] = [2, 1, 1]
                        # node_start_label[0] = 2
                        # node_dict_sorted[node][0][1] = 1
                        # node_start_label[2] = 1
                        # node_label_x = 2
                        # node_label_y = 1
                        # node_label_z = 1
                        find_path_nodes_list.append(node)
                        find_path_node_label_list.append(node_dict_sorted[node][0])
        # Sort find_path_nodes_list and find_path_node_label_list
        # Sort find_path_node_label_list
        # Example
        #     find_path_node_label_list = [[1, 1, 1], [1, 1, 2], [1, 1, 3]]
        for i in range(len(find_path_node_label_list)):
            for j in range(len(find_path_node_label_list)-1):
                if find_path_node_label_list[j][1] > find_path_node_label_list[j+1][1]:
                    temp = find_path_node_label_list[j]
                    find_path_node_label_list[j] = find_path_node_label_list[j+1]
                    find_path_node_label_list[j+1] = temp
        # Sort find_path_nodes_list based on find_path_node_label_list
        # Example
        #     find_path_nodes_list = [1, 2, 3]
        #    find_path_node_label_list = [[1, 1, 1], [1, 1, 2], [1, 1, 3]]
        find_path_nodes_list_temp = []
        for i in range(len(find_path_node_label_list)):
            for node in node_dict_sorted:
                if node_dict_sorted[node][0] == find_path_node_label_list[i]:
                    find_path_nodes_list_temp.append(node)
        find_path_nodes_list = find_path_nodes_list_temp

    # Return find_path_nodes_list and find_path_node_label_list
    return find_path_nodes_list, find_path_node_label_list


def session_path(part_name, path_name, path_type, node_number_list):
#session.Path(name='Path-1', type=NODE_LIST, expression=(('PART-1-1', (205, )), 
#    ('PART-1-1', (206, )), ('PART-1-1', (207, )), ('PART-1-1', (208, )), (
#    'PART-1-1', (209, )), ('PART-1-1', (210, ))))
    path_expression = []
    for node_number in node_number_list:
        path_expression.append((part_name, (node_number, )))
    session_path = ('session.Path(name=\'' + path_name + '\', type=' + path_type + ', expression=' + str(path_expression) + ')')
    return session_path

    
x = create_node_dict('Study_iter02_refined3_1.12microsecond_nodal_coordinates.txt', aligned_angle=0)
#x= create_node_dict('data_test.txt')
angle = 90
y = find_path_nodes(x[0], ['2','1','1'], angle)
print(angle, "\n")

part_name = 'PART-1-1'
path_name = 'Path-1'
path_type = 'NODE_LIST'
r = session_path(part_name, path_name, path_type, y[0])
print(r)


angle = 0
z = find_path_nodes(x[0], ['2','1','1'], angle)
print(angle, "\n")

part_name = 'PART-1-1'
path_name = 'Path-2'
path_type = 'NODE_LIST'
p = session_path(part_name, path_name, path_type, z[0])
print(p)

x = create_node_dict('Study_iter02_aligned1_1.12microsecond_nodal_coordinates.txt', aligned_angle=45)
#x= create_node_dict('data_test.txt')
angle = 90
y = find_path_nodes(x[0], ['2','1','1'], angle)
print(angle, "\n" ,y)
angle = 0
z = find_path_nodes(x[0], ['2','1','1'], angle)
print(angle, "\n", z)



# %%
