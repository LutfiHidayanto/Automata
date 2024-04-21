from django.shortcuts import render
from .Automata import NFA, ENFA, DFA
import os
from django.conf import settings
from .forms import FiniteAutomatonForm

# Create your views here.

BASE_DIR = 'nfadfa/'

MEDIA_DIR = 'nfadfa/static/nfadfa/media'

MEDIA_STATIC_DIR = 'nfadfa/media'

FA_dict = {'nfa': 'nfa'}



def index(request):
    return render(request, BASE_DIR + 'index.html')


def nfa_to_dfa(request):
    nfa = None
    dfa = None
    image_path = None
    form = FiniteAutomatonForm()
    graph_path = dict()

    if request.method == 'POST':
        form = FiniteAutomatonForm(request.POST)
        if form.is_valid():
            symbols = form.cleaned_data['symbols'].split(' ')
            states = form.cleaned_data['states'].split(' ')
            states = set(states)
            final_states = form.cleaned_data['final_state'].split(' ')
            start_state = str(form.cleaned_data['start_state'])
            transitions_input = form.cleaned_data['transitions'].split('\n')

            # Initialize an empty list to store tuples
            transition_functions = []

            # Iterate over each line of transitions input
            for line in transitions_input:
                # Split the line by comma
                transition = line.strip().split(' ')
                # Convert each element to tuple and append to the list
                transition_functions.append(tuple(transition))

            print(symbols, states, final_states, start_state, transition_functions)

            states = sorted(states)
            enfa = ENFA()
            enfa.initFa(states=states, symbols=symbols, start_state=start_state, final_state=final_states,transition_functions=transition_functions)

            enfa.init_transitions()

            image_path = MEDIA_DIR + '/enfa_graph'
            enfa.create_graph()
            enfa.print_graph(filename=image_path)
            graph_path['enfa'] = MEDIA_STATIC_DIR + '/enfa_graph.png'
            # print("ENFA")
            # enfa.print_automaton()

            # convert to nfa
            nfa = NFA()
            nfa = enfa.convert_to_nfa()
            image_path = MEDIA_DIR + '/nfa_graph'
            nfa.create_graph()
            nfa.print_graph(filename=image_path)
            graph_path['nfa'] = MEDIA_STATIC_DIR + '/nfa_graph.png'

            print("NFA")
            nfa.print_automaton()

            # convert to dfa
            dfa = DFA()
            dfa.convert_from_nfa(nfa)
            dfa.create_graph()
            image_path = MEDIA_DIR + '/dfa_graph'
            dfa.print_graph(filename=image_path)
            graph_path['dfa'] = MEDIA_STATIC_DIR + '/dfa_graph.png'

            print("DFA")
            dfa.print_automaton()

            # print(graph_path)

            # Create and save the NFA graph image

    return render(request, BASE_DIR + 'nfa2dfa.html', {'form': form, 'enfa': nfa, 'nfa': nfa, 'dfa': dfa, 'graph_path': graph_path})