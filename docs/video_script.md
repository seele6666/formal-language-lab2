# 演示视频脚本

## 1. 开场

说明本项目完成“形式语言与自动机实验（二）”，包含 CFG 化简和 PDA 到 CFG 转换两个功能。

## 2. 展示项目结构

依次展示：

- `cfg.py`
- `cfg_parser.py`
- `cfg_simplifier.py`
- `pda.py`
- `pda_parser.py`
- `pda_to_cfg.py`
- `main.py`
- `tests/`
- `examples/`

说明算法与命令行入口分离，便于测试和阅读。

## 3. 演示 CFG 化简

展示 `examples\grammar_sample.txt`，运行：

```cmd
py main.py simplify examples\grammar_sample.txt
```

讲解输出中已经消除 epsilon 产生式、单产生式和无用符号。

## 4. 演示 PDA 转 CFG

展示 `examples\pda_sample.txt`，运行：

```cmd
py main.py pda2cfg examples\pda_sample.txt
```

说明原始 CFG 中变量 `[p,A,q]` 的含义。

## 5. 演示 PDA 转 CFG 后化简

运行：

```cmd
py main.py pda2cfg examples\pda_sample.txt --simplify
```

说明转换结果可以继续调用 CFG 化简算法。

## 6. 演示自动化测试

运行：

```cmd
py -m unittest discover -s tests
```

展示所有测试通过。

## 7. 结尾

总结实验功能完成情况，并说明报告中保留了截图位置。
