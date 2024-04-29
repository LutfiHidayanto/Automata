from django.shortcuts import render
from nfadfa.utils.Automata import NFA, ENFA, DFA
from .utils.Regex import *
from .forms import FiniteAutomatonForm, RegexForm
from .utils import MinimizeDfa
from .utils import TestFa
from django.http import HttpResponse


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
    enfa_table = None
    nfa_table = None
    dfa_table = None
    form = FiniteAutomatonForm()
    graph_path = dict()

    if request.method == 'POST':
        form = FiniteAutomatonForm(request.POST)
        if form.is_valid():
            try:
                symbols = form.cleaned_data['symbols'].split(' ')
                states = form.cleaned_data['states'].split(' ')
                states = set(states)
                final_states = form.cleaned_data['final_state'].split(' ')
                start_state = str(form.cleaned_data['start_state'])
                transitions_input = form.cleaned_data['transitions'].split('\n')

                # Initialize an empty list to store tuples
                transition_functions = []

                for line in transitions_input:
                    transition = line.strip().split(' ')
                    transition_functions.append(tuple(transition))

                print(symbols, states, final_states, start_state, transition_functions)

                states = sorted(states)
                enfa = ENFA()
                enfa.initFa(states=states, symbols=symbols, start_state=start_state, final_state=final_states,transition_functions=transition_functions)

                enfa.init_transitions()
                enfa_table = enfa.create_transition_table()

                image_path = MEDIA_DIR + '/enfa_graph'
                enfa.create_graph()
                enfa.print_graph(filename=image_path)
                graph_path['enfa'] = MEDIA_STATIC_DIR + '/enfa_graph.png'
                # print("ENFA")
                # enfa.print_automaton()

                # convert to nfa
                nfa = NFA()
                nfa = enfa.convert_to_nfa()
                nfa.init_transitions()
                nfa_table = nfa.create_transition_table()

                image_path = MEDIA_DIR + '/nfa_graph'
                nfa.create_graph()
                nfa.print_graph(filename=image_path)
                graph_path['nfa'] = MEDIA_STATIC_DIR + '/nfa_graph.png'

                print("NFA")
                nfa.print_automaton()

                # convert to dfa
                dfa = DFA()
                dfa.convert_from_nfa(nfa)
                dfa.init_transitions()
                dfa_table = dfa.create_transition_table()
                dfa.create_graph()
                image_path = MEDIA_DIR + '/dfa_graph'
                dfa.print_graph(filename=image_path)
                graph_path['dfa'] = MEDIA_STATIC_DIR + '/dfa_graph.png'

                print("DFA")
                dfa.print_automaton()
            except Exception as e:
                return HttpResponse("Input Error", status=400)



    context = {'form': form,
               'enfa': nfa,
               'nfa': nfa,
               'dfa': dfa,
               'graph_path': graph_path,
               'enfa_table': enfa_table,
               'nfa_table': nfa_table,
               'dfa_table': dfa_table
               }
    return render(request, BASE_DIR + 'nfa2dfa.html', context)

def regex_to_enfa(request):
    form = RegexForm()
    graph_path = None
    transition_table = None
    if request.method == 'POST':
        form = RegexForm(request.POST)
        if form.is_valid():
            regex = form.cleaned_data['regex']
            print(regex)
            post_fix = postfix(regex)
            print(post_fix)
            tree = constructTree(post_fix)

            fa = evalRegex(tree)

            transition_func = getStateTransitions(fa[0], [], {fa[0]: 0})
            print(transition_func)

            states = []
            symbols = []
            transition_dict = {}
            for transition in transition_func:
                state = transition[0]
                next_state = transition[2]
                symbol = transition[1]

                if state not in states:
                    states.append(state)
                if next_state not in states:
                    states.append(next_state)
                if symbol not in symbols:
                    symbols.append(symbol)

                transition_dict[(state, symbol)] = next_state

            states = sorted(states)
            symbols = sorted(symbols)

            header = ["State"] + symbols
            transition_table = []

            transition_table.append(header)

            for state in states:
                current_state_table = [state]
                for symbol in symbols:
                    try:
                        next_state = transition_dict[(state, symbol)]
                        current_state_table.append(next_state)
                    except KeyError:
                        current_state_table.append('-')
                transition_table.append(current_state_table)

            print(transition_table)


            image_path = MEDIA_DIR + '/regex2e_nfa'
            visualizeTransition(fa, filename=image_path)

            graph_path = MEDIA_STATIC_DIR + '/regex2e_nfa.png'

    context = {'form': form,
               'graph_path': graph_path,
               'transition_table': transition_table}
    return render(request, BASE_DIR + 'regex2enfa.html',
                  context)

def minimize_dfa(request):
    form = FiniteAutomatonForm()
    graph_path = None
    transition_table = None
    if request.method == 'POST':
        form = FiniteAutomatonForm(request.POST)
        if form.is_valid():
            symbols = form.cleaned_data['symbols'].split(' ')
            states = form.cleaned_data['states'].split(' ')
            states = set(states)
            final_states = form.cleaned_data['final_state'].split(' ')
            start_state = str(form.cleaned_data['start_state'])
            transitions_input = form.cleaned_data['transitions'].split('\n')

            transition_functions = []
            transition_dict = {}

            for line in transitions_input:
                transition = line.strip().split(' ')
                state = transition[0]
                symbol = transition[1]
                next_state = transition[2]
                transition_functions.append(tuple(transition))

                transition_dict[(state, symbol)] = next_state

            graph_path = {}

            dfa = MinimizeDfa.DFA(states, set(symbols), transition_dict, start_state, set(final_states))

            image_path = MEDIA_DIR + '/not_minimized_dfa'
            graph_path['before'] = MEDIA_STATIC_DIR + '/not_minimized_dfa.png'
            MinimizeDfa.visualize(dfa.states, dfa.alphabet, dfa.transitions, dfa.start, dfa.finals, image_path)

            dfa.minimize()
            image_path = MEDIA_DIR + '/minimized_dfa'
            graph_path['after'] = MEDIA_STATIC_DIR + '/minimized_dfa.png'
            print(graph_path['after'])
            MinimizeDfa.visualize(dfa.states, dfa.alphabet, dfa.transitions, dfa.start, dfa.finals, image_path)

    context = {
        'form': form,
        'graph_path': graph_path,
        'transition_table': transition_table
    }
    return render(request, BASE_DIR + '/minimize_dfa.html', context)

def test_fa(request):
    if request.method == 'POST':
        pass
    return render(request, BASE_DIR + '/test_fa.html')

def test_fa_details(request, name):
    form = None
    graph_path = None
    transition_table = None
    type = name
    accepted = None
    if name == 'DFA' or name == 'NFA' or name == 'E-NFA':
        form = FiniteAutomatonForm()
    else:
        form = RegexForm()
    if request.method == 'POST':
        # fa expression submitted
        if type == 'Regex':
            form = RegexForm(request.POST)
            if form.is_valid():
                regex = form.cleaned_data['regex'].strip()
                try:
                    pr = TestFa.Regex.postfix(regex)
                    et = TestFa.Regex.constructRegex(pr)
                    fa = TestFa.Regex.evalRegex(et)
                    start_state = fa[0]
                    input_string = request.POST['string_test']
                    print(input_string)
                    if TestFa.Regex.simulateNFA(input_string, start_state):
                        print(f"'{input_string}' is ACCEPTED by the Regular Expression.")
                        accepted = True
                    else:
                        print(f"'{input_string}' is REJECTED by the Regular Expression.")
                        accepted = False
                except Exception as e:
                    return HttpResponse('Error evaluating the regular expression.', status=403)
        else:
            form = FiniteAutomatonForm(request.POST)
            if form.is_valid():
                symbols = form.cleaned_data['symbols'].split(' ')
                states = form.cleaned_data['states'].split(' ')
                states = set(states)
                final_states = form.cleaned_data['final_state'].split(' ')
                start_state = str(form.cleaned_data['start_state'])
                transitions_input = form.cleaned_data['transitions'].split('\n')

                transition_dict = {}

                for line in transitions_input:
                    transition = line.strip().split(' ')
                    state = transition[0]
                    symbol = transition[1]
                    next_state = transition[2]

                    transition_dict[(state, symbol)] = next_state

                fa = None
                if type == 'DFA':
                    fa = TestFa.DFA(states, symbols, start_state, final_states, transition_dict)
                elif type == 'NFA':
                    fa = TestFa.NFA(states, symbols, start_state, final_states, transition_dict)
                else:
                    fa = TestFa.εNFA(states, symbols, start_state, final_states, transition_dict)

                input_string = request.POST['string_test']
                print(input_string)
                if type == 'E-NFA':
                    accepted = fa.is_accepted(input_string)
                else:
                    accepted, prefixes = fa.is_accepted(input_string)
                print(accepted)



    context = {'form': form,
               'graph_path': graph_path,
               'transition_table': transition_table,
               'type': type,
               'accepted': accepted}
    return render(request, BASE_DIR + '/test_fa_details.html', context)