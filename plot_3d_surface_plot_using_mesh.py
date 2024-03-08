# %%

""" Generates and plots a 3D surface from ABAQUS data points using Delaunay triangulation. 

    Input Files:
        ABAQUS input file with node numbers and nodal coordinates.
        ABAQUS report file with node numbers, NCURS (Nodal current, a scalar) and ECD (Electrical current density, a vector) data.
        
    Output Files:
        Image files of 3D surface plot of the NCURS and ECD data.
        
"""

# Importing the required libraries
import numpy as np
import scipy
from matplotlib import pyplot as plt
from scipy.spatial import Delaunay

def read_abaqus_input_file(file_path):
  
  # ABAQUS input file with node numbers and nodal coordinates
  # *Heading
  # E2_211_300x300_00_AllEdges_ins_Aligned
  # ** Job name: E2_211 Model name: Model-1
  # ** Generated by: Abaqus/CAE 2017
  # *Preprint, echo=NO, model=NO, history=NO, contact=NO
  # **
  # ** PARTS
  # **
  # *Part, name=Part-1
  # *Node
  #      1,  -5.47667694,   1.12071931,        0.147
  #      2,  -4.82962894,  -1.29409528,        0.147
  # *Element, type=DC3D8E
  # ...
  # End of file
   
  # Open the file and read the lines
  with open(file_path, 'r') as file:
    lines = file.readlines()
    
  # Initialize lists to store the node numbers and nodal coordinates
  nodes = []
  
  # Loop over the lines and extract the node numbers and nodal coordinates
  for line in lines:
    if line.startswith('*Node'):
      for line in lines[lines.index(line)+1:]:
        if line.startswith('*'):
          break
        else:
          nodes.append([float(x) for x in line.split(',')[1:]]) # Extract the nodal coordinates
      
  # Convert the list to a numpy array
  nodes = np.array(nodes)
  
  return nodes



def read_abaqus_report_file(file_path):
  
#********************************************************************************
#Field Output Report, written Wed Feb 21 15:47:46 2024

# ...
#   Element Label      Node Label           NCURS   ECD.Magnitude        ECD.ECD1        ECD.ECD2        ECD.ECD3
#                                          @Loc 1          @Loc 1          @Loc 1          @Loc 1          @Loc 1
#-----------------------------------------------------------------------------------------------------------------
#               1               1     50.6991E-03     159.973E-03    -932.070E-03     115.353E-06    -61.4617E-06
#               1               2     66.7449E-03         1.33402    -922.488E-03    -128.729E-06    -61.6543E-06

#
#  Minimum                           -112.625E-03     12.1321E-12        -1.01725    -330.916E-06    -65.4858E-06
# ...
#           Total                     15.7227E-09     1.06395E+03     4.78826E-03    -185.427E-09    -87.0518E-03
# End of file


  # Open the file and read the lines
  with open(file_path, 'r') as file:
    lines = file.readlines()
    
  # Initialize lists to store the node numbers, NCURS and ECD data
  node_numbers = []
  NCURS = []
  ECD = []
  
  # Loop over the lines and extract the node numbers, NCURS and ECD data
  for line in lines:
    if line.startswith('Element Label'):
      for line in lines[lines.index(line)+1:]:
        if line.startswith('Minimum'):
          break
        else:
          node_numbers.append(int(line.split()[1])) # Extract the node numbers
          NCURS.append(float(line.split()[2])) # Extract the NCURS data
          ECD.append([float(x) for x in line.split()[3:]]) # Extract the ECD data
          
  # Convert the lists to numpy arrays
  node_numbers = np.array(node_numbers)
  NCURS = np.array(NCURS)
  ECD = np.array(ECD)
  
  return node_numbers, NCURS, ECD


# Main program
# Read the ABAQUS input file
nodes = read_abaqus_input_file('E2_211.inp')

# Print the first 5 nodes
print(nodes[:5])

# Read the ABAQUS report file
node_numbers, NCURS, ECD = read_abaqus_report_file('E2_211.rpt')

# Print the first 5 node numbers, NCURS and ECD data
print(node_numbers[:5])
print(NCURS[:5])
print(ECD[:5])

# Create Delaunay triangulation for interpolation
tri = Delaunay(nodes)

# Create figure and axes
fig = plt.figure(figsize=(8, 6))  
ax = fig.add_subplot(111, projection='3d')

# Plot the surface using triangles
ax.plot_trisurf(nodes[:,0], nodes[:,1], NCURS, triangles=tri.simplices)

# Set axis labels and limits
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("NCURS")
ax.set_xlim([-5.5, 5.5])
ax.set_ylim([-5.5, 5.5])

# Set title
ax.set_title("3D Surface Plot of NCURS")

# Show the plot
plt.show()

# %%
