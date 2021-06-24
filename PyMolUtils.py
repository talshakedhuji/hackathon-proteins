import os
import time
import pymolPy3
import platform
import subprocess

def create_pdb_img(ref_pdb_path, target_pdb_path_list, out_path_dir):
    if platform.system() == 'Linux':
        try:
            # Run command install
            try:
                run_bash_script()
            except Exception as e:
                print(f'Failed running commands, trying pymol anyway :) {e}')

            if not os.path.exists(out_path_dir):
                print(f"No dir in path '{out_path_dir}', trying to create one...")
                os.makedirs(out_path_dir)

            if not (ref_pdb_path.endswith('.pdb')):
                print(f"Error - Reference PDB isn't of type .pdb")
                return
            if not (os.path.isfile(ref_pdb_path)):
                print(f"Error - Reference PDB file isn't found, please verify path: {ref_pdb_path}")
                return

            ref_file_name = os.path.basename(ref_pdb_path)
            ref_file_no_type = ref_file_name.split(".")[0]
            pm = pymolPy3.pymolPy3()
            pm(f"load {ref_pdb_path}")
            pm(f"color yellow, {ref_file_no_type}")

            success_target_count = 0
            for target_pdb_path in target_pdb_path_list:
                if not ((os.path.isfile(target_pdb_path)) and target_pdb_path.endswith('.pdb')):
                    continue
                target_file_name = os.path.basename(target_pdb_path)
                target_file_no_type = target_file_name.split(".")[0]
                # Run commands
                pm(f"load {target_pdb_path}")
                pm(f"color green, {target_file_no_type}")
                pm(f"align {ref_file_no_type}, {target_file_no_type}")
                success_target_count += 1

            if not success_target_count:
                print(f"Error - could not find 1 Target PDB...")
                return

            pm(f"center")
            pm(f"zoom")
            pm(f"png {out_path_dir}/align_img")
            time.sleep(12)
            print(f"Done! the image is here: '{out_path_dir}/align_img.png'")
        except Exception as e:
            print(f'Failed creating image: {e}')

    else:
        print("Only work with Linux, sorry :/")



def run_bash_script():
    # Activate venv
    process = subprocess.Popen(['activate', 'virtual', 'env'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
    # install and load bioinfo
    process = subprocess.Popen(['pip', 'install', 'bioinfo'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
    process = subprocess.Popen(['module', 'load', 'bioinfo'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
    # install and load pymol
    process = subprocess.Popen(['pip', 'install', 'pymol'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
    process = subprocess.Popen(['module', 'load', 'pymol'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    print(stdout, stderr)
