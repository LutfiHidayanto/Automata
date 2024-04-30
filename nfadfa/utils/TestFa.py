""" Class for DFA to ACCEPT or to REJECT """
class DFA:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    # Function to determine the next state in the DFA
    def transition(self, state, symbol):
        return self.transitions.get((state, symbol))

    # Function to test whether DFA accepted or not
    def is_accepted(self, input_string, display=False):
        current_state = self.initial_state
        # Array for the prefix in the accepted string
        prefix_accepted = []
        for i, symbol in enumerate(input_string, 1):
            # If state is invalid
            if symbol not in self.alphabet:
                return False, prefix_accepted
            current_state = self.transition(current_state, symbol)
            # If transition is invalid
            if current_state is None:
                return False, prefix_accepted

            if current_state in self.final_states:
                prefix_accepted.append(input_string[:i])

        return current_state in self.final_states, prefix_accepted


""" Class for NFA to ACCEPT or to REJECT """
class NFA:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    # Function to determine the next states in the NFA
    def transition(self, states, symbol):
        # Using set() to prevents duplicate states from being added
        next_states = set()
        for state in states:
            transitions = self.transitions.get((state, symbol), [])
            next_states.update(transitions)
        return next_states

    # Function to test whether NFA accepted or not
    def is_accepted(self, input_string, display=False):
        current_states = {self.initial_state}
        # Array for the prefix in the accepted string
        prefix_accepted = []

        for i, symbol in enumerate(input_string, 1):
            next_states = set()
            for state in current_states:
                next_states.update(self.transition({state}, symbol))

            # If transition is invalid
            if not next_states:
                return False, prefix_accepted

            current_states = next_states
            if any(state in self.final_states for state in current_states):
                prefix_accepted.append(input_string[:i])

        return any(state in self.final_states for state in current_states), prefix_accepted


""" Class for ε-NFA to ACCEPT or to REJECT """
class εNFA:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    # Function to organize epsilon in εNFA
    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if ('$', state) in self.transitions:
                for next_state in self.transitions[('$', state)]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    # Function to determine the next states in the εNFA
    def transition(self, states, symbol):
        transition_next = set()
        for state in states:
            if (symbol, state) in self.transitions:
                transition_next.update(self.transitions[(symbol, state)])

        return self.epsilon_closure(transition_next)

    # Function to test whether εNFA accepted or not
    def is_accepted(self, input_string):
        current_states = self.epsilon_closure({self.initial_state})
        for symbol in input_string:
            current_states = self.transition(current_states, symbol)

        return any(state in self.final_states for state in current_states)


""" Class for Regular Expression to ACCEPT or to REJECT """
class Regex:
    class Type:
        Symbol = 1
        Concat = 2
        Union  = 3
        Kleene = 4

    class RegularExpression:
        def __init__(self, _type, value=None):
            self._type = _type
            self.value = value
            self.left = None
            self.right = None

    # Operators or Alphanumeric
    def constructRegex(pattern):
        stack = []
        for char in pattern:
            if char.isalnum():
                stack.append(Regex.RegularExpression(Regex.Type.Symbol, char))
            else:
                if char == "+":
                    z = Regex.RegularExpression(Regex.Type.Union)
                    z.right = stack.pop()
                    z.left = stack.pop()
                elif char == ".":
                    z = Regex.RegularExpression(Regex.Type.Concat)
                    z.right = stack.pop()
                    z.left = stack.pop()
                elif char == "*":
                    z = Regex.RegularExpression(Regex.Type.Kleene)
                    z.left = stack.pop()
                stack.append(z)
        return stack[0]

    # Precedence of Operators (Lowest to Highest)
    def higherPrecedence(a, b):
        p = ["+", ".", "*"]
        return p.index(a) > p.index(b)

    # If regex meets operator
    def postfix(pattern):
        temp = []
        for i in range(len(pattern)):
            if i != 0\
                and (pattern[i-1].isalnum() or pattern[i-1] == ")" or pattern[i-1] == "*")\
                and (pattern[i].isalnum() or pattern[i] == "("):
                temp.append(".")
            temp.append(pattern[i])
        pattern = temp

        stack = []
        output = ""

        # If regex meets certain operator
        for char in pattern:
            if char.isalnum():
                output = output + char
                continue

            if char == ")":
                while len(stack) != 0 and stack[-1] != "(":
                    output = output + stack.pop()
                stack.pop()
            elif char == "(":
                stack.append(char)
            elif char == "*":
                output = output + char
            elif len(stack) == 0 or stack[-1] == "(" or Regex.higherPrecedence(char, stack[-1]):
                stack.append(char)
            else:
                while len(stack) != 0 and stack[-1] != "(" and not Regex.higherPrecedence(char, stack[-1]):
                    output = output + stack.pop()
                stack.append(char)

        while len(stack) != 0:
            output = output + stack.pop()

        return output

    # Evaluate the regex string
    def evalRegex(et):
        if et._type == Regex.Type.Symbol:
            return Regex.evalRegexSymbol(et)
        elif et._type == Regex.Type.Concat:
            return Regex.evalRegexConcat(et)
        elif et._type == Regex.Type.Union:
            return Regex.evalRegexUnion(et)
        elif et._type == Regex.Type.Kleene:
            return Regex.evalRegexKleene(et)

    def evalRegexSymbol(et):
        initial_state = Regex.FiniteAutomataState()
        final_state   = Regex.FiniteAutomataState()
        initial_state.next_state[et.value] = [final_state]
        return initial_state, final_state

    def evalRegexConcat(et):
        left_nfa  = Regex.evalRegex(et.left)
        right_nfa = Regex.evalRegex(et.right)
        left_nfa[1].next_state['$'] = [right_nfa[0]]
        return left_nfa[0], right_nfa[1]

    def evalRegexUnion(et):
        initial_state = Regex.FiniteAutomataState()
        final_state   = Regex.FiniteAutomataState()
        up_nfa   = Regex.evalRegex(et.left)
        down_nfa = Regex.evalRegex(et.right)
        initial_state.next_state['$'] = [up_nfa[0], down_nfa[0]]
        up_nfa[1].next_state['$'] = [final_state]
        down_nfa[1].next_state['$'] = [final_state]
        return initial_state, final_state

    def evalRegexKleene(et):
        initial_state = Regex.FiniteAutomataState()
        final_state   = Regex.FiniteAutomataState()
        sub_nfa = Regex.evalRegex(et.left)
        initial_state.next_state['$'] = [sub_nfa[0], final_state]
        sub_nfa[1].next_state['$'] = [sub_nfa[0], final_state]
        return initial_state, final_state

    # εNFA
    class FiniteAutomataState:
        def __init__(self):
            self.next_state = {}

    def simulateNFA(input_string, start_state):
        current_states = Regex.epsilonClosure([start_state])
        for symbol in input_string:
            next_states = []
            for state in current_states:
                if symbol in state.next_state:
                    next_states.extend(state.next_state[symbol])
            current_states = Regex.epsilonClosure(next_states)
        return any(state.next_state == {} for state in current_states)

    def epsilonClosure(states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if '$' in state.next_state:
                for epsilon_state in state.next_state['$']:
                    if epsilon_state not in closure:
                        closure.add(epsilon_state)
                        stack.append(epsilon_state)
        return closure

""" Function to set DFA input """
def dfa_setup():
    states_input = input("Enter states (comma-separated): ")
    states = parse_input_states(states_input)

    alphabet_input = input("Enter alphabet (comma-separated): ")
    alphabet = parse_input_states(alphabet_input)

    initial_state = input("Enter initial state: ")

    final_states_input = input("Enter final states (comma-separated): ")
    final_states = parse_input_states(final_states_input)

    print("Enter transitions in the format 'CurrentState Alphabet NextState'. Enter 'done' to finish:")
    transitions = {}
    while True:
        inline = input().strip()
        if inline.lower() == "done":
            break
        current_state, symbol, transition = inline.split(' ')
        transitions[(current_state, symbol)] = transition

    return DFA(states, alphabet, initial_state, final_states, transitions)


""" Function to set NFA input """
def nfa_setup():
    states_input = input("Enter states (comma-separated): ")
    states = parse_input_states(states_input)

    alphabet_input = input("Enter alphabet (comma-separated): ")
    alphabet = parse_input_states(alphabet_input)

    initial_state = input("Enter initial state: ")

    final_states_input = input("Enter final states (comma-separated): ")
    final_states = parse_input_states(final_states_input)

    print("Enter transitions in the format 'CurrentState Alphabet NextState1,NextState2,...'.")
    print("Enter 'done' to finish:")
    transitions = {}
    while True:
        inline = input().strip()
        if inline.lower() == "done":
            break
        current_state, symbol, transition = inline.split(' ')
        transition_next = transition.split(',')
        transitions[(current_state, symbol)] = transition_next

    return NFA(states, alphabet, initial_state, final_states, transitions)


""" Function to set εNFA input """
def εnfa_setup():
    states_input = input("Enter states (comma-separated): ")
    states = parse_input_states(states_input)

    alphabet_input = input("Enter alphabet (comma-separated): ")
    alphabet = parse_input_states(alphabet_input)

    initial_state = input("Enter initial state: ")

    final_states_input = input("Enter final states (comma-separated): ")
    final_states = parse_input_states(final_states_input)

    print("Enter transitions in the format 'CurrentState Alphabet NextState'.")
    print("Use Alphabet '$' for epsilon transition. Enter 'done' to finish:")

    transitions = {}
    while True:
        inline = input().strip()
        if inline.lower() == "done":
            break
        current_state, symbol, transition = inline.split(' ')
        transition_next = transition.split(',')
        transitions.setdefault((symbol, current_state), set()).update(transition_next)

    return εNFA(states, alphabet, initial_state, final_states, transitions)


""" Function to set Regex input """
def regex_setup():
    # Validation input Regex
    def validateRegexInput(regex):
        characters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+.*()')
        if not regex:
            print("!!\nInput Is Empty. Please Enter a Valid Regular Expression\n!!")
            return False
        if not set(regex).issubset(characters):
            print("!!\nInput Contains Invalid Characters\n!!")
            return False
        if regex.count("(") != regex.count(")"):
            print("!!\nBracket Signs not Paired Properly\n!!")
            return False
        return True

    while True:
        # Inputing Regular Expression
        regex_input = input("Enter Regular Expression: ")
        if validateRegexInput(regex_input):
            print(regex_input)
            return regex_input
            break


""" Function to divide input into several parts with commas as boundaries """
def parse_input_states(states_input):
    return states_input.split(',')


""" Function for main program """
def main():
    while True:
        choice = input("Automaton options :\n1. DFA\n2. NFA\n3. ε-NFA\n4. Regular Expression\nEnter your choice: ")
        if choice == "1":
            dfa = dfa_setup()
            print(dfa.transitions)
            while True:
                input_string = input("Enter a string to check (Enter space to exit): ")
                if input_string == " ":
                    break
                is_accepted, prefixes = dfa.is_accepted(input_string, display=True)
                if is_accepted:
                    print(f"'{input_string}' is ACCEPTED by the DFA.")
                    print("Accepted Prefix/Prefixes :", prefixes)
                else:
                    print(f"'{input_string}' is REJECTED by the DFA.")
            break

        elif choice == "2":
            nfa = nfa_setup()
            while True:
                input_string = input("Enter a string to check (Enter space to exit): ")
                if input_string == " ":
                    break
                is_accepted, prefixes = nfa.is_accepted(input_string, display=True)
                if is_accepted:
                    print(f"'{input_string}' is ACCEPTED by the NFA.")
                    print("Accepted Prefix/Prefixes :", prefixes)
                else:
                    print(f"'{input_string}' is REJECTED by the NFA.")
            break

        elif choice == "3":
            εnfa = εnfa_setup()
            while True:
                input_string = input("Enter a string to check (Enter space to exit): ")
                if input_string == " ":
                    break
                is_accepted = εnfa.is_accepted(input_string)
                if is_accepted:
                    print(f"'{input_string}' is ACCEPTED by the ε-NFA.")
                else:
                    print(f"'{input_string}' is REJECTED by the ε-NFA.")
            break

        elif choice == "4":
            regex = regex_setup()
            while True:
                input_string = input("Enter input string (Enter space to exit): ")
                if input_string == " ":
                    break
                pr = Regex.postfix(regex)
                et = Regex.constructRegex(pr)
                fa = Regex.evalRegex(et)
                start_state = fa[0]
                if Regex.simulateNFA(input_string, start_state):
                    print(f"'{input_string}' is ACCEPTED by the Regular Expression.")
                else:
                    print(f"'{input_string}' is REJECTED by the Regular Expression.")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
