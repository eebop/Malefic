import os
def gen_file(old_file_name, new_file_data_as_str):
    with open(old_file_name, 'r') as f:
        not_same = f.read() != new_file_data_as_str
    if not os.exists(old_file_name + '.original') and not_same:
        os.system(f'mv {old_file_name} {old_file_name + ".original"}')
        with open(old_file_name, 'w') as f:
            f.write(new_file_data_as_str)
