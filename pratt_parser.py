#!/usr/bin/env python3
"""Pratt parser — top-down operator precedence parsing."""
import re
class Token:
    def __init__(self,typ,val):self.typ=typ;self.val=val
def tokenize(s):
    tokens=[]
    for m in re.finditer(r'\d+|[+\-*/()^]',s):
        v=m.group()
        if v.isdigit():tokens.append(Token("NUM",int(v)))
        else:tokens.append(Token("OP",v))
    tokens.append(Token("EOF",None));return tokens
class Parser:
    def __init__(self,tokens):self.tokens=tokens;self.pos=0
    def peek(self):return self.tokens[self.pos]
    def advance(self):t=self.tokens[self.pos];self.pos+=1;return t
    def parse(self,rbp=0):
        t=self.advance();left=self.nud(t)
        while rbp<self.lbp(self.peek()):
            t=self.advance();left=self.led(t,left)
        return left
    def nud(self,t):
        if t.typ=="NUM":return t.val
        if t.val=="-":return -self.parse(70)
        if t.val=="(":v=self.parse();self.advance();return v
        raise SyntaxError(f"Unexpected: {t.val}")
    def led(self,t,left):
        bp={"+":(10,10),"-":(10,10),"*":(20,20),"/":(20,20),"^":(30,29)}
        _,rbp=bp[t.val]
        right=self.parse(rbp)
        return {"+":left+right,"-":left-right,"*":left*right,"/":left/right,"^":left**right}[t.val]
    def lbp(self,t):
        if t.typ=="EOF" or t.val==")":return 0
        return{"+":(10,10),"-":(10,10),"*":(20,20),"/":(20,20),"^":(30,29)}.get(t.val,(0,0))[0]
def evaluate(expr):return Parser(tokenize(expr)).parse()
def main():
    for e in ["2+3*4","(2+3)*4","2^3^2","10-3-2"]:
        print(f"{e} = {evaluate(e)}")
if __name__=="__main__":main()
