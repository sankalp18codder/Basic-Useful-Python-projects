contact = {}

while True:
    print("welcome to contact management system\nplease select your action from the following options : ")
    print("1.create contact")
    print("2. view contact")
    print("3.update contact")
    print("4.delete contact")
    print("5.search contact")
    print("6.count contact")
    print("7.exit")

    choice = int(input("please select the number for the action you need to perform : "))

    if choice == 1 :
        name = input("enter the name of new contact : ")
        if name in contact:
            print("contact of name",name,"already exists")
        else:
            age = int(input("enter the age :"))
            email = input("enter email :")
            mobilenumber = int(input("enter  mobile number : "))
            contact[name] = {"age : ",age,"email id",email,"mobile number : ",mobilenumber}
            print("contact has been created successfully")

    elif choice == 2 :
        name = input("enter name to view profile :")
        if name in contact :
            contact1 = contact[name]
            print("name : ",name,"age : ",age,"mobile number : ",mobilenumber)
        else:
            print("contact not found")
            
    elif choice == 3 :
        name = input("enter name to update : ")
        if name in contact :
            age = int(input("enter the new age :"))
            email = input("enter new email :")
            mobilenumber = int(input("enter new mobile number : "))
            contact[name] = {"age : ",age,"email id",email,"mobile number : ",mobilenumber}
        else:
            print("no contact found")

    elif choice == 4 :
        name = input("enter name to delete : ")
        if name in contact:
            del contact[name]
            print("contact has been deleted successfully")
        else :
            print("contact not found")
    elif choice == 5 :
        searchname = input("enter name to search :")
        found = False
        for name,contacts in contact.items() :
            if searchname.lower() in name.lower():
                 print("name : ",name,"age : ",age,"mobile number : ",mobilenumber)
                 found = True
            else:
               print("no contact found")
    elif choice == 6 :
        print("total contacts in your book :",len(contact))

    elif choice == 7 :
        print("program has been closed successfully")
        break

    else:
        print("invalid input")
        





                               