#%%
# Extract data from a textfile which contains nodal co-ordinates x,y and z and the nodal current'

''' 
textfile format (data.txt)
N1 0.0 0.0 0.0  # Node 1
N2 0.0 0.0 0.0  # Node 2
I0_N1 0.0 # Current at time 0 at node 1
I0_N2 0.0 # Current at time 0 at node 2
I1_N1 0.0 # Current at time 1 at node 1
I1_N2 0.0 # Current at time 1 at node 2
'''

# Import modules
import numpy as np

# Open textfile
f = open('data.txt', 'r')

# Read textfile
data = f.readlines()

# Close textfile
f.close()

# create function to extract nodes and node co-ordinates from a line
# N1    0.0 0.0 0.0  # Node 1
def extract_node(line):
    if line[0] == 'N':
        node = line.split('\t')[0]
        node = node[1:]
        x = line.split('\t')[1]
        y = line.split('\t')[2]
        z = line.split('\t')[3]
    return node, x, y, z

# create function to extract current details from a line
# I0_N1 0.0 # Current at time 0 at node 1
def extract_current(line):
    if line[0] == 'I':
        t = line.split('\t')[0]
        t = t.split('_')[0]
        t = t[1:]
        node = line.split('\t')[0]
        node = node.split('_')[1]
        node = node[1:]
        current = line.split('\t')[1]
    return t, node, current

# Create Dictionary which contains the node number as the key and the node co-ordinates, time and current as the value
# node co-ordinates are stored as a list
# time and current are stored as a dictionary

# Create empty dictionary
node_dict = {}

# Loop through data
for line in data:
    line = line.strip()
    if line[0] == 'N':
        node, x, y, z = extract_node(line)
        node_dict[node] = [(x, y, z)]
    elif line[0] == 'I':
        t, node, current = extract_current(line)
        node_dict[node].append({t: current})

# Print dictionary
print(node_dict)
# {'1': [('0.0', '0.0', '0.0'), {'0': '0.0'}, {'1': '0.0'}], '2': [('0.0', '0.0', '0.0'), {'0': '0.0'}, {'1': '0.0'}], '3': [('0.0', '0.0', '0.0'), {'0': '0.0'}, {'1': '0.0'}]}
# node_dict is a dictionary which contains the node number as the key and the node co-ordinates, time and current as the value
# node co-ordinates are stored as a list
# time and current are stored as a dictionary


# Plot time vs current for a list of nodes
import matplotlib.pyplot as plt
node_list = ['1', '2', '3']
node_dict_plot = {}
# Extracted current are stored as a dictionary which contains the node number as the key and the node co-ordinates, time and current as the value
# node co-ordinates are stored as a list
# time and current are stored as a dictionary
# Example: {'1', [('0.0', '0.0', '0.0'), {'0': '0.0'}, {'1': '0.0'}]}
for node in node_list:
    # Extract current dictionary from node_dict
    current_dict = node_dict[node][1:]
    # Extract time and current from current_dict
    time = []
    current = []
    for i in range(len(current_dict)):
        time.append(float(list(current_dict[i].keys())[0]))
        current.append(float(list(current_dict[i].values())[0]))
    # Sort time and current
    time, current = zip(*sorted(zip(time, current)))
    # Convert time and current to numpy arrays
    time = np.array(time)
    current = np.array(current)
    # Store time and current in node_dict_plot to plot later
    node_dict_plot[node] = [time, current]

# Plot time vs current for all the nodes in node_list
for node in node_list:
    plt.plot(node_dict_plot[node][0], node_dict_plot[node][1], label='node ' + node)
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Time vs Current')
plt.legend()
plt.show()

node_list = ['1']
time_list = [0.0, 1.0]
# Plot nodal location vs current for a list of nodes at a specific time
# Extract node_dict_plot2 from node_dict which contains the node number as the key and the node co-ordinates, time and current as the value for a specific time
node_dict_plot2 = {}
for time in time_list:
    for node in node_list:
        # Extract node co-ordinates from node_dict
        node_location = node_dict[node][0]
        # Extract current dictionary from node_dict for a specific time
        node_current_dict = node_dict[node][1:]
        node_current = 0.0
        for i in range(len(node_current_dict)):
            if float(list(node_current_dict[i].keys())[0]) == time:
                node_current = float(list(node_current_dict[i].values())[0])
        # Store node co-ordinates and current in node_dict_plot2 to plot later
        node_dict_plot2[node] = [node_location, node_current]
    # Extract node co-ordinates and current from node_dict_plot2 and sort them
    node_location = []
    node_current = []
    for node in node_list:
        node_location.append(node_dict_plot2[node][0])
        node_current.append(node_dict_plot2[node][1])
    node_location, node_current = zip(*sorted(zip(node_location, node_current)))





# %%
