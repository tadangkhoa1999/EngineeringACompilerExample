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
        if char == 'ϵ':  # (epsilon / empty) can connect with multi states
            if 'ϵ' in self.edges.keys():
                self.edges[char].append(state)
            else:
                self.edges[char] = [state]
        else:
            self.edges[char] = state


class FiniteAutomaton:
    def __init__(self):
        self.states = []  # all node, start state is first element
        self.accepting_states = []

    def createState(self, is_first=False):
        new_state =  State('S_{}'.format(len(self.states)))
        if is_first:
            self.states.insert(0, new_state)
        else:
            self.states.append(new_state)
        return new_state

    def resetLabel(self):
        for i, state in enumerate(self.states):
            state.label = 'S_{}'.format(i)

    def writeGVFile(self, output_path):
        draw_info = 'digraph finite_state_machine {\n' \
            + '\trankdir=LR;\n' \
            + '\tsize="1000, 1000"\n' \
            + '\tnode [shape = point ]; qi\n' \
            + '\tnode [shape = circle]; S_0\n' \
            + '\tqi -> S_0;\n'
        for state in self.accepting_states:
            draw_info += '\tnode [shape = doublecircle]; {};\n'.format(state.label)
        draw_info += '\tnode [shape = circle];\n'
        for state in self.states:
            for edge in state.edges.keys():
                target_states = state.edges[edge]
                if not isinstance(target_states, list):
                    target_states = [target_states]
                for target_state in target_states:
                    draw_info += '\t{} -> {} [ label = "{}" ];\n'.format(state.label, target_state.label, edge)
        draw_info += '}'
        with open(output_path, 'w') as f:
            f.write(draw_info)

    def readGVFile(self, gv_path):
        state_dict = {}
        with open(gv_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if 'qi ->' in line:
                    start_state_label = line.replace('qi ->', '').replace(';', '').strip()
                    start_state = self.createState(is_first=True)
                    start_state.label = start_state_label
                    state_dict[start_state_label] = start_state
                elif 'node [shape = doublecircle];' in line:
                    accepting_state_label = line.replace('node [shape = doublecircle];', '').replace(';', '').strip()
                    accepting_state = self.createState()
                    accepting_state.label = accepting_state_label
                    self.accepting_states.append(accepting_state)
                    state_dict[accepting_state_label] = accepting_state
                elif '->' in line and 'label' in line:
                    from_label, _, to_label, _, _, _, edge, _ = line.split()
                    edge = edge.replace('"', '')
                    for label in [from_label, to_label]:
                        if label not in state_dict.keys():
                            new_state = self.createState()
                            new_state.label = label
                            state_dict[label] = new_state
                    state_dict[from_label].setNext(edge, state_dict[to_label])

    def getTransitionTable(self):
        transition_table = {}
        alphabet = []
        for state in self.states:
            for char in state.edges.keys():
                if char not in alphabet:
                    alphabet.append(char)
        for state in self.states:
            table_line = []
            for char in alphabet:
                if char in state.edges.keys():
                    next_states = state.edges[char]
                    if isinstance(next_states, list):
                        table_line.append(list(map(lambda x: x.label, next_states)))
                    else:
                        table_line.append([next_states.label])
                else:
                    table_line.append(None)
            transition_table[state.label] = table_line
        return alphabet, transition_table

    def run_operations(self, other_fa=None, type='concatenation'):
        '''
        Params:
        -----
        - type: alternation / concatenation / closure

        Notes:
        -----
        - FAs should only have one accepting state
        - if type is closure, fa2 is None
        '''

        # create new states and accepting_states
        new_states = []
        new_accepting_states = []

        # load current states
        for state in self.states:
            new_states.append(state)
        if other_fa is not None:
            for state in other_fa.states:
                new_states.append(state)

        # create new start state and new end state
        start_state = self.createState()
        new_states.insert(0, start_state)
        end_state = self.createState()
        new_states.append(end_state)
        new_accepting_states.append(end_state)

        if type == 'concatenation':
            self.accepting_states[0].setNext('ϵ', other_fa.states[0])
            new_states.remove(start_state)
            new_states.remove(end_state)
            new_accepting_states.remove(end_state)
            new_accepting_states.append(other_fa.accepting_states[0])
        elif type == 'alternation':
            start_state.setNext('ϵ', self.states[0])
            start_state.setNext('ϵ', other_fa.states[0])
            self.accepting_states[0].setNext('ϵ', end_state)
            other_fa.accepting_states[0].setNext('ϵ', end_state)
        elif type == 'closure':
            start_state.setNext('ϵ', self.states[0])
            start_state.setNext('ϵ', end_state)
            self.accepting_states[0].setNext('ϵ', end_state)
            self.accepting_states[0].setNext('ϵ', self.states[0])

        self.states = new_states
        self.accepting_states = new_accepting_states
        self.resetLabel()
