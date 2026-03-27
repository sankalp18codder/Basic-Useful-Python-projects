history_file = "history.txt"

def showhistory():
    with  open("history.txt" , 'r') as file:
        lines = file.readlines()
      
    if len(lines) == 0:
        print("no history found")
    else:
        for line in reversed(lines):
         strippedline = line.strip()
         print(strippedline)
            
       
         

def clearhistory():
    file = open(history_file,"w")
    file.close()
    print("history cleared")

def savehistory(equation , result):
    file = open(history_file,"a")
    file.write(equation + "=" + str(result) + "\n")
    file.close()

def calculate(user_input):
    parts = user_input.split()
    if len(parts) != 3:
        print("invalid input")
        return
    else:
        num1 = float(parts[0])
    op = parts[1]
    num2 = float(parts[2])

    if op == "+":
        result = num1 + num2
    elif op =="-":
        result = num1 - num2
    elif op =="*":
        result = num1*num2
    elif op =="/":
        if num2 == 0:
            print("cannot divide by zero")
            return
        else:
            result = num1/num2
    else:
        print("invalid input")
        return
    if int(result) == result:
        result = int(result)
        print("result : ",result)
        savehistory(user_input,result)

def main():
        print("welcome to calcultor type (history,clear or exit) : ")
        while True:
            user_input = input("enter calculation or command(history,clear,exit): ")
            if user_input == "exit":
                print("goodbye")
                break
            elif user_input == "history":
                showhistory()
            elif user_input == "clear":
                clearhistory()
            else:
                calculate(user_input)

main()




