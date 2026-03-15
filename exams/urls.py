from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),   # ✅ this is the first page
    path("student/login/", views.student_login, name="student_login"),
     path("student/logout/", views.student_logout, name="student_logout"),
    path("student/register/", views.student_register, name="student_register"),
    path("student/dashboard", views.student_dashboard, name="student_dashboard"),
    path("student/exam-dates/", views.get_exam_dates, name="get_exam_dates"),   
    path('student/results/', views.view_results, name='student_results'),
    
    path("admin-login/", views.admin_login, name="admin_login"),
     path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("faculty/register/", views.faculty_register, name="faculty_register"),
    path("faculty/login/", views.faculty_login, name="faculty_login"),
    path("faculty/manage/", views.manage_faculty, name="manage_faculty"),

    path("faculty/dashboard/", views.faculty_dashboard, name="faculty_dashboard"),
    path("faculty/logout/", views.faculty_logout, name="faculty_logout"),
    path("faculty/subject/<int:sheet_id>/", views.subject_detail, name="subject_detail"),

    path('subjects/', views.manage_subjects, name='manage_subjects'),
    path('subjects/edit/<int:pk>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:pk>/', views.delete_subject, name='delete_subject'),

    path("set-schedule/", views.set_schedule, name="set_schedule"),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),


    path('attendance/', views.attendance_selector, name='attendance_selector'),
    path('attendance/show/', views.attendance_show, name='attendance_show'),
    path("attendance/export-word/<int:sheet_id>/", views.attendance_export_word, name="attendance_export_word"),


    path("add-result/", views.add_result, name="add_result"),
    path("manage-result/", views.manage_result, name="manage_result"),
    path("edit-result/<int:pk>/", views.edit_result, name="edit_result"),
    path("delete-result/<int:pk>/", views.delete_result, name="delete_result"),
    

    path('create-schedule/', views.create_schedule, name='create_schedule'),
    path("assigned-rooms/", views.assigned_rooms, name="assigned_rooms"),


    path('schedule/<int:schedule_id>/update/', views.update_schedule, name='update_schedule'),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule_room, name='delete_schedule'),

    path('student/assigned-rooms/', views.student_assigned_rooms, name='student_assigned_rooms'),

]

  
