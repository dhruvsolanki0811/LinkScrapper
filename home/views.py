from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.contrib import messages
# Create your views here.

def home(request):
    page_name=request.GET.get('page')
    if page_name is not None:
        if page_name.startswith('https'):
            page=requests.get(page_name)
            soup=BeautifulSoup(page.text,'html.parser')
            for link in soup.find_all('a'):
                link_address=link.get('href')
                link_text=link.string             
                if link_address.startswith('http'):
                    Link.objects.create(address=link_address,name=link_text)
            link_addresses=Link.objects.all().order_by('-id')
            return render(request,'home.html',{'page':page_name,'data':link_addresses})
        else: 
            messages.error(request,'Page Not exist')    
    return render(request,'home.html',{})

def clear(request):
    print('okay')
    Link.objects.all().delete()
    return redirect('home')
