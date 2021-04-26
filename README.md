![compiler-pipeline](https://user-images.githubusercontent.com/13399527/116156561-a7d75600-a6b9-11eb-8fd2-34f2dc1d3553.png)

# teaching-compiler
Materials for teaching about compilers.

## Source Language
The concrete syntax of the source language:
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
          | (<name> <expr> ...)

<defn> ::= (def (<name> <name> ...) <expr>)
```

The abstract syntax is given by the following constructors:
```
Expr is one of:
  | Num(value: float)
  | Add1(operand: Expr)
  | Sub1(operand: Expr)
  | Plus(left: Expr, right: Expr)
  | Minus(left: Expr, right: Expr)
  | Times(left: Expr, right: Expr)
  | Equals(left: Expr, right: Expr)
  | If(cond: Expr, thn: Expr, els: Expr)
  | Let(name: str, value: Expr, body: Expr)
  | App(fname: str, args: List[Expr])
  | Name(name: str)
  
A Defn is:
  Defn(name: str, params: List[str], body: Expr)
```

## Target Language

| Instruction           | Description |
| --------------------- | ---------------------------------------- |
| `mov <src>, <dst>`    | Moves the `src` value into the `dst` |
| `add <src>, <dst>`    | Adds `src` and `dst`, storing the result in `dst` |
| `sub <src>, <dst>`    | Subtracts `src` from `dst`, storing the result in `dst` |
| `mul <src>, <dst>`    | Multiplies `src` and `dst`, storing the result in `dst` |
| `cmp <left>, <right>` | Compares `left` and `right` and sets flags accordingly |
| `<label>:`            | Marks a program point that can be jumped to |
| `jmp <label>`         | Start executing at the label, unconditionally |
| `je <label>`          | Start executing at the label, if `fequal` is set |
| `jne <label>`         | Start executing at the label, if `fequal` is NOT set |
| `call <label>`        | Increment `rsp`, write a return address at `[rsp + 0]`, and jump to `<label>` |
| `ret`                 | Jump to the return address at `[rsp + 0]`, decrement `rsp` |

Operands for instructions like `mov` can be immediate values, `rans`, `rsp`, or a location on the stack at an offset from `rsp` (`[rsp + offset]`). Note that for an operand to be a valid destination, it cannot be an immediate value. 

The abstract syntax of the target language is given by the following constructors:
```
Instr is one of:
  | Mov(src: Operand, dest: Operand)
  | Add(src: Operand, dest: Operand)
  | Sub(src: Operand, dest: Operand)
  | Mul(src: Operand, dest: Operand)
  | Cmp(left: Operand, right: Operand)
  | Label(label: str)
  | Jmp(target: str)
  | Je(target: str)
  | Jne(target: str)
  | Call(target: str)
  | Ret()

Operand is one of:
  | Imm(value: float)
  | Rans()
  | Rsp()
  | StackOff(off: int)
```

## Target Architecture

|          | Description |
| -------- | ------------- |
| `rans`   | Answer register  |
| `rsp`    | Stack pointer register  |
| `rip`    | Instruction pointer register (used only in VM)  |
| `fequal` | Flag. Set if `a = b` for previous `cmp a, b`  |
| `fless`  | Flag. Set if `a < b` for previous `cmp a, b`  |
| Stack    | Fixed-size array of memory locations |

## Errors

The compiler, correctly implemented, should raise errors in the following situations:
| Error     | Description |
| -------- | ------------- |
| `ArityMismatch(args, defn)` | A function was called with the wrong number of arguments |
| `UndefinedFun(fname)` | A name was used in application position that did not correspond to a function definition |
| `UnboundName(name)` | An identifier appeared in the program without a binding occurrence |

## Tests
To run all tests, run `make test` from the project root. Note that compiler tests should fail if the compiler hasn't been implemented yet.

## Scripts
There are a few scripts for useful tasks:

| Script           | Description |
| ---------------- | ------------- |
| `./compile_file` | takes a program in a file and compiles it, optionally running or emitting rasm |
| `./run_rasm`     | takes a rasm program and runs it in the rasm VM |
| `./repl`         | launches a repl, optionally using the demo implementation |

You can run any of these with the `-h` flag to see their help message.
