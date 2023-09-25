from django.shortcuts import render
from django.http import HttpResponse
from .models import event
import json
import hashlib
import hmac
import base64
SECRET_TOKEN = 'hi'    #토큰값


# Create your views here.
def webhook(request):
    if request.method == 'POST':
        hmac_msg = hmac.new(      #sha265암호화
            key=bytes(SECRET_TOKEN, 'utf-8'),
            msg=bytes(request.body),
            digestmod=hashlib.sha256
        ).digest() 
        if(f"sha256={base64.b64encode(hmac_msg).decode('utf-8')}"== request.headers['X-Hub-Signature-256']): #base64인코딩하여 header에  X-Hub-Signature-256과 비교
            hook = json.load(request)['Event']['EventHeader']
            event(time=hook['Timestamp'],msg=hook['Message'],cma=hook['Source']['Name']).save()
            return (HttpResponse(request, status=200))
        else:
            return HttpResponse(request, status=403)
    else:
        i = event.objects.order_by('-id')[:8]
        return render(request, 'index.html',{'event': i})