import graphviz


class DFA:
    def __init__(self, states, alphabet, transitions, starting_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.starting_state = starting_state
        self.accepting_states = accepting_states

    def is_accepting(self, state):
        return state in self.accepting_states

    def transition(self, state, symbol):
        if (state, symbol) in self.transitions:
            return self.transitions[(state, symbol)]
        else:
            return None

    def minimize(self):
        from collections import defaultdict

        partition = [self.accepting_states, self.states - self.accepting_states]
        changed = True
        while changed:
            changed = False
            new_partition = []
            for part in partition:
                split_dict = defaultdict(list)
                for state in part:
                    transition_key = tuple(self.transition(state, symbol) for symbol in self.alphabet)
                    split_dict[transition_key].append(state)
                if len(split_dict) > 1:
                    changed = True
                    new_partition.extend(split_dict.values())
                else:
                    new_partition.append(part)
            partition = new_partition

        state_map = {}
        minimized_states = set()
        minimized_accepting_states = set()
        minimized_transitions = {}

        for part in partition:
            representative = next(iter(part))
            minimized_states.add(representative)
            if representative in self.accepting_states:
                minimized_accepting_states.add(representative)
            for state in part:
                state_map[state] = representative

        for (state, symbol), next_state in self.transitions.items():
            new_state = state_map[state]
            new_next_state = state_map[next_state]
            minimized_transitions[(new_state, symbol)] = new_next_state

        self.states = minimized_states
        self.transitions = minimized_transitions
        self.accepting_states = minimized_accepting_states
        self.starting_state = state_map[self.starting_state]

    def simulate(self, input_string):
        current_state = self.starting_state

        for symbol in input_string:
            current_state = self.transition(current_state, symbol)
            if current_state is None:
                return False

        return self.is_accepting(current_state)

    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nStart State: {self.starting_state}\nAccept States: {self.accepting_states}"


def get_dfa_from_user():
    states = input("Enter states (comma-separated): ").split(',')
    alphabet = input("Enter alphabet (comma-separated): ").split(',')
    starting_state = input("Enter start state: ")
    accepting_states = input("Enter accept states (comma-separated): ").split(',')

    transitions = {}
    print("Enter transitions (format: state, symbol, next_state). Type 'done' to finish.")
    while True:
        transition_input = input("Transition: ")
        if transition_input.lower() == 'done':
            break
        state, symbol, next_state = transition_input.split(',')
        transitions[(state.strip(), symbol.strip())] = next_state.strip()

    return DFA(set(states), set(alphabet), transitions, starting_state, set(accepting_states))


def visualize_dfa(states, alphabet, transitions, starting_state, accepting_states, name):
    # Membuat digraph objek
    dot = graphviz.Digraph()

    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')

    # Menambah node
    for state in states:
        if state in accepting_states:
            dot.node(state, shape='doublecircle', style='filled', fillcolor='lightblue', color='lightblue')
        else:
            dot.node(state, style='filled', fillcolor='pink', color='pink')

    # Menambah start node
    dot.node('start', shape='point')
    dot.edge('start', starting_state)

    # Tambah transisi
    for transition in transitions:
        from_state, symbol = transition
        to_state = transitions[transition]
        dot.edge(from_state, to_state, label=symbol)

    # render
    dot.render(name, format='png', view=True)


# def main():
#     dfa = get_dfa_from_user()
#     input_string = input("\nEnter string to test: ")
#
#     print("\nDFA before minimization:")
#     print("Test result:", "Accepted" if dfa.simulate(input_string) else "Rejected")
#     print(dfa)
#     visualize_dfa(dfa.states, dfa.alphabet, dfa.transitions, dfa.starting_state, dfa.accepting_states, 'dfa1')
#
#     dfa.minimize()  # Panggil fungsi minimize di sini
#
#     print("\nDFA after minimization:")
#     print("Test result:", "Accepted" if dfa.simulate(input_string) else "Rejected")
#     visualize_dfa(dfa.states, dfa.alphabet, dfa.transitions, dfa.starting_state, dfa.accepting_states, 'dfa2')
#
#
# if __name__ == "__main__":
#     main()
