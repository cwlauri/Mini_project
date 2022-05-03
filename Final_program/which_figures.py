import numpy as np
import pandas as pd


# This function will set up a matrix called Location, that will hold all the locations of the blocks that the robot
# has to pic up, in a specific order. Where there is two options of ordering the blocks, the first is where
# the robot picks one block and puts it in the end placement. For this option the figure has to be build
# from the ground up. For the second options the block are stacked to one figure and the placed in the
# end placement.

# The location matrix will have the following values. (x, y, z, rotation, figure number), position related parameters
# are used for by the robot to find the block, and the figure number is used by the robot to determine which figure
# it is making, and when the figures are constructed.

def which_figures(f_m, block_matrix, pixiel_scale):
    # To check the function a test block matrix can be used.
    # block_matrix = (x,y,r,c) and we want to get (x,y,z,r,#f)
    # block_matrix = [[1,15,29,1],
    #                 [2,16,30,2],
    #                 [3,17,31,3],
    #                 [4,18,32,2],
    #                 [5,19,33,3],
    #                 [6,20,34,2],
    #                 [7,21,35,3],
    #                 [8,22,36,3],
    #                 [9,23,37,2],
    #                 [10,24,38,3],
    #                 [11,25,39,3],
    #                 [12,26,40,4],
    #                 [13,27,41,4],
    #                 [14,28,42,5]]

    # First the block matrix will be defined as a np array
    bl_np_a = np.array(block_matrix)

    # Check the matrix for error handling.
    # print(bl_np_a)

    # -----------------------------------------Finding colors-----------------------------------------------

    # To determined which figures can be made, a matrix which hold the summed amount of each color block has to be made.
    bl_c_m = bl_np_a[:, 3]

    # Check the matrix for error handling.
    # print(bl_c_m)

    # Now the summed amount of each block color in the workspace is found.
    g_c = np.count_nonzero(bl_c_m == 1)  # 1  # ("Green")
    b_c = np.count_nonzero(bl_c_m == 2)  # 2  # ("Blue")
    y_c = np.count_nonzero(bl_c_m == 3)  # 3  # ("Yellow")
    o_c = np.count_nonzero(bl_c_m == 4)  # 4  # ("Orange")
    bl_c = np.count_nonzero(bl_c_m == 5)  # 5  # ("Black")

    # Now these summed amount is put into the color matrix c_m
    c_m = np.array([g_c,
                    b_c,
                    y_c,
                    o_c,
                    bl_c])

    # check for information, for error handling
    # print(c_m)

    # ----------------------------------------Setting picking option------------------------------------------------

    # Here it is chosen which stacking option is used, the different options also set different z coordinates.

    # Figure stacking
    # Homer_s_o = [3,5,2]
    # marge_s_o = [2,3,1]
    # bart_s_o = [3,4,2]
    # lisa_s_o = [3,4,3]
    # maggi_s_o = [3,2]
    # z_1 = 0
    # z_2 = 19
    # z_3 = 38

    # Pick one block at the time
    Homer_s_o = [2, 5, 3]
    marge_s_o = [1, 3, 2]
    bart_s_o = [2, 4, 3]
    lisa_s_o = [3, 4, 3]
    maggi_s_o = [2, 3]
    z_1 = 0
    z_2 = 0
    z_3 = 0

    # -----------------------------------------Defining figure numbers-----------------------------------------------

    # Each figure gets a number that represents that specific figure.
    f_homer = 1
    f_marge = 2
    f_bart = 3
    f_Lisa = 4
    f_maggi = 5

    # ------------------------------------Constructing the Location matrix------------------------------------------
    # To construct the Location matrix an if statement is used, where the first if statement for Homer is described,
    # and the if statement is the same for the rest of the figures. A walk through for Homer will now be done.
    # -----------------------------------------------Homer----------------------------------------------------------
    # Firstly it is investigated if the Homer figure should be made, and if it is possible to make it with the blocks
    # that are present in the workspace.

    # Fist 3 zero arrays are made for each of the blocks in the figure, if the figure can be made the block position
    # will be inserted in to the Homer1, Homer2 and Homer3 arrays.
    Homer1 = np.zeros((1, 5))
    Homer2 = np.zeros((1, 5))
    Homer3 = np.zeros((1, 5))

    # Check for information, for error handling.
    # print(bl_np_a[(14-1),3])

    # The stacking order is defined as Homer_f
    Homer_f = Homer_s_o

    # The if statement hold a condition for each of the colors that are need in the figure, and the user defined
    # value that is 1 if the user wants to make the given figure.
    if bl_c >= 1 and y_c >= 1 and b_c >= 1 and f_m[0] == 1:
        # If the if statement is true, the block that are needed to make the figure a subtracted from the summed
        # color matrix c_m. This updates the summed color matrix c_m so that no block can be used twice.
        bl_c = bl_c - 1
        y_c = y_c - 1
        b_c = b_c - 1

        # Now that it has been determined that the figure has to be made and the color matrix has been updated,
        # the lines in the location matrix has to be constructed. To do this a For loop for each of the block in the
        # given figure is constructed. Here the for loop searches the block matrix, for the given block that has the
        # desired color and takes the position and rotation and puts it in to the Homer1 line. Then it adds the
        # specific figure number in the end of the Homer1 line, and lastly deletes the line of the pick block from
        # the block matrix, so that no block is used twice. This is also done for the Homer2 ande Homer3 line.
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == Homer_f[0]:
                Homer1 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_1,
                          bl_np_a[(i - 1), 2], f_homer]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == Homer_f[1]:
                Homer2 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] // pixiel_scale), z_2,
                          bl_np_a[(i - 1), 2], f_homer]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == Homer_f[2]:
                Homer3 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_3,
                          bl_np_a[(i - 1), 2], f_homer]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
    else:
        # If the user wants to make the given figure, but it was not possible, the value in the f_m array is changed
        # to 0, to indecate that it was not possible to make the figure.
        f_m[0] = 0

    # Check for information, for error handling.
    # print(Homer1)
    # print(Homer2)
    # print(Homer3)

    # Then the Homer1, Homer2 and Homer3 lines are combined into one matrix called Homer.
    Homer = np.vstack((Homer1, Homer2, Homer3))

    # Check for information, for error handling.
    # print("Homer")
    # print(Homer)
    # print(bl_np_a)

    # -----------------------------------------walk through conclusion----------------------------------------------
    # The walk through and explanation of the code to construct the homer matrix, is the same for each of the figures
    # just with different values. The only exception is maggi, where the reason for this is that maggi is only construct
    # of 2 block but the principals are the same.
    # -----------------------------------------------Marge----------------------------------------------------------
    marge1 = np.zeros((1, 5))
    marge2 = np.zeros((1, 5))
    marge3 = np.zeros((1, 5))

    marge_f = marge_s_o

    if g_c >= 1 and y_c >= 1 and b_c >= 1 and f_m[1] == 1:
        g_c = g_c - 1
        y_c = y_c - 1
        b_c = b_c - 1
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == marge_f[0]:
                marge1 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_1,
                          bl_np_a[(i - 1), 2], f_marge]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == marge_f[1]:
                marge2 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_2,
                          bl_np_a[(i - 1), 2], f_marge]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == marge_f[2]:
                marge3 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_3,
                          bl_np_a[(i - 1), 2], f_marge]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
    else:
        f_m[1] = 0

    # Check for information, for error handling.
    # print(marge1)
    # print(marge2)
    # print(marge3)

    marge = np.vstack((marge1, marge2, marge3))

    # Check for information, for error handling.
    # print("marge")
    # print(marge)
    # print(bl_np_a)

    # ------------------------------------------------Bart----------------------------------------------------------
    bart1 = np.zeros((1, 5))
    bart2 = np.zeros((1, 5))
    bart3 = np.zeros((1, 5))

    bart_f = bart_s_o

    if o_c >= 1 and y_c >= 1 and b_c >= 1 and f_m[2] == 1:
        o_c = o_c - 1
        y_c = y_c - 1
        b_c = b_c - 1
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == bart_f[0]:
                bart1 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_1,
                         bl_np_a[(i - 1), 2], f_bart]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == bart_f[1]:
                bart2 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_2,
                         bl_np_a[(i - 1), 2], f_bart]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == bart_f[2]:
                bart3 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_3,
                         bl_np_a[(i - 1), 2], f_bart]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
    else:
        f_m[2] = 0

    # Check for information, for error handling.
    # print(bart1)
    # print(bart2)
    # print(bart3)

    bart = np.vstack((bart1, bart2, bart3))

    # Check for information, for error handling.
    # print("bart")
    # print(bart)
    # print(bl_np_a)

    # ------------------------------------------------Lisa----------------------------------------------------------
    lisa1 = np.zeros((1, 5))
    lisa2 = np.zeros((1, 5))
    lisa3 = np.zeros((1, 5))

    lisa_f = lisa_s_o

    if o_c >= 1 and y_c >= 2 and f_m[3] == 1:
        o_c = o_c - 1
        y_c = y_c - 2
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == lisa_f[0]:
                lisa1 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_1,
                         bl_np_a[(i - 1), 2], f_Lisa]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == lisa_f[1]:
                lisa2 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_2,
                         bl_np_a[(i - 1), 2], f_Lisa]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == lisa_f[2]:
                lisa3 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_3,
                         bl_np_a[(i - 1), 2], f_Lisa]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
    else:
        f_m[3] = 0

    # Check for information, for error handling.
    # print(lisa1)
    # print(lisa2)
    # print(lisa3)

    lisa = np.vstack((lisa1, lisa2, lisa3))

    # Check for information, for error handling.
    # print("Lisa")
    # print(lisa)
    # print(bl_np_a)

    # ------------------------------------------------Maggi----------------------------------------------------------
    maggi1 = np.zeros((1, 5))
    maggi2 = np.zeros((1, 5))

    maggi_f = maggi_s_o

    if y_c >= 1 and b_c >= 1 and f_m[4] == 1:
        y_c = y_c - 1
        b_c = b_c - 1
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == maggi_f[0]:
                maggi1 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_1,
                          bl_np_a[(i - 1), 2], f_maggi]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
        for i in range(len(bl_np_a)):
            if bl_np_a[(i - 1), 3] == maggi_f[1]:
                maggi2 = [(bl_np_a[(i - 1), 0] / pixiel_scale), (bl_np_a[(i - 1), 1] / pixiel_scale), z_2,
                          bl_np_a[(i - 1), 2], f_maggi]
                bl_np_a = np.delete(bl_np_a, (i - 1), 0)
                break
    else:
        f_m[4] = 0

    # Check for information, for error handling.
    # print(maggi1)
    # print(maggi2)

    maggi = np.vstack((maggi1, maggi2))

    # Check for information, for error handling.
    # print("maggi")
    # print(maggi)
    # print(bl_np_a)

    # --------------------------------------Constructing the matrix--------------------------------------------------
    # Now the Location matrix can be constructed. To tell the robot that it is done and can stop, a "finish" line is
    # added to the Location matrix, this line is shown below.

    robodk_m = [0, 0, 0, 0, 6]

    # To start constructing the Location matrix, the matrix is predefined as an zero array.
    Location = np.zeros([1, 5])

    # Then this set of if statements stack the matrices of the different figures if there is values in them. Which
    # means that it will only be stacked if there are values in the given figure matrix fx Homer. Then if there are no
    # figures detected it will only add the robodk array to the Location matrix, and display a message that reads " no
    # location matrix was made". But if it was possible to make the Location matrix, a message will be displayed which
    # reads "Location matrix done" and "csv file saved". Furthermore, the Location will be saved as a csv file, so
    # that it can be retrieved by the robodk program.
    if f_m[0] > 0:
        Location = np.vstack((Location, Homer))
    else:
        pass
    if f_m[1] > 0:
        Location = np.vstack((Location, marge))
    else:
        pass
    if f_m[2] > 0:
        Location = np.vstack((Location, bart))
    else:
        pass
    if f_m[3] > 0:
        Location = np.vstack((Location, lisa))
    else:
        pass
    if f_m[4] > 0:
        Location = np.vstack((Location, maggi))
    else:
        pass
    if np.sum(f_m) == 0:
        Location = robodk_m

    if np.sum(f_m) == 0:
        print("No location matrix was made")
    else:
        Location = np.vstack((Location, robodk_m))
        print("Location matrix done")
        Location = np.delete(Location, 0, 0)
        df = pd.DataFrame(Location)
        df.to_csv('Location.csv')
        print("csv file saved")

    return Location
