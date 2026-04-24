def intent_prompt(text: str):
    return f"""
Classifique a intenção do usuário.

Responda APENAS JSON.

Formato:
{{"intent":"hora|spotify|ligar_led|fallback"}}

Regras:
- apenas 1 intenção
- sem texto extra
- sem markdown
- fallback se dúvida

Exemplos:

que horas são → {{"intent":"hora"}}
abrir spotify → {{"intent":"spotify"}}
tocar música → {{"intent":"spotify"}}
acender led → {{"intent":"ligar_led"}}

Input:
{text}

Output:
"""
