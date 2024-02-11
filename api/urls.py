from django.urls import path
from .views import signup_and_send_data, signin_and_check_email_verification, reset_password, delete_account, add_cohort, remove_cohort, get_all_cohorts, suspend_student, invitation_teacher, get_student_data_cohort, get_student_data_country, get_student_data_institute, get_student_data_international, get_teacher_cohort

urlpatterns = [
    path('signup_and_send_data/', signup_and_send_data, name='signup_and_send_data'),
    path('signin_and_check_email_verification/', signin_and_check_email_verification, name='signin_and_check_email_verification'),
    path('reset_password/', reset_password, name='reset_password'),
    path('delete_account/', delete_account, name='delete_account'),
    path('add_cohort/', add_cohort, name='add_cohort'),
    path('remove_cohort/', remove_cohort, name='remove_cohort'),
    path('get_all_cohorts/', get_all_cohorts, name='get_all_cohorts'),
    path('suspend_student/', suspend_student, name='suspend_student'),
    path('invitation_teacher/', invitation_teacher, name='invitation_teacher'),
    path('get_student_data_cohort/', get_student_data_cohort, name='get_student_data_cohort'),
    path('get_student_data_country/', get_student_data_country, name='get_student_data_country'),
    path('get_student_data_institute/', get_student_data_institute, name='get_student_data_institute'),
    path('get_student_data_international/', get_student_data_international, name='get_student_data_international'),
    path('get_teacher_cohort/', get_teacher_cohort, name='get_teacher_cohort'),
]