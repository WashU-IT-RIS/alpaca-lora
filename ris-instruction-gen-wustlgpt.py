import openai
import json
import os
import requests
import sys
import subprocess
packages = []
command = ["pip", "install"] + packages
print(f"\nRequirements installing:\n\n" + "\n".join(packages))
result = subprocess.run(command, capture_output=True, text=True)
print("\nPackages installed.\n")

#API_KEY = open("API_KEY", "r").read()
#API_KEY = API_KEY.replace("\n","")
class WUSTLGPT:
	def __init__(self, sessionToken, conversationId):
		self.sessionToken = sessionToken
		self.conversationId = conversationId
	def getResponse(self,prompt):
		promise = requests.post("https://gpt.wustl.edu/api/chat", json = {
									"chatOverFileName":"",
									"chatType":"simple",
									"conversationStyle":"precise",
									"id":self.conversationId,
									"messages":[{"content":prompt, "role":"user"}]
									},
				       cookies={"__Secure-next-auth.session-token": self.sessionToken})	
		return promise.content.decode("utf-8")
#openai.api_key = API_KEY

sessionId = input("Session Authentication Token:")
conversationId = input("Valid conversation id:")
gptManager = WUSTLGPT(sessionId, conversationId)

with open(sys.argv[1]) as file:
    data = json.load(file)

with open(sys.argv[2], 'w') as output_file:
    num_entries = 0
    output_file.write("[")
    output_file.write("\n")
    for index, item in enumerate(data):
        #Copies original instruction
        json.dump(item, output_file)
        output_file.write(',')
        output_file.write('\n')
        print(item['instruction'])
        #Queries API for response
        input = "Do not answer the following question. Only rephrase it in four different ways. Avoid making it overly verbose: " + item['instruction']
        content = gptManager.getResponse(input)
        print(content)
        responses = content.split('\n')
        print(responses)
        responses = [input.strip()[3:] for input in responses] + [item["instruction"]]
        for num, input in enumerate(responses):
            entry = {"instruction": input, "input":item['input'], "output":item['output']}
            num_entries += 1
            json.dump(entry, output_file)
            if index != len(data)-1:
                output_file.write(',')
            if index == len(data)-1 and num != len(responses)-1:
                output_file.write(',')
            output_file.write('\n')
    output_file.write("]")
    print("Generated %d Question/Answer Pairs" % (num_entries))



