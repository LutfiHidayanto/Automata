import sys
from graphviz import Digraph


def read_DFA():
    '''Read DFA from terminal input'''

    print("Enter DFA 1:")
    num_states = int(input("Number of states: "))
    states = input("States (separated by space): ").split()
    alph_size = int(input("Number of alphabets: "))
    alph = input("Alphabets (separated by space): ").split()

    # Validate states for DFA 1
    for state in states:
        if not state.isalnum():  # Ensure states contain only alphanumeric characters
            print("Invalid state name. State names should contain only alphanumeric characters.")
            sys.exit(1)

    # Validate alphabets for DFA 1
    for symbol in alph:
        if not symbol.isalnum() or len(symbol) > 1:  # Ensure symbols are single alphanumeric characters
            print("Invalid alphabet. Alphabets should be single alphanumeric characters.")
            sys.exit(1)

    print("Enter transition function for DFA 1:")
    tf = {}
    for state in states:
        for symbol in alph:
            next_state = input(f"Transition from state {state} with symbol {symbol}: ")
            tf[(state, symbol)] = next_state

    start_state = input("Start state: ")
    if start_state not in states:
        print("Invalid start state. Start state should be one of the defined states.")
        sys.exit(1)

    num_accepts = int(input("Number of accept states: "))
    accepts = input("Accept states (separated by space): ").split()

    # Validate accept states for DFA 1
    for accept_state in accepts:
        if accept_state not in states:
            print("Invalid accept state. Accept states should be one of the defined states.")
            sys.exit(1)

    dfa1 = {
        'states': states,
        'alph': alph,
        'tf': tf,
        'start_state': start_state,
        'accepts': accepts
    }

    print("\nEnter DFA 2:")
    num_states = int(input("Number of states: "))
    states = input("States (separated by space): ").split()

    # Validate states for DFA 2
    for state in states:
        if not state.isalnum():  # Ensure states contain only alphanumeric characters
            print("Invalid state name. State names should contain only alphanumeric characters.")
            sys.exit(1)

    alph_size = int(input("Number of alphabets: "))
    alph = input("Alphabets (separated by space): ").split()

    # Validate alphabets for DFA 2
    for symbol in alph:
        if not symbol.isalnum() or len(symbol) > 1:  # Ensure symbols are single alphanumeric characters
            print("Invalid alphabet. Alphabets should be single alphanumeric characters.")
            sys.exit(1)

    print("Enter transition function for DFA 2:")
    tf = {}
    for state in states:
        for symbol in alph:
            next_state = input(f"Transition from state {state} with symbol {symbol}: ")
            tf[(state, symbol)] = next_state

    start_state = input("Start state: ")
    if start_state not in states:
        print("Invalid start state. Start state should be one of the defined states.")
        sys.exit(1)

    num_accepts = int(input("Number of accept states: "))
    accepts = input("Accept states (separated by space): ").split()

    # Validate accept states for DFA 2
    for accept_state in accepts:
        if accept_state not in states:
            print("Invalid accept state. Accept states should be one of the defined states.")
            sys.exit(1)

    dfa2 = {
        'states': states,
        'alph': alph,
        'tf': tf,
        'start_state': start_state,
        'accepts': accepts
    }

    return dfa1, dfa2


def transition(dfa, state, symbol):
    '''Returns state resulting from state + symbol'''

    new_state = dfa['tf'].get((state, symbol))  # Use .get() method to avoid KeyError
    if new_state is None:
        print(f"No transition defined for state {state} with symbol {symbol}")
        sys.exit(1)
    return new_state


def equivalent(d1, d2):
    '''Returns whether 2 given DFAs are equivalent'''

    start_state = (d1['start_state'], d2['start_state'])  # Use tuple for start state
    queue = [start_state]
    visited = [start_state]

    # check that alphabets match
    if d1['alph'] != d2['alph']:
        print('Alphabets do not match')
        return False
    else:
        alph = d1['alph']

    # while queue is not empty:
    while len(queue) != 0:

        # pop first item in queue
        current_state = queue.pop(0)

        # check if both states are accept/intermediate states- i.e. equivalent
        d1_accept = current_state[0] in d1['accepts']
        d2_accept = current_state[1] in d2['accepts']

        if d1_accept != d2_accept:
            return False

        # for each symbol in alph- calculate next state
        for symbol in alph:
            d1_state = transition(d1, current_state[0], symbol)
            d2_state = transition(d2, current_state[1], symbol)
            state = (d1_state, d2_state)

            # if state not previously visited- add to queue
            if state not in visited:
                visited.append(state)
                queue.append(state)

    return True


def create_dfa_graph(dfa, filename):
    '''Create graph representation of DFA and save as PNG file'''

    dot = Digraph(comment='DFA')

    for state in dfa['states']:
        if state in dfa['accepts']:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    for (start, symbol), end in dfa['tf'].items():
        dot.edge(start, end, label=symbol)

    dot.attr(rankdir='LR')
    dot.render(filename, format='png')


# def main():
#     '''Main program'''
#
#     print("DFA Equivalence Checker")
#     print("-----------------------")
#
#     dfa1, dfa2 = read_DFA()
#
#     if equivalent(dfa1, dfa2):
#         print("\nThe two DFAs are equivalent.")
#     else:
#         print("\nThe two DFAs are not equivalent.")
#
#     create_dfa_graph(dfa1, 'dfa1_graph')
#     create_dfa_graph(dfa2, 'dfa2_graph')
#
#
# if __name__ == "__main__":
#     main()
