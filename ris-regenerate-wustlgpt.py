
import sys
import requests
import os
from requests.auth import HTTPBasicAuth
import time
import json



class GPTManager:

    def __init__(self, url, clientId, clientSecret, scope):
        #Initalizes the connection and gets our access token
        print("[GPT Manager] Initializing GPT Manager...")
        self.tokenUrl = url
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.scope = scope
        self.responseEndpoint = None
        self.getNewToken()
        
        

    def getNewToken(self):
        headers = {'grant_type': 'client_credentials', 'scope': self.scope}
        timeoutDuration = 15
        print("[GPT Manager] Acquiring New Access Token...")
        try:
            timeInit = time.time()
            response = requests.post(self.tokenUrl, auth = HTTPBasicAuth(self.clientId, self.clientSecret), data = headers, timeout = timeoutDuration)
            print("[GPT Manager] Sent request to %s..." % self.tokenUrl, end = "")
            timeEnd = time.time()
            response.raise_for_status()
            print(" complete in %.2f sec" % (timeEnd - timeInit))
            self.accessToken = response.json()['access_token']
        except requests.RequestException as exception:
            print("[GPT Manager] Failed to get access token for following reason:\n%s" % exception)
            self.accessToken = None
        except ValueError as exception:
            print("[GPT Manager] Failed to parse JSON response")
            self.accessToken = None

    def setResponseEndpoint(self, url):
        self.responseEndpoint = url
        
    
    def getResponse(self, data, attempts = 0):
        if (attempts >= 10):
            raise Exception("[GPT Manager] Failed to resolve prompt after 10 attempts")
        if (self.accessToken is None):
            raise Exception("AccessToken is None. Please Check GPT Manager Initialized Correctly.")
            return None
        if (self.responseEndpoint is None):
            raise Exception("ResponseEndpoint is None. Please set a valid API URL.")
            return None
        print("[GPT Manager] Sending request...", end = "")
        headers = {"Authorization": f"Bearer {self.accessToken}", "Content-Type":"application/json"}
        data_wrapped = {"messages":[{"role": "user", "content": data}]}
        try:
            timeInit = time.time()
            response = requests.post(self.responseEndpoint, json = data_wrapped, headers = headers)
            timeEnd = time.time()
           
            if (response.status_code == 401):
                error = response.json().get("message", "")
                if ("Access Token is missing or invalid" in error):
                    print("[GPT Manager] Token expired... updating token")
                    self.getNewToken()
                    return self.getResponse(data, attempts + 1)
            elif response.status_code != 200:
                print(" recieved error code %i " % response.status_code)
                print("[GPT Manager] Response Text: %s" % response.reason)
                print("[GPT Manager] Trying again in 5sec...", end = "", flush=True)
                time.sleep(5)
                print(" trying again...")
                return self.getResponse(data, attempts + 1)
            print(" complete in %.2f sec" % (timeEnd - timeInit))
            return response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as exception:
            print("[GPT Manager] Failed to get response for following reason:\n%s" % exception)
        except KeyError as e:
            print("[GPT Manager] Malformatted Response: ", response.json())       
            print("[GPT Manager] Trying again in 5sec...", end = "", flush=True)
            time.sleep(5)
            print(" trying again...")
            return self.getResponse(data, attempts + 1)


tokenUrl = os.getenv("TOKEN_URL")
responseEndpoint = 'https://api.openai.wustl.edu/base-gpt-4-8k/v1/chat/completions'
scope = os.getenv("GPT_SCOPE")
clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")


gptManager = GPTManager(tokenUrl, clientId, clientSecret, scope)
gptManager.setResponseEndpoint(responseEndpoint)
gptManager.getResponse("Hello?")

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
        #print(item['instruction'])
        #Queries API for response
        input = "Do not answer the following question. Only rephrase it in four different ways. Avoid making it overly verbose: " + item['instruction']
        print(input)
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
        # Mandatory sleep to avoid overwhelming server
        time.sleep(10)
    output_file.write("]")
    print("Generated %d Question/Answer Pairs" % (num_entries))


