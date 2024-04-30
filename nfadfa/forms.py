from django import forms

class FiniteAutomatonForm(forms.Form):
    symbols = forms.CharField(label='Symbols', max_length=100, widget=forms.TextInput(attrs={'placeholder': '0 1'}))
    states = forms.CharField(label='States', widget=forms.TextInput(attrs={'placeholder': 'q0 q1 q2'}))
    final_state = forms.CharField(label='Final States', widget=forms.TextInput(attrs={'placeholder': 'q2 q1'}))
    start_state = forms.CharField(label='Start State', widget=forms.TextInput(attrs={'placeholder': 'q0'}))
    transitions = forms.CharField(label='Transitions', widget=forms.Textarea(attrs={'rows': 5, 'cols': 50, 'placeholder': 'q0 0 q1\nq2 1 q1'}))

class RegexForm(forms.Form):
    regex = forms.CharField(label='Regular Expression', widget=forms.TextInput(attrs={'placeholder': 'Please Enter The Correct Regular Expression... (Example : ab(a+b)*)'}))