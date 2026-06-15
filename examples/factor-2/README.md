# Factor 2：Explicit Tool Contract

## 运行方式

```bash
python solution/tools.py
```

> 本 Factor 不直接调用 LLM，主要展示工具接口设计、参数校验与幂等性。

## 文件

- `starter/tools.py`：骨架代码，留有 TODO。
- `solution/tools.py`：带校验、黑名单、幂等的 write_file 与 calculator 参考实现。
