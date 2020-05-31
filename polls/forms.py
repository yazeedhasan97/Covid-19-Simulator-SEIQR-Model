from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.template.defaultfilters import mark_safe


class ModelForm(forms.Form):
    # Initial Parameters
    susceptible = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(float('inf'))],
        initial='1000', required=True)
    exposed = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(float('inf'))],
        initial='1', required=True)
    infected = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(float('inf'))],
        initial='0', required=True)
    quarantine = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(float('inf'))],
        initial='0', required=True)
    recovered = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(float('inf'))],
        initial='0', required=True)
    tf = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(365)],
        initial='30', required=True)

    # Model Parameters
    b = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        initial='0.0', required=True)
    beta = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 8}),
        initial='0.90', required=True)
    xi = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 15}),
        initial='0.0', required=True)
    gamma = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 16}),
        initial='0.50', required=True)
    epsilon = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 8}),
        initial='0.20', required=True)
    delta = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 12}),
        initial='0.0', required=True)
    theta = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 8}),
        initial='0.0', required=True)
    zeta = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 4}),
        initial='0.0', required=True)

    mu = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 8}),
        initial='0.0', required=True)

    # General Parameters
    hospital_number = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        initial='5', required=True)
    beds_ber_hospital = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1500)],
        widget=forms.TextInput(attrs={'size': 8}),
        initial='150', required=True)
    nurse_ber_hospital = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        widget=forms.TextInput(attrs={'size': 8}),
        initial='30', required=True)
    max_nurse_handel = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        initial='5', required=True)
    d = forms.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        widget=forms.TextInput(attrs={'size': 18}),
        initial='0.0', required=True)
    days_exposed_infected = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(21)],
        initial='14', required=True)
    days_infected_recovered = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(21)],
        initial='17', required=True)
    days_infected_quarantine = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(21)],
        initial='1', required=True)
    days_quarantine_recovered = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(21)],
        initial='16', required=True)
