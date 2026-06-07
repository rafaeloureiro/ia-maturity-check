import streamlit as st
import google.generativeai as genai
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

/* Hero */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}

.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    color: #c4b5fd;
    line-height: 1.15;
    margin-bottom: 0.6rem;
}

.hero p {
    color: #a0a8b8;
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
    color: #f0f0ff;
    margin-bottom: 0.3rem;
}

.section-desc {
    color: #a0a8b8;
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

/* ── Streamlit widget overrides ── */

/* Labels de todos os widgets */
label, .stRadio label, .stCheckbox label,
div[data-testid="stSlider"] label,
div[data-testid="stRadio"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stSelectSlider"] label,
.stTextInput label {
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
}

/* Texto das opções de radio */
div[data-testid="stRadio"] div[role="radiogroup"] label,
div[data-testid="stRadio"] div[role="radiogroup"] p {
    color: #e2e8f0 !important;
}

/* Texto dentro de selectbox e multiselect */
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] span {
    color: #e2e8f0 !important;
}

/* Select slider labels */
div[data-testid="stSelectSlider"] span {
    color: #e2e8f0 !important;
}

/* Slider value */
div[data-testid="stSlider"] div[data-testid="stTickBarMin"],
div[data-testid="stSlider"] div[data-testid="stTickBarMax"] {
    color: #a0a8b8 !important;
}

/* Input de texto */
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

.stTextInput input::placeholder {
    color: #4b5563 !important;
}

/* Botão principal */
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

div.stButton > button:hover { opacity: 0.88; }
div.stButton > button:disabled { opacity: 0.4; cursor: not-allowed; }

hr {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
NIVEL_CONFIG = {
    "Iniciante":   {"emoji": "🌱", "color": "#10b981", "bg": "#052e1699"},
    "Explorador":  {"emoji": "🔭", "color": "#60a5fa", "bg": "#1e3a5f99"},
    "Praticante":  {"emoji": "⚡", "color": "#a78bfa", "bg": "#2d1f6699"},
    "Avançado":    {"emoji": "🚀", "color": "#f59e0b", "bg": "#451a0399"},
    "Especialista":{"emoji": "🧠", "color": "#f87171", "bg": "#450a0a99"},
}


# ── Gemini call ────────────────────────────────────────────────────────────────
def call_gemini(dados: dict) -> dict:
    """Envia os dados dos formulários para o Gemini e retorna o diagnóstico."""
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("gemini_api_key", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada nos Secrets.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
Você é um especialista sênior em avaliação de maturidade em Inteligência Artificial.

Analise o perfil abaixo e retorne um diagnóstico estruturado em JSON. Seja criterioso e preciso.

=== PERFIL DO USUÁRIO ===

LinkedIn: {dados.get('linkedin', 'Não informado')}
Área de atuação: {dados.get('area')}
Cargo/Função: {dados.get('cargo')}
Tempo de experiência com tecnologia: {dados.get('exp_tech')}

--- FORMULÁRIO 1: Conhecimento Teórico ---
Sabe o que é um LLM: {dados.get('f1_llm')}
Conhece ML ou Deep Learning: {dados.get('f1_ml')}
Conhece riscos éticos de IA: {dados.get('f1_etica')}
Acompanha novidades de IA regularmente: {dados.get('f1_novidades')}

--- FORMULÁRIO 2: Uso Prático ---
Usa ferramenta de IA no dia a dia: {dados.get('f2_uso_diario')}
Já automatizou alguma tarefa com IA: {dados.get('f2_automacao')}
Já criou prompts elaborados: {dados.get('f2_prompts')}
Já usou API de alguma IA: {dados.get('f2_api')}

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

    response = model.generate_content(prompt)
    raw = response.text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ── Result renderer ────────────────────────────────────────────────────────────
def render_result(result: dict):
    score = result["score"]
    nivel = result["nivel"]
    cfg = NIVEL_CONFIG.get(nivel, NIVEL_CONFIG["Iniciante"])

    st.markdown(f"""
    <div class="result-card">
        <div class="section-label" style="color:{cfg['color']};border-color:{cfg['color']}44;">
            Diagnóstico Concluído
        </div>
        <div class="score-display" style="color:{cfg['color']};">{score}<span style="font-size:1.5rem;color:#6b7280;">/100</span></div>
        <div style="margin:0.5rem 0 1rem 0;">
            <span class="level-badge" style="background:{cfg['bg']};color:{cfg['color']};border:1px solid {cfg['color']}44;">
                {cfg['emoji']} {nivel}
            </span>
        </div>
        <p style="color:#c4c8d8;font-size:0.95rem;line-height:1.7;margin:0;">{result['resumo']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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

    st.markdown('<div class="section-label" style="margin-top:1rem;">Recomendações</div>', unsafe_allow_html=True)
    for i, rec in enumerate(result.get("recomendacoes", []), 1):
        st.markdown(f"""
        <div class="card" style="margin-bottom:0.75rem;">
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#f0f0ff;font-size:0.95rem;margin-bottom:0.3rem;">
                {i}. {rec['acao']}
            </div>
            <div style="color:#a0a8b8;font-size:0.85rem;">{rec['motivo']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-color:#a78bfa33;background:linear-gradient(135deg,#1a1033,#0a0a0f);">
        <div class="section-label">Próximos Passos</div>
        <p style="color:#c4b5fd;font-size:0.95rem;line-height:1.75;margin:0;">{result['proximos_passos']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↩ Refazer diagnóstico"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    st.markdown("""
    <div class="hero">
        <h1>Diagnóstico de Maturidade em IA</h1>
        <p>Responda dois formulários rápidos e descubra seu nível real de prontidão em Inteligência Artificial.</p>
    </div>
    """, unsafe_allow_html=True)

    if "resultado" in st.session_state:
        render_result(st.session_state["resultado"])
        return

    # ── Perfil ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Perfil</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sobre você</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Essas informações ajudam a contextualizar o diagnóstico.</div>', unsafe_allow_html=True)

    linkedin = st.text_input(
        "LinkedIn (URL do seu perfil)",
        placeholder="https://linkedin.com/in/seuperfil",
        key="linkedin"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Área de atuação",
            ["Tecnologia / TI", "Dados / Analytics", "Marketing / Growth",
             "Produto / UX", "Negócios / Gestão", "Saúde", "Educação",
             "Jurídico / Compliance", "Finanças", "Outra"],
            key="area")
    with col2:
        st.selectbox("Nível do cargo",
            ["Estudante / Estagiário", "Analista / Desenvolvedor Jr",
             "Pleno / Especialista", "Sênior / Lead", "Gerente / Coordenador",
             "Diretor / VP", "C-Level / Fundador"],
            key="cargo")
    st.select_slider("Anos de experiência com tecnologia",
        options=["< 1 ano", "1–2 anos", "3–5 anos", "6–10 anos", "> 10 anos"],
        key="exp_tech")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Formulário 1 ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Formulário 1 · Teoria</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Conhecimento Teórico em IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Responda com Sim ou Não.</div>', unsafe_allow_html=True)

    st.radio("Você sabe o que é um LLM (Large Language Model)?",
        ["Sim", "Não"], horizontal=True, key="f1_llm")

    st.radio("Você já ouviu falar em Machine Learning ou Deep Learning?",
        ["Sim", "Não"], horizontal=True, key="f1_ml")

    st.radio("Você conhece pelo menos um risco ético do uso de IA (ex: viés algorítmico)?",
        ["Sim", "Não"], horizontal=True, key="f1_etica")

    st.radio("Você acompanha regularmente novidades sobre Inteligência Artificial?",
        ["Sim", "Não"], horizontal=True, key="f1_novidades")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Formulário 2 ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Formulário 2 · Prática</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Uso Prático de IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Responda com Sim ou Não.</div>', unsafe_allow_html=True)

    st.radio("Você usa alguma ferramenta de IA no dia a dia (ex: ChatGPT, Claude, Copilot)?",
        ["Sim", "Não"], horizontal=True, key="f2_uso_diario")

    st.radio("Você já automatizou alguma tarefa usando IA?",
        ["Sim", "Não"], horizontal=True, key="f2_automacao")

    st.radio("Você já criou um prompt elaborado para obter resultados mais precisos de uma IA?",
        ["Sim", "Não"], horizontal=True, key="f2_prompts")

    st.radio("Você já usou ou experimentou a API de alguma ferramenta de IA?",
        ["Sim", "Não"], horizontal=True, key="f2_api")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Botão ──────────────────────────────────────────────────────────────────
    linkedin_val = st.session_state.get("linkedin", "")
    btn_disabled = not linkedin_val or "linkedin.com/in/" not in linkedin_val.lower()

    if btn_disabled and linkedin_val:
        st.markdown('<p style="color:#f87171;font-size:0.82rem;margin-bottom:0.5rem;">⚠ Insira uma URL válida do LinkedIn (ex: https://linkedin.com/in/seuperfil)</p>', unsafe_allow_html=True)

    if st.button("🧠 Gerar meu diagnóstico", disabled=btn_disabled):
        dados = {
            "linkedin":     st.session_state.get("linkedin"),
            "area":         st.session_state.get("area"),
            "cargo":        st.session_state.get("cargo"),
            "exp_tech":     st.session_state.get("exp_tech"),
            "f1_llm":       st.session_state.get("f1_llm"),
            "f1_ml":        st.session_state.get("f1_ml"),
            "f1_etica":     st.session_state.get("f1_etica"),
            "f1_novidades": st.session_state.get("f1_novidades"),
            "f2_uso_diario":st.session_state.get("f2_uso_diario"),
            "f2_automacao": st.session_state.get("f2_automacao"),
            "f2_prompts":   st.session_state.get("f2_prompts"),
            "f2_api":       st.session_state.get("f2_api"),
        }
        with st.spinner("Analisando seu perfil com IA..."):
            try:
                resultado = call_gemini(dados)
                st.session_state["resultado"] = resultado
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao gerar o diagnóstico: {e}")

    if btn_disabled:
        st.markdown('<p style="color:#4b5563;font-size:0.82rem;text-align:center;margin-top:0.5rem;">Preencha todos os campos e insira um LinkedIn válido para liberar o diagnóstico.</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
