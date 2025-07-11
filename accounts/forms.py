from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, MemberProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Custom help text
        self.fields['username'].help_text = 'Choose a unique username (letters, digits and @/./+/-/_ only).'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['company', 'position', 'linkedin_url', 'website', 'skills', 'interests']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
class UserProfileForm(forms.ModelForm):
    """Form for editing basic user information"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'bio', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 (555) 123-4567'}),
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name != 'profile_picture':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Custom labels and help text
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'your.email@company.com'
        self.fields['phone'].help_text = 'Optional. Format: +1 (555) 123-4567'
        self.fields['profile_picture'].help_text = 'Upload a professional photo (optional)'

class MemberProfileForm(forms.ModelForm):
    """Form for editing member profile information"""
    class Meta:
        model = MemberProfile
        fields = ['company', 'position', 'linkedin_url', 'website', 'skills', 'interests']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Roll Design, Steel Processing, CAD, Project Management...'}),
            'interests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Metallurgy, Manufacturing Innovation, Quality Control...'}),
            'company': forms.TextInput(attrs={'placeholder': 'Your Company Name'}),
            'position': forms.TextInput(attrs={'placeholder': 'Your Job Title'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://your-website.com'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Help text
        self.fields['linkedin_url'].help_text = 'Your LinkedIn profile URL (optional)'
        self.fields['website'].help_text = 'Your personal or company website (optional)'
        self.fields['skills'].help_text = 'List your professional skills and expertise'
        self.fields['interests'].help_text = 'Your professional interests and areas of focus'

class PasswordChangeFormCustom(forms.Form):
    """Custom password change form"""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
        label='Current Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password',
        help_text='Your password must contain at least 8 characters.'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label='Confirm New Password'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Your current password is incorrect.')
        return current_password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields didn\'t match.')
        return password2
    
    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user