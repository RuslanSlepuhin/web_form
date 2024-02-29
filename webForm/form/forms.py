from django import forms


class FormForms(forms.Form):
    name = forms.CharField(required=False)
    instrumentWorks = forms.CharField()
    whatAmount = forms.CharField()
    whatTradingStrategy = forms.CharField()
    optimalInvestmentPeriod = forms.JSONField()
    howToReach = forms.CharField()
    formName = forms.CharField()
    email = forms.CharField()
