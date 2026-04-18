import streamlit as st
import hashlib
import json
import time

# --- CONFIGURAÇÃO DA PÁGINA E TEMA ---
st.set_page_config(page_title="BlueChain Mining", page_icon="⛏️", layout="centered")

# --- LÓGICA DA BLOCKCHAIN CENTRALIZADA ---
class BlueChain:
    def __init__(self):
        self.chain = []
        # Criar o Bloco Gênese (Primeiro bloco da rede)
        self.create_block(proof=100, previous_hash='0000000000000000')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'reward': 50  # Quantidade de Satoshis ganhos por bloco
        }
        self.chain.append(block)
        return block

    def hash(self, block):
        # Gera o Hash SHA-256 do bloco
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# Inicializar a Blockchain na memória do navegador
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = BlueChain()
    st.session_state.saldo_sats = 0

# --- INTERFACE VISUAL (STREAMLIT) ---
st.title("⛏️ BlueChain Mining System")
st.write("Sistema de Mineração Centralizado conectado à **Wallet of Satoshi**.")

# Painel de Status
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Meu Saldo", value=f"{st.session_state.saldo_sats} SATS")
with col2:
    st.metric(label="Blocos Minerados", value=len(st.session_state.blockchain.chain) - 1)

st.divider()

# --- ÁREA DE MINERAÇÃO ---
st.subheader("Trabalho de Mineração")
if st.button("🚀 INICIAR MINERAÇÃO", use_container_width=True, type="secondary"):
    with st.status("Minerando na rede BlueChain...", expanded=True) as status:
        st.write("Resolvendo desafio matemático...")
        time.sleep(1.5)
        st.write("Assinando bloco com Hash SHA-256...")
        
        bc = st.session_state.blockchain
        ultimo_bloco = bc.chain[-1]
        hash_anterior = bc.hash(ultimo_bloco)
        novo_bloco = bc.create_block(proof=ultimo_bloco['proof'] + 1, previous_hash=hash_anterior)
        
        st.session_state.saldo_sats += novo_bloco['reward']
        status.update(label="Mineração concluída!", state="complete", expanded=False)
    
    st.success(f"Parabéns! Você minerou o bloco #{novo_bloco['index']} e ganhou 50 Satoshis.")

st.divider()

# --- ÁREA DE ENVIO (WALLET OF SATOSHI) ---
st.subheader("📤 Enviar para Wallet of Satoshi")
st.write("Envie seus ganhos para o seu Lightning Address.")

# Input do endereço (Ex: voce@walletofsatoshi.com)
wos_address = st.text_input("Seu endereço Wallet of Satoshi:", placeholder="exemplo@walletofsatoshi.com")
valor_saque = st.number_input("Quantidade para sacar (SATS):", min_value=0, max_value=st.session_state.saldo_sats, step=10)

if st.button("ENVIAR AGORA", type="primary", use_container_width=True):
    if not wos_address:
        st.warning("nearquality49@walletofsatoshi.com")
    elif valor_saque <= 0:
        st.error("Insira um valor válido para o saque.")
    else:
        with st.spinner("Processando transação via Lightning Network..."):
            # Simulando a chamada de API de pagamento
            time.sleep(2)
            st.session_state.saldo_sats -= valor_saque
            st.balloons()
            st.success(f"Sucesso! {valor_saque} SATS enviados para {wos_address}")
            st.info("As transações na rede real dependem de liquidez na sua API de pagamento (LNbits/OpenNode).")

# --- HISTÓRICO DA REDE ---
st.divider()
with st.expander("🔍 Detalhes Técnicos da Blockchain"):
    st.json(st.session_state.blockchain.chain)

st.caption("BlueChain Mining v1.0 - Desenvolvido em Python")
# --- ADICIONE ISSO AO FINAL DO ARQUIVO ---

def processar_saque_real(invoice_destino):
    # Aqui você usará a chave da API que conseguir (Blink ou LNbits)
    URL_API = "URL_DA_API_AQUI"
    CHAVE = "SUA_CHAVE_AQUI"
    
    headers = {"X-Api-Key": CHAVE, "Content-Type": "application/json"}
    payload = {"out": True, "bolt11": invoice_destino}
    
    print("Conectando à rede Lightning para confirmar envio...")
    
    try:
        response = requests.post(URL_API, json=payload, headers=headers)
        if response.status_code == 201 or response.status_code == 200:
            print("✅ SUCESSO: Os Satoshis saíram do sistema para a Wallet of Satoshi!")
        else:
            print(f"❌ FALHA: A rede recusou o envio. Erro: {response.text}")
    except Exception as e:
        print(f"⚠️ ERRO DE CONEXÃO: {e}")

# Exemplo de como você chamaria isso no seu sistema:
# saldo_atual = 250
# if saldo_atual >= 250:
#     fatura = input("Digite a Invoice para receber seus 250 SATS: ")
#     processar_saque_real(fatura)

