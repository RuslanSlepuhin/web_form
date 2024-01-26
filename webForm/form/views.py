import json
from telegram.variables import bot_domain, external_web_hook

import requests
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from telegram.telegram_bot import BotHandlers
from .forms import FormForms
from .models import *
from .serializers import FormSerializer

def home(request):
  pass
  return render(request, 'home.html')

def bot_start():
  token = '6784209473:AAESK6fiESV_ijnf22gwFKBGwiNG9-dalkc'
  bot = BotHandlers(token=token)
  bot.handlers()


class webFormView(generics.ListCreateAPIView, generics.ListAPIView):
  queryset = webFormModel
  serializer_class = FormSerializer

  def post(self, request, *args, **kwargs):
    selected_values = request.POST.getlist('optimalInvestmentPeriod')
    selected_values = selected_values[:-1] if selected_values and not selected_values[-1] else selected_values
    if not selected_values or not selected_values[0]:
      return HttpResponse("<script>alert('You did not check the checkboxes');</script>")

    json_data = json.dumps(selected_values)
    data = request.data.dict()
    data['optimalInvestmentPeriod'] = json_data
    form = FormForms(data)
    if form.is_valid():
      serializer = self.get_serializer(data=data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      path = bot_domain + external_web_hook
      serializer_data = dict(serializer.data)
      response = requests.post(path, json=serializer_data)
      # return Response({"message": "Data was saved"})
      return render(request, "form_is_completed.html")
    else:
      return Response({"message": "Data wasn't saved"})

  def get(self, request, *args, **kwargs):
    queryset = webFormModel.objects.all()
    serializer = self.get_serializer(queryset, many=True)
    return Response({"response": serializer.data})

