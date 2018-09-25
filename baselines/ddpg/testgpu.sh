#!/bin/bash
echo "Start"

# 平行處理多個工作
sleep 3 && echo "Job 1 is done" &
sleep 2 && echo "Job 2 is done" &
sleep 1 && echo "Job 3 is done" &

# 等待所有工作完成
wait

echo "Done"