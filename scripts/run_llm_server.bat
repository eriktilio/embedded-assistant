@echo off
cd /d %~dp0..\assistant\bin

echo ==============================
echo Iniciando LLM Server (llama.cpp)
echo ==============================

llama-server.exe ^
    -m ..\models\qwen2.5-0.5b-instruct-q4_k_m.gguf ^
    --host 127.0.0.1 ^
    --port 8080 ^
    --ctx-size 2048 ^
    --threads 4 ^
    --temp 0.1 ^
    --top-p 0.9

pause
