import argparse
import os
import subprocess
import time


def run_bash_script(project_dir_path=None):
    # if not os.path.isdir(project_dir_path):
    #     exit(f'Please enter a valid path of a dir: {project_dir_path}')

    bash_commands = [
        # f"cd {project_dir_path}",
        "virtualenv -p /usr/bin/python3.7 newenv",
        "source newenv/bin/activate.csh",
        "module load bioinfo",
        "module load pymol",
        "pip install -r requirements.txt",
    ]
    for bash_command in bash_commands:
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()
        print(output)
        if error:
            print(f'an Error occurred for running "{bash_command}", PyMol image may not work: {error}')
        time.sleep(3)
    print('Done creating env!')


if __name__ == "__main__":
    """
       receives path to a Nb fasta file and a path to a trained neural network and creates a pdb file (Ca only) 
       according to the network prediction. the output file name is: "<fasta file name>_nanonet_ca.pdb"
    """

    # parser = argparse.ArgumentParser()
    # parser.add_argument("project_dir_path", help="The path into the dir where the project is located", default="./")

    # args = parser.parse_args()
    # run_bash_script(project_dir_path=args.project_dir_path)
    run_bash_script(project_dir_path=None)
