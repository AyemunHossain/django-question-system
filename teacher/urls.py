from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

app_name = "teacher"

urlpatterns = [
path('click', views.teacherclick_view),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('teacher-add-viva', views.teacher_add_viva_view,name='teacher-add-viva'),
path('teacher-view-viva', views.teacher_view_viva_view,name='teacher-view-viva'),
path('teacher-evaluate-viva', views.teacher_evaluate_viva_view,name='teacher-evaluate-viva'),
path('teacher-evaluate/<int:pk>', views.evaluate_viva_exam_view,name='teacher-evaluate-viva_question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('see-viva-question/<int:pk>', views.see_viva_question_view,name='see-viva-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
path('student-exam', views.student_exam_view,name='student-exam'),
path('student-viva-exam', views.student_viva_exam_view,name='student-viva-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),
path('start-viva-exam/<int:pk>', views.start_viva_exam_view,name='start-viva-exam'),
path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('check-viva-marks-view/<int:pk>', views.check_viva_marks_view,name='check-viva-marks'),

path('student-marks', views.student_marks_view,name='student-marks'),

]