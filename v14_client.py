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
import re
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

/* Área de drag-and-drop usando input nativo */
#drop-area{{
  border:2px dashed #1a6b8a;border-radius:10px;
  background:#fff;padding:1.2rem;text-align:center;
  cursor:pointer;transition:background .15s,border-color .15s;
  position:relative;flex-shrink:0;
}}
#drop-area.over{{background:#dbeafe;border-color:#0e4d66;border-style:solid;}}
#drop-area label{{
  display:block;cursor:pointer;color:#374151;font-size:.85rem;
  pointer-events:none;
}}
/* Input invisível que cobre toda a área de drop */
#file-input{{
  position:absolute;inset:0;width:100%;height:100%;
  opacity:0;cursor:pointer;
}}

#hint{{font-size:.75rem;color:#6b7280;text-align:center;}}
#msg{{font-size:.82rem;color:#1e3a5f;min-height:1.2rem;padding:.2rem 0;}}
#urls{{
  font-size:.75rem;color:#059669;word-break:break-all;
  white-space:pre-wrap;display:none;
  background:#ecfdf5;border:1px solid #6ee7b7;border-radius:8px;
  padding:.5rem .7rem;line-height:1.7;
}}
#urls b{{display:block;margin-bottom:.2rem;color:#065f46;}}
#progress{{font-size:.78rem;color:#1d4ed8;display:none;}}
</style></head><body>

<button id="btn">📎 Selecionar Arquivos (clique aqui)</button>

<div id="drop-area">
  <input type="file" id="file-input" multiple>
  <label>
    🗂️ <strong>Arraste e solte os arquivos aqui</strong><br>
    <span style="font-size:.78rem;color:#6b7280">
      ZIP · STL · DCM · RAR · PDF · PNG · JPG · qualquer formato · qualquer tamanho
    </span>
  </label>
</div>

<div id="hint">Clique no botão azul <em>ou</em> arraste para a área pontilhada</div>
<div id="progress"></div>
<div id="msg"></div>
<div id="urls"></div>

<script>
var cl = filestack.init('{api_key}');
var accumulated = '';

/* ── Botão: abre o picker Filestack ─────────────────────── */
document.getElementById('btn').addEventListener('click', function(){{
  cl.picker({{
    fromSources:['local_file_system','googledrive','dropbox'],
    maxFiles: 20,
    uploadInBackground: false,
    onUploadDone: function(r){{ handleDone(r.filesUploaded||[]); }},
    onFileUploadFailed: function(f,e){{
      setMsg('⚠️ Erro: '+(e.message||String(e)));
    }}
  }}).open();
}});

/* ── Input nativo: seleção por clique na área de drop ────── */
document.getElementById('file-input').addEventListener('change', function(e){{
  uploadFiles(Array.from(e.target.files));
  e.target.value = '';   // reset para permitir selecionar os mesmos arquivos
}});

/* ── Drag-and-drop nativo sobre a área pontilhada ────────── */
var dropArea = document.getElementById('drop-area');

dropArea.addEventListener('dragover', function(e){{
  e.preventDefault(); e.stopPropagation();
  dropArea.classList.add('over');
}});
dropArea.addEventListener('dragleave', function(e){{
  e.preventDefault(); e.stopPropagation();
  dropArea.classList.remove('over');
}});
dropArea.addEventListener('drop', function(e){{
  e.preventDefault(); e.stopPropagation();
  dropArea.classList.remove('over');
  var files = Array.from(e.dataTransfer.files);
  if(files.length) uploadFiles(files);
}});

/* ── Upload via API do Filestack (sem picker) ────────────── */
function uploadFiles(files){{
  if(!files.length) return;
  setMsg('');
  setProgress('⏳ Enviando '+files.length+' arquivo(s)…');

  Promise.all(files.map(function(f){{
    return cl.upload(f, {{}}, {{filename: f.name}});
  }}))
  .then(function(results){{
    setProgress('');
    handleDone(results);
  }})
  .catch(function(err){{
    setProgress('');
    setMsg('⚠️ Erro no upload: '+String(err));
  }});
}}

/* ── Callback unificado para picker e drop ───────────────── */
function handleDone(files){{
  if(!files||!files.length){{ setMsg('⚠️ Nenhum arquivo retornado.'); return; }}
  var newUrls = files.map(function(f){{return f.url||''}})
                     .filter(function(u){{return u.indexOf('http')===0;}});
  if(!newUrls.length){{ setMsg('⚠️ URLs não encontradas.'); return; }}

  accumulated = accumulated ? accumulated+'|'+newUrls.join('|') : newUrls.join('|');
  var count = accumulated.split('|').filter(Boolean).length;

  setMsg('✅ '+files.length+' arquivo(s) enviado(s). Total na fila: '+count);
  var el = document.getElementById('urls');
  el.style.display = 'block';
  el.innerHTML = '<b>🔗 Copie o link e cole no campo "Passo 2" abaixo:</b>\\n' + accumulated;
}}

function setMsg(t){{ document.getElementById('msg').textContent=t; }}
function setProgress(t){{
  var el=document.getElementById('progress');
  el.textContent=t; el.style.display=t?'block':'none';
}}
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
    """
    Odontograma visual anatômico com SVG.
    Cada dente é desenhado com coroa + raiz. Clique alterna o estado:
      0 = Livre        → dente natural (cinza-azulado)
      1 = Implante     → implante (parafuso azul, sem raiz)
      2 = Exodontia    → X vermelho sobre o dente
      3 = Imediato     → X vermelho + implante (sobrepostos)
      4 = Pôntico      → coroa amarela sem raiz
    Bridge JS→Python via campo de texto oculto.
    """
    estados = st.session_state.pp_estados

    # Serializa estados para JS como JSON
    import json
    estados_json = json.dumps(estados)

    # Ordem dos dentes: superior esquerdo → direito, inferior esquerdo → direito
    sup = [18,17,16,15,14,13,12,11, 21,22,23,24,25,26,27,28]
    inf = [48,47,46,45,44,43,42,41, 31,32,33,34,35,36,37,38]

    odo_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,sans-serif;}}
  body{{background:transparent;padding:4px 0;}}

  .odo-wrap{{
    width:100%;max-width:760px;margin:0 auto;
    background:#fff;border-radius:12px;padding:10px 8px 8px;
    box-shadow:0 1px 8px rgba(0,0,0,.08);
  }}

  .jaw-label{{
    text-align:center;font-size:.65rem;font-weight:700;
    color:#64748b;letter-spacing:.08em;text-transform:uppercase;
    margin-bottom:3px;
  }}
  .jaw-sep{{
    border:none;border-top:1.5px dashed #cbd5e1;
    margin:6px 4px;
  }}
  .jaw-row{{
    display:flex;justify-content:center;align-items:flex-end;gap:1px;
  }}
  .jaw-row.inferior{{
    align-items:flex-start;
  }}

  .tooth-wrap{{
    display:flex;flex-direction:column;align-items:center;
    cursor:pointer;padding:1px;border-radius:5px;
    transition:background .12s;
    position:relative;
    -webkit-tap-highlight-color:transparent;
  }}
  .tooth-wrap:hover{{background:rgba(26,107,138,.08);}}
  .tooth-wrap:active{{background:rgba(26,107,138,.18);}}

  .tooth-num{{
    font-size:.58rem;color:#94a3b8;font-weight:600;
    line-height:1;margin:2px 0 0;
    pointer-events:none;
  }}
  .jaw-row.inferior .tooth-num{{margin:0 0 2px;order:-1;}}

  svg.tooth{{display:block;overflow:visible;pointer-events:none;}}

  /* Legenda */
  .legend{{
    display:flex;flex-wrap:wrap;gap:6px;justify-content:center;
    margin-top:8px;padding-top:7px;
    border-top:1px solid #e2e8f0;
  }}
  .leg-item{{
    display:flex;align-items:center;gap:4px;
    font-size:.68rem;color:#475569;font-weight:500;
  }}
  .leg-dot{{
    width:11px;height:11px;border-radius:3px;flex-shrink:0;
  }}

  /* Resumo de seleções */
  .resumo{{
    margin-top:6px;padding:6px 10px;
    background:#f8fafc;border-radius:8px;
    border:1px solid #e2e8f0;
    font-size:.72rem;color:#334155;
    display:none;
  }}
  .resumo-linha{{
    display:flex;align-items:center;gap:5px;
    line-height:1.7;
  }}
  .resumo-dot{{
    width:9px;height:9px;border-radius:50%;flex-shrink:0;
  }}
</style>
</head>
<body>
<div class="odo-wrap">
  <div class="jaw-label">Superior</div>
  <div class="jaw-row" id="row-sup"></div>
  <hr class="jaw-sep">
  <div class="jaw-row inferior" id="row-inf"></div>
  <div class="jaw-label" style="margin-top:4px">Inferior</div>

  <div class="legend">
    <div class="leg-item"><div class="leg-dot" style="background:#c8dff0;border:1.5px solid #7ab3d0"></div>Livre</div>
    <div class="leg-item"><div class="leg-dot" style="background:#3b82f6"></div>Implante</div>
    <div class="leg-item"><div class="leg-dot" style="background:#ef4444"></div>Exodontia</div>
    <div class="leg-item"><div class="leg-dot" style="background:linear-gradient(135deg,#ef4444 50%,#3b82f6 50%)"></div>Imediato</div>
    <div class="leg-item"><div class="leg-dot" style="background:#f59e0b"></div>Pôntico</div>
  </div>

  <!-- Resumo de seleções — atualiza instantaneamente via JS -->
  <div class="resumo" id="resumo"></div>
</div>

<script>
// ── Estado inicial vindo do Python ──────────────────────────
var estados = {estados_json};

// Dentes em ordem de renderização
var sup = {json.dumps(sup)};
var inf = {json.dumps(inf)};

// ── Geometrias SVG dos dentes ────────────────────────────────
// Cada dente tem: tipo (I=incisivo, C=canino, PM=pré-molar, M=molar)
// Molares: dente 16,17,18,26,27,28,36,37,38,46,47,48
// Pré-molares: 14,15,24,25,34,35,44,45
// Caninos: 13,23,33,43
// Incisivos: resto

function getTipo(n) {{
  n = Math.abs(n % 10) || (n % 10 === 0 ? 8 : n % 10);
  var d = n % 10;
  if (d >= 6) return 'M';
  if (d === 4 || d === 5) return 'PM';
  if (d === 3) return 'C';
  return 'I';
}}

// Larguras por tipo — maiores para melhor visualização
var W = {{I:22, C:24, PM:27, M:34}};
var H = 66; // altura total do dente (coroa+raiz)

function makeTooth(num, estado, isInf) {{
  var tipo = getTipo(num);
  var w = W[tipo];
  var h = H;

  // Proporções: coroa ocupa ~45% da altura
  var cH = Math.round(h * 0.44);  // altura da coroa
  var rH = h - cH;                 // altura da raiz

  // Raiz mais estreita que a coroa
  var cW = w;
  var rW = Math.round(w * 0.45);
  if (tipo === 'M') rW = Math.round(w * 0.55);

  var cx = w / 2; // centro horizontal

  // SVG paths para cada estado
  // Coroa (sempre presente exceto implante puro)
  // Raiz (ausente em implante, pôntico)

  var svg = '<svg class="tooth" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '">';

  if (estado === 1) {{
    // ── IMPLANTE: parafuso helicoidal orientado pela maxila/mandíbula ──
    svg += implanteSVG(w, h, cx, isInf);

  }} else if (estado === 2) {{
    // ── EXODONTIA: dente natural + X vermelho ────────────────
    svg += denteSVG(w, h, cx, cW, cH, rW, rH, isInf, '#c8dff0', '#7ab3d0', '#a8c8e0', true);
    svg += xSVG(w, h);

  }} else if (estado === 3) {{
    // ── IMEDIATO: X vermelho + implante ──────────────────────
    svg += implanteSVG(w, h, cx, isInf);
    svg += xSVG(w, h);

  }} else if (estado === 4) {{
    // ── PÔNTICO: apenas coroa, cor âmbar, sem raiz ───────────
    svg += denteSVG(w, h, cx, cW, cH, rW, rH, isInf, '#fde68a', '#f59e0b', '#fbbf24', false);

  }} else {{
    // ── LIVRE: dente natural cinza-azulado ───────────────────
    svg += denteSVG(w, h, cx, cW, cH, rW, rH, isInf, '#c8dff0', '#7ab3d0', '#a8c8e0', true);
  }}

  svg += '</svg>';
  return svg;
}}

function denteSVG(w, h, cx, cW, cH, rW, rH, isInf, fillC, stroke, fillR, showRoot) {{
  var out = '';
  var yC, yR;

  if (!isInf) {{
    // Superior: raiz vai para cima, coroa embaixo
    yC = rH;       // coroa começa aqui
    yR = 0;
  }} else {{
    // Inferior: coroa em cima, raiz vai para baixo
    yC = 0;
    yR = cH;
  }}

  // Coroa: retângulo arredondado com variação por tipo
  var rx = (cW > 20) ? 4 : 3;
  out += '<rect x="' + (cx - cW/2) + '" y="' + yC + '" width="' + cW + '" height="' + cH + '"'
       + ' rx="' + rx + '" fill="' + fillC + '" stroke="' + stroke + '" stroke-width="1.2"/>';

  // Linha oclusal (detalhe central da coroa)
  if (cW >= 22) {{
    // Molar: dois cúspides
    var y1 = isInf ? yC + 3 : yC + cH - 4;
    out += '<line x1="' + (cx - cW/2 + 3) + '" y1="' + y1 + '" x2="' + (cx + cW/2 - 3) + '" y2="' + y1 + '"'
         + ' stroke="' + stroke + '" stroke-width="0.8" opacity="0.5"/>';
    out += '<line x1="' + cx + '" y1="' + (isInf ? yC + 1 : yC + cH - 8) + '" x2="' + cx + '" y2="' + y1 + '"'
         + ' stroke="' + stroke + '" stroke-width="0.8" opacity="0.5"/>';
  }}

  if (!showRoot) return out;

  // Raiz: formato trapezoidal afunilado
  var rxTop = cx - rW/2;
  var rxBot = cx - 2;
  var ryBot = isInf ? yR + rH : yR;
  var ryTop = isInf ? yR : yR + rH;
  var tipY  = isInf ? yR + rH : yR;

  // Trapézio raiz
  var x0 = cx - rW/2, x1c = cx + rW/2;
  var y0 = isInf ? yR : yR + rH;    // lado da coroa
  var tip = isInf ? h : 0;           // ponta da raiz

  if (!isInf) {{
    out += '<path d="M' + x0 + ',' + (yR+rH) + ' L' + x1c + ',' + (yR+rH)
         + ' L' + (cx+2) + ',' + 0 + ' L' + (cx-2) + ',' + 0 + ' Z"'
         + ' fill="' + fillR + '" stroke="' + stroke + '" stroke-width="1" opacity="0.85"/>';
  }} else {{
    out += '<path d="M' + x0 + ',' + yR + ' L' + x1c + ',' + yR
         + ' L' + (cx+2) + ',' + h + ' L' + (cx-2) + ',' + h + ' Z"'
         + ' fill="' + fillR + '" stroke="' + stroke + '" stroke-width="1" opacity="0.85"/>';
  }}
  return out;
}}

function implanteSVG(w, h, cx, isInf) {{
  // ── Implante helicoidal realista ──────────────────────────
  // isInf=true  → pescoço em cima, ponta apical embaixo (mandíbula)
  // isInf=false → pescoço embaixo, ponta apical em cima (maxila)
  var out = '';

  // Dimensões gerais
  var top    = Math.round(h * 0.04);
  var bot    = Math.round(h * 0.96);
  var totalH = bot - top;

  // Pescoço (plataforma): ~18% da altura, cilíndrico
  var neckH  = Math.round(totalH * 0.18);
  var neckW  = Math.round(w * 0.40);
  var tipW   = Math.round(w * 0.10);
  var tipH   = Math.round(totalH * 0.12);
  var bodyH  = Math.round(totalH * 0.70);

  // Posições dependem da orientação
  var neckTop, neckBot, bodyTop, bodyBot, tipTop, tipDir;
  if (isInf) {{
    // Mandíbula: pescoço no topo, ponta apical embaixo
    neckTop = top;
    neckBot = top + neckH;
    bodyTop = neckBot;
    bodyBot = bodyTop + bodyH;
    tipTop  = bodyBot;
    tipDir  = 1;   // ponta aponta para baixo (+y)
  }} else {{
    // Maxila: ponta apical no topo, pescoço embaixo
    tipTop  = top;
    bodyTop = tipTop + tipH;
    bodyBot = bodyTop + bodyH;
    neckTop = bodyBot;
    neckBot = neckTop + neckH;
    tipDir  = -1;  // ponta aponta para cima (-y)
  }}

  // Gradiente metálico
  var gid = 'ig' + Math.round(cx * 10);
  out += '<defs>'
       + '<linearGradient id="' + gid + '" x1="0" y1="0" x2="1" y2="0">'
       + '<stop offset="0%" stop-color="#4b6cb7"/>'
       + '<stop offset="30%" stop-color="#7ab3d0"/>'
       + '<stop offset="60%" stop-color="#3b82f6"/>'
       + '<stop offset="100%" stop-color="#1d4ed8"/>'
       + '</linearGradient>'
       + '</defs>';

  // ── Ponta apical cônica ────────────────────────────────────
  if (isInf) {{
    out += '<path d="M' + (cx - tipW) + ',' + tipTop
         + ' L' + cx + ',' + (tipTop + tipH)
         + ' L' + (cx + tipW) + ',' + tipTop + ' Z"'
         + ' fill="#1d4ed8" stroke="#1e40af" stroke-width="0.8"/>';
  }} else {{
    out += '<path d="M' + (cx - tipW) + ',' + (tipTop + tipH)
         + ' L' + cx + ',' + tipTop
         + ' L' + (cx + tipW) + ',' + (tipTop + tipH) + ' Z"'
         + ' fill="#1d4ed8" stroke="#1e40af" stroke-width="0.8"/>';
  }}
  // Brilho na ponta
  var brilhoY1 = isInf ? (tipTop + 2)      : (tipTop + tipH - 2);
  var brilhoY2 = isInf ? (tipTop + tipH - 2) : (tipTop + 2);
  out += '<line x1="' + (cx - Math.round(tipW*0.4)) + '" y1="' + brilhoY1
       + '" x2="' + cx + '" y2="' + brilhoY2
       + '" stroke="#93c5fd" stroke-width="0.8" opacity="0.4" stroke-linecap="round"/>';

  // ── Corpo cônico com roscas helicoidais ───────────────────
  // Trapézio: largo no lado do pescoço, estreito no lado da ponta
  if (isInf) {{
    out += '<path d="M' + (cx - neckW) + ',' + bodyTop
         + ' L' + (cx + neckW) + ',' + bodyTop
         + ' L' + (cx + tipW)  + ',' + bodyBot
         + ' L' + (cx - tipW)  + ',' + bodyBot + ' Z"'
         + ' fill="url(#' + gid + ')" stroke="#1d4ed8" stroke-width="0.8"/>';
  }} else {{
    out += '<path d="M' + (cx - tipW)  + ',' + bodyTop
         + ' L' + (cx + tipW)  + ',' + bodyTop
         + ' L' + (cx + neckW) + ',' + bodyBot
         + ' L' + (cx - neckW) + ',' + bodyBot + ' Z"'
         + ' fill="url(#' + gid + ')" stroke="#1d4ed8" stroke-width="0.8"/>';
  }}

  // Roscas helicoidais (orientação relativa ao corpo)
  var nRoscas = 9;
  var roscaH  = bodyH / nRoscas;
  for (var i = 0; i < nRoscas; i++) {{
    var t0 = i / nRoscas;
    var t1 = (i + 1) / nRoscas;
    // Largura: interpola de neckW→tipW (mandíbula) ou tipW→neckW (maxila)
    var w0, w1;
    if (isInf) {{
      w0 = neckW - (neckW - tipW) * t0;
      w1 = neckW - (neckW - tipW) * t1;
    }} else {{
      w0 = tipW + (neckW - tipW) * t0;
      w1 = tipW + (neckW - tipW) * t1;
    }}
    var y0r = bodyTop + Math.round(roscaH * i);
    var y1r = bodyTop + Math.round(roscaH * (i + 1));
    var ym  = (y0r + y1r) / 2;

    out += '<line x1="' + (cx - w0) + '" y1="' + y0r
         + '" x2="' + (cx + w1) + '" y2="' + y1r
         + '" stroke="#1e40af" stroke-width="1.2" opacity="0.55"/>';
    out += '<line x1="' + (cx + w0) + '" y1="' + y0r
         + '" x2="' + (cx - w1) + '" y2="' + y1r
         + '" stroke="#93c5fd" stroke-width="0.5" opacity="0.35"/>';
    var proj = Math.round(w0 * 0.22);
    out += '<path d="M' + (cx + w0) + ',' + (y0r + 1)
         + ' L' + (cx + w0 + proj) + ',' + ym
         + ' L' + (cx + w1) + ',' + (y1r - 1) + ' Z"'
         + ' fill="#1d4ed8" opacity="0.4"/>';
    out += '<path d="M' + (cx - w0) + ',' + (y0r + 1)
         + ' L' + (cx - w0 - proj) + ',' + ym
         + ' L' + (cx - w1) + ',' + (y1r - 1) + ' Z"'
         + ' fill="#60a5fa" opacity="0.25"/>';
  }}

  // Brilho lateral
  out += '<line x1="' + (cx - Math.round(neckW * 0.55)) + '" y1="' + (bodyTop + 4)
       + '" x2="' + (cx - Math.round(tipW * 0.6)) + '" y2="' + (bodyBot - 4)
       + '" stroke="#bfdbfe" stroke-width="1.5" opacity="0.35" stroke-linecap="round"/>';

  // ── Pescoço (plataforma protética) ───────────────────────
  out += '<rect x="' + (cx - neckW) + '" y="' + neckTop
       + '" width="' + (neckW*2) + '" height="' + neckH + '"'
       + ' rx="2" fill="url(#' + gid + ')" stroke="#1d4ed8" stroke-width="0.8"/>';
  var midNeck = neckTop + Math.round(neckH / 2);
  out += '<line x1="' + (cx - neckW + 2) + '" y1="' + midNeck
       + '" x2="' + (cx + neckW - 2) + '" y2="' + midNeck
       + '" stroke="#1e40af" stroke-width="0.6" opacity="0.5"/>';

  return out;
}}

function xSVG(w, h) {{
  // X vermelho centralizado
  var m = 4;
  var t = Math.round(h * 0.1);
  var b = Math.round(h * 0.9);
  return '<line x1="' + m + '" y1="' + t + '" x2="' + (w-m) + '" y2="' + b + '"'
       + ' stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>'
       + '<line x1="' + (w-m) + '" y1="' + t + '" x2="' + m + '" y2="' + b + '"'
       + ' stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>';
}}

// ── Renderiza uma linha de dentes ────────────────────────────
function renderRow(ids, containerId, isInf) {{
  var cont = document.getElementById(containerId);
  ids.forEach(function(num) {{
    var wrap = document.createElement('div');
    wrap.className = 'tooth-wrap';
    wrap.id = 'tw-' + num;

    var numDiv = document.createElement('div');
    numDiv.className = 'tooth-num';
    numDiv.textContent = num;

    var svgDiv = document.createElement('div');
    svgDiv.id = 'ts-' + num;

    var estado = estados[num] || 0;
    svgDiv.innerHTML = makeTooth(num, estado, isInf);

    if (isInf) {{
      wrap.appendChild(numDiv);
      wrap.appendChild(svgDiv);
    }} else {{
      wrap.appendChild(svgDiv);
      wrap.appendChild(numDiv);
    }}

    wrap.addEventListener('click', function() {{
      var cur = estados[num] || 0;
      estados[num] = (cur + 1) % 5;
      document.getElementById('ts-' + num).innerHTML =
        makeTooth(num, estados[num], isInf);
      updateSummary();   // atualiza resumo instantaneamente
      sendEstados();     // sincroniza com Python via query param
    }});

    cont.appendChild(wrap);
  }});
}}

// ── Bridge: envia JSON dos estados e força rerun do Streamlit ──
function sendEstados() {{
  var json = JSON.stringify(estados);
  try {{
    var p = new URLSearchParams(window.parent.location.search);
    p.set('odo_estados', json);
    var novaUrl = window.parent.location.pathname + '?' + p.toString();
    window.parent.history.replaceState(null, '', novaUrl);
    window.parent.dispatchEvent(new PopStateEvent('popstate', {{state: null}}));
  }} catch(e) {{}}
}}

// ── Resumo de seleções — atualiza instantaneamente no widget ──
var LABELS = ['Livre','Implante','Exodontia','Imediato','Pôntico'];
var COLORS = ['','#3b82f6','#ef4444','#7c3aed','#f59e0b'];
var NOMES  = ['','Implantar','Extrair','Imediato','Pôntico'];

function updateSummary() {{
  var grupos = {{1:[],2:[],3:[],4:[]}};
  var todos  = sup.concat(inf);
  todos.forEach(function(n) {{
    var e = estados[n] || 0;
    if (e >= 1 && e <= 4) grupos[e].push(n);
  }});

  var linhas = [];
  [1,2,3,4].forEach(function(e) {{
    var dts = grupos[e];
    if (dts.length === 0) return;
    linhas.push(
      '<div class="resumo-linha">'
      + '<div class="resumo-dot" style="background:' + COLORS[e] + '"></div>'
      + '<strong>' + NOMES[e] + ':</strong>&nbsp;' + dts.join(', ')
      + '</div>'
    );
  }});

  var el = document.getElementById('resumo');
  if (linhas.length > 0) {{
    el.innerHTML = linhas.join('');
    el.style.display = 'block';
  }} else {{
    el.style.display = 'none';
    el.innerHTML = '';
  }}
}}

// ── Init ─────────────────────────────────────────────────────
renderRow(sup, 'row-sup', false);
renderRow(inf, 'row-inf', true);
updateSummary();
</script>

<!-- campo oculto de saída -->
<input type="hidden" id="odo-data" value='{estados_json}'>
</body></html>"""

    # Renderiza o componente SVG
    components.html(odo_html, height=430, scrolling=False)

    # Bridge: lê query param se vier do widget (mantém session_state atualizado para o payload)
    qp = st.query_params.get("odo_estados", "")
    if qp:
        import json as _json
        try:
            novos = _json.loads(qp)
            st.session_state.pp_estados = {int(k): v for k, v in novos.items()}
            st.query_params.pop("odo_estados")
        except Exception:
            pass

    # ── Protocolos ────────────────────────────────────────────
    estados = st.session_state.pp_estados
    c1, c2 = st.columns(2)
    st.session_state.pp_prot_max  = c1.checkbox("✅ Protocolo Maxila",
                                                  value=st.session_state.pp_prot_max)
    st.session_state.pp_prot_mand = c2.checkbox("✅ Protocolo Mandíbula",
                                                  value=st.session_state.pp_prot_mand)


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

    # Ícone do dente em malha — isolado da logomarca
    dente_icon = SCRIPT_DIR / "dente_mesh_icon.png"
    if dente_icon.exists():
        dente_b64 = base64.b64encode(dente_icon.read_bytes()).decode()
        icone_html = (f'<img src="data:image/png;base64,{dente_b64}" '
                      f'style="height:72px;width:auto;vertical-align:middle;'
                      f'margin-right:12px;opacity:.92" '
                      f'alt="Implante Digital 3D Guide">')
    else:
        icone_html = ""

    st.markdown(f"""
    <div class="hero-wrapper">
      <div class="hero-left">
        <h1>{icone_html}O Futuro da Implantodontia Digital está Aqui.</h1>
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
# NOTIFICAÇÃO POR EMAIL
# Enviado para maikcalmon@hotmail.com após cada pedido recebido
# Configurar em .streamlit/secrets.toml:
#   [email]
#   smtp_server = "smtp.gmail.com"
#   smtp_port = 587
#   usuario = "seu_email@gmail.com"
#   senha = "app_password_aqui"
# ══════════════════════════════════════════════════════════════

def _enviar_email_notificacao(payload: dict) -> bool:
    """
    Envia email de notificação para maikcalmon@hotmail.com
    com resumo do pedido recebido.
    Retorna True se enviado, False se falhou silenciosamente.
    """
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        cfg = st.secrets.get("email", {})
        smtp_server = cfg.get("smtp_server", "smtp.gmail.com")
        smtp_port   = int(cfg.get("smtp_port", 587))
        usuario     = cfg.get("usuario", "")
        senha       = cfg.get("senha", "")

        if not (usuario and senha):
            return False  # credenciais não configuradas — falha silenciosa

        destinatario = "maikcalmon@hotmail.com"
        prof  = payload.get("profissional","—")
        pac   = payload.get("paciente","—")
        clinica = payload.get("clinica_origem","—")
        marca = payload.get("marca_implante","—")
        modelo= payload.get("modelo_implante","—")
        kit   = payload.get("kit_cirurgico","—")
        data  = payload.get("data_cirurgia","—")
        n_imp = payload.get("num_implantes","—")
        tecnica= payload.get("tecnica","—")
        whats = payload.get("whatsapp","—")
        email_dr= payload.get("email","—")
        desc  = payload.get("descricao_caso","")
        imp_s = payload.get("dentes_implante","")
        exo_s = payload.get("dentes_exodontia","")
        imed_s= payload.get("dentes_imediato","")
        pont_s= payload.get("dentes_pontico","")
        urls  = payload.get("arquivo_url","")
        data_envio = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")

        odo_texto = ""
        if imp_s:  odo_texto += f"  • Implante: {imp_s}\n"
        if exo_s:  odo_texto += f"  • Exodontia: {exo_s}\n"
        if imed_s: odo_texto += f"  • Imediato: {imed_s}\n"
        if pont_s: odo_texto += f"  • Pôntico: {pont_s}\n"

        corpo_txt = f"""
🦷 NOVO PEDIDO DE PLANEJAMENTO — {data_envio}
{'='*55}

PROFISSIONAL
  Nome:     {prof}
  Clínica:  {clinica}
  E-mail:   {email_dr}
  WhatsApp: {whats}

CASO
  Paciente:     {pac}
  Data cirurg.: {data}
  Marca:        {marca}
  Modelo:       {modelo}
  Kit:          {kit}
  Técnica:      {tecnica}
  Nº implantes: {n_imp}

ODONTOGRAMA
{odo_texto if odo_texto else "  (nenhum elemento marcado)"}
{'DESCRIÇÃO' if desc else ''}
{'  ' + desc if desc else ''}

ARQUIVOS
  {"Enviados pelo portal: " + str(len(urls.split("|"))) + " arquivo(s)" if urls.strip() else "Nenhum arquivo enviado pelo portal ainda."}

{'='*55}
Pedido recebido via Portal 3D Guide — www.3dguide.com.br
        """.strip()

        corpo_html = f"""
<html><body style="font-family:Arial,sans-serif;color:#1c2b36;">
<div style="max-width:600px;margin:auto;border:1px solid #d1d5db;border-radius:8px;overflow:hidden;">
  <div style="background:#0e4d66;padding:16px 24px;">
    <h2 style="color:white;margin:0">🦷 Novo Pedido de Planejamento</h2>
    <p style="color:#a8d4e6;margin:4px 0 0">Recebido em {data_envio}</p>
  </div>
  <div style="padding:20px 24px;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr style="background:#e8f1f8"><td colspan="2" style="padding:8px 10px;font-weight:bold;color:#0e4d66">PROFISSIONAL</td></tr>
      <tr><td style="padding:6px 10px;color:#555;width:130px">Nome</td><td style="padding:6px 10px"><b>{prof}</b></td></tr>
      <tr style="background:#f8fafb"><td style="padding:6px 10px;color:#555">Clínica</td><td style="padding:6px 10px">{clinica}</td></tr>
      <tr><td style="padding:6px 10px;color:#555">E-mail</td><td style="padding:6px 10px"><a href="mailto:{email_dr}">{email_dr}</a></td></tr>
      <tr style="background:#f8fafb"><td style="padding:6px 10px;color:#555">WhatsApp</td><td style="padding:6px 10px"><a href="https://wa.me/55{whats.replace(' ','').replace('(','').replace(')','').replace('-','')}">{whats}</a></td></tr>
      <tr style="background:#e8f1f8"><td colspan="2" style="padding:8px 10px;font-weight:bold;color:#0e4d66">CASO CLÍNICO</td></tr>
      <tr><td style="padding:6px 10px;color:#555">Paciente</td><td style="padding:6px 10px"><b>{pac}</b></td></tr>
      <tr style="background:#f8fafb"><td style="padding:6px 10px;color:#555">Data Cirurgia</td><td style="padding:6px 10px">{data}</td></tr>
      <tr><td style="padding:6px 10px;color:#555">Implante</td><td style="padding:6px 10px">{marca} {modelo} — Kit {kit}</td></tr>
      <tr style="background:#f8fafb"><td style="padding:6px 10px;color:#555">Técnica</td><td style="padding:6px 10px">{tecnica} — {n_imp} implante(s)</td></tr>
      {"<tr><td colspan='2' style='padding:8px 10px;background:#e8f1f8;font-weight:bold;color:#0e4d66'>ODONTOGRAMA</td></tr><tr><td colspan='2' style='padding:8px 10px;font-family:monospace'>" + odo_texto.replace(chr(10),'<br>') + "</td></tr>" if odo_texto else ""}
      {"<tr style='background:#e8f1f8'><td colspan='2' style='padding:8px 10px;font-weight:bold;color:#0e4d66'>DESCRIÇÃO</td></tr><tr><td colspan='2' style='padding:8px 10px'>" + desc + "</td></tr>" if desc else ""}
      <tr style="background:#e8f1f8"><td colspan="2" style="padding:8px 10px;font-weight:bold;color:#0e4d66">ARQUIVOS</td></tr>
      <tr><td colspan="2" style="padding:8px 10px">{"✅ " + str(len(urls.split("|"))) + " arquivo(s) enviado(s) pelo portal." if urls.strip() else "⚠️ Nenhum arquivo enviado pelo portal ainda."}</td></tr>
    </table>
  </div>
  <div style="background:#f4f8fb;padding:12px 24px;text-align:center;font-size:12px;color:#888;">
    3D Guide Dental Solutions · www.3dguide.com.br
  </div>
</div>
</body></html>
        """.strip()

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[3D Guide] Novo Pedido — {pac} ({prof})"
        msg["From"]    = usuario
        msg["To"]      = destinatario
        msg.attach(MIMEText(corpo_txt, "plain", "utf-8"))
        msg.attach(MIMEText(corpo_html, "html", "utf-8"))

        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.ehlo()
            s.starttls()
            s.login(usuario, senha)
            s.sendmail(usuario, destinatario, msg.as_string())

        return True

    except Exception:
        return False  # sempre falha silenciosa — não bloqueia o fluxo


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
            Visualize o odontograma acima e use os botões numerados para marcar
            cada elemento. Clique repetido alterna: Livre → Implante → Exodontia
            → Imediato → Pôntico → Livre.</div>""",
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
                    # Notificação por email — falha silenciosa se não configurado
                    _enviar_email_notificacao(payload)
                    # Limpa fila de arquivos para o próximo pedido
                    st.session_state["fs_fila"] = []
                    st.session_state.estado = "sucesso"
                    st.rerun()

                except Exception as e:
                    st.error(f"⚠️ Erro ao enviar: {e}")
                    st.caption("Tente novamente ou entre em contato via WhatsApp.")



# ══════════════════════════════════════════════════════════════
# PDF DE SOLICITAÇÃO DE PLANEJAMENTO
# Gerado após envio — dentista pode imprimir ou salvar
# ══════════════════════════════════════════════════════════════

def _gerar_pdf_solicitacao(payload: dict, estados: dict) -> bytes:
    """
    Gera PDF A4 com todos os dados do pedido + instruções de envio de arquivos.
    Retorna bytes prontos para st.download_button.
    """
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl_colors
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                        Paragraph, Spacer, HRFlowable)
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
        from reportlab.lib.units import mm
        import io as _io
    except ImportError:
        return b""

    COR_H = HexColor("#0e4d66")
    COR_A = HexColor("#1a6b8a")
    COR_BG = HexColor("#e8f1f8")

    buf = _io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=15*mm, bottomMargin=15*mm)

    s_h   = ParagraphStyle("h",  fontSize=16, fontName="Helvetica-Bold",
                            textColor=COR_H, leading=20)
    s_sub = ParagraphStyle("s",  fontSize=9,  fontName="Helvetica",
                            textColor=HexColor("#444444"), leading=13)
    s_lbl = ParagraphStyle("l",  fontSize=8,  fontName="Helvetica-Bold",
                            textColor=HexColor("#555555"))
    s_val = ParagraphStyle("v",  fontSize=9,  fontName="Helvetica",
                            textColor=HexColor("#1c2b36"))
    s_sec = ParagraphStyle("sc", fontSize=10, fontName="Helvetica-Bold",
                            textColor=COR_H, leading=14,
                            spaceBefore=4*mm)
    s_inf = ParagraphStyle("i",  fontSize=8.5, fontName="Helvetica",
                            textColor=HexColor("#374151"), leading=13)
    s_sm  = ParagraphStyle("sm", fontSize=7.5, fontName="Helvetica",
                            textColor=HexColor("#888888"),
                            alignment=TA_CENTER)

    story = []

    # ── Cabeçalho branco — logo | título | data ───────────────
    logo_p = SCRIPT_DIR / "logo_planning.png"
    if logo_p.exists():
        from reportlab.platypus import Image as RLImage
        logo_el = RLImage(str(logo_p), width=45*mm, height=14*mm)
    else:
        logo_el = Paragraph("3D Guide", s_h)

    data_emissao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    ht = Table(
        [[logo_el,
          Paragraph("SOLICITAÇÃO DE PLANEJAMENTO CIRÚRGICO", s_h),
          Paragraph(f"<b>Data:</b> {data_emissao}", s_sub)]],
        colWidths=[50*mm, 95*mm, 47*mm],
    )
    ht.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), rl_colors.white),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(0,-1),  0),
        ("LEFTPADDING",   (1,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LINEBELOW",     (0,0),(-1,-1), 2, COR_A),
    ]))
    story += [ht, Spacer(1, 5*mm)]

    # ── Dados do Profissional ─────────────────────────────────
    story.append(Paragraph("DADOS DO PROFISSIONAL", s_sec))
    story.append(Spacer(1, 1.5*mm))
    dados_prof = [
        ["Profissional:", payload.get("profissional","—"),
         "Clínica:",      payload.get("clinica_origem","—")],
        ["E-mail:",       payload.get("email","—"),
         "WhatsApp:",     payload.get("whatsapp","—")],
    ]
    tp = Table(dados_prof, colWidths=[28*mm, 66*mm, 22*mm, 66*mm])
    tp.setStyle(TableStyle([
        ("FONTNAME",  (0,0),(0,-1), "Helvetica-Bold"),
        ("FONTNAME",  (2,0),(2,-1), "Helvetica-Bold"),
        ("FONTSIZE",  (0,0),(-1,-1), 9),
        ("TEXTCOLOR", (0,0),(0,-1), HexColor("#555555")),
        ("TEXTCOLOR", (2,0),(2,-1), HexColor("#555555")),
        ("TOPPADDING",(0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("GRID",      (0,0),(-1,-1), 0.3, HexColor("#d1d5db")),
        ("BACKGROUND",(0,0),(0,-1), COR_BG),
        ("BACKGROUND",(2,0),(2,-1), COR_BG),
    ]))
    story += [tp, Spacer(1, 4*mm)]

    # ── Dados do Caso ─────────────────────────────────────────
    story.append(Paragraph("DADOS DO CASO", s_sec))
    story.append(Spacer(1, 1.5*mm))
    dados_caso = [
        ["Paciente:", payload.get("paciente","—"),
         "Data Cirurgia:", payload.get("data_cirurgia","—")],
        ["Marca:", payload.get("marca_implante","—"),
         "Modelo:", payload.get("modelo_implante","—")],
        ["Kit:", payload.get("kit_cirurgico","—"),
         "Conexão:", payload.get("conexao","—")],
        ["Técnica:", payload.get("tecnica","—"),
         "Nº Implantes:", str(payload.get("num_implantes","—"))],
    ]
    tc = Table(dados_caso, colWidths=[28*mm, 66*mm, 28*mm, 60*mm])
    tc.setStyle(TableStyle([
        ("FONTNAME",  (0,0),(0,-1), "Helvetica-Bold"),
        ("FONTNAME",  (2,0),(2,-1), "Helvetica-Bold"),
        ("FONTSIZE",  (0,0),(-1,-1), 9),
        ("TEXTCOLOR", (0,0),(0,-1), HexColor("#555555")),
        ("TEXTCOLOR", (2,0),(2,-1), HexColor("#555555")),
        ("TOPPADDING",(0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("GRID",      (0,0),(-1,-1), 0.3, HexColor("#d1d5db")),
        ("BACKGROUND",(0,0),(0,-1), COR_BG),
        ("BACKGROUND",(2,0),(2,-1), COR_BG),
    ]))
    story += [tc, Spacer(1, 3*mm)]

    # Descrição do caso
    desc = payload.get("descricao_caso","").strip()
    if desc:
        story.append(Paragraph("<b>Descrição do caso:</b>", s_lbl))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(desc, s_inf))
        story.append(Spacer(1, 3*mm))

    # ── Odontograma em texto ──────────────────────────────────
    story.append(Paragraph("MAPA CIRÚRGICO (ODONTOGRAMA)", s_sec))
    story.append(Spacer(1, 1.5*mm))

    nomes_estado = {1:"🔵 Implante", 2:"🔴 Exodontia",
                    3:"🟣 Imediato", 4:"🟢 Pôntico/Suspenso"}
    grupos = {}
    for dente, estado in sorted(estados.items()):
        if estado and estado in nomes_estado:
            grupos.setdefault(estado, []).append(str(dente))

    imp_s  = payload.get("dentes_implante","")
    exo_s  = payload.get("dentes_exodontia","")
    imed_s = payload.get("dentes_imediato","")
    pont_s = payload.get("dentes_pontico","")
    prot_max  = payload.get("protocolo_maxila", 0)
    prot_mand = payload.get("protocolo_mandib", 0)

    odo_rows = []
    if imp_s:  odo_rows.append(["🔵 Implante",          imp_s])
    if exo_s:  odo_rows.append(["🔴 Exodontia",         exo_s])
    if imed_s: odo_rows.append(["🟣 Imediato",           imed_s])
    if pont_s: odo_rows.append(["🟢 Pôntico/Suspenso",  pont_s])
    if prot_max:  odo_rows.append(["✅ Protocolo",        "Maxila"])
    if prot_mand: odo_rows.append(["✅ Protocolo",        "Mandíbula"])

    if odo_rows:
        to = Table(odo_rows, colWidths=[45*mm, 137*mm])
        to.setStyle(TableStyle([
            ("FONTNAME",    (0,0),(0,-1), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0),(-1,-1), 9),
            ("TEXTCOLOR",   (0,0),(0,-1), HexColor("#374151")),
            ("TOPPADDING",  (0,0),(-1,-1), 3),
            ("BOTTOMPADDING",(0,0),(-1,-1), 3),
            ("GRID",        (0,0),(-1,-1), 0.3, HexColor("#d1d5db")),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),
             [rl_colors.white, HexColor("#f4f8fb")]),
        ]))
        story += [to, Spacer(1, 5*mm)]
    else:
        story.append(Paragraph("Nenhum elemento marcado no odontograma.", s_inf))
        story.append(Spacer(1, 5*mm))

    # ── Instruções de envio de arquivos ──────────────────────
    story.append(HRFlowable(width="100%", thickness=1.5, color=COR_A))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("📁 ENVIO DE ARQUIVOS DO CASO", s_sec))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Para garantir o melhor resultado do seu planejamento, envie os arquivos "
        "do caso por uma das formas abaixo. Sempre identifique os arquivos com "
        "<b>Nome do Paciente</b> e <b>Data da Cirurgia</b>.",
        s_inf))
    story.append(Spacer(1, 3*mm))

    instrucoes = [
        ["🌐  Portal 3D Guide (preferencial)",
         "www.3dguide.com.br\n"
         "Faça o upload diretamente no formulário do site durante o preenchimento."],
        ["📧  E-mail",
         "maikcalmon@hotmail.com\n"
         "Envie os arquivos como anexo. Indique no assunto: "
         "[CASE] Nome do Paciente."],
        ["💧  WeTransfer / Smash / TransferNow",
         "www.wetransfer.com  |  www.fromsmash.com  |  www.transfernow.net\n"
         "Ideal para arquivos grandes (tomografias, STL, etc.). "
         "Envie o link para maikcalmon@hotmail.com ou via WhatsApp."],
        ["📱  iDoc / Dropbox / Google Drive",
         "Compartilhe o link de acesso via WhatsApp ou e-mail.\n"
         "Certifique-se de que o link esteja público ou compartilhado com "
         "maikcalmon@hotmail.com."],
        ["📲  WhatsApp",
         "(27) 99730-0521  —  apenas para arquivos pequenos (< 16 MB).\n"
         "Para arquivos maiores utilize as opções acima."],
    ]

    ti_tbl = Table(instrucoes, colWidths=[52*mm, 130*mm])
    ti_tbl.setStyle(TableStyle([
        ("FONTNAME",     (0,0),(0,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(-1,-1), 8.5),
        ("TEXTCOLOR",    (0,0),(0,-1), COR_H),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 5),
        ("GRID",         (0,0),(-1,-1), 0.3, HexColor("#d1d5db")),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),
         [rl_colors.white, HexColor("#f0f7ff")]),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    story += [ti_tbl, Spacer(1, 5*mm)]

    # Arquivos já enviados pelo portal
    urls = payload.get("arquivo_url","").strip()
    if urls:
        story.append(Paragraph(
            f"<b>✅ Arquivos enviados pelo portal:</b> "
            f"{len(urls.split('|'))} arquivo(s) registrado(s).",
            s_inf))
        story.append(Spacer(1, 3*mm))

    # Rodapé
    story.append(HRFlowable(width="100%", thickness=0.5,
                            color=HexColor("#d1d5db")))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        f"Pedido gerado em {data_emissao} | 3D Guide Dental Solutions | "
        "www.3dguide.com.br",
        s_sm))

    doc.build(story)
    buf.seek(0)
    return buf.read()


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

    # ── PDF de solicitação ────────────────────────────────────
    payload_atual = {
        "profissional":   st.session_state.get("pp_prof",""),
        "clinica_origem": st.session_state.get("pp_clinica",""),
        "email":          st.session_state.get("pp_email",""),
        "whatsapp":       st.session_state.get("pp_whats",""),
        "paciente":       st.session_state.get("pp_pac",""),
        "data_cirurgia":  st.session_state.get("pp_data_cirurgia",
                           datetime.date.today()).strftime("%d/%m/%Y"),
        "marca_implante": st.session_state.get("pp_marca",""),
        "modelo_implante":st.session_state.get("pp_modelo",""),
        "kit_cirurgico":  st.session_state.get("pp_kit",""),
        "conexao":        st.session_state.get("pp_conexao",""),
        "tecnica":        st.session_state.get("pp_tecnica",""),
        "num_implantes":  st.session_state.get("pp_n_implantes",""),
        "descricao_caso": st.session_state.get("pp_descricao",""),
        "arquivo_url":    "|".join(st.session_state.get("fs_fila",[])),
        "dentes_implante": ",".join(
            str(d) for d,e in sorted(
                st.session_state.get("pp_estados",{}).items()) if e==1),
        "dentes_exodontia": ",".join(
            str(d) for d,e in sorted(
                st.session_state.get("pp_estados",{}).items()) if e==2),
        "dentes_imediato": ",".join(
            str(d) for d,e in sorted(
                st.session_state.get("pp_estados",{}).items()) if e==3),
        "dentes_pontico": ",".join(
            str(d) for d,e in sorted(
                st.session_state.get("pp_estados",{}).items()) if e==4),
        "protocolo_maxila":  int(st.session_state.get("pp_prot_max",0)),
        "protocolo_mandib":  int(st.session_state.get("pp_prot_mand",0)),
    }
    estados_atuais = st.session_state.get("pp_estados", {})

    pdf_bytes = _gerar_pdf_solicitacao(payload_atual, estados_atuais)

    if pdf_bytes:
        nome_pac = re.sub(r'[\\/:*?"<>|]', "_",
                          payload_atual["paciente"].upper().strip() or "CASO")
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_pdf = f"Solicitacao_Planejamento_{nome_pac}_{ts}.pdf"

        st.markdown(
            '<div style="background:#eff6ff;border-left:4px solid #1a6b8a;'
            'padding:.8rem 1rem;border-radius:0 8px 8px 0;margin-bottom:1rem">'
            '<b>📄 Solicitação de Planejamento</b><br>'
            '<span style="font-size:.85rem;color:#374151">'
            'Baixe o PDF com todos os dados do seu pedido e as instruções '
            'para envio dos arquivos do caso (tomografia, STL, etc.).</span>'
            '</div>',
            unsafe_allow_html=True)

        st.download_button(
            label="⬇️ Baixar PDF da Solicitação",
            data=pdf_bytes,
            file_name=nome_pdf,
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
        st.markdown("<br>", unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    if col.button("📋 Enviar outro pedido", use_container_width=True):
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
