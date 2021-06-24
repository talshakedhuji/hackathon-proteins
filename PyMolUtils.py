import os
import pymolPy3
import platform
import subprocess

import os
import pymolPy3
import platform
import subprocess

def create_pdb_img(ref_pdb_path, target_pdb_path, out_path_dir):
    if platform.system() == 'Linux':
        try:
            # Run command install
            try:
                test = subprocess.Popen(["module load bioinfo",
                                         "module load pymol"], stdout=subprocess.PIPE)
                output = test.communicate()[0]
                print(f'cmd command output: {output}')
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

            if not (target_pdb_path.endswith('.pdb')):
                print(f"Error - Target PDB isn't of type .pdb")
                return
            if not (os.path.isfile(target_pdb_path)):
                print(f"Error - Target PDB file isn't found, please verify path: {target_pdb_path}")
                return

            pm = pymolPy3.pymolPy3()
            target_file_name = os.path.basename(target_pdb_path)
            target_file_no_type = target_file_name.split(".")[0]
            ref_file_name = os.path.basename(ref_pdb_path)
            ref_file_no_type = ref_file_name.split(".")[0]
            # Run commands
            pm(f"load {ref_pdb_path}")
            pm(f"color yellow, {ref_file_no_type}")
            pm(f"load {target_pdb_path}")
            pm(f"color green, {target_file_no_type}")
            pm(f"align {ref_file_no_type}, {target_file_no_type}")
            pm(f"center")
            pm(f"zoom")
            pm(f"png {out_path_dir}/align_img")
            print(f"Done! the image is here: '{out_path_dir}/align_img.png'")

        except Exception as e:
            print(f'Failed creating image: {e}')

    else:
        print("Only work with Linux, sorry :/")

def test():
    output_directory = "./outputs"
    file1 = output_directory + "/original.pdb"
    file2 = output_directory + "/mutated_1.pdb"
    create_pdb_img(file1, file2, output_directory)

if __name__ == "__main__":
    output_directory = "./outputs"
    file1 = output_directory + "/original.pdb"
    file2 = output_directory + "/mutated_1.pdb"
    create_pdb_img(file1, file2, output_directory)
    create_pdb_img(file1, file2, output_directory)