# Engineering A Compiler Example

## Install
We use `graphviz` to draw a finite-state machine
```
sudo apt install graphviz
```

We use python version 3.7.11

## Example of a Compiler
```
Program     -> begin Statements end EOF

Statements  -> Statement; Statements
             | ϵ

Statement   -> Decl
             | Assigment
             | Loop
             | print Expr

Decl        -> Type ID ; Decl
             | ϵ

Type        -> int

Assigment   -> Id = Expr

Expr        -> Expr - Expr
             | Expr * Expr
             | Expr ^ Expr
             | ( Expr )
             | ID
             | NUMBER

Loop        -> while Expr do begin Statements end

ID = [a..z]|[A..Z]([a..z]|[A..Z]|[0..9])*
NUMBER = 0|[1..9][0..9]*
```

Priority (in descending order):
- Expr in brackets
- ^
- \*
- \-

## Convert RE to NFA
```
python convert_re_to_nfa.py
```

To visualize NFA
```
dot -Tpng nfa.gv -o nfa.png
```

## Run Scanner
```
python run_table_driven_scanners.py
```

## Run parser
```
python LL\(1\)_parsing_table_parser.py
```

To visualize
```
dot -Tpng parsing_tree.gv -o parsing_tree.png
```
