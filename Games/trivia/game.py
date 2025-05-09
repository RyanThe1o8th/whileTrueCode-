import requests
import json
response = requests.get("https://opentdb.com/api.php?amount=10&category=23&type=multiple")
data = response.json()
returnable = []
for item in data["results"]:
    #print (item["question"])
    #print (item["correct_answer"])
    #print (item["incorrect_answers"])
    #print(item["incorrect_answers"].append(item["correct_answer"]))
    choices = []
    for i in item["incorrect_answers"]:
        choices.append(i)
    choices.append(item["correct_answer"])
    #print(choices)
    returnable.append([item["question"], choices])
print(returnable)
    

#print(data["results"])
