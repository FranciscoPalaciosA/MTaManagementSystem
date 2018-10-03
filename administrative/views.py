from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Administrative Index")

@login_required
def fill_Production_Report(request):
    return render(request, 'administrative/Production_Report.html')

def add_beneficiary(request):
    if request.method == 'GET':
        form =
        context = {'form': form}
        return render(request, 'path/to/tempate.html', context)
