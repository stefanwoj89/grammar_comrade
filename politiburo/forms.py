from django import forms

class ReviewForm(forms.Form):
    comment = forms.CharField(max_length=1000)
    score = forms.IntegerField()
