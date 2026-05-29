from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model (handles all 3 roles)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Student Profile (extra info for students)
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    year_of_study = models.IntegerField()
    company_name = models.CharField(max_length=100)
    company_location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_lecturer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_students'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.reg_number}"


# Weekly Report submitted by student
class WeeklyReport(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    week_number = models.IntegerField()
    tasks_done = models.TextField()
    challenges = models.TextField()
    lessons_learned = models.TextField()
    hours_worked = models.IntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Week {self.week_number} - {self.student}"


# Feedback given by lecturer on a report
class ReportFeedback(models.Model):
    report = models.OneToOneField(WeeklyReport, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    grade = models.CharField(max_length=5)  # e.g. A, B+, C
    date_reviewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.report}"