import graphviz

class DFA:
    def __init__(self, states, alphabet, transitions, start, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.finals = finals

    def is_accept(self, state):
        return state in self.finals

    def next_state(self, state, symbol):
        if (state, symbol) in self.transitions:
            return self.transitions[(state, symbol)]
        else:
            return None

    def minimize(self):
        from collections import defaultdict

        partition = [self.finals, self.states - self.finals]
        changed = True
        while changed:
            changed = False
            new_partition = []
            for part in partition:
                split = defaultdict(list)
                for state in part:
                    transition_key = tuple(self.next_state(state, symbol) for symbol in self.alphabet)
                    split[transition_key].append(state)
                if len(split) > 1:
                    changed = True
                    new_partition.extend(split.values())
                else:
                    new_partition.append(part)
            partition = new_partition

        state_map = {}
        minimized_states = set()
        minimized_finals = set()
        minimized_transitions = {}

        for part in partition:
            rep = next(iter(part))
            minimized_states.add(rep)
            if rep in self.finals:
                minimized_finals.add(rep)
            for state in part:
                state_map[state] = rep

        for (state, symbol), next_state in self.transitions.items():
            new_state = state_map[state]
            new_next_state = state_map[next_state]
            minimized_transitions[(new_state, symbol)] = new_next_state

        self.states = minimized_states
        self.transitions = minimized_transitions
        self.finals = minimized_finals
        self.start = state_map[self.start]

    def run(self, input_str):
        current = self.start

        for symbol in input_str:
            current = self.next_state(current, symbol)
            if current is None:
                return False

        return self.is_accept(current)

    def __str__(self):
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {self.transitions}\nStart State: {self.start}\nAccept States: {self.finals}"

def get_dfa():
    states = input("Enter states (comma-separated): ").split(',')
    alphabet = input("Enter alphabet (comma-separated): ").split(',')
    start = input("Enter start state: ")
    finals = input("Enter accept states (comma-separated): ").split(',')

    transitions = {}
    print("Enter transitions (format: state, symbol, next_state). Type 'done' to finish.")
    while True:
        transition_input = input("Transition: ")
        if transition_input.lower() == 'done':
            break
        state, symbol, next_state = transition_input.split(',')
        transitions[(state.strip(), symbol.strip())] = next_state.strip()

    return DFA(set(states), set(alphabet), transitions, start, set(finals))

def visualize(states, alphabet, transitions, start, finals, name):
    dot = graphviz.Digraph()

    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle')

    for state in states:
        if state in finals:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    dot.node('start', shape='point')
    dot.edge('start', start)

    for transition in transitions:
        from_state, symbol = transition
        to_state = transitions[transition]
        dot.edge(from_state, to_state, label=symbol)

    dot.render(name, format='png', view=True)

# def main():
#     dfa = get_dfa()
#     input_str = input("\nEnter string to test: ")
#
#     print(input_str)
#     print("\nDFA before minimization:")
#     print("Test result:", "Accepted" if dfa.run(input_str) else "Rejected")
#     print(dfa)
#     visualize(dfa.states, dfa.alphabet, dfa.transitions, dfa.start, dfa.finals, 'dfa1')
#
#     dfa.minimize()
#
#     print("\nDFA after minimization:")
#     print("Test result:", "Accepted" if dfa.run(input_str) else "Rejected")
#     visualize(dfa.states, dfa.alphabet, dfa.transitions, dfa.start, dfa.finals, 'dfa2')
#
# if __name__ == "__main__":
#     main()