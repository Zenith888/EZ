import os
import bcrypt
import codecs
from cryptography.fernet import Fernet

def main():
    print("\n--- Main Menu ---\n")
    print("1. New\n2. Open\n3. Delete Note\n4. Reset Password\n5. Search\n6. Exit\n0. Reset All\n\n\n* 'exit()' to save and exit")
    define = ""
    Try = 0
    while define == "" or define != "1" or define != "2" or define != "3":
        Try += 1
        if Try == 1:
            define = input(": ")
            if define == "1":
                Newfile()
                break
            
            elif define == "2":
                Openfile()
                break
            
            elif define == "3":
                DeleteFile()
                break

            elif define == "4":
                file = open("1.txt","w")
                file.writelines("")
                file.close()
                file = open("2.txt", "w")
                file.writelines("0")
                file.close()
                print("PASSWORD RESET. Restart to enter new password\nPress 'Enter' to exit")
                input()
                exit()

            elif define == "5":
                Search()
                break

            elif define == "6" or define == "exit()":
                exit()
            elif define == "0":
                Reset()
                break
        else:
            define = input("Please Input a valid number (1, 2, 3, 4, 5, 6, 0): ")
            print(define)
            if define == "1":
                Newfile()
                break
            
            elif define == "2":
                Openfile()
                break
            
            elif define == "3":
                DeleteFile()
                break

            elif define == "4":
                file = open("1.txt","w")
                file.writelines("")
                file.close()
                file = open("2.txt", "w")
                file.writelines("0")
                file.close()
                print("PASSWORD RESET. Restart to enter new password\nPress 'Enter' to exit")
                input()
                exit()

            elif define == "5":
                Search()
                break

            elif define == "6" or define == "exit()":
                exit()
            elif define == "0":
                Reset()
                break

def Newfile():
    print("---- New File ----\n")
    FileName = input("""File Name (type "exit()" to return to main menu): """)
    if "\\" in FileName or "/" in FileName or ":" in FileName or "*" in FileName or "?" in FileName or '"' in FileName or "<" in FileName or ">" in FileName or "|" in FileName:
        print('File name cannot contain these characters: \\ / : * ? " < > |')
        input("Press Enter to retry\n")
        Newfile()
        
    else:
        if FileName == "exit()":
            main()
        FileName = FileName + ".txt"
        Check = Checkfile(FileName)
        if Check == False:
            print("Your file name is unavailable, please choose other name.\n\n")
            Newfile()
        if Check == True:
            File = open("FileNameProgrammeApplication.txt","a")
            File.writelines(FileName + "\n")
            File.close()
            print("\n\t\t"+ FileName.replace(".txt","") + "\n")
            writinglines(FileName)

def Openfile():
    print("\n---- Open ----\n")
    linecount = printList()
    print()
    if linecount < 1:
        print("No File Found, returning to main menu")
        main()

    FileName = input("FileName (enter the number): ")
    if int(FileName) > linecount:
        print("\nError Please retry")
        Openfile()
    else:
        file = open("FileNameProgrammeApplication.txt","r")
        fileList = []
        for line in file:
            fileList.append(line.replace("\n",""))
        file.close()
        FileName = fileList[int(FileName) - 1]
        Check = Checkfile(FileName)
        if Check == True:
            print("No File Found")
            Openfile()
        if Check == False:
            readlines(FileName)

def Checkfile(x):
    File = open("FileNameProgrammeApplication.txt", "r")
    x = x + "\n"
    if x.replace(".txt","").replace("\n", "").isnumeric() == True or x.replace(".txt","").isspace() or x.replace(".txt","") == "" or '\\' in x:
        return False
    for line in File:
        if x == line:
            File.close()
            return False
    File.close()
    return True

def writinglines(FileName):
    key = Fernet(open("ky.key","rb").read())
    File = open(FileName, "a")
    while True:
        NewLine = input("")
        if NewLine == "exit()" or NewLine == '''"exit()"''' or NewLine == """'exit()'""":
            File.close()
            print("File has been saved, returning to main menu")
            main()
        NewLine = NewLine.encode()
        NewLine = key.encrypt(NewLine)
        File.writelines(str(NewLine).replace("b'","").replace("'","") + "\n")

def readlines(FileName):
    key = Fernet(open("ky.key","rb").read())
    File = open(FileName, "r")
    print("\n\t\t"+ FileName.replace(".txt","") + "\n")
    for line in File:
        line = line.encode()
        line = key.decrypt(line)
        line = str(line).replace("b'","").replace("'","")
        print(line.replace("\n",""))
    File.close()
    writinglines(FileName)

def password():
    file = open("2.txt", "r")
    line = file.readline()
    if int(line) < 1 or line == "" or line == " ":
        file.close()            
        file = open("1.txt", "w")
        password = input("Set Password: ")
        if password.lower() == "exit()" or password.lower() == '''"exit()"''' or password.lower() == """'exit()'""":
            exit()
        check = isValidPassword(password)
        while check == False:
            password = input("Set Password (1 Uppercase, 1 Lowercase, 1 Number, 1 Symbol, 10 letters in total: )")
            check = isValidPassword(password)
        if check == True:
            password = password.encode("utf-8")
            salt = bcrypt.gensalt()
            Hash = bcrypt.hashpw(password, salt)
            Hash = codecs.decode(Hash,"utf-8")
            file.writelines(Hash)
            file.close()
            file = open("2.txt", "w")
            file.writelines("1")
            file.close()
            #geberate the key to encryption data
            key = Fernet.generate_key()
            keyFile = open("ky.key","wb")
            keyFile.write(key)
            keyFile.close()
            print("Success!\n\n")
            return False
    else:
        file.close()
        password = input("password: ")
        if password.lower() == "exit()" or password.lower() == '''"exit()"''' or password.lower() == """'exit()'""":
            exit()
        password = password.encode("utf-8")
        File = open("1.txt","r")
        current_password = File.readline().encode("utf-8")
        File.close()
        if bcrypt.checkpw(password, current_password):
            file = open("2.txt", "r")
            number = file.readline()
            file.close()
            number = int(number) + 1
            file = open("2.txt", "w")
            file.write(str(number))
            file.close()
            return True
        else:
            return False

def DeleteFile():
    print("\n --- Delete Note ---\n")
    linecount = printList()
    print()
    Choose = input("File to delete (enter the number) (or press 'Enter' to return to main menu): ")
    if Choose == "" or Choose.isspace():
        main()
    if Choose.isnumeric():
        if int(Choose) > linecount:
            print("\ninput invalid, please try again")
            DeleteFile()
        else:
            fileList = []
            file = open("FileNameProgrammeApplication.txt","r")
            for line in file:
                fileList.append(line.replace("\n",""))
            file.close()
            DeletedFile = fileList[int(Choose) - 1]
            fileList[int(Choose) - 1] = ""
            file = open("FileNameProgrammeApplication.txt","w")
            for x in range (len(fileList)):
                if fileList[x] != "":
                    file.writelines(fileList[x] + "\n")
            file.close()
            os.remove(DeletedFile)
            print("\nFILE DELETED.\n-Press 'Enter' to return to main menu-")
            input()
            main()
    else:
        print("\nPlease try again")
        DeleteFile()

def printList():
    File = open("FileNameProgrammeApplication.txt", "r")
    linecount = 0
    for line in File:
        linecount += 1
        print(str(linecount) + ". " + line.replace(".txt","").replace("\n",""))
    File.close()
    #it will return the exact number of files
    return linecount

def Search():
    Search = input("Search(Press enter to return to main menu): ")
    if Search.isspace() or Search == " ":
        main()
    else:
        file = open("FileNameProgrammeApplication.txt", "r")
        FileList = []
        for line in file:
            FileList.append(line.replace("\n", ""))
        file.close()
        for variable in FileList:
            file = open(variable, "r")
            Available = False
            for line in file:
                if Search in line:
                    Available = True
                    print("\nTitle: " + variable.replace(".txt","") + "\n" + line + "________________________________")
            file.close()
            if Available == True:    
                Choose = input("\nInput note name to open note\nor press 'Enter' to return to main menu\nInput: ")
            else:
                input("No file found, returning to main menu")
                main()
        if Choose.isspace() or Choose == "":
            print()
            main()
        Check = Checkfile(Choose + '.txt')
        while Check == True:
            Choose = input("\nNo note found, Please enter a valid note name\nor press 'Enter' to return to main menu: ")
            Check = Checkfile(Choose + '.txt')
            if Choose .isspace() or Choose == "":
                print()
                main()
        if Check == False:
            readlines(Choose + ".txt")

def Reset():
    Choose = input("Are You Sure?\n(y/n): ")
    if Choose.lower() == "y":
        file = open ("FileNameProgrammeApplication.txt", "r")
        for line in file:
            os.remove(line.replace("\n",""))
        file.close()
        file = open("FileNameProgrammeApplication.txt", "w")
        file.close()
        file = open("1.txt", "w")
        file.close()
        file = open("2.txt", "w")
        file.write("0")
        file.close()
        os.remove("ky.key")
        logout()

def isValidPassword(x):
    UpperCheck = "False"
    LowerCheck = "False"
    DigitCheck = "False"
    SCharCheck = "False"
    CombiCheck = "False"
    Digitcheck = []
    URSpecialChar = []
    for z in range(len(x)):
        if x[z].isdigit() and x[z].isnumeric():
            Digitcheck.append(x[z])
    for z in range(len(x)):
        if not x[z].isalpha() and not x[z].isdigit() or x[z].isspace():
            URSpecialChar.append(x[z])
    for z in range(len(x)):
        if x[z].isupper():
            UpperCheck = "True"
            break
    for z in range(len(x)):
        if x[z].islower():
            LowerCheck = "True"
            break
    if len(Digitcheck) >= 1:
        DigitCheck = "True"
    if len(URSpecialChar) >= 1:
        SCharCheck = "True"
    if len(x) >= 10:
        CombiCheck = "True"
    if UpperCheck == "True" and LowerCheck == "True" and DigitCheck == "True" and SCharCheck == "True"\
        and CombiCheck == "True":
        return True
    else:
        return False

def logout():
    print("\n\t-- Secure Note --\b\n")
    passwordcheck = False
    while passwordcheck == False:
        passwordcheck = password()
    if passwordcheck == True:
        main()







logout()
