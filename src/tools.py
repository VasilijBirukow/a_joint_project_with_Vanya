from os import path
from subprocess import CalledProcessError, run
from threading import Thread
from yaml import safe_load


def run_update_script(prefix_path):
    try:
        run(f'bash {prefix_path}/update.sh', shell=True, check=True)
    except CalledProcessError:
        pass


def run_restart_script(prefix_path):
    try:
        run(f'bash {prefix_path}/restart.sh', shell=True, check=True)
    except CalledProcessError:
        pass


def get_config_data(config_file_path=None):
    config_file_path = config_file_path if config_file_path else find_config_file('.', 'config.yaml')

    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        config_info = safe_load(config_file)

    return config_info


def find_config_file(start_dir, file_name):
    current_dir = path.abspath(start_dir)
    while True:
        file_path = path.join(current_dir, file_name)
        if path.exists(file_path):
            return file_path

        parent_dir = path.dirname(current_dir)
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    return None


def set_server_files(prefix_path):
    try:
        set_thread = Thread(target=run_set_script(prefix_path))
        set_thread.start()
        set_thread.join()

        restart_thread = Thread(target=run_restart_script(prefix_path))
        restart_thread.start()
        exit(0)

    except CalledProcessError:
        pass


def run_set_script(prefix_path):
    try:
        run(f'bash {prefix_path}/set.sh', shell=True, check=True)
    except CalledProcessError:
        pass
