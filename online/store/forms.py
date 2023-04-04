from django import forms
from django.core.validators import EmailValidator


class GameSearchForm(forms.Form):
    game_name = forms.CharField(
        max_length=50, help_text="Enter searched", widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class DateSearchForm(forms.Form):
    date = forms.DateField(help_text="Enter login")

    def clean_date(self):
        import datetime

        date = self.cleaned_data["date"]
        if date < datetime.date(1990, 1, 1):
            raise forms.ValidationError("Date must be greater than 1990-01-01")
        return date
