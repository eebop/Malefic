import os
def gen_file(old_file_data, new_file_data_as_str, old_file_name):
    not_same = old_file_data != new_file_data_as_str
    if not os.path.exists(old_file_name + '.original') and not_same:
        os.system(f'mv {old_file_name} {old_file_name + ".original"}')
        with open(old_file_name, 'w') as f:
            f.write(new_file_data_as_str)


def format_prog(list_to_format):
    out = ''
    for line in list_to_format:
        out = out + ' '.join(line) + '\n'
    return out
