from django import forms
from .models import Comment, Stage, Request, RequestHistory

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ('title',)

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'description', 'url',  'method',  'header',  'queryParameters',  'body', )

class RequestHistoryForm(forms.ModelForm):
    class Meta:
        model = RequestHistory
        fields = ()