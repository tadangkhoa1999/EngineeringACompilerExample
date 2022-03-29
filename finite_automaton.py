# Ta Dang Khoa - VNU - 21025077
# Finite Automaton Class


class State:
    def __init__(self, label):
        self.label = label
        self.edges = {}

    def getNext(self, char):
        if char in self.edges.keys():
            return self.edges[char]
        else:
            return None

    def setNext(self, char, state):
        if char == 'ϵ':  # epsilon / empty can connect with multi states
            if 'ϵ' in self.edges.keys():
                self.edges[char].append(state)
            else:
                self.edges[char] = [state]
        else:
            self.edges[char] = state


class FiniteAutomaton:
    def __init__(self):
        self.states = []  # all node
        self.start_state = self.createState()  # S0
        self.accepting_states = []  # SA

    def createState(self):
        new_state =  State('S_{}'.format(len(self.states)))
        self.states.append(new_state)
        return new_state

    def resetLabel(self):
        for i, state in enumerate(self.states):
            state.label = 'S_{}'.format(i)

    def getGVFile(self, output_path):
        draw_info = '''
            digraph finite_state_machine {
                rankdir=LR;
                size="1000, 1000"
                node [shape = point ]; qi
                node [shape = circle]; S_0
                qi -> S_0;
        '''
        for state in self.accepting_states:
            draw_info += 'node [shape = doublecircle]; {};\n'.format(state.label)
        draw_info += 'node [shape = circle];\n'
        for state in self.states:
            for edge in state.edges.keys():
                target_states = state.edges[edge]
                if not isinstance(target_states, list):
                    target_states = [target_states]
                for target_state in target_states:
                    draw_info += '{} -> {} [ label = "{}" ];\n'.format(state.label, target_state.label, edge)
        draw_info += '}'
        with open(output_path, 'w') as f:
            f.write(draw_info)


def run_operations(fa1, fa2, type='concatenation'):
    '''
    Params:
    -----
    - type: alternation / concatenation / closure

    Notes:
    -----
    - fa1 and fa2 should only have one accepting state
    - if type is closure, fa2 is None
    '''
    output_fa = FiniteAutomaton()
    for state in fa1.states:
        output_fa.states.append(state)
    if fa2 is not None:
        for state in fa2.states:
            output_fa.states.append(state)
    end_state = output_fa.createState()  # create end state
    output_fa.accepting_states.append(end_state)

    if type == 'concatenation':
        output_fa.states.remove(output_fa.start_state)
        output_fa.states.remove(end_state)
        output_fa.accepting_states.remove(end_state)
        output_fa.start_state = fa1.start_state
        fa1.accepting_states[0].setNext('ϵ', fa2.start_state)
        output_fa.accepting_states.append(fa2.accepting_states[0])
    elif type == 'alternation':
        output_fa.start_state.setNext('ϵ', fa1.start_state)
        output_fa.start_state.setNext('ϵ', fa2.start_state)
        fa1.accepting_states[0].setNext('ϵ', end_state)
        fa2.accepting_states[0].setNext('ϵ', end_state)
    elif type == 'closure':
        output_fa.start_state.setNext('ϵ', fa1.start_state)
        output_fa.start_state.setNext('ϵ', end_state)
        fa1.accepting_states[0].setNext('ϵ', end_state)
        fa1.accepting_states[0].setNext('ϵ', fa1.start_state)

    output_fa.resetLabel()
    return output_fa
