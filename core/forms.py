from django import forms
from django.forms import ModelForm
from .models import  IntellectualProperty , Student,Coordinator,User,College,Department, SubType
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import transaction
from django.core.exceptions import ValidationError


class UserForm(ModelForm):
  
    password = None
    class Meta:
        model = User 
        fields = ['profile','first_name','last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter email'}),
        }

class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User 
        fields = ['old_password','new_password1','new_password2']
   

class AddStudentForm(UserCreationForm):
   class Meta:
        model = User

        fields = ['username', 'email',  'first_name', 'last_name', 'password1', 'password2']


class StudentForm(UserCreationForm):
   class Meta:
        model = User

        fields = ['college', 'department','username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'college': forms.Select(attrs={'placeholder': 'Enter the title of the intellectual property'}),
            'department': forms.Select(attrs={'placeholder': 'Select type'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.TextInput(attrs={'placeholder': 'mipo@gmail.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'password1': forms.Textarea(attrs={'placeholder': '************'}),
            'password2': forms.Textarea(attrs={'placeholder': '************'}),
        }
        labels = {
            'college': 'College',
            'deparment': 'Department',
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First name',
            'last_name': 'Last name',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

  

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'college' in self.data:
            try:
                college_id = int(self.data.get('college'))
                self.fields['department'].queryset = Department.objects.filter(college_id=college_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.college.department_set.order_by('name')


class CoordinatorForm(UserCreationForm):
   class Meta:
        model = User
        
        fields = ['college', 'department','username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'college': forms.Select(attrs={'placeholder': 'Enter the title of the intellectual property'}),
            'department': forms.Select(attrs={'placeholder': 'Select type'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.TextInput(attrs={'placeholder': 'mipo@gmail.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'password1': forms.Textarea(attrs={'placeholder': '************'}),
            'password2': forms.Textarea(attrs={'placeholder': '************'}),
        }
        labels = {
            'college': 'College',
            'deparment': 'Department',
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First name',
            'last_name': 'Last name',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
     
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'college' in self.data:
            try:
                college_id = int(self.data.get('college'))
                self.fields['department'].queryset = Department.objects.filter(college_id=college_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.college.department_set.order_by('name')
            
class IntellectualPropertyForm(forms.ModelForm):
    author = forms.CharField(
        label="Co-Authors",
        widget=forms.Textarea(attrs={'placeholder': 'Enter co-author/s usernames separated by commas. e.g (vyylmalyyn_19, maimah_02, aisah_09)'}),
        required=False
    )
    
    mainauthor_username = forms.CharField(
        label="Main Author",
        widget=forms.Textarea(attrs={'placeholder': 'Enter main author username'}),
        required=True
    )
 
    class Meta:
        model = IntellectualProperty
        fields = ['tittle', 'type', 'file', 'subtype', 'cover', 'year', 'mainauthor_username', 'author', 'description']
        widgets = {
            'tittle': forms.TextInput(attrs={'placeholder': 'Enter the title of the intellectual property'}),
            'type': forms.Select(attrs={'placeholder': 'Select type'}),
            'file': forms.ClearableFileInput(attrs={'placeholder': 'Upload a file'}),
            'subtype': forms.Select(attrs={'placeholder': 'Select subtype'}),
            'cover': forms.ClearableFileInput(attrs={'placeholder': 'Upload a cover image'}),
            'year': forms.DateInput(attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd',
                'class': 'form custom-date-input'
            }),
            'description': forms.Textarea(attrs={'placeholder': 'Enter a description of the intellectual property'}),
        }
        labels = {
            'tittle': 'Title',
            'type': 'Intellectual Property Type',
            'file': 'File',
            'subtype': 'Subtype',
            'cover': 'Cover Image',
            'year': 'Year',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subtype'].queryset = SubType.objects.none()
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['subtype'].queryset = SubType.objects.filter(type_id=type_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subtype'].queryset = self.instance.type.subtype_set.order_by('name')
    

    
class AdminIntellectualPropertyForm(forms.ModelForm):
    author = forms.CharField(
        label="Co-Authors",
        widget=forms.Textarea(attrs={'placeholder': 'Enter authors as "last_name first_name", separated by commas (for example: Sanchez Vilmalyn, Dangco Omaimah, Mangompia Aisah).'}),
        required=False,
    )
    mainauthor_username = forms.CharField(
        label="Main Author",
        widget=forms.Textarea(attrs={'placeholder': 'Enter the main author name as "last_name first_name" (for example: Sanchez Vilmalyn).'}),
        required=True,
    )

    class Meta:
        model = IntellectualProperty
        fields = ['college', 'department', 'type', 'subtype', 'tittle', 'year', 'file', 'cover', 'mainauthor_username', 'author', 'description']
        widgets = {
            'college': forms.Select(attrs={'placeholder': 'Select college'}),
            'department': forms.Select(attrs={'placeholder': 'Select department'}),
            'type': forms.Select(attrs={'placeholder': 'Select type'}),
            'subtype': forms.Select(attrs={'placeholder': 'Select subtype'}),
            'tittle': forms.TextInput(attrs={'placeholder': 'Enter the title of the intellectual property'}),
            'year': forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
        }
        labels = {
            'college': 'College',
            'department': 'Department',
            'tittle': 'Title',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'college' in self.data:
            try:
                college_id = int(self.data.get('college'))
                self.fields['department'].queryset = Department.objects.filter(college_id=college_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.college.department_set.order_by('name')

        self.fields['subtype'].queryset = SubType.objects.none()

        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['subtype'].queryset = SubType.objects.filter(type_id=type_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subtype'].queryset = self.instance.type.subtype_set.order_by('name')







 

