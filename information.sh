#!/bin/bash

# 运行 crawler/main.py
echo "Running crawler/main.py..."
python3 crawler_rebuild/main.py

# 检查是否成功
if [ $? -ne 0 ]; then
  echo "crawler/main.py 执行失败，终止脚本。"
  exit 1
fi

# 运行 langchain/deepseek.py
echo "Running langchain/deepseek.py..."
python3 langchain/deepseek.py

# 检查是否成功
if [ $? -ne 0 ]; then
  echo "langchain/deepseek.py 执行失败。"
  exit 1
fi

echo "全部脚本执行完毕。"