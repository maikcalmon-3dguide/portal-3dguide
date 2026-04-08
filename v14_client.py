"""
3D Guide Planning — Portal Premium do Cliente (v14_client.py) V8-Filestack
Landing Page → Formulário 5 passos → Supabase.
Upload de arquivos via Filestack (widget profissional).

Secrets necessários em .streamlit/secrets.toml (ou Streamlit Cloud):
    [supabase]
    url = "https://qdwlgtormzzhppoaxmao.supabase.co"
    key = "SUA_KEY_ANON"

    [filestack]
    api_key = "SUA_FILESTACK_API_KEY"

Arquivos na mesma pasta:
    logo_planning.png   — logo 3D Guide
    fundo.jpeg          — imagem de impacto
"""

import streamlit as st
import streamlit.components.v1 as components   # obrigatório conforme requisito
import datetime
from pathlib import Path
from supabase import create_client, Client

# ══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="3D Guide — Portal de Pedidos",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SCRIPT_DIR = Path(__file__).parent
_AZUL      = "#1a6b8a"
_AZUL2     = "#0e4d66"
_VERDE     = "#2e9e72"
_TABLE     = "pedidos_producao"

# ══════════════════════════════════════════════════════════════
# SUPABASE
# ══════════════════════════════════════════════════════════════
def get_supa() -> Client:
    if "supa" not in st.session_state:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        st.session_state.supa = create_client(url, key)
    return st.session_state.supa


def inserir_pedido(payload: dict) -> str:
    resp = get_supa().table(_TABLE).insert(payload).execute()
    if resp.data:
        return str(resp.data[0].get("id", ""))
    raise RuntimeError(f"Supabase insert error: {resp}")


# ══════════════════════════════════════════════════════════════
# CONSTANTES CLÍNICAS
# ══════════════════════════════════════════════════════════════
_MARCAS = [
    "SIN", "Neodent", "Straumann", "Implacil de Bortoli",
    "Kopp", "Titaniumfix", "Medens", "Conexão", "Nobel Biocare", "FGM", "Outro",
]
_MODELOS = {
    "SIN":                 ["Unitite Prime", "Unitite Slim", "Unitite Compact",
                            "Epikut", "Strong SW", "Outro"],
    "Neodent":             ["Helix GM", "Drive GM", "Titamax", "Alvim",
                            "Grand Morse (GM)", "Outro"],
    "Straumann":           ["BLT", "BLX", "TL (Tissue Level)", "Outro"],
    "Implacil de Bortoli": ["Due Cone (Duo)", "Maestro", "Ideale", "Facility", "Outro"],
    "Kopp":                ["Cone Morse", "Hexágono Externo", "Outro"],
    "Titaniumfix":         ["Cônico", "Hexágono Externo", "Outro"],
    "Medens":              ["Active", "Standard", "Outro"],
    "Conexão":             ["Alvim", "Porous", "Cônico", "Outro"],
    "Nobel Biocare":       ["Nobel Active", "Nobel Parallel", "NobelReplace", "Outro"],
    "FGM":                 ["Safe", "Active", "Outro"],
    "Outro":               ["Outro"],
}
_KITS = [
    "Kit Neodent (EasyGuide)", "Kit Neodent (NGS)",
    "Kit SIN (Unitite)", "Kit SIN (Epikut)", "Kit SIN (Strong SW)",
    "Kit Straumann", "Kit Implacil de Bortoli", "Kit Universal", "Outro",
]
_CONEXOES = ["HE", "CM", "HI"]
_TECNICAS = ["Aberta", "Fechada", "A definir"]
_QUADRANTES = {
    "Superior Direito (1x)":  [18, 17, 16, 15, 14, 13, 12, 11],
    "Superior Esquerdo (2x)": [21, 22, 23, 24, 25, 26, 27, 28],
    "Inferior Esquerdo (3x)": [31, 32, 33, 34, 35, 36, 37, 38],
    "Inferior Direito (4x)":  [48, 47, 46, 45, 44, 43, 42, 41],
}
_PASSOS = ["Identificação", "Técnico", "Odontograma", "Cirurgia", "Arquivos + Envio"]

# ══════════════════════════════════════════════════════════════
# CSS PREMIUM — landing (wide) e formulário (centralizado)
# ══════════════════════════════════════════════════════════════
def inject_css(estado: str):
    max_w = "1200px" if estado == "landing" else "760px"
    st.markdown(f"""
    <style>
    /* ── Streamlit chrome removal ── */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stToolbar"],
    .stAppDeployButton {{ display: none !important; }}

    .stApp {{ background: #f0f4f8; }}
    img {{ image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; }}

    .block-container {{
        max-width: {max_w} !important;
        padding-top: 0 !important; padding-bottom: 3rem !important;
        padding-left: 1.5rem !important; padding-right: 1.5rem !important;
        margin: 0 auto !important;
    }}
    .block-container > div:first-child,
    .block-container > div:first-child > div {{
        margin-top: 0 !important; padding-top: 0 !important;
    }}
    section[data-testid="stAppViewContainer"] > div:first-child {{
        padding-top: 0 !important;
    }}

    /* ── Logo ── */
    .logo-topo {{
        background: #ffffff; text-align: center;
        padding: 0.5rem 2rem; border-bottom: 1px solid #e2e8f0;
        margin: 0 -1.5rem; line-height: 1;
    }}
    .logo-topo img {{
        max-width: 450px !important; width: 100%;
        height: auto !important; object-fit: contain !important;
        display: inline-block; vertical-align: middle;
    }}

    /* ── HERO split-screen ── */
    .hero-wrapper {{
        display: flex; align-items: stretch; gap: 0;
        background: #ffffff; border-radius: 0 0 18px 18px;
        overflow: hidden; box-shadow: 0 6px 32px rgba(14,77,102,.12);
        margin: 0 -1.5rem 2rem; min-height: 460px;
    }}
    .hero-left {{
        flex: 2; padding: 2.5rem; background: #ffffff;
        display: flex; flex-direction: column; justify-content: flex-start;
    }}
    .hero-left h1 {{
        font-size: 2.2rem; font-weight: 700; color: {_AZUL2};
        line-height: 1.25; margin: 0 0 .75rem; letter-spacing: -.02em;
    }}
    .hero-left .sub {{
        font-size: .95rem; font-weight: 600; color: {_AZUL}; margin-bottom: 1.1rem;
    }}
    .hero-left p {{
        font-size: 1.05rem; color: #4b5563;
        line-height: 1.75; margin: 0 0 1.6rem; flex: 1;
    }}
    .hero-right {{
        flex: 1; overflow: hidden; line-height: 0;
    }}
    .hero-right img {{
        width: 100%; height: 100%; min-height: 460px;
        object-fit: cover; object-position: center; display: block;
        border-radius: 0 0 18px 0;
        box-shadow: -6px 0 24px rgba(14,77,102,.15);
    }}
    .hero-right-fallback {{
        width: 100%; height: 100%; min-height: 460px;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, {_AZUL2}, {_AZUL} 60%, {_VERDE});
        font-size: 5rem;
    }}
    .features {{ display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 1.4rem; }}
    .feat-badge {{
        background: #dbeafe; color: {_AZUL2};
        font-size: .72rem; font-weight: 700;
        padding: .3rem .8rem; border-radius: 20px; border: 1px solid #93c5fd;
    }}

    /* ── Barra de progresso ── */
    .prog-bar {{ display:flex; align-items:center; justify-content:center; gap:0; margin:2rem 0 1.6rem; }}
    .prog-step {{ display:flex; flex-direction:column; align-items:center; }}
    .prog-circle {{
        width:38px; height:38px; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:.8rem; font-weight:800;
        border:2px solid #d1d5db; background:#fff; color:#9ca3af;
    }}
    .prog-circle.done   {{ background:{_VERDE}; border-color:{_VERDE}; color:white; }}
    .prog-circle.active {{ background:{_AZUL};  border-color:{_AZUL};  color:white;
                           box-shadow:0 0 0 5px rgba(26,107,138,.18); }}
    .prog-label {{ font-size:.6rem; font-weight:700; color:#9ca3af; margin-top:.3rem; white-space:nowrap; }}
    .prog-label.done   {{ color:{_VERDE}; }}
    .prog-label.active {{ color:{_AZUL}; }}
    .prog-line {{ width:44px; height:2px; background:#e5e7eb; margin-bottom:1.5rem; flex-shrink:0; }}
    .prog-line.done {{ background:{_VERDE}; }}

    /* ── Cards de passo ── */
    .passo-card {{
        background:#ffffff; border-radius:16px;
        padding:2.5rem; margin-bottom:1.4rem;
        box-shadow:0 2px 20px rgba(0,0,0,.07);
    }}
    .passo-titulo {{
        font-size:1.1rem; font-weight:800; color:{_AZUL2};
        padding-bottom:.7rem; border-bottom:2px solid {_AZUL}; margin-bottom:1.4rem;
    }}
    .info-box {{
        background:#eff6ff; border-left:4px solid {_AZUL};
        padding:.7rem 1rem; border-radius:0 8px 8px 0;
        font-size:.83rem; color:#1e3a5f; margin-bottom:1.2rem; line-height:1.6;
    }}

    /* ── Botões ── */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {_AZUL2}, {_AZUL}) !important;
        border:none !important; color:white !important; font-weight:700 !important;
        border-radius:9px !important;
        box-shadow:0 3px 12px rgba(26,107,138,.25) !important;
        transition: opacity .15s !important;
    }}
    .stButton > button[kind="primary"]:hover {{ opacity:.88 !important; }}

    /* ── Odontograma ── */
    .odo-quad {{ font-size:.7rem; font-weight:700; color:#6b7280;
                 text-transform:uppercase; letter-spacing:.05em; margin-bottom:.2rem; }}
    .odo-leg  {{ display:flex; gap:.5rem; flex-wrap:wrap; margin:.8rem 0; font-size:.75rem; }}
    .odo-leg span {{ padding:3px 10px; border-radius:20px; font-weight:700; }}

    /* ── Filestack upload card ── */
    .fs-card {{
        border: 2px dashed {_AZUL};
        border-radius: 12px;
        background: #f0f9ff;
        padding: 1.2rem 1.5rem;
        margin: .5rem 0 1rem;
        text-align: center;
    }}
    .fs-card p {{ color: #1e3a5f; font-size: .85rem; margin:.4rem 0 0; }}

    /* ── Resumo ── */
    .rv-row {{ display:flex; padding:.32rem 0; border-bottom:1px solid #f3f4f6; font-size:.85rem; }}
    .rv-lbl {{ color:#6b7280; width:150px; flex-shrink:0; }}
    .rv-val {{ color:#111827; font-weight:600; }}

    /* ── Tela de sucesso ── */
    .ok-hero {{
        background: linear-gradient(135deg, {_AZUL2} 0%, {_AZUL} 60%, {_VERDE} 100%);
        border-radius:18px; padding:3.5rem 2rem;
        text-align:center; color:white; margin:2rem 0;
    }}
    .ok-hero .ico {{ font-size:3.5rem; margin-bottom:.8rem; }}
    .ok-hero h2 {{ font-size:1.6rem; font-weight:900; margin:0 0 .9rem; }}
    .ok-hero p  {{ font-size:.95rem; opacity:.92; line-height:1.75;
                   max-width:420px; margin:0 auto; }}

    input[type="text"]::spelling-error {{ text-decoration:none; }}
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# JS — autocomplete/autocorrect off
# ══════════════════════════════════════════════════════════════
_JS_NOAUTOCORRECT = """<script>
(function(){
    /* ── Autocomplete/autocorrect off ── */
    const A={autocomplete:"off",autocorrect:"off",
              autocapitalize:"none",spellcheck:"false"};
    function p(e){for(const[k,v]of Object.entries(A))
        if(e.getAttribute(k)!==v)e.setAttribute(k,v);}
    function s(){document.querySelectorAll(
        'input[type="text"],input:not([type]),textarea').forEach(p);}
    s(); new MutationObserver(s).observe(document.body,{childList:true,subtree:true});
})();
</script>"""

def inject_js():
    components.html(_JS_NOAUTOCORRECT, height=0, scrolling=False)


def ti(label, key=None, placeholder="", value="", help=None):
    kw = dict(label=label, placeholder=placeholder, autocomplete="off")
    if key  is not None: kw["key"]   = key
    if value:            kw["value"] = value
    if help is not None: kw["help"]  = help
    return st.text_input(**kw)


# ══════════════════════════════════════════════════════════════
# UPLOAD VIA FILESTACK CDN — arquivos grandes sem limite
#
# O Filestack faz o upload diretamente do browser para o CDN
# deles — sem passar pelo Python/Streamlit, sem limite de 50MB.
# O dentista usa o widget, vê a URL gerada e confirma no campo.
# ══════════════════════════════════════════════════════════════
import streamlit.components.v1 as components   # noqa: E402


def _fs_picker_html(api_key: str) -> str:
    """HTML auto-contido do picker Filestack. Roda dentro do iframe do Streamlit."""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="https://static.filestackapi.com/filestack-js/3.x.x/filestack.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,sans-serif;}}
html,body{{height:100%;background:#f0f9ff;}}
body{{padding:.6rem;display:flex;flex-direction:column;gap:.5rem;}}
#btn{{
  width:100%;background:linear-gradient(135deg,#0e4d66,#1a6b8a);
  color:#fff;font-size:.95rem;font-weight:700;padding:.8rem 1rem;
  border:none;border-radius:9px;cursor:pointer;
  box-shadow:0 3px 12px rgba(14,77,102,.3);flex-shrink:0;
}}
#btn:hover{{opacity:.88;}}
#hint{{font-size:.78rem;color:#4b5563;text-align:center;}}
#msg{{font-size:.82rem;color:#1e3a5f;min-height:1.2rem;padding:.3rem 0;}}
#urls{{
  font-size:.75rem;color:#059669;word-break:break-all;
  white-space:pre-wrap;display:none;
  background:#ecfdf5;border:1px solid #6ee7b7;border-radius:8px;
  padding:.5rem .7rem;line-height:1.6;
}}
#urls b{{display:block;margin-bottom:.2rem;color:#065f46;}}
</style></head><body>
<button id="btn">📎 Clique aqui para selecionar ou arrastar arquivos</button>
<div id="hint">Aceita ZIP · STL · DCM · PDF · PNG · JPG · qualquer formato · qualquer tamanho</div>
<div id="msg"></div>
<div id="urls"></div>
<script>
var cl = filestack.init('{api_key}');
var accumulated = '';

document.getElementById('btn').addEventListener('click', function(){{
  cl.picker({{
    fromSources:['local_file_system','googledrive','dropbox'],
    maxFiles: 20,
    uploadInBackground: false,
    onUploadDone: function(r){{
      var files = r.filesUploaded || [];
      if(!files.length){{ setMsg('⚠️ Nenhum arquivo retornado.'); return; }}
      var newUrls = files.map(function(f){{return f.url;}}).join('|');
      accumulated = accumulated ? accumulated+'|'+newUrls : newUrls;
      var count = accumulated.split('|').filter(Boolean).length;
      setMsg('✅ '+files.length+' arquivo(s) enviado(s) agora. Total acumulado: '+count);
      var el = document.getElementById('urls');
      el.style.display='block';
      el.innerHTML = '<b>🔗 Copie o link abaixo e cole no campo "Passo 2":</b>' + accumulated;
    }},
    onFileUploadFailed: function(f,e){{
      setMsg('⚠️ Erro: '+(e.message||String(e)));
    }}
  }}).open();
}});

function setMsg(t){{ document.getElementById('msg').textContent=t; }}
</script></body></html>"""


def render_uploader() -> None:
    """
    Upload de arquivos grandes via Filestack CDN (sem limite de tamanho).

    Fluxo:
    1. Dentista clica no botão → janela do Filestack abre
    2. Filestack faz upload direto para o CDN deles (browser → CDN)
    3. URL aparece no widget em verde
    4. Dentista copia e cola no campo de texto abaixo
    5. Sistema registra e acumula as URLs
    """
    if "fs_fila" not in st.session_state:
        st.session_state["fs_fila"] = []   # [{nome, url}]

    # Tenta ler a api_key do Filestack
    try:
        api_key = st.secrets["filestack"]["api_key"]
        tem_filestack = bool(api_key)
    except Exception:
        api_key = ""
        tem_filestack = False

    st.warning(
        "⚠️ **DICOM:** envie a pasta compactada em **.ZIP** ou **.7z**. "
        "STL, fotos e PDFs podem ser individuais."
    )

    if tem_filestack:
        st.markdown(
            "**Passo 1:** Clique no botão abaixo para selecionar os arquivos "
            "(qualquer tamanho, inclusive tomografias de 1GB+)."
        )
        components.html(_fs_picker_html(api_key), height=520, scrolling=True)

        st.markdown(
            "**Passo 2:** Após o upload terminar, o link aparece em verde no widget acima. "
            "**Copie-o e cole no campo abaixo** para confirmar:"
        )
    else:
        st.error("⚠️ Filestack não configurado. Adicione `[filestack] api_key` nos Secrets.")
        st.info("Sem o Filestack, apenas arquivos pequenos (< 50 MB) podem ser enviados "
                "pelo campo abaixo.")

    # Campo de texto — único ponto de entrada confiável JS→Python
    # O dentista cola a URL gerada pelo widget (ou digita manualmente)
    url_colada = st.text_input(
        "🔗 Cole aqui a URL do arquivo após o upload",
        placeholder="https://cdn.filestackcontent.com/...",
        key="fs_url_input",
        help="Após o upload terminar no widget acima, copie o link verde "
             "e cole aqui. Para múltiplos uploads, cole cada link separado por |",
    ).strip()

    col_add, col_clear = st.columns([3, 1])

    if col_add.button("➕ Adicionar à fila", key="fs_add",
                      use_container_width=True,
                      help="Adiciona o link colado à lista de arquivos do pedido"):
        if url_colada:
            # Processa múltiplos links separados por |
            novos = [u.strip() for u in url_colada.split("|")
                     if u.strip().startswith("http")]
            ja_na_fila = {item["url"] for item in st.session_state["fs_fila"]}
            adicionados = 0
            for u in novos:
                if u not in ja_na_fila:
                    nome = u.rstrip("/").split("/")[-1].split("?")[0] or "arquivo"
                    st.session_state["fs_fila"].append({"nome": nome, "url": u})
                    adicionados += 1
            if adicionados:
                st.success(f"✅ {adicionados} link(s) adicionado(s) à fila.")
                st.rerun()
            else:
                st.warning("Link já está na fila ou não é uma URL válida.")
        else:
            st.warning("Cole a URL do arquivo antes de adicionar.")

    if col_clear.button("🗑️ Limpar", key="fs_clear_all",
                        use_container_width=True):
        st.session_state["fs_fila"] = []
        st.rerun()

    # Lista de arquivos na fila
    fila = st.session_state["fs_fila"]
    if fila:
        st.success(f"**📋 {len(fila)} arquivo(s) na fila para envio:**")
        for i, item in enumerate(fila):
            c1, c2 = st.columns([7, 1])
            c1.markdown(f"&nbsp;&nbsp;✅ **{i+1}.** `{item['nome']}`")
            if c2.button("✕", key=f"rm_{i}", help=f"Remover {item['nome']}"):
                st.session_state["fs_fila"].pop(i)
                st.rerun()
    else:
        st.info("ℹ️ Nenhum arquivo na fila. Use o widget acima para fazer o upload.")


def get_urls_fila() -> str:
    """Retorna todas as URLs da fila unidas por | para gravar no Supabase."""
    return "|".join(
        item["url"] for item in st.session_state.get("fs_fila", [])
        if item.get("url", "").startswith("http")
    )


# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
def _init():
    defaults = {
        "estado":           "landing",
        "pp_passo":         1,
        "pp_email":         "",
        "pp_prof":          "",
        "pp_whats":         "",
        "pp_pac":           "",
        "pp_clinica":       "",
        "pp_descricao":     "",
        "pp_marca":         _MARCAS[0],
        "pp_marca_outro":   "",
        "pp_modelo":        _MODELOS[_MARCAS[0]][0],
        "pp_modelo_outro":  "",
        "pp_kit":           _KITS[0],
        "pp_kit_outro":     "",
        "pp_conexao":       _CONEXOES[0],
        "pp_estados":       {},
        "pp_prot_max":      False,
        "pp_prot_mand":     False,
        "pp_n_implantes":   1,
        "pp_tecnica":       _TECNICAS[0],
        "pp_data_cirurgia": datetime.date.today() + datetime.timedelta(days=30),
        "fs_fila":          [],    # lista de {nome, url} — upload nativo
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _reset_form():
    for k in [k for k in st.session_state if k.startswith("pp_") or k == "fs_fila"]:
        del st.session_state[k]
    if "estado" in st.session_state:
        del st.session_state["estado"]
    _init()


def _resolve(val, outro):
    return outro.strip() if val == "Outro" and outro.strip() else val


# ══════════════════════════════════════════════════════════════
# LOGO
# ══════════════════════════════════════════════════════════════
def _render_logo():
    import base64
    logo = SCRIPT_DIR / "logo_planning.png"
    if logo.exists():
        b64 = base64.b64encode(logo.read_bytes()).decode()
        img = (f'<img src="data:image/png;base64,{b64}" '
               f'alt="3D Guide" style="max-width:450px;height:auto;">')
    else:
        img = f'<span style="font-size:1.8rem;font-weight:900;color:{_AZUL2}">🦷 3D GUIDE</span>'
    st.markdown(f'<div class="logo-topo">{img}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# BARRA DE PROGRESSO
# ══════════════════════════════════════════════════════════════
def _prog(passo):
    total  = len(_PASSOS)
    partes = []
    for i, lbl in enumerate(_PASSOS, start=1):
        cls = "done" if i < passo else ("active" if i == passo else "")
        ico = "✓" if i < passo else str(i)
        partes.append(
            f'<div class="prog-step">'
            f'<div class="prog-circle {cls}">{ico}</div>'
            f'<div class="prog-label {cls}">{lbl}</div>'
            f'</div>')
        if i < total:
            partes.append(f'<div class="prog-line {"done" if i < passo else ""}"></div>')
    st.markdown(f'<div class="prog-bar">{"".join(partes)}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ODONTOGRAMA — 5 estados
# ══════════════════════════════════════════════════════════════
def _odontograma():
    estados = st.session_state.pp_estados
    _I = {0:("",""),1:("🔵","#bfdbfe"),2:("🔴","#fecaca"),
          3:("🟣","#e9d5ff"),4:("🟢","#bbf7d0")}

    for quad, dentes in _QUADRANTES.items():
        st.markdown(f'<div class="odo-quad">{quad}</div>', unsafe_allow_html=True)
        cols = st.columns(len(dentes))
        for col, d in zip(cols, dentes):
            est   = estados.get(d, 0)
            emoji, _ = _I[est]
            lbl   = f"{emoji}{d}" if emoji else str(d)
            tip   = ["Limpo","Implante","Exodontia","Imediato","Pôntico"][est]
            if col.button(lbl, key=f"d_{d}", use_container_width=True, help=tip):
                estados[d] = (est + 1) % 5
                st.rerun()

    st.markdown("""<div class="odo-leg">
        <span style="background:#bfdbfe">🔵 Implante</span>
        <span style="background:#fecaca">🔴 Exodontia</span>
        <span style="background:#e9d5ff">🟣 Imediato</span>
        <span style="background:#bbf7d0">🟢 Pôntico</span>
        <span style="background:#f3f4f6;color:#9ca3af">Sem marcação = Livre</span>
    </div><small style="color:#9ca3af">Clique repetido alterna em ciclo.</small>
    """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    st.session_state.pp_prot_max  = c1.checkbox("✅ Protocolo Maxila",
                                                  value=st.session_state.pp_prot_max)
    st.session_state.pp_prot_mand = c2.checkbox("✅ Protocolo Mandíbula",
                                                  value=st.session_state.pp_prot_mand)

    imp  = sorted(d for d, e in estados.items() if e == 1)
    exo  = sorted(d for d, e in estados.items() if e == 2)
    imed = sorted(d for d, e in estados.items() if e == 3)
    pont = sorted(d for d, e in estados.items() if e == 4)
    linhas = []
    if imp:  linhas.append(f"🔵 **Implantar:** {', '.join(str(d) for d in imp)}")
    if exo:  linhas.append(f"🔴 **Extrair:** {', '.join(str(d) for d in exo)}")
    if imed: linhas.append(f"🟣 **Imediato:** {', '.join(str(d) for d in imed)}")
    if pont: linhas.append(f"🟢 **Suspenso:** {', '.join(str(d) for d in pont)}")
    if linhas:
        st.markdown("  \n".join(linhas))


# ══════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════
def render_landing():
    import base64

    fundo = SCRIPT_DIR / "fundo.jpeg"
    if fundo.exists():
        img_data = base64.b64encode(fundo.read_bytes()).decode()
        img_html = (
            '<div class="hero-right">'
            f'<img src="data:image/jpeg;base64,{img_data}" '
            'alt="3D Guide Implantodontia Digital">'
            '</div>'
        )
    else:
        img_html = (
            '<div class="hero-right">'
            '<div class="hero-right-fallback">🦷</div>'
            '</div>'
        )

    st.markdown(f"""
    <div class="hero-wrapper">
      <div class="hero-left">
        <h1>🦾 O Futuro da Implantodontia Digital está Aqui.</h1>
        <div class="sub">Precisão cirúrgica e suporte especializado
        para o seu planejamento virtual.</div>
        <p>
          Sua cirurgia começa com a máxima precisão no Portal 3D Guide.
          Transformamos sua tomografia em um protocolo digital
          <strong>seguro, previsível e de alta fidelidade</strong>.<br><br>
          Para garantirmos a acurácia total do seu guia cirúrgico,
          preencha as informações abaixo com atenção aos detalhes.
          <em>Cada campo é fundamental para o sucesso do seu caso.</em>
        </p>
        <div class="features">
          <span class="feat-badge">🦷 Odontograma Digital</span>
          <span class="feat-badge">🔩 Tríade de Implantes</span>
          <span class="feat-badge">📅 Agendamento Cirúrgico</span>
          <span class="feat-badge">🔒 Dados Seguros</span>
        </div>
      </div>
      {img_html}
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    if col.button("➕  Iniciar Planejamento Virtual",
                  type="primary", use_container_width=True):
        st.session_state.estado = "formulario"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# FORMULÁRIO — 5 passos
# ══════════════════════════════════════════════════════════════
def render_formulario():
    passo = st.session_state.pp_passo
    _prog(passo)

    # ── Passo 1: Identificação ────────────────────────────────
    if passo == 1:
        st.markdown('<div class="passo-card">', unsafe_allow_html=True)
        st.markdown('<div class="passo-titulo">👤 Identificação</div>',
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.pp_email = ti(
                "📧 E-mail", key="pp_email_in",
                placeholder="voce@clinica.com.br",
                value=st.session_state.pp_email)
            st.session_state.pp_prof = ti(
                "🩺 Nome do Profissional", key="pp_prof_in",
                placeholder="Dr. Nome Sobrenome",
                value=st.session_state.pp_prof)
        with c2:
            st.session_state.pp_whats = ti(
                "📱 WhatsApp (com DDD)", key="pp_whats_in",
                placeholder="(27) 9 9999-9999",
                value=st.session_state.pp_whats)
            st.session_state.pp_clinica = ti(
                "🏥 Nome da Clínica", key="pp_clinica_in",
                placeholder="Ex.: Clínica Sorriso",
                value=st.session_state.pp_clinica)
        st.markdown("---")
        st.session_state.pp_pac = ti(
            "👤 Nome completo do Paciente", key="pp_pac_in",
            placeholder="Nome exato como no prontuário",
            value=st.session_state.pp_pac)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        b1, b2 = st.columns([1, 3])
        if b1.button("← Início", use_container_width=True):
            st.session_state.estado = "landing"; st.rerun()
        if b2.button("Próximo →", type="primary", use_container_width=True):
            if not all([st.session_state.pp_email.strip(),
                        st.session_state.pp_prof.strip(),
                        st.session_state.pp_pac.strip(),
                        st.session_state.pp_clinica.strip()]):
                st.error("⚠️ Preencha todos os campos para continuar.")
            else:
                st.session_state.pp_passo = 2; st.rerun()

    # ── Passo 2: Configuração Técnica ─────────────────────────
    elif passo == 2:
        st.markdown('<div class="passo-card">', unsafe_allow_html=True)
        st.markdown('<div class="passo-titulo">⚙️ Configuração Técnica</div>',
                    unsafe_allow_html=True)
        st.session_state.pp_descricao = st.text_area(
            "📝 Breve Descrição do Caso",
            value=st.session_state.pp_descricao, height=110,
            placeholder="Descreva o caso, histórico relevante...",
            key="pp_desc_in")
        st.markdown("---")
        st.markdown("**🔩 Sistema de Implante**")
        st.caption("Marca e Modelo identificam o implante. Kit é independente.")
        c1, c2, c3 = st.columns(3)
        with c1:
            idx_m = (_MARCAS.index(st.session_state.pp_marca)
                     if st.session_state.pp_marca in _MARCAS else 0)
            nova = st.selectbox("🏷️ Marca", _MARCAS, index=idx_m, key="pp_marca_in")
            if nova != st.session_state.pp_marca:
                st.session_state.pp_marca  = nova
                st.session_state.pp_modelo = _MODELOS.get(nova, ["Outro"])[0]
                st.rerun()
            if st.session_state.pp_marca == "Outro":
                st.session_state.pp_marca_outro = ti(
                    "Especifique", key="pp_marca_out",
                    value=st.session_state.pp_marca_outro)
        with c2:
            mods = _MODELOS.get(st.session_state.pp_marca, ["Outro"])
            idx_mod = (mods.index(st.session_state.pp_modelo)
                       if st.session_state.pp_modelo in mods else 0)
            st.session_state.pp_modelo = st.selectbox(
                "📐 Modelo", mods, index=idx_mod, key="pp_modelo_in")
            if st.session_state.pp_modelo == "Outro":
                st.session_state.pp_modelo_outro = ti(
                    "Especifique", key="pp_modelo_out",
                    value=st.session_state.pp_modelo_outro)
        with c3:
            idx_k = (_KITS.index(st.session_state.pp_kit)
                     if st.session_state.pp_kit in _KITS else 0)
            st.session_state.pp_kit = st.selectbox(
                "🧰 Kit Cirúrgico", _KITS, index=idx_k, key="pp_kit_in")
            if st.session_state.pp_kit == "Outro":
                st.session_state.pp_kit_outro = ti(
                    "Especifique", key="pp_kit_out",
                    value=st.session_state.pp_kit_outro)
        st.markdown("---")
        idx_con = (_CONEXOES.index(st.session_state.pp_conexao)
                   if st.session_state.pp_conexao in _CONEXOES else 0)
        st.session_state.pp_conexao = st.selectbox(
            "🔗 Tipo de Conexão", _CONEXOES, index=idx_con, key="pp_con_in")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col_v, col_n = st.columns(2)
        if col_v.button("← Voltar", use_container_width=True):
            st.session_state.pp_passo = 1; st.rerun()
        if col_n.button("Próximo →", type="primary", use_container_width=True):
            st.session_state.pp_passo = 3; st.rerun()

    # ── Passo 3: Odontograma ──────────────────────────────────
    elif passo == 3:
        st.markdown('<div class="passo-card">', unsafe_allow_html=True)
        st.markdown('<div class="passo-titulo">🦷 Odontograma Digital</div>',
                    unsafe_allow_html=True)
        st.markdown("""<div class="info-box">
            Clique nos dentes para indicar o tipo de intervenção.
            Clique repetido alterna os estados em ciclo.</div>""",
            unsafe_allow_html=True)
        _odontograma()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col_v, col_n = st.columns(2)
        if col_v.button("← Voltar", use_container_width=True):
            st.session_state.pp_passo = 2; st.rerun()
        if col_n.button("Próximo →", type="primary", use_container_width=True):
            st.session_state.pp_passo = 4; st.rerun()

    # ── Passo 4: Detalhes Cirúrgicos ──────────────────────────
    elif passo == 4:
        st.markdown('<div class="passo-card">', unsafe_allow_html=True)
        st.markdown('<div class="passo-titulo">🔬 Detalhes Cirúrgicos</div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        st.session_state.pp_n_implantes = c1.number_input(
            "Nº de Implantes", min_value=1, max_value=32,
            value=st.session_state.pp_n_implantes, step=1)
        idx_tec = (_TECNICAS.index(st.session_state.pp_tecnica)
                   if st.session_state.pp_tecnica in _TECNICAS else 0)
        st.session_state.pp_tecnica = c2.selectbox(
            "Técnica Preferida", _TECNICAS, index=idx_tec, key="pp_tec_in")
        st.session_state.pp_data_cirurgia = c3.date_input(
            "📅 Data Prevista", value=st.session_state.pp_data_cirurgia,
            format="DD/MM/YYYY", key="pp_dci_in")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col_v, col_n = st.columns(2)
        if col_v.button("← Voltar", use_container_width=True):
            st.session_state.pp_passo = 3; st.rerun()
        if col_n.button("Ver Resumo e Enviar →", type="primary",
                        use_container_width=True):
            st.session_state.pp_passo = 5; st.rerun()

    # ── Passo 5: Arquivos (Filestack) + Revisão + Envio ───────
    elif passo == 5:
        marca_final  = _resolve(st.session_state.pp_marca,  st.session_state.pp_marca_outro)
        modelo_final = _resolve(st.session_state.pp_modelo, st.session_state.pp_modelo_outro)
        kit_final    = _resolve(st.session_state.pp_kit,    st.session_state.pp_kit_outro)
        estados      = st.session_state.pp_estados

        imp_s  = ",".join(str(d) for d, e in sorted(estados.items()) if e == 1)
        exo_s  = ",".join(str(d) for d, e in sorted(estados.items()) if e == 2)
        imed_s = ",".join(str(d) for d, e in sorted(estados.items()) if e == 3)
        pont_s = ",".join(str(d) for d, e in sorted(estados.items()) if e == 4)

        # ── Upload Filestack ──────────────────────────────────
        st.markdown('<div class="passo-card">', unsafe_allow_html=True)
        st.markdown('<div class="passo-titulo">📎 Arquivos do Caso</div>',
                    unsafe_allow_html=True)
        st.markdown("""<div class="info-box">
            Selecione ou arraste os arquivos do caso. O upload é feito
            automaticamente assim que você escolher — sem passos extras.
            </div>""", unsafe_allow_html=True)

        render_uploader()

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Resumo ────────────────────────────────────────────
        def rv(lbl, val):
            return (f'<div class="rv-row">'
                    f'<span class="rv-lbl">{lbl}</span>'
                    f'<span class="rv-val">{val}</span></div>')

        odo_html = ""
        if imp_s:  odo_html += rv("🔵 Implantar", imp_s)
        if exo_s:  odo_html += rv("🔴 Extrair", exo_s)
        if imed_s: odo_html += rv("🟣 Imediato", imed_s)
        if pont_s: odo_html += rv("🟢 Suspenso", pont_s)
        if st.session_state.pp_prot_max:
            odo_html += rv("", "✅ Protocolo Maxila")
        if st.session_state.pp_prot_mand:
            odo_html += rv("", "✅ Protocolo Mandíbula")

        st.markdown('<div class="passo-card">', unsafe_allow_html=True)
        st.markdown('<div class="passo-titulo">📋 Revisar e Enviar</div>',
                    unsafe_allow_html=True)
        st.markdown(
            rv("Profissional", st.session_state.pp_prof) +
            rv("Clínica",      st.session_state.pp_clinica) +
            rv("Paciente",     st.session_state.pp_pac) +
            rv("WhatsApp",     st.session_state.pp_whats) +
            rv("E-mail",       st.session_state.pp_email) +
            rv("Marca",        marca_final) +
            rv("Modelo",       modelo_final) +
            rv("Kit",          kit_final) +
            rv("Conexão",      st.session_state.pp_conexao) +
            rv("Técnica",      st.session_state.pp_tecnica) +
            rv("Nº Implantes", str(st.session_state.pp_n_implantes)) +
            rv("Data Cirurgia",
               st.session_state.pp_data_cirurgia.strftime("%d/%m/%Y")) +
            odo_html,
            unsafe_allow_html=True)

        if st.session_state.pp_descricao.strip():
            st.info(f"📝 {st.session_state.pp_descricao[:300]}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col_v, col_env = st.columns([1, 2])
        if col_v.button("← Voltar", use_container_width=True):
            st.session_state.pp_passo = 4; st.rerun()

        if col_env.button("🚀 Enviar Pedido para a 3D Guide",
                          type="primary", use_container_width=True):
            with st.spinner("Salvando pedido…"):
                try:
                    urls_validas = get_urls_fila()   # URLs já no Supabase Storage

                    payload = {
                        "email":            st.session_state.pp_email.strip(),
                        "profissional":     st.session_state.pp_prof.strip(),
                        "whatsapp":         st.session_state.pp_whats.strip(),
                        "paciente":         st.session_state.pp_pac.strip(),
                        "clinica_origem":   st.session_state.pp_clinica.strip(),
                        "descricao_caso":   st.session_state.pp_descricao.strip(),
                        "sistema_implante": marca_final,
                        "marca_implante":   marca_final,
                        "modelo_implante":  modelo_final,
                        "kit_cirurgico":    kit_final,
                        "conexao":          st.session_state.pp_conexao,
                        "dentes_implante":  imp_s,
                        "dentes_exodontia": exo_s,
                        "dentes_imediato":  imed_s,
                        "dentes_pontico":   pont_s,
                        "protocolo_maxila": int(st.session_state.pp_prot_max),
                        "protocolo_mandib": int(st.session_state.pp_prot_mand),
                        "num_implantes":    st.session_state.pp_n_implantes,
                        "tecnica":          st.session_state.pp_tecnica,
                        "data_cirurgia":    st.session_state.pp_data_cirurgia.strftime("%Y-%m-%d"),
                        # ── Status ────────────────────────────────────────
                        # "Caixa de Entrada" é a 1ª coluna do Painel Operacional
                        # no app.py (_KANBAN_COLS[0]). NÃO altere este valor.
                        "status":           "Caixa de Entrada",
                        # ── URLs do Filestack ──────────────────────────────
                        # urls_validas: links filtrados e unidos por |
                        # Gravadas em DUAS colunas para compatibilidade total
                        "arquivo_url":      urls_validas,
                        "arquivos_paths":   urls_validas,
                        "faturado":         False,
                        "empresa_destino":  "",
                    }
                    inserir_pedido(payload)
                    # Limpa fila de arquivos para o próximo pedido
                    st.session_state["fs_fila"] = []
                    st.session_state.estado = "sucesso"
                    st.rerun()

                except Exception as e:
                    st.error(f"⚠️ Erro ao enviar: {e}")
                    st.caption("Tente novamente ou entre em contato via WhatsApp.")


# ══════════════════════════════════════════════════════════════
# TELA DE SUCESSO
# ══════════════════════════════════════════════════════════════
def render_sucesso():
    st.balloons()
    st.markdown("""
    <div class="ok-hero">
        <div class="ico">✅</div>
        <h2>Pedido recebido com sucesso!</h2>
        <p>Nossa equipe técnica iniciará o planejamento em breve.<br>
        Você receberá as atualizações via <strong>WhatsApp</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    if col.button("📋 Enviar outro pedido", type="primary",
                  use_container_width=True):
        _reset_form()
        st.rerun()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
def main():
    _init()
    estado = st.session_state.estado

    inject_css(estado)
    inject_js()

    if estado == "sucesso":
        render_sucesso()
        return

    _render_logo()

    if estado == "landing":
        render_landing()
    else:
        render_formulario()


if __name__ == "__main__":
    main()
