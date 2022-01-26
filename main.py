import funcs
import math
from datetime import datetime

groups, response = funcs.returnRequest()

groups_num = len(groups)

group_choice = ''
page = 1

while group_choice == '':
    print("\n           Showing page " + str(page) + " of " + str(math.ceil(groups_num/10)))
    print("--------------------------------------------")
    
    if groups_num - ((page-1)*10) < 10:
        for i in range(0,groups_num - ((page-1)*10)):
            print("[" + str(i) + "] : " + groups[i+(page-1)*10]['name'])
    else:
        for i in range(0,10):
            print("[" + str(i) + "] : " + groups[i+(page-1)*10]['name'])
            
    print("--------------------------------------------")
    print("    [P]revious page    |    [N]ext page")
    group_choice = input("Select a group to download all messages:")
    if group_choice == '':
        print("\n"*100)
    elif group_choice[0].isnumeric():
        group_id = response[page-1][int(group_choice)]["id"] # First index indicates page, second indicates group. E.G: response[Page 0][Group 0]
        print("Selected Group: " + response[page-1][int(group_choice)]['name'])
    elif group_choice[0].lower() == 'p':
        print("\n"*100)
        if page == 1:
            print("Error: Reached end of list")
        else:
            page -= 1
        group_choice = ''
    elif group_choice[0].lower() == 'n':
        print("\n"*100)
        if page == math.ceil(groups_num/10):
            print("Error: Reached end of list")
        else:
            page += 1
        group_choice = ''
    else:
        group_choice = ''

group_response = funcs.returnGroup(group_id)
print("Retrieving messages from GroupMe API......")
message_all = funcs.returnAllMessages(group_id)


group_name = group_response["name"]
invalid = '/\:*?\"<>|'
for char in invalid:
    group_name = group_name.replace(char,'') # Clean file name of illegal windows chars.

message_output = open(group_name + '.txt','wb')

print("Writing to " + group_name + ".txt ...")

for i in reversed(message_all):
    date_i = datetime.fromtimestamp(i["created_at"])
    sender_i = i["name"]
    message_i = i["text"]
    line_out = str(date_i) + "[" + str(sender_i) + "] : " + str(message_i) + '\n'
    message_output.write(line_out.encode('utf8'))

message_output.close()

print("File successfully written!")