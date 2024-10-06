from django.contrib import admin
from .models import  College, Comment,IntellectualProperty, Type, User,Coordinator,Student,\
    IPSimilarityScore,Department,SubType


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Coordinator)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Type)
admin.site.register(Comment)
admin.site.register(IntellectualProperty)
admin.site.register(SubType)

class IPSimilarityScoreAdmin(admin.ModelAdmin):
    list_display = ["doc_source", "doc_target", "score", "remarks", "timestamp"]
    ordering = ["pk"]

admin.site.register(IPSimilarityScore, IPSimilarityScoreAdmin)
