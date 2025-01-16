import subprocess
import argparse
import os
import fnmatch
import shutil
# from selenium.webdriver.common.keys import Keys 
# from selenium.webdriver.common.by import By    

def check_and_create_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' has been created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def get_path(*args):
    arguments = [str(item) for item in list(args)] 
    ans = '/'.join(arguments)
    return ans

def get_prefix_path(*args):
    arguments = [str(item) for item in list(args)] 
    ans = '-'.join(arguments)
    return ans



def command_benmark_of_caching(server=None, port=None, connection=10, number=10, ratio = "1:0", measure = 1, thread = 1):
  argument_of_command = []
  if(server == None):
    raise ValueError("Server is required") 
  argument_of_command.append(f'-s {server}')

  if(port == None):
    raise ValueError("Port is required")
  argument_of_command.append(f'-p {port}')
  prefix_file = get_prefix_path(server, port, measure) 
  argument_of_command.append(f'--hdr-file-prefix {prefix_file}')
  argument_of_command.append(' --distinct-client-seed --hide-histogram')
  argument_of_command.append(f'-t {thread}')

  if connection == None:
    connection = 10
  argument_of_command.append(f'-c {connection}') 

  if number == None: 
    number = 100
  argument_of_command.append(f'-n {number}') 

  if ratio == None: 
    ratio = "1:0"
  argument_of_command.append(f'--ratio {ratio}')

  command = 'memtier_benchmark ' +  ' '.join(argument_of_command) 
  print(f"Running with command line \n{command}")
  result = subprocess.run(command, shell=True, text=True, capture_output=True) 


def export_data_to_histogram():
  print('export data to histogram')

def execute_task_in_directory(target_path, task, *args, **kwargs):
    # Save the current working directory
    original_path = os.getcwd()
    
    try:
        # Change to the target directory
        os.chdir(target_path)
        
        # Execute the provided task
        task(*args, **kwargs)  # Call the task function
        
    finally:
        # Change back to the original directory
        os.chdir(original_path)

def find_and_copy_hgrm_files(source_directory, target_directory):
    # Ensure the target directory exists
    os.makedirs(target_directory, exist_ok=True)
    print('calling source directory', source_directory)
    # Find and copy .hgrm files
    for dirpath, dirnames, filenames in os.walk(source_directory):
        for filename in fnmatch.filter(filenames, '*.txt'):
            source_file = os.path.join(dirpath, filename)
            prefixes = ["GET", "SET", "FULL_RUN"]
            for prefix in prefixes:
               if(source_file.find(prefix) != -1):
                  target_directory_type = f"{target_directory}/{prefix}"
                  check_and_create_folder(target_directory_type)
                  shutil.copy(source_file, target_directory_type)
                  print(f"Copied: {source_file} to {target_directory_type}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that adds 3 numbers from CMD"
    )

    parser.add_argument("--server", required=True, type=str, help = 'Entering url')
    parser.add_argument("--port", required=True, type=int, help = 'Entering port of server')
    parser.add_argument("--connection", required=False, type=int, help = 'Entering port of server')
    parser.add_argument("--number", required=False, type=int, help = 'Entering port of server')
    parser.add_argument("--measure", required=False, type=int, help = 'Entering the number of measure')
    parser.add_argument("--ratio", required=False, type=str, help = 'Entering Set:Get ratio (default: 1:10)')
    parser.add_argument("--thread", required=False, type=str, help = 'Entering Thread to Run')
     
    
    args = parser.parse_args()    
    measure = args.measure
    server = args.server
    port = args.port
    ratio = args.ratio
    connection = args.connection
    number = args.number
    thread = args.thread

    if measure == None:
      measure = 1

    if thread == None:
      thread = 1


    #execute the benchmark of redis
    index = 1
    while index <= measure: 
      print(f'Starting the {index} calculation')
      path = get_path('log', server, port, ratio, connection, number, index)
      check_and_create_folder(path)
      execute_task_in_directory(path, command_benmark_of_caching, server, port, connection, number, ratio, index, thread)
      print(f'End the {index} calculation')
      index = index + 1

      source_directory = os.getcwd() + f"/{get_path( 'log', server, port, ratio,connection, number)}/"
      target_directory = os.getcwd() + f"/results/{get_path(server, port, ratio, connection, number)}/"
      # group data to check stable caching performance
      find_and_copy_hgrm_files(source_directory, target_directory) 