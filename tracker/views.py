from .forms import LoginForm, WeeklyReportForm, FeedbackForm, RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, WeeklyReportForm, FeedbackForm, RegisterForm
from .models import StudentProfile, WeeklyReport, ReportFeedback, User


# ─── AUTH VIEWS ───────────────────────────────────────────

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'lecturer':
                return redirect('lecturer_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                # No role set — show helpful error
                logout(request)
                return render(request, 'tracker/login.html', {
                    'form': form,
                    'error': 'Your account has no role assigned. Contact admin.'
                })
    return render(request, 'tracker/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = form.cleaned_data['role']
        user.save()
       
        if user.role == 'student':
            login(request, user)
            return redirect('complete_profile')
        else:
            login(request, user)
            return redirect('lecturer_dashboard')
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def complete_profile(request):
    if StudentProfile.objects.filter(user=request.user).exists():
        return redirect('student_dashboard')
    
    form = StudentProfileForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect('student_dashboard')
    return render(request, 'tracker/complete_profile.html', {'form': form})

# ─── STUDENT VIEWS ────────────────────────────────────────

@login_required
def student_dashboard(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    reports = WeeklyReport.objects.filter(student=profile).order_by('-week_number')
    return render(request, 'tracker/student_dashboard.html', {
        'profile': profile,
        'reports': reports
    })


@login_required
def submit_report(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    form = WeeklyReportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        report = form.save(commit=False)
        report.student = profile
        report.save()
        return redirect('my_reports')
    return render(request, 'tracker/submit_report.html', {'form': form})


@login_required
def my_reports(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    reports = WeeklyReport.objects.filter(student=profile).order_by('-date_submitted')
    return render(request, 'tracker/my_reports.html', {'reports': reports})


# ─── LECTURER VIEWS ───────────────────────────────────────

@login_required
def lecturer_dashboard(request):
    students = StudentProfile.objects.filter(assigned_lecturer=request.user)
    return render(request, 'tracker/lecturer_dashboard.html', {'students': students})


@login_required
def view_student_reports(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    reports = WeeklyReport.objects.filter(student=student).order_by('-week_number')
    return render(request, 'tracker/student_reports.html', {
        'student': student,
        'reports': reports
    })


@login_required
def give_feedback(request, report_id):
    report = get_object_or_404(WeeklyReport, id=report_id)
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        feedback.report = report
        feedback.lecturer = request.user
        feedback.save()
        return redirect('view_student_reports', student_id=report.student.id)
    return render(request, 'tracker/give_feedback.html', {
        'form': form,
        'report': report
    })


# ─── ADMIN VIEWS ──────────────────────────────────────────

@login_required
def admin_dashboard(request):
    students = StudentProfile.objects.all()
    lecturers = User.objects.filter(role='lecturer')
    return render(request, 'tracker/admin_dashboard.html', {
        'students': students,
        'lecturers': lecturers
    })