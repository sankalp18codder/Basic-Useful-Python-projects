import os

def createfile(filename):
    try:
        with open(filename,"x") as f:
            print("file with name",filename,"has been created successfully")
    except FileExistsError:
        print("file with name",filename,"already exists")
    except Exception as E:
        print(" an error occured")

def viewallfiles():
    files = os.listdir()
    if not files:
        print("no file found")
    else:
        print("file found in directory")
    for file in files:
        print(file)
def deletefile(filename):
    try:
        os.remove(filename)
        print(filename,"has been deleted successfully")
    except FileNotFoundError:
        print("file not found")

    except Exception as E:
        print(" an error occured")
def readfile(filename):
    try:
        with open("sample.txt","r") as f:
            content = f.read()
            print("content of",filename,"is",content)   
    except FileNotFoundError:
        print("file not found")

    except Exception as E:
        print(" an error occured")   

def editfile(filename):
    try:
        with open("sample.txt","a") as f:
            content = input("enter data you want to enter ",)
            f.write(content + "\n")
            print("content has been succesfully added to",filename)
            
    except FileNotFoundError:
        print("file not found")

    except Exception as E:
        print(" an error occured")

def main():
    
        while True:
            print("welcome to file management app. please select among the following actions")
            print("1.create file")
            print("2.update file")
            print("3.delete file")
            print("4.view all file")
            print("5.read file")
            print("6.exit")

            choice = int(input("enter serial number of the action you need to perform : "))

            if choice == 1 :
                filename = input("enter file name to create : ")
                createfile(filename)
            elif choice == 2 :
                filename = input("enter file name to update : ")
                editfile(filename)
            elif choice == 3 :
                filename = input("enter file name to delete : ")
                deletefile(filename)
            elif choice == 4 :
                viewallfiles()
            elif choice == 5 :
                filename = input("enter file name to read : ")
                readfile(filename)
            elif choice == 6 :
                print("you have successfully closed our program . thank you")
                break
            else:
                print("invalid input")

main()
    

                
                

    
                  

    
