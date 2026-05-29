from django import forms
from .models import WeeklyReport, ReportFeedback, StudentProfile
from django.contrib.auth.forms import AuthenticationForm


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


# Student Profile Form (for admin)
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['reg_number', 'course', 'year_of_study', 'company_name',
                  'company_location', 'start_date', 'end_date', 'assigned_lecturer']