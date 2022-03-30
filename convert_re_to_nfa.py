# Ta Dang Khoa - VNU - 21025077
# REs to NFA - Thompson's Construction


from string import ascii_lowercase
from finite_automaton import FiniteAutomaton


def shunt(infix):
    '''
    convert in-fix RE to po-fix RE

    Notes:
    -----
    We only support some basic operations (for example only)
    - * = 0 or more
    - | = or
    - . = concatenate
    '''
    specials = {'*': 50, '.': 40, '|': 30}
    pofix = ""
    stack = ""
    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]  # remove '(' from stack
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            pofix = pofix + c
    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]
    return pofix


def thompson_construction(RE, use_operation=True):
    '''
    convert RE to NFA

    Params:
    -----
    RE: Regular expression in post fix

    Notes:
    -----
    Only support for |, *, [0-9], [1-9], [a-z], [A-Z]
    '''
    nfa_stack = []
    idx = 0
    while True:
        if idx == len(RE):
            break
        c = RE[idx]
        if c == '*' and use_operation:
            fa = nfa_stack.pop()
            fa.run_operations(type='closure')
            nfa_stack.append(fa)
        elif c == '.' and use_operation:
            fa2 = nfa_stack.pop() 
            fa1 = nfa_stack.pop()
            fa1.run_operations(fa2, 'concatenation')
            nfa_stack.append(fa1)
        elif c == '|' and use_operation:
            fa2 = nfa_stack.pop() 
            fa1 = nfa_stack.pop()
            fa1.run_operations(fa2, 'alternation')
            nfa_stack.append(fa1)
        elif c == '[' and use_operation:
            begin_idx = idx + 1
            while RE[idx] != ']':
                idx += 1
                end_idx = idx
            if RE[begin_idx:end_idx] == 'a-z':
                fa = FiniteAutomaton()
                start_state = fa.createState()
                end_state = fa.createState()
                fa.accepting_states.append(end_state)
                for i in ascii_lowercase:
                    state = fa.createState()
                    start_state.setNext(i, state)
                    state.setNext('ϵ', end_state)
                nfa_stack.append(fa)
            elif RE[begin_idx:end_idx] == 'A-Z':
                fa = FiniteAutomaton()
                start_state = fa.createState()
                end_state = fa.createState()
                fa.accepting_states.append(end_state)
                for i in ascii_lowercase.upper():
                    state = fa.createState()
                    start_state.setNext(i, state)
                    state.setNext('ϵ', end_state)
                nfa_stack.append(fa)
            elif RE[begin_idx:end_idx] == '0-9':
                fa = FiniteAutomaton()
                start_state = fa.createState()
                end_state = fa.createState()
                fa.accepting_states.append(end_state)
                for i in map(lambda x: str(x), range(10)):
                    state = fa.createState()
                    start_state.setNext(i, state)
                    state.setNext('ϵ', end_state)
                nfa_stack.append(fa)
            elif RE[begin_idx:end_idx] == '1-9':
                fa = FiniteAutomaton()
                start_state = fa.createState()
                end_state = fa.createState()
                fa.accepting_states.append(end_state)
                for i in map(lambda x: str(x), range(1, 10)):
                    state = fa.createState()
                    start_state.setNext(i, state)
                    state.setNext('ϵ', end_state)
                nfa_stack.append(fa)
        else:
            fa = FiniteAutomaton()
            start_state = fa.createState()
            end_state = fa.createState()
            fa.accepting_states.append(end_state)
            start_state.setNext(c, end_state)
            nfa_stack.append(fa)
        idx += 1
    return nfa_stack.pop()


def thompson_construction_list_RE(REs):
    nfa = FiniteAutomaton()
    start_state = nfa.createState()
    end_state = nfa.createState()
    nfa.accepting_states.append(end_state)

    for RE in REs:
        if RE not in [';', '=', '-', '*', '^', '(', ')']:
            fa = thompson_construction(shunt(RE))
        else:
            fa = thompson_construction(RE, use_operation=False)
        for state in fa.states:
            nfa.states.append(state)
        start_state.setNext('ϵ', fa.states[0])
        fa.accepting_states[0].setNext('ϵ', end_state)
    nfa.resetLabel()
    return nfa


if __name__ == '__main__':
    # test some RE
    thompson_construction(shunt('a.(b|c)*')).writeGVFile('test_nfa_1.gv')
    thompson_construction(shunt('(a.b)|(a.c)')).writeGVFile('test_nfa_2.gv')

    # run all
    REs = ['b.e.g.i.n', 'e.n.d', 'E.O.F', 'p.r.i.n.t', 'i.n.t', 'w.h.i.l.e', 'd.o', ';', '=', '-', '*', '^', '(', ')', '([a-z]|[A-Z]).([a-z]|[A-Z]|[0-9])*', '0|([1-9].[0-9]*)']
    thompson_construction_list_RE(REs).writeGVFile('nfa.gv')
