from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course
from .forms import CourseEnrollForm, ProfileUpdateForm, StudentUpdateForm
from .models import Profile


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'

    # This can be excluded if no email is required @ the signup page.
    # StudentRegistrationForm should also be excluded @ forms.py
    # form_class = UserCreationForm

    form_class = StudentRegistrationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context


@login_required
def profile_update(request, *args, **kwargs):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your Profile has been Updated!')
            return redirect('student_course_list')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'students/student/profile_update.html',
                  {'p_form': p_form})


@login_required
def account_mgt(request):
    if request.method == 'POST':
        u_form = StudentUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('student_course_list')
    else:
        u_form = StudentUpdateForm(instance=request.user)
    return render(request, 'students/student/account.html', {'u_form': u_form})


class StudentProfilePageView(LoginRequiredMixin, DetailView):
    model = Profile

    def get_context_data(self, *args, **kwargs):
        context = super(StudentProfilePageView, self).get_context_data(**kwargs)
        student = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['student'] = student
        return context
