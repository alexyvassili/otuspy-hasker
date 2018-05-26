from django.contrib import admin

from questions.models import Profile, Question, Answer, Tag


class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Question._meta.fields]
    class Meta:
        model = Question

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Answer._meta.fields]
    class Meta:
        model = Answer

admin.site.register(Answer, AnswerAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tag._meta.fields]
    class Meta:
        model = Tag

admin.site.register(Tag, TagAdmin)
