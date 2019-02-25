# coloring cells in vtk files

import sys

if len(sys.argv) != 4:
    print ("4 arguments are expected:")
    print ("n_cells")
    print ("n_node")
    print ("n_vtk")
    print ("steps_vtk")
    print (" ")
else:
    n_cells = int(sys.argv[1])
    n_node = int(sys.argv[2])
    n_vtk = int(sys.argv[3])
    steps_vtk = int(sys.argv[4])

    for j in range(0, n_vtk):
        cycle = j * steps_vtk
        # cells
        for k in range(0, n_cells):
            out_file = open("cell" + str(k) + "_" + str(cycle) + ".vtk", "a")
            out_file.write("POINT_DATA " + str(n_node) + "\n")
            out_file.write("SCALARS red float 1\n")
            out_file.write("LOOKUP_TABLE default\n")
            for i in range(0, n_node):
                out_file.write("1.0\n")
            out_file.close()