from django import forms

from app.models import Profile, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']  # Only description field for the comment
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'Написать комментарий...',
                'class': 'form-control'
            }),
        }