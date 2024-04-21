from django import forms

class FiniteAutomatonForm(forms.Form):
    symbols = forms.CharField(label='Symbols', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter symbols separated by comma'}))
    states = forms.CharField(label='States', widget=forms.TextInput(attrs={'placeholder': 'Enter state names separated by space'}))
    final_state = forms.CharField(label='Final States', widget=forms.TextInput(attrs={'placeholder': 'Enter final states separated by comma'}))
    start_state = forms.CharField(label='Start State', widget=forms.TextInput(attrs={'placeholder': 'Enter start state'}))
    transitions = forms.CharField(label='Transitions', widget=forms.Textarea(attrs={'rows': 5, 'cols': 50, 'placeholder': 'Enter transitions in the format: start_state, symbol, end_state'}))
