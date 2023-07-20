from django.shortcuts import render
from django.http import HttpResponse
from gradio_client import Client


# Create your views here.
def home(request):
    return render(request, 'home.html')

def getResponse(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        client = Client("http://compute1-exec-201.ris.wustl.edu:7860/") 
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

    return HttpResponse(result)