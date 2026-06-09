from django import forms
from .models import User, WeeklyReport, ReportFeedback, StudentProfile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


# Weekly Report Form (for students)
class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ['week_number', 'tasks_done', 'challenges', 'lessons_learned', 'hours_worked']
        widgets = {
            'tasks_done': forms.Textarea(attrs={'rows': 4}),
            'challenges': forms.Textarea(attrs={'rows': 4}),
            'lessons_learned': forms.Textarea(attrs={'rows': 4}),
        }


# Feedback Form (for lecturers)
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = ReportFeedback
        fields = ['comment', 'grade']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


# Student Profile Form
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['reg_number', 'course', 'year_of_study', 'company_name',
                  'company_location', 'start_date', 'end_date', 'assigned_lecturer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_lecturer'].queryset = User.objects.filter(role='lecturer')
        self.fields['assigned_lecturer'].required = False
        self.fields['assigned_lecturer'].empty_label = "Not assigned yet"


# Register Form
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[('student', 'Student'), ('lecturer', 'Lecturer')])
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']