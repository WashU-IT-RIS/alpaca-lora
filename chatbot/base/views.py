from django.shortcuts import render
from django.http import HttpResponse
from gradio_client import Client
from django.views.decorators.csrf import csrf_exempt
import os
import json
import time
import sqlite3

numberLogs = 0
chatLogs = []
logsPerDump = 10

dbPath = "/db/serverdb"

# Create your views here.
def home(request):
    return render(request, 'home.html')

@csrf_exempt
def getHeader(request):
    print(request)
    ip_addr = request.META.get("HTTP_X_FORWARDED_FOR").split(",")[0] if request.META.get("HTTP_X_FORWARDED_FOR") else request.META.get("REMOTE_ADDR")
    print(request.get_host())
    print(ip_addr)
    return HttpResponse("Request Printed in Server Log")


@csrf_exempt
def updateRating(request):
    if request.method == 'POST':
        connection = sqlite3.connect(dbPath)
        #Get the interaction ID 
        InteractionID = int(request.POST.get('interactionId'))
        #Get the rating:
        rating = max(min(int(request.POST.get('rating')), 127), -127)
        
        #Get the IP
        ip_addr = request.META.get("HTTP_X_FORWARDED_FOR").split(",")[0] if request.META.get("HTTP_X_FORWARDED_FOR") else request.META.get("REMOTE_ADDR")

        #Ensure the IP address matches the one on file
        dbCursor = connection.cursor()
        record = dbCursor.execute("SELECT ip FROM Interactions WHERE id = " + str(InteractionID))
        response = record.fetchone()
        if response == None:
            connection.close()
            return HttpResponse("NO_SUCH_INTERACTION")
        if response[0] != ip_addr:
            connection.close()
            return HttpResponse("IP_ADDR_MISMATCH")
        #They match
        #Update the record accordingly
        query = "UPDATE Interactions SET rating = " + str(rating) + " WHERE id = " + str(InteractionID)
        print("EXEC QUERY:")
        print(query)
        dbCursor.execute(query)
        connection.commit()
        connection.close()
        return HttpResponse(rating)
    return HttpResponse("METHOD_NOT_POST") 

@csrf_exempt
def getResponse(request):
    global chatLogs, numberLogs, logsPerDump, dbPath
    if request.method == 'POST':
        #We don't care too much about the overhead, mostly because
        #we have the overhead of running an ENTIRE LLM
        connection = sqlite3.connect(dbPath) 
        message = request.POST.get('message')
        #print("THIS IS THE HOST" + os.environ['HOSTNAME'])
        client = Client("http://" + os.environ['HOSTNAME'] + ":7860/") 
        result = client.predict(
                        message,	# str  in 'Instruction' Textbox component
                        "",	# str  in 'Input' Textbox component
                        0.6,	# int | float (numeric value between 0 and 1) in 'Temperature' Slider component
                        0.75,	# int | float (numeric value between 0 and 1) in 'Top p' Slider component
                        10,	# int | float (numeric value between 0 and 100) in 'Top k' Slider component
                        1,	# int | float (numeric value between 1 and 4) in 'Beams' Slider component
                        128,	# int | float (numeric value between 1 and 2000) in 'Max tokens' Slider component
                        False,	# bool  in 'Stream output' Checkbox component
                        api_name="/predict"
        )
        print(result)
    
        ip_addr = request.META.get("HTTP_X_FORWARDED_FOR").split(",")[0] if request.META.get("HTTP_X_FORWARDED_FOR") else request.META.get("REMOTE_ADDR")
        #add to database
        messageCleaned = message.replace("\"", "&quot").replace("'", "&squot").replace("\\", "&slash")
        responseCleaned = result.replace("\"", "&quot").replace("'", "&squot").replace("\\", "&slash")
        dbCursor = connection.cursor()
        #How bad would a race condition be?
        #As such, this program does NOT implement semaphores currently
        res = dbCursor.execute("SELECT MAX(id) FROM Interactions")
        maxId = res.fetchone()[0] + 1
        dbCursor.execute("INSERT INTO Interactions VALUES (" + str(maxId) + ", 0, CURRENT_TIMESTAMP, \"" + str(ip_addr) + "\",\"" + messageCleaned + "\", \"" + responseCleaned + "\")")
        connection.commit()
        connection.close()
        
        returnObject = {"message": result, "interactionId": maxId}

        """datasetRecord = {"question":message, "answer":result}
        chatLogs.append(datasetRecord)
        if (len(chatLogs) >= logsPerDump):
            filename = "logs/ChatLogs%05d-%05d.json" % ((numberLogs - logsPerDump), numberLogs)
            fp = open(filename, "w")
            json.dump(chatLogs, fp)
            fp.close()
            chatLogs = []
        numberLogs += 1
        """
        return HttpResponse(json.dumps(returnObject), content_type="application/json")
