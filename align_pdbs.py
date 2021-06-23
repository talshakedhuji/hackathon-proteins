import os
import pymolPy3
import platform


def create_pdb_img(ref_pdb_path, target_pdb_path, out_path_dir):
    if platform.system() == 'Linux':
        try:
            pm = pymolPy3.pymolPy3()
            target_file_name = os.path.basename(target_pdb_path)
            ref_file_name = os.path.basename(ref_pdb_path)
            # Run commands
            pm(f"load {ref_pdb_path}")
            pm(f"load {target_pdb_path}")
            pm(f"align {target_file_name}, {ref_file_name}")
            pm(f"png {out_path_dir}/align_img")
        except Exception as e:
            pass

    else:
        print("Only work with Linux, sorry :/")


# create_pdb_img(ref_pdb_path="/Users/tal/Documents/proteins_76562/ex4/6dlb_re.pdb",
#                target_pdb_path="Users/tal/Documents/proteins_76562/ex4/created_re.pdb",
#                out_path_dir="/Users/tal/Documents/proteins_76562/ex4")