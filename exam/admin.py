from django.contrib import admin
from exam.models import Course,Question,Result,Viva, VivaResult
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Viva)
admin.site.register(VivaResult)

# Register your models here.
