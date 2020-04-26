from django.contrib import admin
from .models import School, Grade, Student, Mentor, Student_Group_Mentor_Assignment, Session_Schedule, Attendance, User, remark


# Register your models here.
class UserList(admin.ModelAdmin):
    list_display = ('email','username','is_active','created_on','role','is_staff','is_mentor')
    list_filter = ('email','username','is_active','created_on','role','is_staff','is_mentor')
    search_fields = ('email','username','is_active','created_on','role','is_staff','is_mentor')
    ordering = ['email']

class SchoolList(admin.ModelAdmin):
    list_display = ('school_name', 'school_email', 'school_phone')
    list_filter = ('school_name', 'school_email')
    search_fields = ('school_name',)
    ordering = ['school_name']


class GradeList(admin.ModelAdmin):
    list_display = ['grade_num']
    list_filter = ['grade_num']
    search_fields = ['grade_num']
    ordering = ['grade_num']


class StudentList(admin.ModelAdmin):
    list_display = ('student_first_name', 'student_middle_name', 'student_last_name', 'school', 'grade')
    list_filter = ('student_first_name', 'student_last_name', 'school', 'grade')
    search_fields = ('student_first_name', 'student_last_name', 'school', 'grade')
    ordering = ['student_first_name']


class MentorList(admin.ModelAdmin):
    list_display = ('mentor_first_name', 'mentor_middle_name', 'mentor_last_name', 'mentor_email', 'mentor_phone')
    list_filter = ('mentor_first_name', 'mentor_middle_name', 'mentor_last_name', 'mentor_email', 'mentor_phone')
    search_fields = ('mentor_first_name', 'mentor_middle_name', 'mentor_last_name', 'mentor_email', 'mentor_phone')
    ordering = ['mentor_first_name']


class GroupMentorAssignmentList(admin.ModelAdmin):
    list_display = ('group_name', 'school', 'grade', 'mentor')
    list_filter = ('group_name', 'school', 'grade', 'mentor')
    search_fields = ('group_name', 'school', 'grade', 'mentor')
    ordering = ['group_name']


class SessionScheduleList(admin.ModelAdmin):
    list_display = ('session_name', 'session_location', 'mentor', 'group', 'session_start_date', 'session_end_date')
    list_filter = ('session_name', 'session_location', 'mentor', 'group', 'session_start_date', 'session_end_date')
    search_fields = ('session_name', 'session_location', 'mentor', 'group', 'session_start_date', 'session_end_date')
    ordering = ['session_name']

class remarkList(admin.ModelAdmin):
    list_display = ('remark_notes','remark_student_id', 'remark_mentor_id')




class AttendanceList(admin.ModelAdmin):
    list_display = (
        'attendance_student_id', 'attendance_grade_id', 'attendance_mentor_id', 'attendance_session_ID',
        'attendance_ID')
    list_filter = (
        'attendance_student_id', 'attendance_grade_id', 'attendance_mentor_id', 'attendance_session_ID',
        'attendance_ID')
    search_fields = (
        'attendance_student_id', 'attendance_grade_id', 'attendance_mentor_id', 'attendance_session_ID',
        'attendance_ID')
    ordering = ['attendance_session_ID']

admin.site.register(User,UserList)
admin.site.register(School, SchoolList)
admin.site.register(Grade, GradeList)
admin.site.register(Student, StudentList)
admin.site.register(Mentor, MentorList)
admin.site.register(Student_Group_Mentor_Assignment, GroupMentorAssignmentList)
admin.site.register(Session_Schedule, SessionScheduleList)
admin.site.register(Attendance, AttendanceList)
admin.site.register(remark,remarkList)
