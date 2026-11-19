import sys
import os
import hashlib
import zlib


def main():
    # for i in range(len(sys.argv)):
    #     print(f'sys.argv[{i}] = {sys.argv[i]}')

    # TODO: create dict object to map files/args/types in the cmd

    # type = 
    # name = 
    dictionary = {
        'cmd': sys.argv[1] if len(sys.argv) > 1 else None,
        'arg': sys.argv[2] if len(sys.argv) > 2 else None,
        'obj': sys.argv[3] if len(sys.argv) > 3 else None,
    }

    cmd = dictionary['cmd']
        
    if cmd == 'init':
        init(dictionary)
    elif cmd == 'hash-object':
        if len(sys.argv) > 3:
            hash_object(dictionary)
    elif cmd == 'cat-file':
        if len(sys.argv) > 3:
            cat_file(dictionary)
    elif cmd == 'ls-tree':
        ls_tree(dictionary)
    elif cmd == 'write-tree':
        write_tree(dictionary)

def add_update_index(dictionary: dict) -> str:
    # TODO: git add & git update-index --add basically do the same thing
    # TODO: what is the format of the index file
    # TODO: what exactly is being indexed? the hash object? the file(s)?
    # TODO: COMING BACK TO THIS!!!!
    return ''

def write_tree(dictionary: dict) -> str:
    data = []
    # TODO: 1. loop over files and dirs in cwd
    for entry in os.scandir(os.getcwd()):
        if entry.is_file():
            create_blob_hash(entry.path)
            print(f'F - {entry}')
        if entry.is_dir():
            print(f'D - {entry.path}')
    
    # TODO: 2. if entry is file -> create blob object and record it's SHA-1 hash
    # TODO: 3. if entry is dir -> 
    return ''

def ls_tree(dictionary: dict) -> None:
    # TODO: help me please :3
    return

# TODO: implement cat file to get data from the generated blob objects
def cat_file(dictionary: dict) -> str:
    # TODO: find dir with [:2] hash object
    # TODO: once dir found then search for file name that matches [2:]
    # TODO: open that file and de-compress w/ zlib??? and print contents of file?
    obj = dictionary['obj']
    metadata = ''
    if exists_in_fs(os.getcwd(), obj[:2]):
        # print('I found a folder ....')
        os.chdir(navigate_to_directory(os.getcwd(), obj[:2]))
        # print(f'current directory: {os.getcwd()}')
        if exists_in_fs(os.getcwd(), obj[2:]):
            # print('I found the file!!!')
            with open(obj[2:], 'rb') as f:
                data = zlib.decompress(f.read())
                header, content = data.split(b'\0', 1)
                # print('header', header.decode('utf-8'))
                # print('content', content.decode('utf-8'))

                metadata = content.decode('utf-8')
                print(metadata, end='')
    else:
        print("Folder not found!") 

    return metadata

# TODO: need to store an object in the hash file in this format -> blob <size>\0contents
# TODO: zlib compress files python???
def hash_object(dictionary: dict) -> str:
    # TODO: generate sha-1 hash of file
    # TODO: how to deal with --stdin? (maybe don't worry about this for now)
    # TODO: ...
    # file_hash_str = '' # file hash string
    # file_hash = '' # file hash itself (the binary data)

    arg = dictionary['arg']
    obj = dictionary['obj']
    
    hash_obj, store = create_blob_hash(obj)

    if arg == "-w":
        dir = hash_obj[:2]
        # print(f'dir = {dir}')
        filename = hash_obj[2:]
        # print(f'filename = {filename}')
        # print(f'store = {store}')

        if not exists_in_fs(os.getcwd(), '.pygit'):
            os.chdir(navigate_to_directory(os.getcwd(), '.pygit'))
            print(os.getcwd())
            os.chdir('objects')
            os.mkdir(dir)
            os.chdir(dir)
            with open(filename, 'wb') as f:
                f.write(zlib.compress(store))

    print(hash_obj)
    return hash_obj

def create_blob_hash(filepath=''):
    print(f'opening this file ... {filepath}')
    with open(filepath, "rb") as f:
        data = f.read()
        header = f"blob {len(data)}\0".encode("utf-8")
        store = header + data
        hash = hashlib.sha1(store).hexdigest()

        print(hash)
        return hash, store

def exists_in_fs(curr_dir : str, search: str) -> bool:
    for root, dirs, files in os.walk(curr_dir):
        if search in dirs:
            return True
        elif search in files:
            return True
    return False

def navigate_to_directory(current_directory: str, search: str) -> str:
    full_path = ''
    for root, dirs, files in os.walk('.'):
            if search in dirs:
                full_path = os.path.abspath(os.path.join(root, search))
            
    return full_path

def init(dictionary : dict) -> None:
    # check to see if the .pygit folder exists somewhere
    name = dictionary['arg']

    if exists_in_fs(os.getcwd(), '.pygit'):
        print("PyGit folder already exists!")
        return    
    elif name:
        print(f'Initialized empty Git repository in {os.getcwd()}/{name}/.pygit')
        # create name directory and cd into it
        os.mkdir(name)
        os.chdir(name)
    else:
        print(f'Initialized empty Git repository in {os.getcwd()}/.pygit')

    # create pygit directory and cd into it
    os.mkdir('.pygit')
    os.chdir('.pygit')

    # create git folders in pygit folder
    os.mkdir('hooks')
    os.mkdir('info')
    os.mkdir('objects')
    os.mkdir('refs')

    # create files git files in <name> folder
    filenames = ['config', 'description', 'HEAD']
    for filename in filenames:
        with open(filename, 'w') as f:
            if filename == 'description':
                f.write(f"Unnamed repository; edit this file 'description' to name the repository.")
            elif filename == 'HEAD':
                f.write("ref: refs/heads/main\n")
            else: 
                # need to figure out how we want to write to config file since its multi-line
                pass

if __name__ == '__main__':
    main()