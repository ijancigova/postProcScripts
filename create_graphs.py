import numpy as np
import os, sys, shutil

# shutil.rmtree("/work/zujancigova/simulations/output/sim" + str(sim_no))

for k in range(0,61):
    # creation of folder structure
    directory = "output_cluster/sim"+str(k)
    os.makedirs(directory + "/gnuplot")

    # writing gnuplot script for fluid velocity
    scriptName = directory + "/gnuplot/fluid_vel.gnuplot"
    out_file = open(scriptName, "w")
    out_file.write("set terminal postscript enhanced eps color\n")
    out_file.write("set output \"output_cluster/sim" + str(k) +"/gnuplot/fluid_vel.eps\"\n")
    out_file.write("set title \"Fluid velocity at four points, x-coordinates\"\n")
    out_file.write("set xlabel \"t [{/Symbol m}s]\"\n")
    out_file.write("set ylabel \"v [m/s]\"\n")
    out_file.write("set size 1, 1\n")
    out_file.write("set origin 0, 0\n")
    out_file.write("set key bottom center\n")
    out_file.write("set key samplen 2 spacing 1 font \",15\"\n")
    out_file.write("set yrange[0:0.002]\n")
    out_file.write("set xtics font \", 15\"\n")
    out_file.write("set ytics font \", 15\"\n")
    out_file.write("set xlabel font \", 15\"\n")
    out_file.write("set ylabel font \", 15\"\n")
    out_file.write("set title font \", 20\"\n")
    out_file.write("set border 3\n")
    out_file.write("set style line 1 lt rgb \"red\" lw 4\n")
    out_file.write("set style line 2 lt rgb \"black\" lw 4\n")
    out_file.write("set style line 3 lt rgb \"brown\" lw 4\n")
    out_file.write("set style line 4 lt rgb \"orange\" lw 4\n")
    out_file.write("\n")
    out_file.write("plot \"output_cluster/sim" + str(k) + "/fluid_vel.txt\" using 1:2 title \"primary left\" with lines ls 1, \\\n")
    out_file.write("    \"output_cluster/sim" + str(k) + "/fluid_vel.txt\" using 1:3 title \"wider branch\" with lines ls 2, \\\n")
    out_file.write("    \"output_cluster/sim" + str(k) + "/fluid_vel.txt\" using 1:4 title \"narrow branch\" with lines ls 3, \\\n")
    out_file.write("    \"output_cluster/sim" + str(k) + "/fluid_vel.txt\" using 1:5 title \"primary right\" with lines ls 4 \n")
    out_file.close()

    # run the gnuplot script
    os.system("gnuplot " + scriptName)