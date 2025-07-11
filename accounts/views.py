from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser, MemberProfile
from .forms import (
    CustomUserCreationForm, 
    UserProfileForm, 
    MemberProfileForm, 
    PasswordChangeFormCustom
)

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after registration
        login(self.request, self.object)
        # Create member profile
        MemberProfile.objects.create(user=self.object)
        messages.success(self.request, 'Welcome to IRD! Your account has been created successfully.')
        return response

@login_required
def profile(request):
    """User profile view"""
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Edit user profile"""
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = MemberProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = MemberProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeFormCustom(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeFormCustom(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def delete_profile_picture(request):
    """Delete user's profile picture"""
    if request.method == 'POST':
        if request.user.profile_picture:
            request.user.profile_picture.delete()
            request.user.save()
            messages.success(request, 'Profile picture removed successfully!')
        else:
            messages.info(request, 'No profile picture to remove.')
    return redirect('accounts:edit_profile')