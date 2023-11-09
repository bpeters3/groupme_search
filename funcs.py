from urllib.request import urlopen
from urllib.error import HTTPError
import json
import config # Config not included for token anonymity
from datetime import datetime
import math


def parseJSON(url):
    response = urlopen(url)   
    data_json = json.loads(response.read())
    response_json = data_json["response"]
    return response_json

def returnRequest(): # Returns groups from all pages including the response from each page
    url = "https://api.groupme.com/v3/groups?token=" + config.token # groupme API url
    response_json = parseJSON(url)
    groups = []
    response_full = []
    response_full.append(response_json)
    for i in response_json:
        groups.append({"id": i["id"],"name": i["name"]})
    j = 2
    while response_json != []:
        url = "https://api.groupme.com/v3/groups?token=" + config.token + "&page=" + str(j)
        response_json = parseJSON(url)
        for i in response_json:
            groups.append({"id": i["id"],"name": i["name"]})
        response_full.append(response_json)
        j += 1
    return groups, response_full

def returnGroup(group_id):
    url = "https://api.groupme.com/v3/groups/" + group_id + "?token=" + config.token # groupme API url
    response_json = parseJSON(url)
    return response_json

def returnAllMessages(group_id,msg_id = '0'):
    if msg_id == '0':
        url = "https://api.groupme.com/v3/groups/" + group_id + "/messages?limit=100&token=" + config.token # groupme API url
        response_json = parseJSON(url)
        messages = response_json["messages"]
        messages = messages + returnAllMessages(group_id,response_json["messages"][-1]["id"])
        return messages
    else:
        url = "https://api.groupme.com/v3/groups/" + group_id + "/messages?limit=100&before_id=" + msg_id + "&token=" + config.token # groupme API url
        try:
            response = urlopen(url)   
        except HTTPError:
            return []
        data_json = json.loads(response.read())
        if data_json["meta"]["code"] == 200: # Will have to come up with a case for responses E.G. rate limiting
            response_json = data_json["response"]
            messages = response_json["messages"]
            messages = messages + returnAllMessages(group_id,response_json["messages"][-1]["id"])
            return messages
        else:   
            return []

def printGroups(groups_num,page,groups):
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

def groupWrite(group_id):
    group_response = returnGroup(group_id)
    print("Retrieving messages from GroupMe API......")
    message_all = returnAllMessages(group_id)


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