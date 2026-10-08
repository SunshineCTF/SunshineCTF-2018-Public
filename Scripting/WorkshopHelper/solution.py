#!/usr/bin/env python3
# API port of the intended Selenium solve. GET /start gives 30 questions plus a
# featureHint{Type} naming which question (by its id/name/class value) is the one
# to answer. Evaluate that question's math expression (JS int semantics: divide
# and modulo truncate toward zero; operands are positive) and GET /submit with
# the Authorization token until level passes NUM_QUESTIONS and the flag returns.
import sys, os, requests
BASE=os.environ.get("URL", sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:18202")
def jseval(expr):
    a,op,b=expr.split()
    a=int(a); b=int(b)
    if op=="+": v=a+b
    elif op=="-": v=a-b
    elif op=="*": v=a*b
    elif op=="/": v=a/b
    elif op=="%": v=a - b*int(a/b)   # JS % (truncated), positive operands
    r=int(v)                         # parseInt truncates toward zero
    return str(r)
def answer_for(data):
    ht=data["featureHintType"]; hv=data["featureHint"]
    for q in data["questions"]:
        if q[ht]==hv:
            return jseval(q["question"])
    raise Exception("hint question not found")
s=requests.Session()
data=s.get(BASE+"/start").json()
token=data["token"]
for _ in range(60):
    ans=answer_for(data)
    r=s.get(BASE+"/submit", headers={"Authorization":token}, params={"answer":ans})
    j=r.json()
    if "flag" in j:
        print(j["flag"].strip()); break
    if j.get("result")!="Correct":
        print("STOP:", j); break
    data=j
