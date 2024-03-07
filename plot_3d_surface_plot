import numpy as np
import scipy
from matplotlib import pyplot as plt
from scipy.spatial import Delaunay


def plot_3d_surface(n_points, limits=(-1, 1), func=None):
  """
  Generates and plots a 3D surface from randomly spaced data points.

  Args:
      n_points: Number of data points to generate.
      limits: Tuple of (min, max) defining the limits for x and y axes.
      func: Optional function defining the surface equation.
          If None, random z values are used.

  Raises:
      ValueError: If n_points is less than 3.
  """

  # Check for invalid number of points
  if n_points < 3:
    raise ValueError("Number of points must be greater than or equal to 3")

  # Generate random data points
  x = np.random.rand(n_points) * (limits[1] - limits[0]) + limits[0]
  y = np.random.rand(n_points) * (limits[1] - limits[0]) + limits[0]

  # Generate z values based on the function or randomly
  if func is None:
    z = np.random.rand(n_points)
  else:
    z = func(x, y)

  # Create Delaunay triangulation for interpolation
  tri = Delaunay(np.vstack((x, y)).T)

  # Create figure and axes
  fig = plt.figure(figsize=(8, 6))
  ax = fig.add_subplot(111, projection='3d')

  # Plot the surface using triangles
  ax.plot_trisurf(x, y, z, triangles=tri.simplices)

  # Set axis labels and limits
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_zlabel("Z")
  ax.set_xlim(limits)
  ax.set_ylim(limits)

  # Set title
  ax.set_title("3D Surface Plot")

  # Show the plot
  plt.show()


# Example usage
plot_3d_surface(100)  # Random surface

# Example usage with a custom function
def custom_surface(x, y):
  return np.sin(x) * np.cos(y)

plot_3d_surface(50, func=custom_surface)  # Surface from a custom function
