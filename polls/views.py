from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages

###
from .forms import ModelForm
from .models import Inputs
from .models import CalculationModel


API_KEY = 'AIzaSyBqmaSMESUuaWht383WqtEtLDyGff5GrKs'
# Create your views here.
def home(request):
    template_name = 'home.html'
    if request.method == 'POST':
        input_form = Inputs()
        model = ModelForm(request.POST)

        if model.is_valid():
            # Initial Parameters
            input_form.susceptible = model.cleaned_data.get("susceptible")
            input_form.exposed = model.cleaned_data.get("exposed")
            input_form.quarantine = model.cleaned_data.get("quarantine")
            input_form.infected = model.cleaned_data.get("infected")
            input_form.recovered = model.cleaned_data.get("recovered")
            input_form.tf = model.cleaned_data.get("tf")

            # General Parameters
            input_form.hospital_number = model.cleaned_data.get("hospital_number")
            input_form.beds_ber_hospital = model.cleaned_data.get("beds_ber_hospital")
            input_form.nurse_ber_hospital = model.cleaned_data.get("nurse_ber_hospital")
            input_form.max_nurse_handel = model.cleaned_data.get("max_nurse_handel")
            input_form.d = model.cleaned_data.get("d")

            # Parameters To Add in The Future
            # input_form.weekly_infection_rate = request.POST.get("weekly_infection_rate")
            # input_form.days_before_diagnosis = request.POST.get("days_before_diagnosis")
            # input_form.days_to_recover = request.POST.get("days_to_recover")
            # input_form.days_undiagnosed_infectious = request.POST.get("days_undiagnosed_infectious")
            # input_form.number_of_patients_diagnosed = request.POST.get("number_of_patients_diagnosed")
            # input_form.diagnosed_patient_death = request.POST.get("diagnosed_patient_death")
            # input_form.max_diagnosed_death = request.POST.get("max_diagnosed_death")

            # Model Parameters
            input_form.b = model.cleaned_data.get("b")
            input_form.beta = model.cleaned_data.get("beta")
            input_form.xi = model.cleaned_data.get("xi")
            input_form.gamma = model.cleaned_data.get("gamma")
            input_form.epsilon = model.cleaned_data.get("epsilon")
            input_form.delta = model.cleaned_data.get("delta")
            input_form.theta = model.cleaned_data.get("theta")
            input_form.zeta = model.cleaned_data.get("zeta")
            input_form.mu = model.cleaned_data.get("mu")

            x = CalculationModel(input_form)
            # gmaps = x.google_map()
            context = {
                'model_form': model,
                # 'sick_undiagnosed': input_form.total_population,
                # 'sick_all_time': input_form.total_population,
                # 'sick_diagnosed': input_form.total_population,
                # 'recovered_diagnosed': input_form.total_population,
                # 'recovered_never_diagnosed': input_form.total_population,
                'deceased': x.final_death_number,
                'API_KEY': API_KEY
            }
            return render(request, template_name, context)  # template_name
    else:

        import gmaps.datasets
        # df = gmaps.datasets.load_dataset_as_df('acled_africa_by_year')
        df = gmaps.datasets.load_dataset_as_df("starbucks_kfc_uk")

        context = {
            'model_form': ModelForm(),
            # 'google_map': ReverseGeocoder().render(),
            # 'google_map': AcledExplorer(df).render(),
            'API_KEY': API_KEY
        }
        return render(request, template_name, context)
