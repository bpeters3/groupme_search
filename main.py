from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime # Timestamps are in unix time. To be used in the future

import json
import config # Config not included for token anonymity

def returnRequest(): # Returns groups from all pages including the response from each page
    url = "https://api.groupme.com/v3/groups?token=" + config.token # groupme API url
    response = urlopen(url)   
    data_json = json.loads(response.read())
    response_json = data_json["response"]
    groups = []
    response_full = []
    response_full.append(response_json)
    for i in response_json:
        groups.append({"id": i["id"],"name": i["name"]})
    j = 2
    while response_json != []:
        url = "https://api.groupme.com/v3/groups?token=" + config.token + "&page=" + str(j)
        response = urlopen(url)   
        data_json = json.loads(response.read())
        response_json = data_json["response"]
        for i in response_json:
            groups.append({"id": i["id"],"name": i["name"]})
        response_full.append(response_json)
        j += 1
    return groups, response_full

def returnGroup(group_id):
    url = "https://api.groupme.com/v3/groups/" + group_id + "?token=" + config.token # groupme API url
    response = urlopen(url)   
    data_json = json.loads(response.read())
    response_json = data_json["response"]
    return response_json

def returnAllMessages(group_id,msg_id = '0'):
    if msg_id == '0':
        url = "https://api.groupme.com/v3/groups/" + group_id + "/messages?limit=100&token=" + config.token # groupme API url
        response = urlopen(url)   
        data_json = json.loads(response.read())
        response_json = data_json["response"]
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
        print(data_json["meta"]["code"])
        if data_json["meta"]["code"] == 200: # Will have to come up with a case for responses E.G. rate limiting
            response_json = data_json["response"]
            messages = response_json["messages"]
            print(response_json["messages"][-1]["id"])
            messages = messages + returnAllMessages(group_id,response_json["messages"][-1]["id"])
            return messages
        else:   
            return []


groups, response = returnRequest()
for i in groups:
    print(i)
group_id = response[0][1]["id"] # First index indicates page, second indicates group. E.G: response[Page 0][Group 1]
group_response = returnGroup(group_id)
print(group_response)
message_all = returnAllMessages(group_id)