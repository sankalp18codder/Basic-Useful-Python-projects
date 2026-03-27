import random
item_list = ["rock","paper","scissor"]
user_choice = input("enter your move(rock,paper,scissor) : ")
comp_choice = random.choice(item_list)

print(f"user choice = {user_choice}, computer choice = {comp_choice}")

if user_choice == comp_choice:
    print("both chooses same,match tie")
elif user_choice == "rock":
    if comp_choice == "paper":
        print("paper covers rock,computer wins")
    elif comp_choice == "scissor":
        print("rock breaks scissor,user wins")
elif user_choice == "paper":
    if comp_choice == "rock":
        print("paper covers rock,user win")
    elif comp_choice == "scissor":
        print("scissor cuts paper,computer wins")
elif user_choice == "scissor":
    if comp_choice == "paper":
        print("scissor cuts paper,user wins")
    if comp_choice == "rock":
        print("rock break scissor,computer wins")
else:
    print("invalid input")