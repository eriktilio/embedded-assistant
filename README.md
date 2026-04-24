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

Fluxo principal do sistema:

``` text
microfone
   ↓
STT (Vosk)
   ↓
Intent Classifier (TF-IDF + sklearn .pkl)
   ↓
Router (decisão primária)
   ↓
Actions (GPIO / sistema / APIs)
   ↓
TTS (voz)
   ↓
alto-falante

        ↘
         ↘ fallback inteligente (quando necessário)
            └── llama.cpp (GGUF quantizado)
                • interpretação de linguagem natural
                • comandos complexos
                • fallback para baixa confiança
```

## Estrutura do projeto

```text
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
│   └── 📄 qwen2.5-0.5b-instruct-q4_k_m.gguf
├── 📁 src
│   └── 📁 assistant
│       ├── 📁 actions
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 gpio.py
│       │   └── 🐍 system.py
│       ├── 📁 audio
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 stt.py
│       │   └── 🐍 tts.py
│       ├── 📁 brain
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 intents.py
│       │   ├── 🐍 llm.py
│       │   ├── 🐍 nlp.py
│       │   ├── 🐍 prompts.py
│       │   └── 🐍 train_intents.py
│       ├── 📁 core
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 logger.py
│       │   └── 🐍 router.py
│       ├── 🐍 __init__.py
│       └── 🐍 main.py
├── 📁 tests
├── 📝 README.md
├── 📄 poetry.lock
└── ⚙️ pyproject.toml
```

## Módulos

```audio/```

Responsável pelo processamento de áudio.

- ```stt.py``` → converte fala em texto
- ```tts.py``` → converte texto em fala

```brain/```

Camada de inteligência do sistema.

- ```nlp.py``` → TF-IDF + sklearn intents
- ```router.py``` → decisão de ação
- ```llm.py``` → fallback opcional (llama.cpp) qwen2.5-0.5b-instruct-q4_k_m.gguf
- ```train_intents.py``` → treino do modelo

```actions/```

Camada de execução. Exemplos:

- abrir aplicativos
- obter hora do sistema
- controlar GPIO
- acionar periféricos

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
- Ollama (para modelo local)
- Vosk
- Piper (opcional para TTS offline)

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

1. Executar via script configurado no ```pyproject.toml```:

```bash
poetry run assistant
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
