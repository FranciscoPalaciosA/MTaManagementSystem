from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Administrative Index")

@login_required
def production_report(request):
    production_report_form = ProductionReportForm()
    context = {'production_report_form': production_report_form}
    return render(request, 'administrative/Production_Report.html', context)

def add_production_report(request):
    if request.method == 'POST':
        form = ProductionReportForm(request.POST)
        #print(form.data['self_seed'])
        if form.is_valid():
            newProductionReport = ProductionReport(
                                                    beneficiary = Beneficiary.objects.get(id = 1),
                                                    self_seed = form.cleaned_data['self_seed'],
                                                    self_leaf = form.cleaned_data['self_leaf'],
                                                    self_flour = form.cleaned_data['self_seed'],
                                                    days_per_month = form.cleaned_data['days_per_month'],
                                                    exch_seed = form.cleaned_data['exch_seed'],
                                                    exch_leaf = form.cleaned_data['exch_leaf']
                                                    )
            newProductionReport.save()
            return HttpResponseRedirect('/administrative/')

        else:
            print("-------------------")
            print("\n\n\n\n\n")
            print("Form is not valid")
            print(form.errors)
            print("\n\n\n\n\n")

def add_beneficiary(request):
    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'path/to/tempate.html', context)
