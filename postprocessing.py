import numpy as np
import os


def norm(x, y, z):
    return np.sqrt(x*x+y*y+z*z)


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


branch = Enum(["NONE", "WIDER", "NARROW"])
directory = "output_cluster"
y_threshold = 36
x1_threshold = 40
x2_threshold = 110
entered = branch.NONE

out_file = open("rbc_distribution.txt", "w")
out_file.write(
    "sim_type perc_rbc_narrow_while_wbc_in perc_rbc_wider_while_wbc_in perc_rbc_narrow_while_wbc_out perc_rbc_wider_while_wbc_out n_rbc_while_wbc_in n_rbc_while_wbc_out n_rbc_narrow n_rbc_wider\n")
out_file.close()

out_file = open("rbc_mean_velocity.txt", "w")
out_file.write(
    "sim_type mean_vel_rbc_narrow_while_wbc_in mean_vel_rbc_wider_while_wbc_in mean_vel_rbc_narrow_while_wbc_out mean_vel_rbc_wider_while_wbc_out \n")
out_file.close()

out_file = open("rbc_mean_forces.txt", "w")
out_file.write(
    "sim_type mean_f_rbc_narrow_while_wbc_in mean_f_rbc_wider_while_wbc_in mean_f_rbc_narrow_while_wbc_out mean_f_rbc_wider_while_wbc_out \n")
out_file.close()

for j in range (0,6):

    rbc_narrow_while_wbc_in = 0
    rbc_wider_while_wbc_in = 0
    rbc_narrow_while_wbc_out = 0
    rbc_wider_while_wbc_out = 0

    mean_vel_rbc_narrow_while_wbc_in = 0
    mean_vel_rbc_wider_while_wbc_in = 0
    mean_vel_rbc_narrow_while_wbc_out = 0
    mean_vel_rbc_wider_while_wbc_out = 0

    mean_f_rbc_narrow_while_wbc_in = 0
    mean_f_rbc_wider_while_wbc_in = 0
    mean_f_rbc_narrow_while_wbc_out = 0
    mean_f_rbc_wider_while_wbc_out = 0

    for k in range(j*10+1,j*10+10):

        wbc_file = open(directory+"/sim"+str(k)+"/positions/wbc_pos.txt","r")
        wbc_positions = wbc_file.read().split("\n")
        wbc_file.close()
        wbc_positions = filter(None, wbc_positions)

        enter_branch = -1
        exit_branch = -1

        for line in wbc_positions:
            line = np.array([float(x) for x in line.split()])
            # wbc entered a branch
            if (line[1] > x1_threshold) and (enter_branch == -1):
                enter_branch = line[0]
            # wbc exited the branch
            if (line[1] > x2_threshold) and (exit_branch == -1):
                exit_branch = line[0]
            # was it the wider branch? (in case both are of the same width, this represents "lower" branch)
            if (line[1] > x1_threshold+20) and (entered == branch.NONE):
                if line[2] < y_threshold:
                    entered = branch.WIDER
                else:
                    entered = branch.NARROW

        if j < 3:
            ncells = 40
        else:
            ncells = 60

        for i in range(0,ncells):
            rbc_file = open(directory + "/sim" + str(k) + "/positions/rbc" + str(i) + "_pos.txt", "r")
            rbc_positions = rbc_file.read().split("\n")
            rbc_file.close()
            rbc_positions = filter(None, rbc_positions)

            rbc_file = open(directory + "/sim" + str(k) + "/velocities/rbc" + str(i) + "_vel.txt", "r")
            rbc_velocities = rbc_file.read().split("\n")
            rbc_file.close()
            rbc_velocities = filter(None, rbc_velocities)

            rbc_file = open(directory + "/sim" + str(k) + "/forces/rbc" + str(i) + "_force.txt", "r")
            rbc_forces = rbc_file.read().split("\n")
            rbc_file.close()
            rbc_forces = filter(None, rbc_forces)

            steps_in_branch1 = 0
            steps_in_branch2 = 0
            steps_in_branch3 = 0
            steps_in_branch4 = 0
            rbc_vel1 = 0
            rbc_vel2 = 0
            rbc_vel3 = 0
            rbc_vel4 = 0
            rbc_f1 = 0
            rbc_f2 = 0
            rbc_f3 = 0
            rbc_f4 = 0

            rbc_enter = -1
            previous_rbc_x = 150
            id = 0

            for linerbc in rbc_positions:

                # read corresponding lines from three datasets
                linerbc = np.array([float(x) for x in linerbc.split()])
                line_vel = np.array([float(x) for x in rbc_velocities[id].split()])
                line_f = np.array([float(x) for x in rbc_forces[id].split()])

                # determine when this rbc entered branch
                if (previous_rbc_x < x1_threshold) and (linerbc[1] > x1_threshold):
                    rbc_enter = linerbc[0]

                # rbc in narrow branch while wbc in branch (wbc will exit)
                if (linerbc[2] > y_threshold) and (rbc_enter > enter_branch) and (exit_branch > -1) and (rbc_enter < exit_branch):

                    if entered == branch.NARROW: # in these simulations wbc went up, so upper channel is considered "wider"
                        rbc_vel2 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f2 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch2 += 1
                    else:
                        rbc_vel1 += norm(line_vel[1],line_vel[2],line_vel[3])
                        rbc_f1 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch1 += 1

                    if linerbc[0] == rbc_enter + 5:  # I want to check this after the cell actually entered !!ONCE!!
                        rbc_narrow_while_wbc_in += 1

                # rbc in narrow branch while wbc in branch (wbc will not exit)
                elif (linerbc[2] > y_threshold) and (rbc_enter > enter_branch):

                    if entered == branch.NARROW:
                        rbc_vel2 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f2 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch2 += 1
                    else:
                        rbc_vel1 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f1 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch1 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_narrow_while_wbc_in += 1

                # rbc in wider branch while wbc in branch (wbc will exit)
                elif (linerbc[2] < y_threshold) and (rbc_enter > enter_branch) and (exit_branch > -1) and (rbc_enter < exit_branch):

                    if entered == branch.NARROW:
                        rbc_vel1 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f1 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch1 += 1
                    else:
                        rbc_vel2 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f2 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch2 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_wider_while_wbc_in += 1

                # rbc in wider branch while wbc in branch (wbc will not exit)
                elif (linerbc[2] < y_threshold) and (rbc_enter > enter_branch):

                    if entered == branch.NARROW:
                        rbc_vel1 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f1 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch1 += 1
                    else:
                        rbc_vel2 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f2 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch2 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_wider_while_wbc_in += 1

                # rbc in narrow branch while wbc in early wide
                elif (linerbc[2] > y_threshold) and (rbc_enter < enter_branch) and (enter_branch > -1):

                    if entered == branch.NARROW:
                        rbc_vel4 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f4 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch4 += 1
                    else:
                        rbc_vel3 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f3 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch3 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_narrow_while_wbc_out += 1

                # rbc in wider branch while wbc in early wide
                elif (linerbc[2] < y_threshold) and (rbc_enter < enter_branch) and (enter_branch > -1):

                    if entered == branch.NARROW:
                        rbc_vel3 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f3 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch3 += 1
                    else:
                        rbc_vel4 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f4 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch4 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_wider_while_wbc_out += 1

                # rbc in narrow branch while wbc in late wide
                elif (linerbc[2] > y_threshold) and (rbc_enter > exit_branch) and (exit_branch > -1):

                    if entered == branch.NARROW:
                        rbc_vel4 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f4 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch4 += 1
                    else:
                        rbc_vel3 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f3 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch3 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_narrow_while_wbc_out += 1

                # rbc in wider branch while wbc in late wide
                elif (linerbc[2] < y_threshold) and (rbc_enter > exit_branch) and (exit_branch > -1):

                    if entered == branch.NARROW:
                        rbc_vel3 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f3 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch3 += 1
                    else:
                        rbc_vel4 += norm(line_vel[1], line_vel[2], line_vel[3])
                        rbc_f4 += norm(line_f[1], line_f[2], line_f[3])
                        steps_in_branch4 += 1

                    if linerbc[0] == rbc_enter + 5:
                        rbc_wider_while_wbc_out += 1

                previous_rbc_x = linerbc[1]
                id += 1

            if steps_in_branch1 != 0:
                mean_vel_rbc_narrow_while_wbc_in += rbc_vel1 / steps_in_branch1
                mean_f_rbc_narrow_while_wbc_in += rbc_f1 / steps_in_branch1
            if steps_in_branch2 != 0:
                mean_vel_rbc_wider_while_wbc_in += rbc_vel2 / steps_in_branch2
                mean_f_rbc_wider_while_wbc_in += rbc_f2 / steps_in_branch2
            if steps_in_branch3 != 0:
                mean_vel_rbc_narrow_while_wbc_out += rbc_vel3 / steps_in_branch3
                mean_f_rbc_narrow_while_wbc_out += rbc_f3 / steps_in_branch3
            if steps_in_branch4 != 0:
                mean_vel_rbc_wider_while_wbc_out += rbc_vel4 / steps_in_branch4
                mean_f_rbc_wider_while_wbc_out += rbc_f4 / steps_in_branch4

    # number of cells in the narrow and wider channel
    rbc_while_wbc_in = rbc_wider_while_wbc_in + rbc_narrow_while_wbc_in
    rbc_while_wbc_out = rbc_wider_while_wbc_out + rbc_narrow_while_wbc_out

    switcher = {
        0: "A40",
        1: "B40",
        2: "C40",
        3: "A60",
        4: "B60",
        5: "C60"
    }

    out_file = open("rbc_distribution.txt", "a")
    out_file.write(switcher.get(j,"unknown") +" "+ str(rbc_narrow_while_wbc_in * 100.0 / rbc_while_wbc_in) + " " +
                   str(rbc_wider_while_wbc_in * 100.0 / rbc_while_wbc_in) + " " +
                   str(rbc_narrow_while_wbc_out * 100.0 / rbc_while_wbc_out) + " " +
                   str(rbc_wider_while_wbc_out * 100.0 / rbc_while_wbc_out) + " " +
                   str(rbc_while_wbc_in) + " " +
                   str(rbc_while_wbc_out) + " " +
                   str(rbc_narrow_while_wbc_in + rbc_narrow_while_wbc_out) + " " +
                   str(rbc_wider_while_wbc_in + rbc_wider_while_wbc_out) + "\n")

    out_file.close()

    # velocity: calculating the means from the sums and outputting them
    mean_vel_rbc_narrow_while_wbc_in /= rbc_narrow_while_wbc_in
    mean_vel_rbc_wider_while_wbc_in /= rbc_wider_while_wbc_in
    mean_vel_rbc_narrow_while_wbc_out /= rbc_narrow_while_wbc_out
    mean_vel_rbc_wider_while_wbc_out /= rbc_wider_while_wbc_out
    out_file = open("rbc_mean_velocity.txt", "a")
    out_file.write(switcher.get(j, "unknown") + " " + str(mean_vel_rbc_narrow_while_wbc_in) + " " +
                   str(mean_vel_rbc_wider_while_wbc_in) + " " +
                   str(mean_vel_rbc_narrow_while_wbc_out) + " " +
                   str(mean_vel_rbc_wider_while_wbc_out) + "\n")

    out_file.close()

    # forces: calculating the means from the sums and outputting them
    mean_f_rbc_narrow_while_wbc_in /= rbc_narrow_while_wbc_in
    mean_f_rbc_wider_while_wbc_in /= rbc_wider_while_wbc_in
    mean_f_rbc_narrow_while_wbc_out /= rbc_narrow_while_wbc_out
    mean_f_rbc_wider_while_wbc_out /= rbc_wider_while_wbc_out
    out_file = open("rbc_mean_forces.txt", "a")
    out_file.write(switcher.get(j, "unknown") + " " + str(mean_f_rbc_narrow_while_wbc_in) + " " +
                   str(mean_f_rbc_wider_while_wbc_in) + " " +
                   str(mean_f_rbc_narrow_while_wbc_out) + " " +
                   str(mean_f_rbc_wider_while_wbc_out) + "\n")

    out_file.close()