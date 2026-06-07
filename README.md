# 🧠 ia-maturity-check

> Aplicação web de diagnóstico de maturidade em Inteligência Artificial — inspirada no [Polinexus.ai](https://polinexus.ai)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Anthropic](https://img.shields.io/badge/Claude_API-Anthropic-7C3AED?style=flat-square)
![Status](https://img.shields.io/badge/status-MVP-22c55e?style=flat-square)

---

## Sobre o projeto

Este projeto é uma implementação própria inspirada no **[Polinexus.ai](https://polinexus.ai)** — plataforma desenvolvida pelo cliente, que diagnostica o nível de prontidão em IA de profissionais, empresas e instituições.

No Polinexus, o usuário acessa a plataforma via web, responde formulários de autoavaliação, informa o link do seu perfil no LinkedIn, e recebe um diagnóstico estruturado com seu nível de maturidade em Inteligência Artificial.

O **ia-maturity-check** segue a mesma filosofia e fluxo de produto, construído com **Streamlit** para máxima agilidade de entrega e **Claude API** como motor de análise.

---

## Como funciona

```
Usuário acessa a aplicação
        ↓
Informa a URL do seu perfil no LinkedIn
        ↓
Responde Formulário 1 — Conhecimento Teórico (Sim / Não)
        ↓
Responde Formulário 2 — Uso Prático (Sim / Não)
        ↓
Claude API analisa o perfil completo
        ↓
Diagnóstico: Score · Nível · Pontos fortes · Gaps · Recomendações
```

---

## MVP — Versão atual

O MVP foi desenhado para ser o mais simples possível, mantendo a proposta de valor intacta: **fazer o fluxo funcionar de ponta a ponta**.

Cada formulário tem no máximo **4 perguntas de Sim ou Não** — o formato mais rápido de responder e mais fácil de processar, reduzindo atrito e aumentando a taxa de conclusão.

### Formulário 1 — Conhecimento Teórico

| # | Pergunta |
|---|----------|
| 1 | Você sabe o que é um LLM (Large Language Model)? |
| 2 | Você já ouviu falar em Machine Learning ou Deep Learning? |
| 3 | Você conhece pelo menos um risco ético do uso de IA (ex: viés algorítmico)? |
| 4 | Você acompanha regularmente novidades sobre Inteligência Artificial? |

### Formulário 2 — Uso Prático

| # | Pergunta |
|---|----------|
| 1 | Você usa alguma ferramenta de IA no dia a dia (ex: ChatGPT, Claude, Copilot)? |
| 2 | Você já automatizou alguma tarefa usando IA? |
| 3 | Você já criou um prompt elaborado para obter resultados mais precisos de uma IA? |
| 4 | Você já usou ou experimentou a API de alguma ferramenta de IA? |

### O que o diagnóstico retorna

- 🎯 **Score** de 0 a 100
- 🏷️ **Nível**: Iniciante · Explorador · Praticante · Avançado · Especialista
- ✅ **Pontos fortes** identificados
- ◎ **Gaps** a desenvolver
- 💡 **3 recomendações** práticas e personalizadas
- 🗺️ **Próximos passos** na jornada em IA

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend + Backend | [Streamlit](https://streamlit.io) (Python) |
| Motor de análise | [Claude API](https://www.anthropic.com) — `claude-sonnet-4-20250514` |
| Deploy | [Streamlit Cloud](https://share.streamlit.io) |

---

## Estrutura do projeto

```
ia-maturity-check/
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências
└── README.md
```

---

## Roadmap

| Fase | Funcionalidade | Tipo de pergunta | Status |
|------|---------------|-----------------|--------|
| **MVP** | Formulário 1 — Conhecimento Teórico (4 perguntas) | Sim / Não | ✅ Concluído |
| **MVP** | Formulário 2 — Uso Prático (4 perguntas) | Sim / Não | ✅ Concluído |
| **MVP** | Input de perfil LinkedIn | Campo de texto | ✅ Concluído |
| **MVP** | Score + Nível via Claude API | — | ✅ Concluído |
| **v1.1** | Perguntas subjetivas (texto livre) | Dissertativa | 🔵 Próximo |
| **v1.1** | Múltipla escolha nos formulários | 4 opções por pergunta | 🔵 Próximo |
| **v1.2** | Enriquecimento automático via LinkedIn | Automatizado | 🟡 Futuro |
| **v1.3** | Dashboard de respostas para o cliente | Admin panel | 🟡 Futuro |
| **v2.0** | Relatório exportável em PDF | — | 🟡 Futuro |

---

## Próximas evoluções planejadas

**v1.1 — Perguntas subjetivas e múltipla escolha**
Os formulários ganharão profundidade. Perguntas subjetivas (texto livre) permitem que a Claude API interprete nuances que respostas binárias não capturam. A múltipla escolha adiciona gradação — por exemplo: *Nunca / Raramente / Às vezes / Sempre* — tornando o diagnóstico muito mais preciso.

**v1.2 — Enriquecimento via LinkedIn**
Com o link já coletado desde o MVP, versões futuras farão scraping ou integração via LinkedIn API para extrair cargo, área e formação automaticamente, sem que o usuário precise digitar essas informações.

**v1.3 — Dashboard para o cliente**
Painel administrativo para visualizar todas as respostas coletadas, com filtros por nível, área de atuação e data. Armazenamento em banco de dados leve (SQLite ou Supabase).

**v2.0 — Relatório em PDF**
Geração automática de um relatório personalizado em PDF com o diagnóstico completo, que o usuário pode baixar e compartilhar.

---

## Inspiração

Este projeto é diretamente inspirado no **[Polinexus.ai](https://polinexus.ai)** — plataforma de diagnóstico de prontidão em IA para profissionais, empresas e instituições, desenvolvida pelo mesmo cliente. O Polinexus transforma o diagnóstico de capacidades em IA em vantagem competitiva real.

---

*MVP v1.0 · Diagnóstico de Maturidade em IA*
