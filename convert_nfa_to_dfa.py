# Ta Dang Khoa - VNU - 21025077
# NFA to DFA - Subset Construction


from finite_automaton import FiniteAutomaton


def find_e_closure(transition_table, e_idx, check_state, e_closure_list=[]):
    if check_state not in e_closure_list:
        e_closure_list.append(check_state)
    else:
        return e_closure_list
    if transition_table[check_state][e_idx] is not None:
        for next_e_state in transition_table[check_state][e_idx]:
            e_closure_list = find_e_closure(transition_table, e_idx, next_e_state, e_closure_list)
    return e_closure_list


def subset_construction(nfa):
    alphabet, transition_table = nfa.getTransitionTable()
    e_idx = alphabet.index('ϵ')

    # create DFA transition table
    dfa_sate_list = []
    dfa_transition_table = []
    list_check = [find_e_closure(transition_table, e_idx, nfa.states[0].label, e_closure_list=[])]
    while len(list_check) != 0:
        # get list nfa state need to check:
        list_check_state = list_check.pop(0)
        if list_check_state in dfa_sate_list:
            continue
        else:
            dfa_sate_list.append(list_check_state)

        # find e-closure with all states connect by char with one of current states
        table_line = []
        for idx, char in enumerate(alphabet):
            if char != 'ϵ':
                list_state_connect_by_char = []
                for state in list_check_state:
                    if transition_table[state][idx] is not None:
                        for s1 in transition_table[state][idx]:
                            for s2 in find_e_closure(transition_table, e_idx, s1, e_closure_list=[]):
                                if s2 not in list_state_connect_by_char:
                                    list_state_connect_by_char.append(s2)
                if len(list_state_connect_by_char) == 0:
                    table_line.append(None)
                else:
                    table_line.append(list_state_connect_by_char)
                    list_check.append(list_state_connect_by_char)
        dfa_transition_table.append(table_line)

    # remove ϵ from alphabet
    alphabet.remove('ϵ')

    # get list accepting states
    list_idx_of_accepting_states = []
    for i, list_state in enumerate(dfa_sate_list):
        if nfa.accepting_states[0].label in list_state:
            list_idx_of_accepting_states.append(i)

    # convert to dfa state idx
    new_dfa_transition_table = []
    for table_line in dfa_transition_table:
        new_table_line = []
        for state in table_line:
            if state is None:
                new_table_line.append(None)
            else:
                for i in range(len(dfa_sate_list)):
                    if dfa_sate_list[i] == state:
                        new_table_line.append(i)
        new_dfa_transition_table.append(new_table_line)

    # create DFA
    list_state = [None for _ in range(len(dfa_sate_list))]
    dfa = FiniteAutomaton()
    for from_state_idx, state_idx_line in enumerate(new_dfa_transition_table):
        if list_state[from_state_idx] is None:
            from_state = dfa.createState()
            from_state.label = 'S_{}'.format(from_state_idx)
            list_state[from_state_idx] = from_state
        for char_idx, to_state_idx in enumerate(state_idx_line):
            if to_state_idx is not None:
                if list_state[to_state_idx] is None:
                    to_state = dfa.createState()
                    to_state.label = 'S_{}'.format(to_state_idx)
                    list_state[to_state_idx] = to_state
                list_state[from_state_idx].setNext(alphabet[char_idx], list_state[to_state_idx])
    dfa.states[0] = list_state[0]
    for state_idx in list_idx_of_accepting_states:
        dfa.accepting_states.append(list_state[state_idx])

    return dfa


if __name__ == '__main__':
    # test some NFA
    nfa = FiniteAutomaton()
    nfa.readGVFile('test_nfa_1.gv')  # a.(b|c)*
    dfa = subset_construction(nfa)
    dfa.writeGVFile('test_dfa_1.gv')

    nfa = FiniteAutomaton()
    nfa.readGVFile('test_nfa_2.gv')  # (a.b)|(a.c)
    dfa = subset_construction(nfa)
    dfa.writeGVFile('test_dfa_2.gv')

    # run all
    nfa = FiniteAutomaton()
    nfa.readGVFile('nfa.gv')
    dfa = subset_construction(nfa)
    dfa.writeGVFile('dfa.gv')
