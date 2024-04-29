from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

EPSILON = 'ε'
EMPTY = '-'


class FA:
    def __init__(self):
        self.num_states = 0
        self.symbols = []
        self.num_final_states = 0
        self.final_state = []
        self.start_state = 0
        self.transition_functions = []
        self.states = set()
        self.graph = Digraph(format="png")

        self.transition_dict = {}


    def initFa(self, states, start_state, final_state, symbols, transition_functions):
        self.states = states
        self.num_states = len(states)
        self.start_state = start_state
        self.final_state = final_state
        self.num_final_states = len(final_state)
        self.symbols = symbols
        self.transition_functions = transition_functions


    def init_transitions(self):
        for transition in self.transition_functions:
            start_state = transition[0]
            symbol = transition[1]
            ending_state = transition[2]

            if (start_state, symbol) in self.transition_dict:
                self.transition_dict[(start_state, symbol)].append(ending_state)
            else:
                self.transition_dict[(start_state, symbol)] = [ending_state]

    def create_transition_table(self):
        table = []
        states = sorted(self.states)
        symbols = sorted(self.symbols)

        # Construct header row
        header = ["State"] + symbols
        table.append(header)

        # Construct transition rows
        for state in states:
            row = [state]
            for symbol in symbols:
                next_state = self.transition_dict.get((state, symbol), '-')
                row.append(next_state)
            table.append(row)

        return table

    def init_states(self):
        self.states = set(range(self.num_states))

    def print_automaton(self):
        print(f"No of state: {self.num_states}")
        print(f"States: {self.states}")
        print(f"Symbols: {self.symbols}")
        print(f"No of final states: {self.num_final_states}")
        print(f"Final states: {self.final_state}")
        print(f"Start state: {self.start_state}")
        print(f"Transitions: {self.transition_functions}")

    def create_graph(self):
        # add node/state for graph
        for state in self.states:
            if state not in self.final_state:
                self.graph.node(str(state), label=str(state), shape='circle', style="filled", fillcolor="pink", color="pink")
            else:
                self.graph.node(str(state), label=str(state), shape='doublecircle', style="filled", fillcolor="lightblue", color="lightblue")

        # add start state arrow
        self.graph.node('x', label='start', shape='none')
        self.graph.edge('x', str(self.start_state))

        # add transitions
        for transition in self.transition_functions:
            self.graph.edge(str(transition[0]), str(transition[2]), label=transition[1])

    def print_graph(self, filename="graph.png"):
        self.graph.view(filename=filename)


class NFA(FA):
    def print_nfa(self):
        print(self.num_states)
        print(self.states)
        print(self.symbols)
        print(self.num_final_states)
        print(self.final_state)
        print(self.start_state)
        print(self.transition_functions)

    def construct_nfa_from_file(self, lines):
        self.num_states = int(lines[0])
        self.init_states()
        self.symbols = list(lines[1].strip())

        final_states_line = lines[2].split(" ")
        for index in range(len(final_states_line)):
            if index == 0:
                self.num_final_states = int(final_states_line[index])
            else:
                self.final_state.append(int(final_states_line[index]))

        self.startState = int(lines[3])

        for index in range(4, len(lines)):
            transition_func_line = lines[index].split(" ")

            starting_state = int(transition_func_line[0])
            transition_symbol = transition_func_line[1]
            ending_state = int(transition_func_line[2])

            transition_function = (starting_state, transition_symbol, ending_state);
            self.transition_functions.append(transition_function)


class ENFA(FA):
    def __init__(self):
        super().__init__()
        # Initialize an empty dictionary for transitions
        # Initialize an empty dictionary for epsilon transitions
        self.epsilon_transitions = {}

    def init_transitions(self):
        for transition in self.transition_functions:
            start_state = transition[0]
            symbol = transition[1]
            ending_state = transition[2]

            if (start_state, symbol) in self.transition_dict:
                self.transition_dict[(start_state, symbol)].append(ending_state)
            else:
                self.transition_dict[(start_state, symbol)] = [ending_state]

            if symbol == EPSILON:
                if start_state not in self.epsilon_transitions:
                    self.epsilon_transitions[start_state] = []
                self.epsilon_transitions[start_state].append(ending_state)

    def construct_enfa_from_file(self, lines):
        """Constructs an epsilon-NFA (eNFA) from input lines."""
        self.num_states = int(lines[0])
        self.init_states()
        self.symbols = list(lines[1].strip())

        # Read final states
        final_states_line = lines[2].split()
        self.num_final_states = int(final_states_line[0])
        self.final_state = [int(state) for state in final_states_line[1:]]

        # Read start state
        self.start_state = int(lines[3])

        # Read transitions
        for line in lines[4:]:
            parts = line.split()
            starting_state = int(parts[0])
            transition_symbol = parts[1]
            ending_state = int(parts[2])

            # Add transition to transition functions
            self.transition_functions.append((starting_state, transition_symbol, ending_state))

            # Add transition to transition dictionary
            if (starting_state, transition_symbol) in self.transition_dict:
                self.transition_dict[(starting_state, transition_symbol)].append(ending_state)
            else:
                self.transition_dict[(starting_state, transition_symbol)] = [ending_state]

            # If the transition symbol is EPSILON, also add it to the epsilon_transitions dictionary
            if transition_symbol == EPSILON:
                if starting_state not in self.epsilon_transitions:
                    self.epsilon_transitions[starting_state] = []
                self.epsilon_transitions[starting_state].append(ending_state)

    def get_next_states(self, state, symbol):
        """Returns the next states for a given state and symbol in the eNFA."""
        try:
            return self.transition_dict[(state, symbol)]
        except KeyError:
            return []
        # if (state, symbol) in self.transition_dict:
        #     return self.transition_dict[(state, symbol)]
        # else:
        #     return []

    def get_epsilon_closure(self, state, visited=None):
        """Returns the epsilon closure of a given state."""
        if visited is None:
            visited = set()

        next_state = self.get_next_states(state, EPSILON)

        if next_state == []:
            return None
        else:
            return next_state

    def convert_to_nfa(self):
        symbol_without_epsilon = self.symbols[:-1].copy()
        """Converts ENFA to NFA."""
        nfa = NFA()
        nfa.symbols = self.symbols[:-1].copy()
        nfa.num_final_states = self.num_final_states
        nfa.final_state = self.final_state.copy()
        nfa.start_state = self.start_state

        # Convert transition functions
        for transition in self.transition_functions:
            start_state = transition[0]
            symbol = transition[1]
            end_state = transition[2]
            if symbol != EPSILON:
                nfa.transition_functions.append((start_state, symbol, end_state))
                nfa.states.add(start_state)
                nfa.states.add(end_state)

        for start_state, end_states in self.epsilon_transitions.items():
            closure = self.get_epsilon_closure(start_state)
            print(f"Closure {start_state}: {closure}")
            for state in closure:
                if state in self.final_state:
                    nfa.final_state.append(start_state)
            # for state in closure:
            #     for transition in self.transition_functions:
            #         if transition[0] == state:
            #             symbol = transition[1]
            #             end_state = transition[2]
            #             nfa.transition_functions.append((start_state, symbol, end_state))

            for state in closure:
                for symbol in symbol_without_epsilon:
                    next_state = self.get_next_states(state, symbol)
                    if next_state != []:
                        if type(next_state) == list:
                            for s in next_state:
                                nfa.transition_functions.append((start_state, symbol, s))
                                nfa.states.add(start_state)
                                nfa.states.add(s)
                                print(s)
                        else:
                            nfa.transition_functions.append((start_state, symbol, next_state))
                            nfa.states.add(start_state)
                            nfa.states.add(next_state)
                            print("bruh", next_state)

        nfa.num_final_states = len(nfa.final_state)

        unique_transition_functions = []
        for transition in nfa.transition_functions:
            if transition not in unique_transition_functions:
                unique_transition_functions.append(transition)

        nfa.transition_functions = unique_transition_functions

        for state in nfa.states:
            if state not in self.states:
                nfa.states.remove(state)

        nfa.num_states = len(nfa.states)

        print(f"nfa states: {nfa.states}")

        return nfa

    def print_automaton(self):
        print(f"No of state: {self.num_states}")
        print(f"States: {self.states}")
        print(f"Symbols: {self.symbols}")
        print(f"No of final states: {self.num_final_states}")
        print(f"Final states: {self.final_state}")
        print(f"Start state: {self.start_state}")
        print(f"Transitions: {self.transition_functions}")
        print(f"Transitions dicitonary: {self.transition_dict}")
        print(f"Epsilon: {self.epsilon_transitions}")


class DFA(FA):
    def __init__(self):
        super().__init__()
        self.q = []

    def print_dfa(self):
        print(len(self.q))
        print("".join(self.symbols))
        print(str(self.num_final_states) + " " + " ".join(str(final_state) for final_state in self.final_state))
        print(self.start_state)

        for transition in sorted(self.transition_functions):
            print(" ".join(str(value) for value in transition))

    def convert_from_nfa(self, nfa):
        self.symbols = nfa.symbols.copy()
        self.start_state = nfa.start_state
        self.states = nfa.states.copy()

        nfa_transition_dict = {}
        dfa_transition_dict = {}

        # Combine NFA transitions
        for transition in nfa.transition_functions:
            starting_state = transition[0]
            transition_symbol = transition[1]
            ending_state = transition[2]

            if (starting_state, transition_symbol) in nfa_transition_dict:
                nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)
            else:
                nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]

        self.q.append(('0',))

        # Convert NFA transitions to DFA transitions
        for dfa_state in self.q:
            for symbol in nfa.symbols:
                if len(dfa_state) == 1 and (dfa_state[0], symbol) in nfa_transition_dict:
                    dfa_transition_dict[(dfa_state, symbol)] = nfa_transition_dict[(dfa_state[0], symbol)]

                    if tuple(dfa_transition_dict[(dfa_state, symbol)]) not in self.q:
                        self.q.append(tuple(dfa_transition_dict[(dfa_state, symbol)]))
                else:
                    destinations = []
                    final_destination = []

                    for nfa_state in dfa_state:
                        if (nfa_state, symbol) in nfa_transition_dict and nfa_transition_dict[
                            (nfa_state, symbol)] not in destinations:
                            destinations.append(nfa_transition_dict[(nfa_state, symbol)])

                    if not destinations:
                        final_destination.append(None)
                    else:
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)

                    dfa_transition_dict[(dfa_state, symbol)] = final_destination

                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))

        # Convert NFA states to DFA states
        for key in dfa_transition_dict:
            self.transition_functions.append(
                (str(self.q.index(tuple(key[0]))), key[1], str(self.q.index(tuple(dfa_transition_dict[key])))))
            # changed
            self.states.add(str(self.q.index(tuple(key[0]))))
            self.states.add(str(self.q.index(tuple(dfa_transition_dict[key]))))

        for q_state in self.q:
            for state in nfa.final_state:
                if state in q_state:
                    self.final_state.append(str(self.q.index(q_state)))
                    self.num_final_states += 1