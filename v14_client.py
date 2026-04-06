import streamlit as st
from supabase import create_client

# Configurações de conexão
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
except Exception as e:
    st.error("Erro nas credenciais do banco de dados.")

st.set_page_config(page_title="Portal 3D Guide", layout="centered")
st.title("📦 Envio de Pedido - 3D Guide")

with st.form("form_pedido", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        profissional = st.text_input("Nome do Profissional *")
        whatsapp = st.text_input("WhatsApp para Contato *")
    with col2:
        paciente = st.text_input("Nome do Paciente *")
        clinica = st.text_input("Clínica/Localidade")

    servico = st.selectbox("Tipo de Serviço", ["Guia Cirúrgico", "Planejamento Digital", "Prototipagem", "Outros"])
    
    # Campo para Tomografias Pesadas
    link_externo = st.text_input("Link da Tomografia (Google Drive, WeTransfer, etc.)")
    st.info("💡 Use o link acima para arquivos maiores que 50MB.")

    observacoes = st.text_area("Observações do Caso")
    
    arquivo = st.file_uploader("Anexar STL ou Fotos (Máx 50MB)", type=['stl', 'png', 'jpg', 'jpeg', 'pdf', 'zip'])

    submit = st.form_submit_button("🚀 Enviar Pedido para a 3D Guide")

    if submit:
        if not profissional or not whatsapp or not paciente:
            st.error("Por favor, preencha os campos obrigatórios (*)")
        else:
            with st.spinner("Enviando dados..."):
                try:
                    url_arquivo = ""
                    if arquivo:
                        file_path = f"{paciente}_{arquivo.name}".replace(" ", "_")
                        supabase.storage.from_('arquivos_pacientes').upload(file_path, arquivo.getvalue())
                        url_arquivo = supabase.storage.from_('arquivos_pacientes').get_public_url(file_path)

                    # Gravação no Supabase
                    dados = {
                        "profissional": profissional,
                        "whatsapp": whatsapp,
                        "paciente": paciente,
                        "clinica": clinica,
                        "servico": servico,
                        "observacoes": observacoes,
                        "arquivo_url": url_arquivo,
                        "link_externo": link_externo
                    }
                    
                    supabase.table("pedidos_producao").insert(dados).execute()
                    st.success("✅ Pedido enviado com sucesso!")
                    
                except Exception as e:
                    st.error(f"Erro técnico: {e}")
