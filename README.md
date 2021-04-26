# teaching-compiler
Materials for teaching about compilers.

## Source Language
```
<expr> ::=  <number>
          | <name>
          | (add1 <expr>)
          | (sub1 <expr>)
          | (+ <expr> <expr>)
          | (- <expr> <expr>)
          | (* <expr> <expr>)
          | (= <expr> <expr>)
          | (let (<name> <expr>) <expr>)
          | (if <expr> <expr> <expr>)
          | ((<name> <expr> ...)

<defn> ::= (def (<name> <name> ...) <expr>)
```

## Target Language
```
<instr> ::= mov <operand>, <operand>
          | add <operand>, <operand>
          | sub <operand>, <operand>
          | mul <operand>, <operand>
          | cmp <operand>, <operand>
          | label:
          | jmp <label>
          | je <label>
          | jne <label>
          | call <label>
          | ret
          
<operand> ::= <number>
            | rans
            | rsp
            | [rsp + <number>]
```

## Target Architecture

- answer register: `rans`
- stack pointer register: `rsp`
- instruction pointer register: `rip`
- flags `fless`, `fequal`
- stack
