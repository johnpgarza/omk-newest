from django import forms
from .models import User, Session_Schedule,remark,Student,Mentor


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class SignUpForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if user.is_staff:
                user_role = "Staff"

            else:
                user_role = "Mentor"
            raise forms.ValidationError(
                "{} with this email already exists, use another email.".format(
                    user_role
                )
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError("Password should be minimum 6 characters long")

        if password != self.data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return password


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session_Schedule
        fields = ('session_name', 'session_location')


class EmailForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class EmailClassForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    to = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class RemarkForm(forms.ModelForm):
    # remark_notes= forms.CharField(widget=forms.Textarea, required=True)
    class Meta:

        model = remark
        fields = ('remark_notes',)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('school', 'grade', 'created_date', 'updated_date')


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        exclude = ('created_date', 'updated_date')
class StudentaddForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ()
class MentoraddForm(forms.ModelForm):
    class Meta:
        model = Mentor
        exclude = ()


