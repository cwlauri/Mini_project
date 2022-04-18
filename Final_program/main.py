from take_picture import take_picture
from undistort import undistort
from homography import homography
from vision import vision
from which_figures import which_figures

# This program will run the whole code as one, before running the code a few things has to be done.
# Fist the size of the QR code, the width and length of the work space has to be messuered.
# Next a pixel scale has to be set, this scale will scale the picture done in the homography.
# Here it is set to 10 this means 1mm will become 10 pixels.

# Qr size in mm
qr_dim = 97

# Work space width, sort side in mm
workspace_width_x = 283

# Work space length, long side in mm
workspace_length_y = 402

# The scale number the pixels should be scaled with
pixiel_scale = 10

# Then the path for the pictures folder has to be set, this is defined in the line below.
# path for pictures
path = 'C:/Users/Christian Wagner Lau/Desktop/Final_program/pictures'

# Then The picture is taken, where the input is only the path to the pictures folder.
# Function for taking the picture
take_picture(path)

# Now that the picture is taken, the picture has to be undistorted.
# Function for undistorted the picture
undistort(path)

# Now to be able to map the pixel coordinates from the picture to the real world, homography is used.
# Here the inputs are, the qr code size, the workspaces width and length, the pixel scale and the path to the picture
# folder.
# Function for doing the homography
homography(qr_dim, workspace_width_x, workspace_length_y, pixiel_scale, path)

# Then we do the vision part, and find the x and y coordinates, angle and color of each block.
# Where the input is the qr code size, the pixel scale and path for the picture folder.
block_matrix = vision(qr_dim, pixiel_scale, path)

# Then location matrix for robodk has to be set up and sorted, so that the order of block locations in the Location
# matrix is in the right order to make the desired figures. The f_m matrix describes which figures the user wants to
# make want to make, so if for the given figure type the value is 1, it should be made if the required block are in the
# workspace. As default this value is 1 for all the figures, so that if it is possible to make the figure, it is made.

# f_m = [homer, marge, bart, Lisa, maggi]
f_m = [1, 1, 1, 1, 1]

# The Location matrix is found through the which figures function, and defined.
Location = which_figures(f_m, block_matrix, pixiel_scale)

# Then the Location matrix is displayed.
print(Location)
