from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.db import connection
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404
from .forms import *
from sma.models import Session_Schedule, Student, Student_Group_Mentor_Assignment, Grade, Attendance, remark, Mentor


# Create your views here.

def staffSignup(request):
    if request.method == "GET":
        return render(request, "staff_signup.html", {})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
                is_staff=True, role='staff'
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect(reverse('home', ))
        else:
            return render(
                request, "staff_signup.html", {"errors": form.errors}
            )


def mentorSignup(request):
    if request.method == "GET":
        return render(request, "mentor_signup.html", {})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
                is_mentor=True, role="mentor",
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect(reverse('home', ))
        else:
            return render(
                request, "mentor_signup.html", {"errors": form.errors}
            )


def mentorLogin(request):
    if request.method == "GET":
        return render(request, "mentor_login.html", {})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password, )
            if user is None:
                return render(
                    request,
                    "mentor_login.html",
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_mentor:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home', ))
                elif user.is_active and user.is_mentor is False:
                    return render(
                        request,
                        "mentor_login.html",
                        {
                            "errors": {
                                "account_error": ["Email is not associated with Mentor"]
                            }
                        },
                    )

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

            else:
                pass
        else:
            return render(request, "mentor_login.html", {"errors": form.errors})


def staffLogin(request):
    if request.method == "GET":
        return render(request, "staff_login.html", {})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password, )
            if user is None:
                return render(
                    request,
                    "staff_login.html",
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home', ))
                elif user.is_active and user.is_mentor is False:
                    return render(
                        request,
                        "staff_login.html",
                        {
                            "errors": {
                                "account_error": ["Email is not associated with Staff"]
                            }
                        },
                    )

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

            else:
                pass
        else:
            return render(request, "staff_login.html", {"errors": form.errors})


def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'GET':
        return render(request, "password_change_form.html", {"form": form})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(
                request, "password_change_done.html", {}
            )
        return render(
            request, "password_change_form.html", {"errors": form.errors}
        )


def homepage(request):
    return render(request, "landing_page.html", {})


def user_logout(request):
    logout(request)
    return redirect(reverse('home'))


def session_list(request):
    # Jgarza 4/11/2020
    # removed session_start_date__lte=timezone.now() because it would not display future sessions.
    session = Session_Schedule.objects.all()
    return render(request, 'session_list.html', {'session_list': session})


def session_details(request, pk):
    session = Session_Schedule.objects.get(pk=pk)
    group = Student_Group_Mentor_Assignment.objects.get(pk=pk)
    grade = Grade.objects.get(pk=pk)
    students = Student.objects.filter(grade=grade)
    attendance=Attendance.objects.get(pk=pk)
    return render(request, 'session_details.html', {'session': session, 'group': group, 'students': students,
                                                    'grade': grade,'attendance':attendance})


# Jgarza 3/27/2020
# Created email form view
def email_form(request):
    if request.method == 'GET':
        form = EmailForm()
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['jgarza@unomaha.edu'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email_form.html", {'form': form})


# JGarza 4/11/2020
# Added email the class
def email_class_form(request, grade):
    students = list(Student.objects.filter(grade=grade).values_list('student_email', flat=True))
    if request.method == 'GET':
        form = EmailClassForm(initial={'to': students})
    else:
        form = EmailClassForm(request.POST,)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, students)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email_class_form.html", {'form': form, 'class': students})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')

def review_form(request, pk1,pk2):
    student = get_object_or_404(Student, pk=pk2)
    session = get_object_or_404(Session_Schedule, pk=pk1)
    # mentor=get_object_or_404(Mentor,pk=request.user.id)
    if request.method == 'GET':
        form = RemarkForm()



        return render(request, 'remark_new.html', {'form': form,'session':session,'student':student})
    if request.method == 'POST':
        form = RemarkForm(request.POST)

        if form.is_valid():
            user=get_object_or_404(User, pk=request.user.id)
            print(user)
            review = form.save(commit=False)
            # review.save(instance=student)
            # review.save(instance=session)
            # review.save(instance=mentor)

            review.remark_student_id = get_object_or_404(Student, pk=pk2)
            review.remark_mentor_id = get_object_or_404(User, pk=request.user.id)
            review.remark_session_ID = get_object_or_404(Session_Schedule, pk=pk1)
            review.save()
            print('here')
            session = Session_Schedule.objects.all()
            return render(request, 'session_list.html', {'session_list': session})



def review_class_form(request,pk1,pk2):
    form= RemarkForm(request.POST)
    student = get_object_or_404(Student, pk=pk2)
    session = get_object_or_404(Session_Schedule, pk=pk1)
    # if form.is_valid():
    review=form.save(commit=False)
    # review.remark_student_id=student.id
    # review.remark_mentor_id=request.user.id
    # review.remark_session_ID=session.id
    review.save()
    print('here')
    session = Session_Schedule.objects.all()
    return render(request, 'session_list.html', {'session_list': session})


def mentor_student_list_view(request,user_type):
    if user_type == 'students':
        students_list = Student.objects.all()
        return render(request, 'mentor_student_list_page.html', {'list_info': students_list,'user_type':user_type})
    elif user_type == 'mentors':
        mentors_list = Mentor.objects.all()
        return render(request, 'mentor_student_list_page.html', {'list_info': mentors_list,'user_type':user_type})

def edit_student_or_mentor(request,user_type,user_id):
    if user_type == 'students':
        student_data = get_object_or_404(Student, pk=user_id)
        if request.method == "GET":
            form=StudentForm(instance=student_data)
            return render(request,'student_mentor_data_edit.html',{'form':form})
        if request.method == "POST":
            form = StudentForm(request.POST, instance=student_data)
            if form.is_valid():
                form.save()
            else:
                form=StudentForm(instance=student_data)
                return render(request,'student_mentor_data_edit.html',{'form':form})
    elif user_type == 'mentors':
        mentor_data = get_object_or_404(Mentor, pk=user_id)
        if request.method == "GET":
            form=MentorForm(instance=mentor_data)
            return render(request,'student_mentor_data_edit.html',{'form':form})
        if request.method == "POST":
            form = MentorForm(request.POST, instance=mentor_data)
            if form.is_valid():
                form.save()
            else:
                form=MentorForm(instance=mentor_data)
                return render(request,'student_mentor_data_edit.html',{'form':form})
    return redirect(reverse('mentor_student_list_view', kwargs={'user_type':user_type}))


def delete_student_or_mentor(request,user_type,user_id):
    if user_type == 'students':
        student = get_object_or_404(Student, pk=user_id)
        student.delete()
    elif user_type == 'mentors':
        mentor = get_object_or_404(Mentor, pk=user_id)
        mentor.delete()
    return redirect(reverse('mentor_student_list_view', kwargs={'user_type':user_type}))

def add_student_or_mentor(request,user_type):
    if user_type == 'students':

        if request.method == "GET":
            form=StudentaddForm()
            return render(request,'student_add.html',{'form':form})
        if request.method == "POST":
            form = StudentaddForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form=StudentaddForm()
                return render(request,'student_add.html',{'form':form})
    elif user_type == 'mentors':

        if request.method == "GET":
            form=MentorForm()
            return render(request,'student_add.html',{'form':form})
        if request.method == "POST":
            form = MentoraddForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form=MentoraddForm()
                return render(request,'student_add.html',{'form':form})
    return redirect(reverse('mentor_student_list_view', kwargs={'user_type':user_type}))




from django.http import HttpResponse
from django.views.generic import View
from sma.utils import render_to_pdf
from django.template.loader import get_template

def mentor_summary_pdf(request):
    mentors = Mentor.objects.all()
    context = {'mentors': mentors,}
    template = get_template('mentor_summary_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('mentor_summary_pdf.html', context)
    return pdf

def student_summary_pdf(request):
    students = Student.objects.all()
    context = {'students': students,}
    template = get_template('student_summary_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('student_summary_pdf.html', context)
    return pdf