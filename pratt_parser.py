#!/usr/bin/env python3
"""Pratt parser for expression parsing with operator precedence."""
import sys, re

class Token:
    def __init__(self,type,value): self.type=type; self.value=value
    def __repr__(self): return f"{self.type}({self.value})"

def tokenize(expr):
    tokens=[]
    for m in re.finditer(r"(\d+\.?\d*)|([+\-*/^()])|\s+", expr):
        if m.group(1): tokens.append(Token("NUM",float(m.group(1))))
        elif m.group(2): tokens.append(Token("OP",m.group(2)))
    tokens.append(Token("EOF",None)); return tokens

PREC={"+":(1,"L"),"-":(1,"L"),"*":(2,"L"),"/":(2,"L"),"^":(3,"R")}

class PrattParser:
    def __init__(self,tokens): self.tokens=tokens; self.pos=0
    def peek(self): return self.tokens[self.pos]
    def next(self): t=self.tokens[self.pos]; self.pos+=1; return t
    def parse(self,min_bp=0):
        t=self.next()
        if t.type=="NUM": left=t.value
        elif t.value=="-": left=-self.parse(100)
        elif t.value=="(":
            left=self.parse(0); self.next()  # consume )
        else: raise SyntaxError(f"Unexpected {t}")
        while self.peek().type=="OP" and self.peek().value in PREC:
            op=self.peek().value; prec,assoc=PREC[op]
            if prec<min_bp: break
            self.next(); rbp=prec if assoc=="R" else prec+1
            right=self.parse(rbp)
            if op=="+": left+=right
            elif op=="-": left-=right
            elif op=="*": left*=right
            elif op=="/": left/=right
            elif op=="^": left=left**right
        return left

if __name__ == "__main__":
    exprs=["2 + 3 * 4", "(2 + 3) * 4", "2 ^ 3 ^ 2", "10 - 3 - 2", "-5 + 3"]
    for expr in exprs:
        result=PrattParser(tokenize(expr)).parse()
        print(f"  {expr:20s} = {result}")
