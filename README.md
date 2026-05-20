# 褰㈠紡璇█涓庤嚜鍔ㄦ満瀹為獙锛堜簩锛?
鏈」鐩疄鐜扳€滀笂涓嬫枃鏃犲叧鏂囨硶涓庝笅鎺ㄨ嚜鍔ㄦ満鈥濆疄楠岋細

- CFG 鍖栫畝锛氭秷闄?epsilon 浜х敓寮忋€佸崟浜х敓寮忋€佹棤鐢ㄧ鍙枫€?- PDA 杞?CFG锛氬皢绌烘爤鎺ュ彈 PDA 杞崲涓虹瓑浠?CFG銆?- PDA 杞?CFG 鍚庡彲缁х画璋冪敤 CFG 鍖栫畝娴佺▼銆?
## 杩愯鐜

- Python 3.10 鎴栨洿楂樼増鏈€?- 浠呬娇鐢?Python 鏍囧噯搴擄紝娴嬭瘯浣跨敤 `unittest`銆?
## 甯哥敤鍛戒护

```powershell
py main.py simplify examples/grammar_sample.txt
py main.py pda2cfg examples/pda_sample.txt
py main.py pda2cfg examples/pda_sample.txt --simplify
py -m unittest discover -s tests
```

鍏煎鍛戒护锛?
```powershell
py main.py simplify-cfg examples/grammar_sample.txt
py main.py pda-to-cfg examples/pda_sample.txt --simplify
py main.py demo
```

## 杈撳叆鏍煎紡

CFG 绀轰緥锛?
```text
S -> a | b A | B | c c D
A -> a b B | eps
B -> a A
C -> d d C
D -> d d d
```

PDA 绀轰緥锛?
```text
states: q0 q1
input_symbols: a b
stack_symbols: B z0
start_state: q0
start_stack: z0
accept: empty_stack
transitions:
q0,b,z0 -> q0,B z0
q0,b,B -> q0,B B
q0,a,B -> q1,eps
q1,a,B -> q1,eps
q1,eps,B -> q1,eps
q1,eps,z0 -> q1,eps
```

## 椤圭洰缁撴瀯

- `cfg.py`锛欳FG 鏁版嵁缁撴瀯銆?- `cfg_parser.py`锛欳FG 鏂囨湰瑙ｆ瀽銆?- `cfg_simplifier.py`锛欳FG 鍖栫畝绠楁硶銆?- `pda.py`锛歅DA 鏁版嵁缁撴瀯銆?- `pda_parser.py`锛歅DA 鏂囨湰瑙ｆ瀽銆?- `pda_to_cfg.py`锛歅DA 鍒?CFG 鐨勬瀯閫犵畻娉曘€?- `main.py`锛氬懡浠よ鍏ュ彛銆?- `tests/`锛氬崟鍏冩祴璇曘€?- `examples/`锛氬疄楠屾寚瀹氭牱渚嬭緭鍏ャ€?
