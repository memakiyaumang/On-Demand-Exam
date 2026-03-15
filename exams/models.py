from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

SEMESTER_CHOICES = [
    (1, "Semester 1"),
    (2, "Semester 2"),
    (3, "Semester 3"),
    (4, "Semester 4"),
    (5, "Semester 5"),
    (6, "Semester 6"),
]

# -------------------------
# Custom User
# -------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False)

    # Extra fields for students
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)  

    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
# -------------------------
# Manage Subjects
# -------------------------


class Subject(models.Model):
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.semester})"


# -------------------------
# Exam Duration (Schedule)
# -------------------------
class ExamDuration(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

     # ✅ Generate all dates between start and end
    def get_date_range(self):
        current = self.start_date
        while current <= self.end_date:
            yield current
            current += datetime.timedelta(days=1)

    def __str__(self):
        return f"Exam Duration: {self.start_date} → {self.end_date}"


# -------------------------
# Exam Booking
# -------------------------
class ExamBooking(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name="student_bookings"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    date = models.DateField()

    schedule = models.ForeignKey(
        ExamDuration,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    def __str__(self):
     return f"{self.student.username} → {self.subject.name} on {self.date}"




# -------------------------
# Attendance Sheet
# -------------------------
class AttendanceSheet(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="attendance_sheets"
    )
    date = models.DateField()

    # ✅ AttendanceSheet also tied to a schedule
    schedule = models.ForeignKey(
        ExamDuration,
        on_delete=models.CASCADE,   
        related_name="attendance_sheets"
    )

    bookings = models.ManyToManyField(
        ExamBooking,
        blank=True,
        related_name="attendance_sheets"
    )

    assigned_faculty = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role': 'faculty'},
        related_name="assigned_attendance_sheets"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("subject", "date", "schedule")

    def __str__(self):
        return f"Attendance: {self.subject.name} on {self.date}"
    

class AdminResult(models.Model):
    student_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    r_date = models.DateField()
    out_of_marks = models.CharField(default=0)
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)
    faculty_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student_name} - {self.subject_name} ({self.r_date})"

    class Meta:
        db_table = "admin_results"


class RoomAssignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    room = models.CharField(max_length=20)
    faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomUser, related_name="room_students")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    schedule = models.ForeignKey(
    ExamDuration,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)


class ExamSchedule(models.Model):
    subject = models.ForeignKey(
        'Subject',  # Assuming you have a Subject model
        on_delete=models.CASCADE,
        related_name='exam_schedules'
    )
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)  # optional
    end_time = models.TimeField(null=True, blank=True)    # optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject} on {self.date}"