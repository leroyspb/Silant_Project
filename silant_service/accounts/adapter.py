from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import render
from django.urls import reverse


class NoSignupAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
    
    def ajax_response(self, request, response, redirect_to=None, form=None, data=None):
        return super().ajax_response(request, response, redirect_to, form, data)