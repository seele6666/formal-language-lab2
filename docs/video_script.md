# 婕旂ず瑙嗛鑴氭湰

## 1. 寮€鍦?
璇存槑鏈」鐩畬鎴愨€滃舰寮忚瑷€涓庤嚜鍔ㄦ満瀹為獙锛堜簩锛夆€濓紝鍖呭惈 CFG 鍖栫畝鍜?PDA 鍒?CFG 杞崲涓や釜鍔熻兘銆?
## 2. 灞曠ず椤圭洰缁撴瀯

渚濇灞曠ず锛?
- `cfg.py`
- `cfg_parser.py`
- `cfg_simplifier.py`
- `pda.py`
- `pda_parser.py`
- `pda_to_cfg.py`
- `main.py`
- `tests/`
- `examples/`

璇存槑绠楁硶涓庡懡浠よ鍏ュ彛鍒嗙锛屼究浜庢祴璇曞拰闃呰銆?
## 3. 婕旂ず CFG 鍖栫畝

灞曠ず `examples/grammar_sample.txt`锛岃繍琛岋細

```powershell
py main.py simplify examples/grammar_sample.txt
```

璁茶В杈撳嚭涓凡缁忔秷闄?epsilon 浜х敓寮忋€佸崟浜х敓寮忓拰鏃犵敤绗﹀彿銆?
## 4. 婕旂ず PDA 杞?CFG

灞曠ず `examples/pda_sample.txt`锛岃繍琛岋細

```powershell
py main.py pda2cfg examples/pda_sample.txt
```

璇存槑鍘熷 CFG 涓彉閲?`[p,A,q]` 鐨勫惈涔夈€?
## 5. 婕旂ず PDA 杞?CFG 鍚庡寲绠€

杩愯锛?
```powershell
py main.py pda2cfg examples/pda_sample.txt --simplify
```

璇存槑杞崲缁撴灉鍙互缁х画璋冪敤 CFG 鍖栫畝绠楁硶銆?
## 6. 婕旂ず鑷姩鍖栨祴璇?
杩愯锛?
```powershell
py -m unittest discover -s tests
```

灞曠ず鎵€鏈夋祴璇曢€氳繃銆?
## 7. 缁撳熬

鎬荤粨瀹為獙鍔熻兘瀹屾垚鎯呭喌锛屽苟璇存槑鎶ュ憡涓繚鐣欎簡鎴浘浣嶇疆銆?
