from urllib.request import urlopen

import json

def returnRequest(token):
    url = "https://api.groupme.com/v3/groups?token=" + token # groupme API url
    response = urlopen(url)   
    data_json = json.loads(response.read())
    response_json = data_json["response"]
    groups = []
    response_full = []
    response_full.append(response_json)
    for i in response_json:
        groups.append({i["id"], i["name"]})
    j = 2
    while response_json != []:
        url = "https://api.groupme.com/v3/groups?token=" + token + "&page=" + str(j)
        response = urlopen(url)   
        data_json = json.loads(response.read())
        response_json = data_json["response"]
        for i in response_json:
            groups.append({"id": i["id"],"name": i["name"]})
        response_full.append(response_json)
        j += 1
    return groups, response_full

def returnGroup(group_id):
    url = "https://api.groupme.com/v3/groups/" + group_id + "/messages?limit=100&token=" + token # groupme API url
    response = urlopen(url)   
    data_json = json.loads(response.read())
    response_json = data_json["response"]
    return response_json

token = "" # Insert groupme token here
groups, response = returnRequest(token)
for i in groups:
    print(i)
group_id = response[0][1]["id"] # First index indicates page, second indicates group. E.G: response[Page 0][Group 1]
group_response = returnGroup(group_id)