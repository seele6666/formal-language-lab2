# 鍙墽琛岀▼搴忚鏄?
鏈」鐩槸 Python 鍛戒护琛岀▼搴忥紝涓嶉渶瑕侀澶栫紪璇戙€?
## 杩愯鍓嶅噯澶?
纭宸茬粡瀹夎 Python 3.10 鎴栨洿楂樼増鏈紝骞朵笖鍛戒护琛屼腑鍙互鎵ц锛?
```powershell
py --version
```

## 绋嬪簭鍏ュ彛

```powershell
py main.py simplify examples/grammar_sample.txt
py main.py pda2cfg examples/pda_sample.txt
py main.py pda2cfg examples/pda_sample.txt --simplify
```

## 娴嬭瘯鍏ュ彛

```powershell
py -m unittest discover -s tests
```

濡傛灉鏁欏笀瑕佹眰鎻愪氦鈥滃彲鎵ц绋嬪簭鈥濓紝鍙互灏嗘暣涓唬鐮佺洰褰曚綔涓虹▼搴忔彁浜わ紱涔熷彲浠ヤ娇鐢?PyInstaller 鍦ㄦ湰鏈烘墦鍖咃細

```powershell
pyinstaller --onefile main.py
```

鎵撳寘鍚庡彲鎵ц鏂囦欢浣嶄簬 `dist/main.exe`銆?
