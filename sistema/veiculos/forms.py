from django.forms import ModelForm, DateInput, TimeInput
from .models import Evento, SetMusical
import datetime


class FormularioEvento(ModelForm):
    class Meta:
        model = Evento
        exclude = []
        widgets = {
            'data': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'hora': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['data'].initial = datetime.date.today()
            self.fields['hora'].initial = datetime.datetime.now().strftime('%H:%M')


class FormularioSet(ModelForm):
    class Meta:
        model = SetMusical
        exclude = []
        widgets = {
            'data': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['data'].initial = datetime.date.today()
