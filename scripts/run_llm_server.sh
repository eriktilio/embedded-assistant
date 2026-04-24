#!/bin/bash

set -e

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$BASE_DIR/assistant/bin"
MODEL="$BASE_DIR/assistant/models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

LLAMA_SERVER="$BIN/llama-server"

echo "=============================="
echo " Iniciando LLM Server (llama.cpp)"
echo "=============================="
echo "BIN:   $BIN"
echo "MODEL: $MODEL"
echo ""

if [ ! -f "$LLAMA_SERVER" ]; then
    echo "❌ Erro: llama-server não encontrado em $LLAMA_SERVER"
    exit 1
fi

if [ ! -f "$MODEL" ]; then
    echo "❌ Erro: modelo GGUF não encontrado em $MODEL"
    exit 1
fi

chmod +x "$LLAMA_SERVER"

"$LLAMA_SERVER" \
    -m "$MODEL" \
    --host 127.0.0.1 \
    --port 8080 \
    --ctx-size 2048 \
    --threads 4 \
    --temp 0.1 \
    --top-p 0.9
