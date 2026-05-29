from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
path('complete-profile/', views.complete_profile, name='complete_profile'),
    # Auth
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/submit-report/', views.submit_report, name='submit_report'),
    path('student/my-reports/', views.my_reports, name='my_reports'),

    # Lecturer
    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('lecturer/student/<int:student_id>/reports/', views.view_student_reports, name='view_student_reports'),
    path('lecturer/feedback/<int:report_id>/', views.give_feedback, name='give_feedback'),

    # Admin
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]