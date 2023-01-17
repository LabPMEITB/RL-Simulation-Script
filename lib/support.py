"""
PROGRAMMER  : ANDI MUHAMMAD RIYADHUS ILMY
CREATE DATE : 2022/11/30 10:18
DESCRIPTION : Library for support functions
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

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

def scan_maze(mazeDir):
    """
    Scan all available maze config files
    """
    # Print intial status
    print(f'Scanning Maze Config File...')
    # Get list of maze config available in the folder
    mazeFiles = os.listdir(mazeDir)

    # Sort file
    mazeFiles.sort()
    
    # Filter files to individual and set conviguration lists
    mazeConfigList = []
    setConfigList = []
    for file in mazeFiles:
        extension = os.path.splitext(file)[1]
        if (extension == ".txt"):
            mazeConfigList.append(file)
        else:
            setConfigList.append(file)

    # Print scan results
    print("\t%d maze config file(s) found."% len(mazeConfigList))
    print("\t%d maze config set(s) found."% len(setConfigList))
    print('Scanning finished.')

    return mazeFiles

def select_maze(mazeDir):
    # Scan maze config files
    mazeConfigs = scan_maze(mazeDir)
    
    # Check if config files exist
    if len(mazeConfigs)==0:
        print('No available config file.')
        return None
    else:
        # Print all available configs
        print('List of available maze configs:')
        for config in mazeConfigs:
            idx = mazeConfigs.index(config) + 1
            print(f'\t{idx}) {config}')
            
        # Request user to select maze config
        print('Please choose maze configuration file!')
        loop = True
        while(loop):
            idx = int(input('\tInput Select Index (1-%d) : '%(len(mazeConfigs))))-1
            if ((0 <= idx) and (idx < len(mazeConfigs))):
                loop = False
                selectedMazeConfig = mazeConfigs[idx]
                print("\tSelected '%s'"% selectedMazeConfig)
            else:
                print('\tInput out of range. Please try again.')
        return selectedMazeConfig

def load_mazeConfig(mazeDir, configFile, TAB=''):
    """
    Read and separate data from config file to a list.
    """
    # Check config file, different behavior for maze set.
    print(f'{TAB}Reading Config File...')
    configTarget = os.path.join(mazeDir, configFile)
    if os.path.isdir(configTarget):
        # Config file is maze set
        print(f'{TAB}\tConfig file contain multiple mazes.')
        mazeConfigs = os.listdir(configTarget)
        mazeConfigs.sort()
        print(f'{TAB}\t{len(mazeConfigs)} maze config files found:')
        configDataList = []
        for mazeConfig in mazeConfigs:
#             print(f'{TAB}\t\t{mazeConfig}')
            fileTarget = os.path.join(configTarget, mazeConfig)
            configData = get_config_data(fileTarget, TAB=f'{TAB}\t\t')
            configDataList.append(configData)
        return configDataList
        
    elif os.path.isfile(configTarget):
        # Config file is a single maze configuration.
        print(f'{TAB}\tConfig file contain 1 maze.')
        print(f'{TAB}\tLoading maze config...')
        configData = get_config_data(configTarget, TAB=f'{TAB}\t\t')
        return [configData]
    else:
        # Config file is neither.
        print(f'{TAB}\tError: Not a config file or set.')

def get_config_data(configFile, TAB = ''):
    """
    Read and separate data from config file to a list.
    """
    # Read Maze config file
    with open(configFile, 'r') as f:
        print(f'{TAB}Loading "{configFile}"...')
        lines = f.readlines()
        totalLine = len(lines)
        print(f'{TAB}\tFile consists of {totalLine} lines of data.')
        f.close()
        
    # Load Maze Size
    mazeX = int(lines[0])
    mazeY = int(lines[1])
    totalState = mazeX * mazeY
    print(f'{TAB}\tMaze size loaded. {mazeX}X{mazeY} ({totalState} states)')

    # Load total action
    totalAct = int(lines[2])
    print(f'{TAB}\tNumber of action loaded. There are {totalAct} actions')

    # Load Next State list
    NSList = [[0] * totalAct for i in range(totalState)]
    for i in range(totalState):
        x = lines[3+i].split(';')
        x.remove('\n')
        for j in range(totalAct):
            NSList[i][j] = int(x[j])
    print(f'{TAB}\tNext State list loaded.')

    # Load Current Reward List
    RTList = [[0.0] * totalAct for i in range(totalState)]
    for i in range(totalState):
        x = lines[3+totalState+i].split(';')
        x.remove('\n')
        for j in range(totalAct):
            RTList[i][j] = float(x[j])
    print(f'{TAB}\tCurrent Reward list loaded.')
    print(f'{TAB}Finish loading "{configFile}"')
    
    # Create dictionary
    mazeDictionary = {'mX': mazeX, 
                      'mY': mazeY, 
                      'N': totalState, 
                      'Z': totalAct, 
                      'NS': NSList,
                      'RT': RTList}
    
    return mazeDictionary

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

def gen_maxMatrix(qTable):
    matrix = []
    for item in qTable:
        maxQ = max(item)
        act = np.argmax(item)
        # print(item)
        # print(maxQ)
        # print(act)
        matrix.append([maxQ, act])
    return matrix

def display_qTable(qTable, fsize=None, print_val=True, gen_file=None, show=True):
    """
    Function to display the Q-Table as a heatmap. Also save the heatmap as 
    a file.
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
    
    ## Show the plot if configured
    if show:
        plt.show()
    else:
        plt.close()

    ## Save the resulting image
    if gen_file:
        file_dir = os.path.join(gen_file, 'q_table.png')
        plt.savefig(file_dir, dpi=300, bbox_inches='tight')
        print(f"Saved 'q_table.png' to '{gen_file}'")
        
    return None

def plot(dat, fsize=(20,5), gen_file=None, show=True, title=None, xlabel="", ylabel=""):
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
    if title:
        plt.title(title)
        filename = f'{title}.png'
    else:
        filename = './temp/graph.png'

    ## Show the plot if configured
    if show:
        plt.show()
    else:
        plt.close()

    ## Save the resulting image
    if gen_file:
        file_dir = os.path.join(gen_file, filename)
        plt.savefig(file_dir, dpi=300, edgecolor='white', facecolor='white', bbox_inches='tight')
        print(f"Saved '{filename}' to '{gen_file}'")
    
    return None

def vis_svc(svc_arr, gen_file=None, show=True, title="State Visit Count"):
    x, y = svc_arr.shape
    plt.figure(figsize=(x,y))
    plt.imshow(svc_arr, interpolation='none')
    for i in range(x):
        for j in range(y):
            plt.text(j, i, f'S{j+i*x}', ha='center', va='center', color='lightgray', weight='bold', fontsize=20)
            plt.text(j, i, f'{int(svc_arr[i, j])}', ha='center', va='center', color='black', weight='bold', fontsize=10)
    plt.title(title)
    
    ## Save the resulting image
    if gen_file:
        file_dir = os.path.join(gen_file,'svc.png')
        plt.savefig(file_dir, dpi=300)
        print(f"Saved 'svc.png' to '{gen_file}'")
    
    ## Show the plot if configured
    if show:
        plt.show()
    else:
        plt.close()
    
    return None

def write_result_summary(filename, content, target_dir=None, quiet=False):
    # Initialize file content
    file_content = ""

    # Write Content
    for item in content:
        file_content += f"[{item[0]}]\n"
        for dat in item[1]:
            file_content += f"{dat[0]} = {dat[1]}\n"
    
    ## Generate Target File
    if target_dir:
        target_file = os.path.join(target_dir, filename)
    else:
        target_file = filename
    
    ## Open and write to file
    with open(target_file, 'w') as f:
        ## Write data to the file
        f.write(file_content)
    
        ## Close the file
        f.close()
    
    ## Print Status message
    if not(quiet):
        print(f"File '{filename}' generated and saved to '{target_dir}'")

    return None

def gen_save_folder(dir, status=False):
    """
        Function to generate save folder.
    """
    ## Create save subfolder directories
    save_subfolder = ['raw_data', 'shortest_path_test', 'qMatrix_change']
    for subfolder in save_subfolder:
        path = os.path.join(dir, subfolder)
        if status: print(f'CREATING {path}')
        os.mkdir(path)

    return None

def gen_save_dir(result_path, total_run, status=False):
    """
        Function to generate run result folder based on the run mode. This 
        function return the list of the folder directories.
    """
    ## Define run_mode
    if total_run == 1:
        run_mode = 'idv'
    else:
        run_mode = 'set'

    ## Create run results folder based on run mode
    run_result_folder = f'{run_mode}_runs'
    run_results_path = os.path.join(result_path, run_result_folder)
    if os.path.isdir(run_results_path):
        if status: print(f'UPDATING {run_results_path}')
    else:
        if status: print(f'CREATING {run_results_path}')
        os.mkdir(run_results_path)
    
    ## Get the current date
    today = date.today()
    current_date = today.strftime("%y%m%d")

    ## Generate a new save folder
    idx = 0
    save_folder = f'{current_date}_{run_mode}{idx}'
    save_path = os.path.join(run_results_path, save_folder)
    while os.path.isdir(save_path):
        idx += 1
        save_folder = f'{current_date}_{run_mode}{idx}'
        save_path = os.path.join(run_results_path, save_folder)
    if status: print(f'CREATING {save_path}')
    os.mkdir(save_path)

    ## Check if run_mode is 'set'
    if run_mode=='set':
        ## Generate save folder for eact test case
        for i in range(total_run):
            run_folder = f'run_{i}'
            run_folder_path = os.path.join(save_path, run_folder)
            if status: print(f'CREATING {run_folder_path}')
            os.mkdir(run_folder_path)

            ## Create subfolder directories in the save folder
            gen_save_folder(run_folder_path, status=status)
            # for dir in subdirs:
            #     return_list.append(dir)
    else:
        ## Create subfolder directories in the save folder
        gen_save_folder(save_path, status=status)

    return save_path