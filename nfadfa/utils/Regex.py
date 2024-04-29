from graphviz import Digraph


class Type:
    SYMBOL = 1
    CONCAT = 2
    UNION = 3
    KLEENE = 4


class ExpressionTree:
    def __init__(self, _type, value=None):
        self._type = _type
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.value, self._type), str(self.left), str(self.right)

def constructTree(regexp):
    stack = []
    for c in regexp:
        if c.isalnum():
            stack.append(ExpressionTree(Type.SYMBOL, c))
        else:
            if c == "+":
                z = ExpressionTree(Type.UNION)
                z.right = stack.pop()
                z.left = stack.pop()
            elif c == ".":
                z = ExpressionTree(Type.CONCAT)
                z.right = stack.pop()
                z.left = stack.pop()
            elif c == "*":
                z = ExpressionTree(Type.KLEENE)
                z.left = stack.pop()
            stack.append(z)

    return stack[0]


def inorder(et):
    if et._type == Type.SYMBOL:
        print(et.value)
    elif et._type == Type.CONCAT:
        inorder(et.left)
        print(".")
        inorder(et.right)
    elif et._type == Type.UNION:
        inorder(et.left)
        print("+")
        inorder(et.right)
    elif et._type == Type.KLEENE:
        inorder(et.left)
        print("*")


def higherPrecedence(a, b):
    p = ["+", ".", "*"]
    return p.index(a) > p.index(b)


def postfix(regexp):
    # adding dot "." between consecutive symbols
    temp = []
    for i in range(len(regexp)):
        if i != 0 \
                and (regexp[i - 1].isalnum() or regexp[i - 1] == ")" or regexp[i - 1] == "*") \
                and (regexp[i].isalnum() or regexp[i] == "("):
            temp.append(".")
        temp.append(regexp[i])
    regexp = temp

    stack = []
    output = ""

    for c in regexp:
        if c.isalnum():  # Memeriksa apakah alphanumeric (letter or number)
            output = output + c
            continue

        if c == ")":
            while len(stack) != 0 and stack[-1] != "(":
                output = output + stack.pop()
            stack.pop()
        elif c == "(":
            stack.append(c)
        elif c == "*":
            output = output + c
        elif len(stack) == 0 or stack[-1] == "(" or higherPrecedence(c, stack[-1]):
            stack.append(c)
        else:
            while len(stack) != 0 and stack[-1] != "(" and not higherPrecedence(c, stack[-1]):
                output = output + stack.pop()
            stack.append(c)

    while len(stack) != 0:
        output = output + stack.pop()

    return output


class FiniteAutomataState:
    def __init__(self):
        self.next_state = {}


def evalRegex(et):
    # returns equivalent E-NFA for given expression tree (representing a Regular Expression)
    if et._type == Type.SYMBOL:
        return evalRegexSymbol(et)
    elif et._type == Type.CONCAT:
        return evalRegexConcat(et)
    elif et._type == Type.UNION:
        return evalRegexUnion(et)
    elif et._type == Type.KLEENE:
        return evalRegexKleene(et)


def evalRegexSymbol(et):
    start_state = FiniteAutomataState()
    end_state = FiniteAutomataState()

    start_state.next_state[et.value] = [end_state]
    return start_state, end_state


def evalRegexConcat(et):
    left_nfa = evalRegex(et.left)
    right_nfa = evalRegex(et.right)

    left_nfa[1].next_state['ε'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]


def evalRegexUnion(et):
    start_state = FiniteAutomataState()
    end_state = FiniteAutomataState()

    up_nfa = evalRegex(et.left)
    down_nfa = evalRegex(et.right)

    start_state.next_state['ε'] = [up_nfa[0], down_nfa[0]]
    up_nfa[1].next_state['ε'] = [end_state]
    down_nfa[1].next_state['ε'] = [end_state]

    return start_state, end_state


def evalRegexKleene(et):
    start_state = FiniteAutomataState()
    end_state = FiniteAutomataState()

    sub_nfa = evalRegex(et.left)

    start_state.next_state['ε'] = [sub_nfa[0], end_state]
    sub_nfa[1].next_state['ε'] = [sub_nfa[0], end_state]

    return start_state, end_state


# Fungsi tambahan untuk membuat gambar transition menggunakan Graphviz
def visualizeTransition(finite_automata, filename='E-NFA_transition_graph'):
    dot = Digraph()
    states_done = []
    symbol_table = {finite_automata[0]: 'q0'}  # Menyimpan mapping antara state dengan label 'q' + nomor state
    dot.attr(rankdir='LR')  # Menyetel tata letak mendatar (left to right)
    dot.node('q0', shape='circle', style='filled', fillcolor='lightblue', color='lightblue')  # Menandai start state sebagai circle biasa
    stack = [finite_automata[0]]

    while stack:
        state = stack.pop()
        if state not in states_done:
            states_done.append(state)
            for symbol in list(state.next_state):
                for ns in state.next_state[symbol]:
                    if ns not in symbol_table:
                        symbol_table[ns] = 'q' + str(len(symbol_table))
                    if ns == finite_automata[1]:
                        dot.node(symbol_table[ns], shape='doublecircle', style='filled', fillcolor='pink', color='pink')
                    else:
                        dot.node(symbol_table[ns], shape='circle', style='filled', fillcolor='lightblue', color='lightblue')
                    dot.edge(symbol_table[state], symbol_table[ns], label=symbol)
                    if ns not in states_done:
                        stack.append(ns)

    dot.render(filename, format='png', cleanup=True)
    print("\n<!--Stored Successfully--!>")
    print("Transition Graph is Saved as E-NFA_transition_graph.png")


def printStateTransitions(state, states_done, symbol_table):
    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        line_output = "q" + str(symbol_table[state]) + "\t\t" + symbol + "\t\t"
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = 1 + sorted(symbol_table.values())[-1]
            line_output = line_output + "q" + str(symbol_table[ns]) + " "

        print(line_output)

        for ns in state.next_state[symbol]:
            printStateTransitions(ns, states_done, symbol_table)


def printTransitionTable(finite_automata):
    print("|State|\t\t|Symbol|\t|Next State|")
    print("-------\t\t--------\t------------")
    printStateTransitions(finite_automata[0], [], {finite_automata[0]: 0})


# Memvalidasi input regex dari pengguna
def validateRegexInput(regex):
    allowed_characters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+.*()')
    # Mengecek apakah input regex sudah terisi dan tidak dalam kondisi kosong
    if not regex:
        print("<!--ERROR OCCURRED--!>\nInput Is Empty. Please Enter a Valid Regular Expression.")
        return False
    # Mengecek apakah regex hanya terdiri dari karakter alfanumerik atau karakter khusus (+, *, (), .)
    if not set(regex).issubset(allowed_characters):
        print(
            "<!--ERROR OCCURRED--!>\nInput Contains Invalid Characters. Please Only Use Alphanumeric Characters, '+', '.', '*', '(', and ')'.")
        return False
    # Mengecek apakah simbol "(" dan ")" berpasangan
    if regex.count("(") != regex.count(")"):
        print(
            "<!--ERROR OCCURRED--!>\nThe Open and Close Bracket Signs Aren't Paired Properly, Please Double Check Your Input.")
        return False
    return True


def getStateTransitions(state, states_done=None, symbol_table=None, transitions=None):
    if states_done is None:
        states_done = []
    if symbol_table is None:
        symbol_table = {}
    if transitions is None:
        transitions = []

    if state in states_done:
        return transitions

    states_done.append(state)

    for symbol in list(state.next_state):
        line_output = ["q" + str(symbol_table[state]), symbol]
        next_states = []
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = 1 + sorted(symbol_table.values())[-1]
            next_states.append("q" + str(symbol_table[ns]))

        line_output.extend(next_states)
        transitions.append(line_output)

        for ns in state.next_state[symbol]:
            getStateTransitions(ns, states_done, symbol_table, transitions)

    return transitions

# Meminta pengguna untuk input regex yang valid
def promptValidRegexInput():
    while True:
        r = input("\nPlease Enter The Correct Regex: ")
        print("Processing...")
        if validateRegexInput(r):
            return r


def main():
    r = promptValidRegexInput()
    pr = postfix(r)
    et = constructTree(pr)

    fa = evalRegex(et)
    print()
    print("\t     Transition Table")
    print("============================================")
    printTransitionTable(fa)
    print("Visualizing Transition...")
    visualizeTransition(fa)


if __name__ == "__main__":
    main()