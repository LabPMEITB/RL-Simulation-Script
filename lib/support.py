"""
PROGRAMMER  : ANDI MUHAMMAD RIYADHUS ILMY
CREATE DATE : 2022/11/30 10:18
DESCRIPTION : Library for support functions
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def gen_path(c_dir, target_file):
    """
    Generate path to a target file in a directory. If the file does not 
    exist then a new file is generated. 
    """
    # Create path to sub directory
    generated_path = os.path.join(c_dir, target_file)
    
    # Check if subdirectory exist. If doesn't exist generate new one.
    if os.path.isdir(generated_path)==False:
        print(f"File '{target_file}' does not exist in '{c_dir}'. A new file named '{target_file}' is created.")
        os.mkdir(generated_path)
    else:
        print(f"File '{target_file}' exist in '{c_dir}'")

    # Return the generated path  
    return generated_path

def scan_maze(maze_dir):
    """
    Scan all available maze config files
    """
    # Get list of maze config available in the folder
    maze_files = os.listdir(maze_dir)

    # Sort file
    maze_files.sort()
    
    # Filter to only bitstream files
    mazeConfig_list = []
    for file in maze_files:
        extension = os.path.splitext(file)[1]
        if (extension == ".txt"):
            mazeConfig_list.append(file)

    # Print all maze configuration files
    print("%d maze cofing file(s) detected."% len(mazeConfig_list))
    for file in mazeConfig_list:
        idx = mazeConfig_list.index(file) + 1
        print("%d) %s"% (idx, file))
    
    return mazeConfig_list

def select_maze(maze_dir):
    # Scan maze config files
    mazeConfig_list = scan_maze(maze_dir)
    if len(mazeConfig_list)==0:
        print('No available config file.')
        return None
    else:
        loop = True
        while(loop):
            idx = int(input('\nInput Select Index (1-%d) : '%(len(mazeConfig_list))))-1
            if ((0 <= idx) and (idx < len(mazeConfig_list))):
                loop = False
                selected_mazeConfig = mazeConfig_list[idx]
                print("\nSelected '%s'"% selected_mazeConfig)
            else:
                print('Input out of range. Please try again.')
        return selected_mazeConfig

def load_mazeConfig(maze_dir, config_file):
    """
    Read and separate data from config file to a list.
    """
    # Read Maze config file
    config_target = os.path.join(maze_dir, config_file)
    with open(config_target, 'r') as f:
        print(f'Loading {config_file}...')
        lines = f.readlines()
        total_line = len(lines)
        print(f'\tFile consists of {total_line} lines of data.')
        f.close()
        
    # Load Maze Size
    maze_x = int(lines[0])
    maze_y = int(lines[1])
    total_state = maze_x * maze_y
    print(f'\tMaze size loaded. {maze_x}X{maze_y} ({total_state} states)')

    # Load total action
    total_act = int(lines[2])
    print(f'\tNumber of action loaded. There are {total_act} actions')

    # Load Next State list
    NS_list = [[0] * total_act for i in range(total_state)]
    for i in range(total_state):
        x = lines[3+i].split(';')
        x.remove('\n')
        for j in range(total_act):
            NS_list[i][j] = int(x[j])
    print('\tNext State list loaded.')

    # Load Current Reward List
    RT_list = [[0.0] * total_act for i in range(total_state)]
    for i in range(total_state):
        x = lines[3+total_state+i].split(';')
        x.remove('\n')
        for j in range(total_act):
            RT_list[i][j] = float(x[j])
    print('\tCurrent Reward list loaded.')
    print(f'Finish loading {config_file}')
    
    return maze_x, maze_y, total_state, total_act, NS_list, RT_list

def draw_maze(height, maze_x, maze_y, ns_list, filename):
    """Write an SVG image of the maze to filename."""

    aspect_ratio = maze_x / maze_y
    # Pad the maze all around by this amount.
    padding = 10
    # Height and width of the maze image (excluding padding), in pixels
    width = int(height * aspect_ratio)
    # Scaling factors mapping maze coordinates to image coordinates
    scy, scx = height / maze_y, width / maze_x
    # Font size for texts
    font_size = scy/5

    def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
        """Write a single wall to the SVG image file handle f."""

        print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

    def write_coords(wc_f, maze_x, wc_x, wc_y, wc_tx, wc_ty):
        """Write a state coordinate to the SVG image file handle f."""
        state_number = wc_tx+(wc_ty*maze_x)
        print('<text x="{}" y="{}" class="small">S{}</text>'.format(wc_x, wc_y, state_number), file=wc_f)

    def draw_arrow(wc_f, x1, y1, x2, y2):
        """Write arrow dircetion based on the given action on the state coordinate to the SVG image file handle f."""
        print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="4" marker-end="url(#arrow)" />', file=wc_f)

    # Write the SVG image file for maze
    with open(filename, 'w') as f:
        # SVG preamble and styles.
        print('<?xml version="1.0" encoding="utf-8"?>', file=f)
        print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
        print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
        print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                .format(width + 2 * padding, height + 2 * padding,
                        -padding, -padding, width + 2 * padding, height + 2 * padding),
                file=f)
        print('<defs>', file=f)
        print('<style type="text/css"><![CDATA[', file=f)
        print('line {', file=f)
        print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
        print('    stroke-width: 4;\n}', file=f)
        print(']]>', file=f)
        print('.small {{ font: bold {}px sans-serif;'.format(font_size), file=f)
        print('         fill: lightgray; }}', file=f)
        print('</style>', file=f)
        # Add arrow
        print('<marker id="arrow" markerWidth="10" markerHeight="7" refX="0" refY="2" orient="auto">', file=f)
        print('\t<polygon points="0 0, 4 2, 0 4" />', file=f)
        print('</marker>', file=f)
        print('</defs>', file=f)

        # Draw layout square
        for x in range(maze_x):
            for y in range(maze_y):
                print(f'<rect x="{x*scx}" y="{y*scy}" width="{scx}" height="{scy}" fill="none" stroke="gray" stroke-width="1"/>', file = f)
        print('',file=f)

        # Draw State Coordinates
        for x in range(maze_x):
            for y in range(maze_y):
                wx, wy = (x+0.1)*scx, (y+0.3)*scy
                write_coords(f, maze_x, wx, wy, x, y)
        print('',file=f)

        # Draw the "South" and "East" walls of each cell, if present (these
        # are the "North" and "West" walls of a neighbouring cell in
        # general, of course).
        for x in range(maze_x):
            for y in range(maze_y):
                st = x+(y*maze_x)
                if ns_list[st][0]==st:
                    x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                    write_wall(f, x1, y1, x2, y2)

                if ns_list[st][1]==st:
                    x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                    write_wall(f, x1, y1, x2, y2)
        print('',file=f)

        # Draw the North and West maze border, which won't have been drawn
        # by the procedure above.
        print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
        print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
        print('</svg>', file=f)

def find_goals(ns_list):
    """
    Find all possible goal state (dead end state) in a generated maze. Dead
    end states have only one next state that is not its own state.
    """
    length = len(ns_list)
    possible_goals = []
    for i in range(length):
        count = 0
        for ns in ns_list[i]:
            if (ns == i):
                count +=1
        if (count == 3):
            possible_goals.append(i)
    return possible_goals

def display_qTable(qTable, fsize=None, print_val=True, gen_file=False, show=True):
    """
        Function to display the Q-Table as a heatmap. Also save the heatmap as a file.
    """
    
    # Determine the number of heatmap to be shown
    q_table = qTable
    n_state, n_act = q_table.shape
    
    if (n_state > 25):
        n_rows = 25
        n_graph = n_state//n_rows
        extra = n_state%25
        if extra:
            n_graph +=1
        print(extra)
    else:
        n_graph = 1
        n_rows = n_state
        extra = 0
        
    # Set the size of the plots
    if (fsize==None):
        width = 5*n_graph
        height = width*4
        plt.figure(figsize=(width, height))
    else:
        plt.figure(figsize=fsize)
    # Divide the Q-table into four separate graphs, each containing 25 states
    for i in range(n_graph):
        plt.subplot(1, n_graph, i+1)
        plt.imshow(q_table[i*n_rows:(i+1)*n_rows, :], cmap="RdYlGn")

        # Add x-axis labels for each action direction at the top of the plot
        if (n_act == 4):
            plt.xticks(range(n_act), ["Down", "Right", "Left", "Up"])

        # Add y-axis labels for each state, prefixed with 'S'
        plt.yticks(range(n_rows), [f"S{i*n_rows+j}" for j in range(n_rows)])

        # Overlay the Q-values on top of the heatmap
        if print_val:
            if extra and i == n_graph - 1:
                n_rows = extra
            for j in range(n_rows):
                for k in range(n_act):
                        text = plt.text(k, j, f"{q_table[i*n_rows+j, k]:.3f}", ha="center", va="center", color="k", weight="bold", fontsize=10)

    # Save the resulting image
    if gen_file:
        plt.savefig("q_table.png", dpi=300)
             
    if show:
        plt.show()
    else:
        plt.close()

    return None

def plot(dat, fsize=(20,5), gen_file=False, show=True, title="", xlabel="", ylabel=""):
    """
        Function to plot a graph. The generated plot can be saved as a picture.
    """
    # Set the size of the plots
    plt.figure(figsize=fsize)

    # Plot the points
    x = len(dat)
    plt.plot(dat)

    # Set the x axis
    plt.xlabel(xlabel)
    # Set the y axis
    plt.ylabel(ylabel)

    # Set the title
    plt.title(title)

    # Save the resulting image
    if gen_file:
        plt.savefig('graph.png', dpi=300, edgecolor='white', facecolor='white', bbox_inches='tight')
        # plt.savefig("graph.png", dpi=300, )

    # Show the plot if configured
    if show:
        plt.show()
    else:
        plt.close()
    
    return None

def vis_svc(svc_arr, gen_file=False, show=True, title=""):
    x, y = svc_arr.shape
    plt.figure(figsize=(x,y))
    plt.imshow(svc_arr, interpolation='none')
    for i in range(x):
        for j in range(y):
            plt.text(j, i, f'S{j+i*x}', ha='center', va='center', color='lightgray', weight='bold', fontsize=20)
            plt.text(j, i, f'{int(svc_arr[i, j])}', ha='center', va='center', color='black', weight='bold', fontsize=10)
    plt.title(title)
    
    # Save the resulting image
    if gen_file:
        plt.savefig('svc.png', dpi=300)
    
    # Show the plot if configured
    if show:
        plt.show()
    else:
        plt.close()