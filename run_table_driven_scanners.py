# Ta Dang Khoa - VNU - 21025077
# NFA to DFA - Table-Driven Scanners


from finite_automaton import FiniteAutomaton


def table_driven_scanners(alphabet, transition_table, accepting_states, word):
    state = 'S_0'
    lexeme = ""
    stack = ['bad']
    char_idx = -1

    while state is not None:
        char_idx += 1
        char = word[char_idx]
        lexeme += char
        if state in accepting_states:
            stack.clear()
        stack.append(state)
        if char not in alphabet or transition_table[state][alphabet.index(char)] is None:
            state = None
        else:
            state = transition_table[state][alphabet.index(char)][0]

    while state not in accepting_states and state != 'bad':
        state = stack.pop()
        lexeme = lexeme[:-1]
        char_idx -= 1

    if state in accepting_states:
        outputs = [lexeme]
    else:
        return ['error']

    if char_idx < len(word) - 2:
        outputs.extend(table_driven_scanners(alphabet, transition_table, accepting_states, word[char_idx+1:]))
        if 'error' in outputs:
            return ['error']

    return outputs


if __name__ == '__main__':
    dfa = FiniteAutomaton()
    dfa.readGVFile('dfa.gv')
    alphabet, transition_table = dfa.getTransitionTable()
    accepting_states = [state.label for state in dfa.accepting_states]

    all_words = []
    with open('input_code.txt', 'r') as f:
        for line in f.readlines():
            all_words.extend(line.split())

    output_words = []
    for word in all_words:
        output_words.extend(table_driven_scanners(alphabet, transition_table, accepting_states, word + ' '))  # add space to confirm that it always contain error state
        if 'error' in output_words:
            output_words = ['error']
            break

    for word in output_words:
        print(word)
