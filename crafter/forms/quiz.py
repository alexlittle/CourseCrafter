from django import forms
from crafter.models import ModuleQuestion, ModuleResponseOption

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')  # Pass questions dynamically
        super().__init__(*args, **kwargs)

        for question in questions:
            choices = [(choice.id, choice.response) for choice in question.questionresponses.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.question,
                choices=choices,
                widget=forms.RadioSelect
            )