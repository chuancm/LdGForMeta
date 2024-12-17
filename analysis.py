import numpy as np
import sys
import math
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


# def mpi_stitch(in_filenames, out_filename=None):
#     """
#     Stitches together a set of data text files from an MPI run into a single
#     file with the proper ordering of lines for use by openViewMin. First three
#     columns must be x y z coords.

#     """

#     data = np.concatenate([np.loadtxt(f) for f in in_filenames])
#     coords = np.asarray(data[:, :3], dtype=int)
#     order = np.lexsort(coords.T)
#     ordered_data = data[order]
#     if out_filename is not None:
#         fmt = "%d\t%d\t%d"
#         for i in range(data.shape[1] - 3):
#             fmt += "\t%f"
#         np.savetxt(
#             out_filename,
#             ordered_data,
#             fmt=fmt
#         )
#         print(in_filenames, "->", out_filename)
#     return ordered_data





def n_and_site_types_from_open_Qmin(filename):
    """ Import Q-tensor data in the open-Qmin format """
    data = np.loadtxt(filename, delimiter='\t')
    # data_ranked= np.zeros(data.shape)
    
    director=np.zeros((Lx,Ly,Lz,3))
    site_types= np.zeros((Lx,Ly,Lz))
    for i in range(data.shape[0]):
        x= int(data[i][0])
        y= int(data[i][1])
        z= int(data[i][2])
        site_types[x][y][z]=data[i][8]
        
        [Qxx, Qxy, Qxz, Qyy, Qyz] = data[i][3:8]

    # take system dimensions from coordinates on last line
    # dims = tuple(np.asarray(data[-1][:3] + 1, dtype=int))

    # form traceless, symmetric matrix from indep. Q-tensor components
        Qmat=np.array([
                [Qxx, Qxy, Qxz],
                [Qxy, Qyy, Qyz],
                [Qxz, Qyz, -Qxx - Qyy]
            ])
        # print(Qmat)
        # Calculate director as eigevector with leading eigenvalue
        val, evecs = np.linalg.eigh(Qmat)
        # print(evecs.shape)
        n = evecs[:, 2]
        director[x][y][z][:]=n
        
        # Reshape 1D arrays into system (Lx, Ly, Lz) dimensions

    return director, site_types


num=float(sys.argv[1])
infname=str(sys.argv[2])
outfname=str(sys.argv[3])
num=int(num)
[Lx,Ly,Lz]=[num,num,150]

[director,site_types]=n_and_site_types_from_open_Qmin(infname) #test.txt is a merged file with uncertain order
print(site_types[:][:][0])
print(site_types[:][:][1])
print(site_types[:][:][2])
sphere_coor = np.zeros((Lx,Ly,Lz,2))

for i in range(0,sphere_coor.shape[0]):
    for j in range(0,sphere_coor.shape[1]):
        for k in range (0,sphere_coor.shape[2]):
            x=director[i][j][k][0]
            y=director[i][j][k][1]
            z=director[i][j][k][2]
            r= np.sqrt(x**2+y**2+z**2) #the length of the director    
            if r != 0:
                theta = math.pi/2-np.arccos(z/r)
            else:
                theta = math.pi/2
            phi = -np.arctan2(y,x)
            sphere_coor[i][j][k][:]=[theta,phi]



theta = np.degrees(sphere_coor[..., 0])  # Take the first element from the last dimension (theta)
phi = np.degrees(sphere_coor[..., 1] )    # Take the second element from the last dimension (phi)

# Prepare formatted output
output = ""

nm=1e-2 #in lumerical the unit is um, the scale in the simualation result is 10nm

# Iterate over the z dimension (150)
for z in range(sphere_coor.shape[2]):
    output += "THETA\n"
    output += f"Z={z*nm},"  # Add the current z layer to the output
    
    # Output theta values for the current z layer
      # Indicate the start of theta values
    for x in range(Lx):
        output += f"X={x*nm},"
    output = output.rstrip(',') + "\n"
    
    
    for y in range(sphere_coor.shape[1]):
        
        output += f"Y={y *nm},"  # Add the current y layer to the output
        for x in range(sphere_coor.shape[0]):
            if site_types[x][y][z]!=1:
                output += f"{theta[x, y, z]:.2f},"  # Append theta value
            else:
                output += "-,"
        output = output.rstrip(',') + "\n"  # Remove the trailing comma and add a newline

    # Output phi values for the current z layer
    output += "PHI\n"  # Indicate the start of phi values
    output += f"Z={z*nm},"
    
    for x in range(Lx):
        output += f"X={x*nm},"
    output = output.rstrip(',') + "\n"

    for y in range(sphere_coor.shape[1]):
        output += f"Y={y*nm},"  # Add the current y layer to the output
        for x in range(sphere_coor.shape[0]):
            if site_types[x][y][z]!=1:
                output += f"{phi[x, y, z]:.2f},"  # Append theta value
            else:
                output += "-,"
        output = output.rstrip(',') + "\n"  # Remove the trailing comma and add a newline

# Print the result (can also write to a file)
# print(output)

# If needed, save the results to a file
with open(outfname, "w") as f:
    f.write(output)
