"""
Entry point for File Server project
"""

import sys
from file_server import File, FileServerError


if __name__ == '__main__':

    PROMPT = "------======##########======------"
    print ("Welcome to File server v0.1")
    print (PROMPT)
    try:
        CWD = File.chg_dir()
        print ("Currently you are here:\n" + CWD)
    except FileServerError as err:
        print (err)


    while True:
        print (PROMPT)
        inp = input("""Please Enter desired action:
 1 - list files
 2 - create file
 3 - read file
 4 - see file metadata
 5 - delete file
 6 - Exit\n""")

        if inp == "6":
            print ("Thank you for using our service! Good bye.")
            exit(0)

        print (PROMPT)
        try:
            if inp == "1":
                for filename in File.list_files():
                    print (filename)
            elif inp == "2":
                print ("Please Enter file contents. To stop entering data " \
                                    "send EOF signal (Ctrl+Z or Ctrl+D)")
                data = sys.stdin.read()
                filename = File.create_file(data)
            elif inp == "3":
                filename = input("Please Enter file name to read: ")
                print ("File contents:")
                print (File.read_file(filename))
            elif inp == "4":
                filename = input("Please Enter file name to see: ")
                print ("File metadata:")
                print (File.get_metadata(filename))
            elif inp == "5":
                filename = input("Please Enter file name to remove: ")
                confirm = input(
                    "Really remove: {}? Y/N ".format(filename)
                ).upper().strip()
                if confirm == "Y":
                    File.del_file(filename)
        except FileServerError as err:
            print ("Error occured: " + str(err))
