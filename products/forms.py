from django.forms import ModelForm
from django import forms
from products.models import *


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = '__all__'


class AddReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class UpdateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class FilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=CategoryProducts.objects.all(), empty_label="Select a category")
    size = forms.ModelChoiceField(queryset=SizeProduct.objects.all(), empty_label="Select a size")
    type = forms.ModelChoiceField(queryset=TypeProduct.objects.all(), empty_label="Select a type")
    color = forms.ModelChoiceField(queryset=ColorProduct.objects.all(), empty_label="Select a color")
    made_company = forms.ModelChoiceField(queryset=MadeCompany.objects.all(), empty_label="Select a made company")
    made_country = forms.ModelChoiceField(queryset=MadeCountry.objects.all(), empty_label="Select a made country")
    lather = forms.ModelChoiceField(queryset=Lather.objects.all(), empty_label="Select a lather")
    season = forms.ModelChoiceField(queryset=Season.objects.all(), empty_label="Select a season")
    price_min = forms.IntegerField(required=False)
    price_max = forms.IntegerField(required=False)
