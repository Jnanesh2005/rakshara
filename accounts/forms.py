from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    height_cm = forms.FloatField(required=False)
    weight_kg = forms.FloatField(required=False)
    personal_contact = forms.CharField(required=False)
    parent_contact = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)
    roll_no = forms.CharField(required=True)
    class_name = forms.CharField(required=True)
    section = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",
                  "roll_no", "dob", "height_cm", "weight_kg", "personal_contact",
                  "parent_contact", "address", "school", "class_name", "section")

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)
    verification_id = forms.CharField(required=True, help_text="Enter school verification id provided by admin")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "school", "verification_id", "contact", "address")
