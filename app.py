import streamlit as st
import anthropic
import json
import re

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diagnóstico de Maturidade em IA",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, .big-title {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

.main .block-container {
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* Header */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}

.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.6rem;
}

.hero p {
    color: #6b7280;
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
}

/* Section labels */
.section-label {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a78bfa;
    border: 1px solid #a78bfa33;
    border-radius: 4px;
    padding: 3px 10px;
    margin-bottom: 0.8rem;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #e8e8f0;
    margin-bottom: 0.3rem;
}

.section-desc {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* Cards */
.card {
    background: #11111b;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.5rem;
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, #1a1033 0%, #0d1f33 100%);
    border: 1px solid #2d2050;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
}

.level-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

.score-display {
    font-family: 'Syne', sans-serif;
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1;
    margin: 0.5rem 0 0.2rem 0;
}

/* Streamlit overrides */
div[data-testid="stSlider"] > label {
    color: #9ca3af !important;
    font-size: 0.9rem !important;
}

div[data-testid="stRadio"] > label {
    color: #9ca3af !important;
    font-size: 0.9rem !important;
}

.stTextInput > label {
    color: #9ca3af !important;
}

.stTextInput input {
    background: #0a0a0f !important;
    border: 1px solid #1e1e2e !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
}

.stTextInput input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 1px #a78bfa33 !important;
}

div[data-testid="stSelectbox"] > label {
    color: #9ca3af !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.03em;
    padding: 0.75rem 2.5rem;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
}

div.stButton > button:hover {
    opacity: 0.88;
}

div.stButton > button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* Progress bar */
.progress-bar-bg {
    background: #1e1e2e;
    border-radius: 8px;
    height: 8px;
    margin: 0.4rem 0 1.5rem 0;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #7c3aed, #2563eb, #059669);
    transition: width 0.6s ease;
}

.stSpinner {
    color: #a78bfa !important;
}

hr {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
NIVEL_CONFIG = {
    "Iniciante": {"emoji": "🌱", "color": "#10b981", "bg": "#052e1699", "range": "0–39"},
    "Explorador": {"emoji": "🔭", "color": "#60a5fa", "bg": "#1e3a5f99", "range": "40–59"},
    "Praticante": {"emoji": "⚡", "color": "#a78bfa", "bg": "#2d1f6699", "range": "60–74"},
    "Avançado": {"emoji": "🚀", "color": "#f59e0b", "bg": "#451a0399", "range": "75–89"},
    "Especialista": {"emoji": "🧠", "color": "#f87171", "bg": "#450a0a99", "range": "90–100"},
}


# ── Helpers ────────────────────────────────────────────────────────────────────
def score_to_nivel(score: int) -> str:
    if score < 40:
        return "Iniciante"
    elif score < 60:
        return "Explorador"
    elif score < 75:
        return "Praticante"
    elif score < 90:
        return "Avançado"
    else:
        return "Especialista"


def call_claude(dados: dict) -> dict:
    """Envia os dados dos formulários para o Claude e retorna o diagnóstico."""
    client = anthropic.Anthropic()

    prompt = f"""
Você é um especialista sênior em avaliação de maturidade em Inteligência Artificial.

Analise o perfil abaixo e retorne um diagnóstico estruturado em JSON. Seja criterioso e preciso.

=== PERFIL DO USUÁRIO ===

LinkedIn: {dados.get('linkedin', 'Não informado')}
Área de atuação: {dados.get('area')}
Cargo/Função: {dados.get('cargo')}
Tempo de experiência com tecnologia: {dados.get('exp_tech')}

--- FORMULÁRIO 1: Conhecimento Teórico ---
Conhecimento geral de IA (0-10): {dados.get('f1_conhecimento')}
Familiaridade com LLMs: {dados.get('f1_llm')}
Familiaridade com ML/Deep Learning: {dados.get('f1_ml')}
Conhecimento em ética e bias em IA: {dados.get('f1_etica')}
Acompanha novidades do setor: {dados.get('f1_novidades')}

--- FORMULÁRIO 2: Uso Prático ---
Usa ferramentas de IA no dia a dia: {dados.get('f2_uso_diario')}
Frequência de uso: {dados.get('f2_frequencia')}
Ferramentas que utiliza: {dados.get('f2_ferramentas')}
Já automatizou algum processo com IA: {dados.get('f2_automacao')}
Já criou prompts avançados ou fluxos de IA: {dados.get('f2_prompts')}
Já usou APIs de IA em projetos: {dados.get('f2_api')}
Nível de impacto da IA no seu trabalho: {dados.get('f2_impacto')}

=== INSTRUÇÕES ===

Retorne SOMENTE um JSON válido, sem markdown, sem explicações externas, com esta estrutura exata:

{{
  "score": <inteiro de 0 a 100>,
  "nivel": "<Iniciante|Explorador|Praticante|Avançado|Especialista>",
  "resumo": "<2-3 frases descrevendo o perfil atual da pessoa>",
  "pontos_fortes": ["<ponto 1>", "<ponto 2>", "<ponto 3>"],
  "gaps": ["<gap 1>", "<gap 2>", "<gap 3>"],
  "recomendacoes": [
    {{"acao": "<ação concreta>", "motivo": "<por quê isso ajuda>"}},
    {{"acao": "<ação concreta>", "motivo": "<por quê isso ajuda>"}},
    {{"acao": "<ação concreta>", "motivo": "<por quê isso ajuda>"}}
  ],
  "proximos_passos": "<parágrafo motivacional e direcional de 2-3 frases>"
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # Remove possíveis backticks de markdown
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def render_result(result: dict):
    """Renderiza o card de resultado."""
    score = result["score"]
    nivel = result["nivel"]
    cfg = NIVEL_CONFIG.get(nivel, NIVEL_CONFIG["Iniciante"])

    # Header do resultado
    st.markdown(f"""
    <div class="result-card">
        <div class="section-label" style="color:{cfg['color']}; border-color:{cfg['color']}44;">
            Diagnóstico Concluído
        </div>
        <div class="score-display" style="color:{cfg['color']};">{score}<span style="font-size:1.5rem;color:#6b7280;">/100</span></div>
        <div style="margin:0.5rem 0 1rem 0;">
            <span class="level-badge" style="background:{cfg['bg']};color:{cfg['color']};border:1px solid {cfg['color']}44;">
                {cfg['emoji']} {nivel}
            </span>
        </div>
        <p style="color:#9ca3af;font-size:0.95rem;line-height:1.7;margin:0;">{result['resumo']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pontos fortes e gaps lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label" style="color:#34d399;border-color:#34d39933;">Pontos Fortes</div>', unsafe_allow_html=True)
        for ponto in result.get("pontos_fortes", []):
            st.markdown(f'<p style="color:#d1fae5;font-size:0.88rem;margin:0.3rem 0;">✓ {ponto}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label" style="color:#f87171;border-color:#f8717133;">Gaps Identificados</div>', unsafe_allow_html=True)
        for gap in result.get("gaps", []):
            st.markdown(f'<p style="color:#fee2e2;font-size:0.88rem;margin:0.3rem 0;">◎ {gap}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recomendações
    st.markdown('<div class="section-label" style="margin-top:1rem;">Recomendações</div>', unsafe_allow_html=True)
    for i, rec in enumerate(result.get("recomendacoes", []), 1):
        st.markdown(f"""
        <div class="card" style="margin-bottom:0.75rem;">
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#e8e8f0;font-size:0.95rem;margin-bottom:0.3rem;">
                {i}. {rec['acao']}
            </div>
            <div style="color:#6b7280;font-size:0.85rem;">{rec['motivo']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Próximos passos
    st.markdown(f"""
    <div class="card" style="border-color:#a78bfa33;background:linear-gradient(135deg,#1a1033,#0a0a0f);">
        <div class="section-label">Próximos Passos</div>
        <p style="color:#c4b5fd;font-size:0.95rem;line-height:1.75;margin:0;">{result['proximos_passos']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Botão de refazer
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↩ Refazer diagnóstico"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ── App principal ──────────────────────────────────────────────────────────────
def main():
    # Hero
    st.markdown("""
    <div class="hero">
        <h1>Diagnóstico de Maturidade em IA</h1>
        <p>Responda dois formulários rápidos e descubra seu nível real de prontidão em Inteligência Artificial.</p>
    </div>
    """, unsafe_allow_html=True)

    # Se já tem resultado, exibe e para
    if "resultado" in st.session_state:
        render_result(st.session_state["resultado"])
        return

    # ── Perfil básico ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Perfil</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sobre você</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Essas informações ajudam a contextualizar o diagnóstico.</div>', unsafe_allow_html=True)

    with st.container():
        linkedin = st.text_input(
            "LinkedIn (URL do seu perfil)",
            placeholder="https://linkedin.com/in/seuperfil",
            key="linkedin"
        )
        col1, col2 = st.columns(2)
        with col1:
            area = st.selectbox(
                "Área de atuação",
                ["Tecnologia / TI", "Dados / Analytics", "Marketing / Growth",
                 "Produto / UX", "Negócios / Gestão", "Saúde", "Educação",
                 "Jurídico / Compliance", "Finanças", "Outra"],
                key="area"
            )
        with col2:
            cargo = st.selectbox(
                "Nível do cargo",
                ["Estudante / Estagiário", "Analista / Desenvolvedor Jr",
                 "Pleno / Especialista", "Sênior / Lead", "Gerente / Coordenador",
                 "Diretor / VP", "C-Level / Fundador"],
                key="cargo"
            )
        exp_tech = st.select_slider(
            "Anos de experiência com tecnologia",
            options=["< 1 ano", "1–2 anos", "3–5 anos", "6–10 anos", "> 10 anos"],
            key="exp_tech"
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Formulário 1: Conhecimento teórico ────────────────────────────────────
    st.markdown('<div class="section-label">Formulário 1 · Teoria</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Conhecimento Teórico em IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Avalie seu entendimento conceitual e teórico sobre IA.</div>', unsafe_allow_html=True)

    f1_conhecimento = st.slider(
        "Como você avalia seu conhecimento geral sobre Inteligência Artificial? (0 = nenhum, 10 = especialista)",
        min_value=0, max_value=10, value=3, key="f1_conhecimento"
    )

    f1_llm = st.radio(
        "Qual seu nível de familiaridade com LLMs (ChatGPT, Claude, Gemini, etc.)?",
        ["Nunca ouvi falar", "Sei o que são, mas nunca usei", "Uso como usuário final",
         "Entendo como funcionam tecnicamente", "Consigo fine-tunar ou integrar via API"],
        key="f1_llm"
    )

    f1_ml = st.radio(
        "E com Machine Learning / Deep Learning?",
        ["Não sei o que é", "Conheço os conceitos básicos", "Já treinei modelos simples",
         "Trabalho com ML regularmente", "Implanto modelos em produção"],
        key="f1_ml"
    )

    f1_etica = st.radio(
        "Você conhece os princípios de ética em IA e os riscos de viés algorítmico?",
        ["Não conheço", "Ouvi falar superficialmente", "Tenho conhecimento básico",
         "Aplico esses conceitos no meu trabalho"],
        key="f1_etica"
    )

    f1_novidades = st.radio(
        "Com que frequência você acompanha novidades do setor de IA?",
        ["Raramente / nunca", "Mensalmente", "Semanalmente", "Diariamente"],
        key="f1_novidades"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Formulário 2: Uso prático ──────────────────────────────────────────────
    st.markdown('<div class="section-label">Formulário 2 · Prática</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Uso Prático de IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Agora fale sobre como você aplica IA no dia a dia.</div>', unsafe_allow_html=True)

    f2_uso_diario = st.radio(
        "Você usa alguma ferramenta de IA no seu trabalho ou estudos?",
        ["Não", "Raramente", "Sim, ocasionalmente", "Sim, todo dia"],
        key="f2_uso_diario"
    )

    f2_ferramentas = st.multiselect(
        "Quais ferramentas de IA você utiliza? (pode marcar várias)",
        ["ChatGPT", "Claude", "Gemini", "Copilot (Microsoft)", "GitHub Copilot",
         "Midjourney / DALL-E / Stable Diffusion", "Perplexity", "Notion AI",
         "Ferramentas de BI com IA (Power BI, Looker)", "APIs de LLM (OpenAI, Anthropic...)",
         "Frameworks de ML (TensorFlow, PyTorch, scikit-learn)", "Nenhuma"],
        key="f2_ferramentas"
    )

    f2_automacao = st.radio(
        "Você já automatizou algum processo ou fluxo de trabalho usando IA?",
        ["Não", "Estou tentando, mas sem sucesso ainda",
         "Sim, automações simples", "Sim, fluxos complexos e recorrentes"],
        key="f2_automacao"
    )

    f2_prompts = st.radio(
        "Você já criou prompts avançados, chains ou agentes de IA?",
        ["Não sei o que é isso", "Conheço mas nunca fiz",
         "Fiz alguns experimentos", "Uso regularmente em projetos reais"],
        key="f2_prompts"
    )

    f2_api = st.radio(
        "Já utilizou APIs de IA (OpenAI, Anthropic, Google...) em algum projeto ou código?",
        ["Nunca", "Tentei mas não finalizei", "Sim, em projetos pessoais",
         "Sim, em projetos profissionais / produção"],
        key="f2_api"
    )

    f2_impacto = st.select_slider(
        "Qual o impacto que a IA tem hoje no seu trabalho ou carreira?",
        options=["Nenhum", "Muito pequeno", "Moderado", "Alto", "Transformador"],
        key="f2_impacto"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Botão de análise ───────────────────────────────────────────────────────
    linkedin_val = st.session_state.get("linkedin", "")
    btn_disabled = not linkedin_val or "linkedin.com/in/" not in linkedin_val.lower()

    if btn_disabled and linkedin_val:
        st.markdown('<p style="color:#f87171;font-size:0.82rem;margin-bottom:0.5rem;">⚠ Insira uma URL válida do LinkedIn (ex: https://linkedin.com/in/seuperfil)</p>', unsafe_allow_html=True)

    if st.button("🧠 Gerar meu diagnóstico", disabled=btn_disabled):
        dados = {
            "linkedin": st.session_state.get("linkedin"),
            "area": st.session_state.get("area"),
            "cargo": st.session_state.get("cargo"),
            "exp_tech": st.session_state.get("exp_tech"),
            "f1_conhecimento": st.session_state.get("f1_conhecimento"),
            "f1_llm": st.session_state.get("f1_llm"),
            "f1_ml": st.session_state.get("f1_ml"),
            "f1_etica": st.session_state.get("f1_etica"),
            "f1_novidades": st.session_state.get("f1_novidades"),
            "f2_uso_diario": st.session_state.get("f2_uso_diario"),
            "f2_frequencia": "Informado via uso diário",
            "f2_ferramentas": ", ".join(st.session_state.get("f2_ferramentas", [])) or "Nenhuma",
            "f2_automacao": st.session_state.get("f2_automacao"),
            "f2_prompts": st.session_state.get("f2_prompts"),
            "f2_api": st.session_state.get("f2_api"),
            "f2_impacto": st.session_state.get("f2_impacto"),
        }

        with st.spinner("Analisando seu perfil com IA... isso pode levar alguns segundos."):
            try:
                resultado = call_claude(dados)
                st.session_state["resultado"] = resultado
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao gerar o diagnóstico: {e}")

    if btn_disabled:
        st.markdown('<p style="color:#4b5563;font-size:0.82rem;text-align:center;margin-top:0.5rem;">Preencha todos os campos e insira um LinkedIn válido para liberar o diagnóstico.</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
