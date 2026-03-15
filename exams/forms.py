from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import ExamDuration,Subject,AdminResult, CustomUser,SEMESTER_CHOICES
import datetime

# --------------------
# Admin (Committee) Login
# --------------------
class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


# --------------------
#  Faculty Registeration
# --------------------
class FacultyRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "faculty"
        user.is_approved = False  # New faculty always pending
        if commit:
            user.save()
        return user


# --------------------
# Faculty Login
# --------------------

class FacultyLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
# --------------------
# Student Registration
# --------------------
class StudentRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = CustomUser
        fields = ['student_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'semester','password']

        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': 'Student ID'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepend the placeholder to the choices
        self.fields['semester'].choices = [('', '-- Select Semester --')] + list(self.fields['semester'].choices)
        self.fields['semester'].widget.attrs.update({'class': 'input-box'})
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")


    def save(self, commit=True):
        """Make sure password is hashed before saving"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  
        if commit:
            user.save()
        return user


# --------------------
# Student Login
# --------------------
class StudentLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


# --------------------
# Exam Duration
# --------------------
class ExamDurationForm(forms.ModelForm):
    class Meta:
        model = ExamDuration
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "min": datetime.date.today().strftime("%Y-%m-%d")  # ✅ Disable past dates in picker
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "min": datetime.date.today().strftime("%Y-%m-%d")  # ✅ Disable past dates in picker
                }
            ),
        }

    # Extra backend validation (safety check)
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and start <= datetime.date.today():
            raise forms.ValidationError("Start date must be in the future ❌")

        if start and end and end < start:
            raise forms.ValidationError("End date cannot be before start date ❌")

        return cleaned_data
    
# --------------------
# Manage subjects
# -------------------
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['semester', 'code', 'name']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
        }

class AdminResultForm(forms.ModelForm):
    class Meta:
        model = AdminResult
        fields = ['student_id', 'student_name', 'subject_name', 'out_of_marks', 'r_date', 'faculty_name']




