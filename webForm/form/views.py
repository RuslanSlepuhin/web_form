import json

from django.views.decorators.http import require_POST

from form.variables.variables import bot_domain, external_web_hook, server_domain, endpoint_form, form_page, subdomain

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response

# from telegram.telegram_bot import BotHandlers
from .forms import FormForms
from .models import *
from .serializers import FormSerializer

def home(request):
  return render(request, 'home.html', {'server_domain': server_domain, 'subdomain': subdomain, 'endpoint_form': endpoint_form, 'form_name': 'Simpleatom connection form'})

def home_rus(request):
  return render(request, 'home_rus.html', {'server_domain': server_domain, 'subdomain': subdomain, 'endpoint_form': endpoint_form, 'form_name': 'Simpleatom форма для подключения'})

def form_is_completed(request):
  return render(request, 'form_is_completed.html', {'server_domain': server_domain, 'endpoint_form': endpoint_form})

class webFormView(generics.ListCreateAPIView, generics.ListAPIView):
  queryset = webFormModel.objects.using('sqlite').all()
  serializer_class = FormSerializer

  # @require_POST
  def post(self, request, *args, **kwargs):
    selected_values = request.POST.getlist('optimalInvestmentPeriod')
    print(selected_values)
    selected_values = selected_values[:-1] if selected_values and not selected_values[-1] else selected_values
    if not selected_values or not selected_values[0]:
      return HttpResponse("<script>alert('You did not check the checkboxes');</script>")

    json_data = json.dumps(selected_values)
    data = request.data.dict()
    json_data = json.loads(json_data)
    data['optimalInvestmentPeriod'] = json_data
    form = FormForms(data)
    if form.is_valid():
      serializer = self.get_serializer(data=data)
      if serializer.is_valid(raise_exception=True):
        # pass
        self.create_object(data)
      path = bot_domain + external_web_hook
      # serializer_data = dict(serializer.data)
      response = requests.post(path, json=data)
      if 200 >=response.status_code < 300:
        return redirect(server_domain + subdomain + "form_is_completed/")

    elif form.errors.get('email'):
      # return render(request, 'home_rus.html', {'form': form})
      pass
    return Response({"message": "Data wasn't saved"})

  def get(self, request, *args, **kwargs):
    queryset = webFormModel.objects.using('sqlite').all()
    serializer = self.get_serializer(queryset, many=True)
    return Response({"response": serializer.data})

  def create_object(self, validated_data):
    # if 'submit' in validated_data:
    #   validated_data.pop('submit')
    return webFormModel.objects.using('sqlite').create(**validated_data)

