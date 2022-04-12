import os
import shutil


def delete(dirname):
    path_to_dir = os.path.join(os.path.abspath(os.sep), 'Users', 'sologuboved', dirname)
    print(f"Path to {dirname}:", path_to_dir)
    del_ds_store(path_to_dir)
    for dirname in os.listdir(path_to_dir):
        path = os.path.join(path_to_dir, dirname)
        del_ds_store(path)
        del_pycache(path)


def del_ds_store(path):
    path = os.path.join(path, '.Ds_Store')
    try:
        os.remove(path)
    except FileNotFoundError as e:
        print(e)
    else:
        print(f"{path} deleted")


def del_pycache(path):
    path = os.path.join(path, '__pycache__')
    try:
        shutil.rmtree(path)
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    delete('scripts')
