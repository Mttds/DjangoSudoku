from django import forms
from .models import Score
import datetime

class ScoreForm(forms.ModelForm): # derived class from django's ModelForm class
    sudoku = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder":"........","class":"new-class-name"}
        )
    ) # forms don't have a TextField so we do it with a widget
    num_moves  = forms.IntegerField()
    solution   = forms.CharField(widget=forms.Textarea)
    solved     = forms.BooleanField()
    solve_time = forms.DurationField()
    run_date   = forms.DateTimeField(initial=datetime.datetime.now())
    class Meta:
        model = Score
        fields = [
            'sudoku',
            'num_moves',
            'solution',
            'solved',
            'solve_time',
            'run_date'
        ]
    # overrides the method clean_<field_name> of ModelForm
    # which is aware of our datamodel. Added for extra input validation
    def clean_sudoku(self, *args, **kwargs):
        sudoku = self.cleaned_data.get("sudoku")
        if('.' not in sudoku):
            raise forms.ValidationError("The initial sudoku needs at least an empty cell represented by \".\"")
        return sudoku
            

class RawScoreForm(forms.Form): # derived from standard django's Form class
    sudoku = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder":"........","class":"new-class-name"}
        )
    ) # forms don't have a TextField so we do it with a widget
    num_moves  = forms.IntegerField()
    solution   = forms.CharField(widget=forms.Textarea)
    solved     = forms.BooleanField()
    solve_time = forms.DurationField()
    run_date   = forms.DateTimeField(initial=datetime.datetime.now())