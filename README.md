# Embedded Assistant

Assistente virtual local em Python com arquitetura modular para
**desktop e sistemas embarcados**.

O projeto foi projetado para rodar **100% offline**, com foco em
dispositivos de baixo consumo como:

- Smart TVs
- Raspberry Pi
- Edge devices
- Sistemas Linux embarcados

## Arquitetura

O sistema segue um modelo **NLP-first com fallback LLM local**. Fluxo principal do sistema:

``` text
microfone
   ↓
STT (Vosk)
   ↓
preprocessing (limpeza de texto opcional)
   ↓
Intent Classifier (TF-IDF + sklearn .pkl)
   ↓
confidence gate (decisão de confiança)
   ↓
┌──────────────────────────────────────────┐
│                                          │
│  NLP confiável (alta confiança)         │
│                                          │
│          ↓                               │
│       Router (decisão primária)         │
│          ↓                               │
│ Actions (GPIO / sistema / APIs)         │
│          ↓                               │
│ TTS (voz)                               │
│          ↓                               │
│ alto-falante                            │
│                                          │
└──────────────────────────────────────────┘
                 ↓
                 ↓ fallback inteligente (quando necessário)
                 ↓
        llama.cpp (CLI local: llama-cli / llama-completion)
                 ↓
     modelo GGUF quantizado (ex: Qwen 2.5 0.5B)
                 ↓
     extração estruturada de intenção (JSON)
                 ↓
        Router (segunda decisão)
                 ↓
        Actions (GPIO / sistema / APIs)
                 ↓
        TTS (voz)
                 ↓
        alto-falante
```

## Estrutura do projeto

```text
└── 📁 assistant
    ├── 📁 actions
    │   ├── 🐍 __init__.py
    │   ├── 🐍 gpio.py
    │   └── 🐍 system.py
    │
    ├── 📁 audio
    │   ├── 🐍 __init__.py
    │   ├── 🐍 stt.py
    │   └── 🐍 tts.py
    │
    ├── 📁 brain
    │   ├── 🐍 __init__.py
    │   ├── 📄 intent_model.pkl
    │   ├── 🐍 intents.py
    │   ├── 🐍 llm.py
    │   ├── 🐍 nlp.py
    │   ├── 🐍 prompts.py
    │   ├── 🐍 train_intents.py
    │   └── 📄 vectorizer.pkl
    │
    ├── 📁 core
    │   ├── 🐍 __init__.py
    │   ├── 🐍 logger.py
    │   └── 🐍 router.py
    │
    ├── 📁 datasets
    │   ├── 🐍 __init__.py
    │   └── ⚙️ intents.json
    │
    ├── 📁 models
    │   ├── 📁 vosk-pt
    │   │   ├── 📁 ivector
    │   │   │   ├── 📄 final.dubm
    │   │   │   ├── 📄 final.ie
    │   │   │   ├── 📄 final.mat
    │   │   │   ├── 📄 global_cmvn.stats
    │   │   │   ├── ⚙️ online_cmvn.conf
    │   │   │   └── ⚙️ splice.conf
    │   │   ├── 📄 Gr.fst
    │   │   ├── 📄 HCLr.fst
    │   │   ├── 📄 README
    │   │   ├── 📄 disambig_tid.int
    │   │   ├── 📄 final.mdl
    │   │   ├── ⚙️ mfcc.conf
    │   │   ├── 📄 phones.txt
    │   │   └── 📄 word_boundary.int
    │   │
    │   └── 📄 qwen2.5-0.5b-instruct-q4_k_m.gguf
    │
    ├── 📁 bin
    │   ├── 🧩 llama-cli.exe
    │   ├── 🧩 llama-completion.exe
    │   ├── 🧩 llama-server.exe
    │   ├── 🧩 llama.dll
    │   ├── 🧩 ggml.dll
    │   ├── 🧩 ggml-base.dll
    │   ├── 🧩 ggml-cpu*.dll
    │   ├── 🧩 ggml-rpc.dll
    │   ├── 🧩 libomp*.dll
    │   └── 🧩 (outros backends CPU/GPU)
    │
    ├── 🐍 __init__.py
    └── 🐍 main.py
```

## Módulos

```audio/```

Responsável pelo processamento de áudio em tempo real.

- ```stt.py``` → converte fala em texto (Vosk)
- ```tts.py``` → converte texto em fala (TTS offline)

```brain/```

Camada de inteligência do sistema (decisão e interpretação).

- ```nlp.py``` → classificador leve de intents (TF-IDF + sklearn ```.pkl```)
- ```router.py``` → orquestra decisão final entre NLP e LLM
- ```llm.py``` → fallback inteligente via ```llama.cpp``` (GGUF quantizado: ```qwen2.5-0.5b-instruct-q4_k_m.gguf```)
- ```train_intents.py``` → treino do modelo de intents (geração dos ```.pkl```)

```actions/```

Camada de execução de comandos.
Responsável por executar ações reais do sistema:

- controle de GPIO (LED, sensores)
- ações do sistema operacional (abrir apps, comandos)
- integração com APIs externas
- execução de comandos de dispositivo (TV / embedded)

```datasets/```

Camada de dados utilizada para treino e evolução do NLP.

- ```intents.json``` → base de intenções do sistema

Contém exemplos estruturados de frases mapeadas para intents, usados para:

- treino do modelo TF-IDF
- geração dos ```.pkl``` (```vectorizer.pkl``` e ```intent_model.pkl```)
- expansão contínua do reconhecimento de comandos

```bin/```

Camada nativa do sistema para execução do modelo de linguagem local.
Contém o runtime do llama.cpp compilado para Windows/Linux, responsável pelo fallback inteligente.

```main.py```

Ponto de entrada da aplicação. Responsável por executar o loop principal:

```python
while True:
    text = listen()
    intent = think(text)
    response = route(intent)
    speak(response)
```

## Modelo de IA

Utiliza:

- TF-IDF Vectorizer
- Logistic Regression / LinearSVC
- .pkl serializado
- llama.cpp (GGUF quantizado) qwen2.5-0.5b-instruct-q4_k_m.gguf

## Requisitos

- Python 3.11+
- Poetry
- Vosk (STT offline)
- Piper (opcional para TTS offline)
- scikit-learn (TF-IDF + LogisticRegression para intents)
- numpy / scipy (dependências do modelo NLP)
- llama.cpp (via Python bindings ou build local)
- modelo GGUF quantizado (ex: qwen2.5-0.5b-instruct-q4_k_m.gguf)

## Instalação

1. Clone o projeto:

```bash
git clone <repo-url>
cd embedded-assistant
```

1. Instale as dependências:

```bash
poetry install
```

1. Treinar modelo de intents
Antes de rodar o assistente, você pode treinar o classificador:

```bash
poetry run train
```

👉 Isso irá:

- Ler datasets/intents.json
- Treinar modelo TF-IDF + LogisticRegression
- Gerar arquivos:
  - ```brain/vectorizer.pkl```
  - ```brain/intent_model.pkl```

1. Executar via script configurado no ```pyproject.toml```:

```bash
poetry run assistant
```

1. Subir o servidor local do LLM (fallback)
O sistema utiliza o llama.cpp local como fallback inteligente quando o NLP não tem confiança suficiente.
Você pode iniciar o servidor LLM usando os scripts prontos:

Windows

```bash
scripts/run_llm_server.bat
```

Linux / WSL / Git Bash

```bash
chmod +x scripts/run_llm_server.sh
./scripts/run_llm_server.sh
```

Eles iniciam o servidor local do ```llama.cpp```, carregam o modelo GGUF: ```assistant/models/qwen2.5-0.5b-instruct-q4_k_m.gguf```

Expõem API local em:

```bash
http://127.0.0.1:8080
```

Configuração padrão:

```bash
ctx-size: 2048
threads: 4
temperature: 0.1
top-p: 0.9
```

## Build do pacote

1. Gerar wheel:

```bash
poetry build
```

Saída esperada:

```text
dist/
├── embedded_assistant-0.1.0-py3-none-any.whl
└── embedded_assistant-0.1.0.tar.gz
```

1. Instalação do wheel localmente ou em dispositivo embarcado:

```bash
pip install dist/embedded_assistant-0.1.0-py3-none-any.whl
```

1. Execute:

```bash
assistant
```
