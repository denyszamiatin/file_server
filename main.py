"""
Entry point for File Server project
"""

import sys
import file_srv


if __name__ == '__main__':

    PROMPT = "------======##########======------"
    print "Welcome to File server v0.1"
    print PROMPT
    try:
        CWD = file_srv.chg_dir()
        print "Currently you are here:\n" + CWD
    except file_srv.FileServerError as err:
        print err


    while True:
        print PROMPT
        inp = raw_input("""Please Enter desired action:
 1 - list files
 2 - create file
 3 - read file
 4 - see file metadata
 5 - delete file
 6 - Exit\n""")

        if inp == "6":
            print "Thank you for using our service! Good bye."
            exit(0)

        print PROMPT
        try:
            if inp == "1":
                for filename in file_srv.list_files():
                    print filename
            elif inp == "2":
                print "Please Enter file contents. To stop entering data " \
                    "send EOF signal (Ctrl+Z or Ctrl+D)"
                data = sys.stdin.read()
                filename = file_srv.create_file(data)
            elif inp == "3":
                filename = raw_input("Please Enter file name to read: ")
                print "File contents:"
                print file_srv.read_file(filename)
            elif inp == "4":
                filename = raw_input("Please Enter file name to see: ")
                print "File metadata:"
                print file_srv.get_metadata(filename)
            elif inp == "5":
                filename = raw_input("Please Enter file name to remove: ")
                confirm = raw_input(
                    "Really remove: {}? Y/N ".format(filename)
                ).upper().strip()
                if confirm == "Y":
                    file_srv.del_file(filename)
        except file_srv.FileServerError as err:
            print "Error occured: " + str(err)
