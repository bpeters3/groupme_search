import funcs
import math
import os
clear = lambda: os.system('cls') #on Windows System


groups, response = funcs.returnRequest()

groups_num = len(groups)

group_choice = ''
page = 1

while group_choice == '':
    
    funcs.printGroups(groups_num,page,groups)

    group_choice = input("Select a group to download all messages:")
    if group_choice == '':
        clear()
    elif group_choice[0].isnumeric():
        group_id = response[page-1][int(group_choice)]["id"] # First index indicates page, second indicates group. E.G: response[Page 0][Group 0]
        print("Selected Group: " + response[page-1][int(group_choice)]['name'])
    elif group_choice[0].lower() == 'p':
        clear()
        if page == 1:
            print("Error: Reached end of list")
        else:
            page -= 1
        group_choice = ''
    elif group_choice[0].lower() == 'n':
        clear()
        if page == math.ceil(groups_num/10):
            print("Error: Reached end of list")
        else:
            page += 1
        group_choice = ''
    else:
        group_choice = ''

funcs.groupWrite(group_id)

print("File successfully written!")