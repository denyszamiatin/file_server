import os
import time
import util
import config


class FileServerError(Exception):
    pass


def handle_os_error(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (OSError, IOError) as e:
            raise FileServerError(str(e))
    return wrapper


@handle_os_error
def chg_dir():
    working_dir = config.get_working_dir()
    if not os.path.isdir(working_dir):
        os.mkdir(working_dir)
    os.chdir(working_dir)
    return os.getcwd()
    

@handle_os_error
def create_file(data):
    fname = util.get_random_name()
    with open(fname, "wb") as f:
        f.write(data)
    return fname


@handle_os_error
def del_file(filename):
        os.remove(filename)


@handle_os_error
def read_file(filename):
        with open(filename, "r") as f:
            return f.read()


@handle_os_error
def get_metadata(filename):
        md = os.stat(filename)
        return {
            "size": md.st_size,
            "date": time.ctime(md.st_birthtime),
        }


@handle_os_error
def list_files():
        cwd = os.getcwd()
        return [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
