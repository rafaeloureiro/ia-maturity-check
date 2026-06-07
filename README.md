# 🧠 ia-maturity-check

> Aplicação web de diagnóstico de maturidade em Inteligência Artificial — inspirada no [Polinexus.ai](https://polinexus.ai)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_3.5_Flash-Google_AI-4285F4?style=flat-square&logo=google&logoColor=white)
![Status](https://img.shields.io/badge/status-MVP-22c55e?style=flat-square)

---

## Sobre o projeto

Este projeto é uma implementação própria inspirada no **[Polinexus.ai](https://polinexus.ai)** — plataforma desenvolvida pelo cliente, que diagnostica o nível de prontidão em IA de profissionais, empresas e instituições.

No Polinexus, o usuário acessa a plataforma via web, responde formulários de autoavaliação, informa o link do seu perfil no LinkedIn, e recebe um diagnóstico estruturado com seu nível de maturidade em Inteligência Artificial.

O **ia-maturity-check** segue a mesma filosofia e fluxo de produto, construído com **Streamlit** para máxima agilidade de entrega e **Google Gemini API** como motor de análise.

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
Gemini 3.5 Flash analisa o perfil completo
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
| Motor de análise | [Google Gemini API](https://ai.google.dev) — `gemini-3.5-flash` |
| Deploy | [Streamlit Cloud](https://share.streamlit.io) |

> **API Key:** a chave `GEMINI_API_KEY` deve ser configurada nos Secrets do Streamlit Cloud (`Settings → Secrets`). Obtenha a sua gratuitamente em [aistudio.google.com](https://aistudio.google.com) — o Gemini 3.5 Flash possui free tier generoso sem necessidade de cartão de crédito.

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
| **MVP** | Score + Nível via Gemini API | — | ✅ Concluído |
| **v1.1** | Perguntas subjetivas (texto livre) | Dissertativa | 🔵 Próximo |
| **v1.1** | Múltipla escolha nos formulários | 4 opções por pergunta | 🔵 Próximo |
| **v1.2** | Definir habilidades/critérios objetivos de avaliação | — | 🔵 Próximo |
| **v1.2** | Spider chart das habilidades no resultado | Visualização | 🔵 Próximo |
| **v1.3** | Enriquecimento automático via LinkedIn | Automatizado | 🟡 Futuro |
| **v1.4** | Dashboard de respostas para o cliente | Admin panel | 🟡 Futuro |
| **v2.0** | Relatório exportável em PDF | — | 🟡 Futuro |

---

## Próximas evoluções planejadas

**v1.1 — Perguntas subjetivas e múltipla escolha**
Os formulários ganharão profundidade. Perguntas subjetivas (texto livre) permitem que o Gemini interprete nuances que respostas binárias não capturam. A múltipla escolha adiciona gradação — por exemplo: *Nunca / Raramente / Às vezes / Sempre* — tornando o diagnóstico muito mais preciso.

**v1.2 — Habilidades objetivas e spider chart**
Definição de um conjunto fixo de habilidades avaliadas (ex: Fundamentos Teóricos, Uso de Ferramentas, Prompt Engineering, Automação, Uso de APIs, Ética em IA). O resultado passará a exibir um spider chart com o score em cada eixo, tornando o diagnóstico visual, comparável e mais rico para o usuário.

**v1.3 — Enriquecimento via LinkedIn**
Com o link já coletado desde o MVP, versões futuras farão scraping ou integração via LinkedIn API para extrair cargo, área e formação automaticamente, sem que o usuário precise digitar essas informações.

**v1.4 — Dashboard para o cliente**
Painel administrativo para visualizar todas as respostas coletadas, com filtros por nível, área de atuação e data. Armazenamento em banco de dados leve (SQLite ou Supabase).

**v2.0 — Relatório em PDF**
Geração automática de um relatório personalizado em PDF com o diagnóstico completo, incluindo o spider chart, que o usuário pode baixar e compartilhar.

---

## Equipe

| Nome | Papel |
|------|-------|
| **Rafael Fernandes Loureiro Pereira** | Desenvolvedor Python |
| **Iago Wandalsen Prates** | Tech Lead |
| **Moyses Perim Netto** | Business Lead |

---

## Alinhamentos pendentes com o cliente

Antes de evoluir o produto além do MVP, os itens abaixo precisam ser discutidos e definidos com o cliente. Cada decisão impacta diretamente o escopo de desenvolvimento.

### Produto & identidade visual

| # | Pergunta | Impacto |
|---|----------|---------|
| 1 | **Nome do projeto** — qual será o nome definitivo da aplicação? | Branding, domínio, repositório |
| 2 | **Paleta de cores** — quais cores representam a identidade visual do produto? | CSS, componentes visuais |
| 3 | **A aplicação será publicada na web?** — domínio próprio ou subdomínio do Streamlit Cloud? | Infraestrutura, custo |

### Formulários & perguntas

| # | Pergunta | Impacto |
|---|----------|---------|
| 4 | **Os formulários ficam na mesma página web ou em páginas separadas?** | UX, fluxo de navegação |
| 5 | **As perguntas serão objetivas ou subjetivas?** — Sim/Não, múltipla escolha ou texto livre? | Lógica de análise, prompt da IA |
| 6 | **Quais serão as perguntas definitivas de cada formulário?** | Conteúdo central do produto |
| 7 | **Quantas perguntas por formulário?** — o MVP tem 4; qual o limite aceitável para o usuário? | UX, taxa de conclusão |

### Avaliação & resultado

| # | Pergunta | Impacto |
|---|----------|---------|
| 8 | **Quais serão os critérios objetivos de avaliação?** — quais habilidades o diagnóstico mede? | Motor de análise, spider chart |
| 9 | **Quais são os baselines de referência para cada nível?** — o que define um "Especialista"? | Calibração do score da IA |
| 10 | **O resultado será exibido com um gráfico (spider chart)?** | Escopo da v1.2 |
| 11 | **O usuário receberá o resultado por e-mail ou apenas na tela?** | Backend, integração de e-mail |

### LinkedIn

| # | Pergunta | Impacto |
|---|----------|---------|
| 12 | **Quais dados do LinkedIn serão usados?** — cargo, área, formação, publicações? | Scraping, integração via API |
| 13 | **O usuário precisa autorizar acesso ao LinkedIn ou apenas informar a URL?** | OAuth, conformidade com os termos da plataforma |

### Dados & privacidade

| # | Pergunta | Impacto |
|---|----------|---------|
| 14 | **As respostas dos usuários serão armazenadas?** | Banco de dados, LGPD |
| 15 | **O cliente quer acesso a um painel com os diagnósticos gerados?** | Dashboard admin (v1.4) |
| 16 | **Haverá política de privacidade e termos de uso?** | Conformidade legal, LGPD |

---

## Inspiração

Este projeto é diretamente inspirado no **[Polinexus.ai](https://polinexus.ai)** — plataforma de diagnóstico de prontidão em IA para profissionais, empresas e instituições, desenvolvida pelo mesmo cliente. O Polinexus transforma o diagnóstico de capacidades em IA em vantagem competitiva real.

---

*MVP v1.0 · Diagnóstico de Maturidade em IA*
