from django.views.decorators.cache import cache_page
from django.urls import path
from .views import StudentRegistrationView, StudentEnrollCourseView, \
    StudentCourseListView, StudentCourseDetailView, StudentProfilePageView, profile_update

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(),
         name='student_registration'),

    path('enroll-course/', StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),

    path('courses/',
         StudentCourseListView.as_view(),
         name='student_course_list'),

    # This urls would be used when cache isn't needed
    # path('course/<pk>/',
    #      StudentCourseDetailView.as_view(),
    #      name='student_course_detail'),
    #
    # path('course/<pk>/<module_id>/',
    #      StudentCourseDetailView.as_view(),
    #      name='student_course_detail_module'),

    path('course/<pk>/', cache_page(60 * 15)(StudentCourseDetailView.as_view()),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/', cache_page(60 * 15)(StudentCourseDetailView.as_view()),
         name='student_course_detail_module'),

    path('<int:pk>/<username>/profile/', StudentProfilePageView.as_view(template_name='students/student/profile.html'),
         name='profile'),
    path('<username>/profile-update/', profile_update, name='profile_update'),
]