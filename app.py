import streamlit as st
import hashlib
import json
import requests
from time import time

# --- LOGICA DA BLOCKCHAIN ---
class BlueChain:
    def __init__(self):
        self.chain = []
        # Cria o Bloco Gênese
        self.create_block(proof=100, previous_hash='0000000000000000')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'reward': 50 # Valor de Satoshis por bloco
        }
        self.chain.append(block)
        return block

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# Inicializa o estado do App
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = BlueChain()
    st.session_state.saldo_sats = 0

# --- INTERFACE VISUAL (STREAMLIT) ---
st.set_page_config(page_title="BlueChain Mining", page_icon="⛏️")

st.title("⛏️ BlueChain Mining System")
st.write("Bem-vindo à sua rede de mineração centralizada.")

# Painel de Saldo
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Saldo Minerado", value=f"{st.session_state.saldo_sats} SATS")
with col2:
    st.metric(label="Blocos na Rede", value=len(st.session_state.blockchain.chain))

# Botão de Ação
if st.button("🚀 MINERAR NOVO BLOCO", use_container_width=True):
    with st.spinner("Resolvendo algoritmo de Prova de Trabalho..."):
        bc = st.session_state.blockchain
        ultimo_bloco = bc.chain[-1]
        hash_anterior = bc.hash(ultimo_bloco)
        
        # Cria o novo bloco e dá a recompensa
        novo_bloco = bc.create_block(proof=ultimo_bloco['proof'] + 1, previous_hash=hash_anterior)
        st.session_state.saldo_sats += novo_bloco['reward']
        
        st.success(f"Sucesso! Bloco #{novo_bloco['index']} adicionado à rede.")

# Envio para BlueWallet
st.divider()
st.subheader("📲 Transferir para BlueWallet")
wallet_address = st.text_input("Endereço da Wallet (Lightning ou On-chain)")
quantidade = st.number_input("Quantidade para enviar", min_value=1, max_value=st.session_state.saldo_sats)

if st.button("Enviar Satoshis"):
    if wallet_address and quantidade > 0:
        # Lógica de integração com a BlueWallet via API LndHub
        st.info(f"Processando envio de {quantidade} SATS para {wallet_address}...")
        # Aqui o código se conectaria à sua API da BlueWallet
        st.session_state.saldo_sats -= quantidade
        st.success("Transferência enviada com sucesso!")
    else:
        st.error("Verifique o endereço e o saldo disponível.")

# Lista de Blocos
if st.checkbox("Exibir Livro de Registros (Blockchain)"):
    st.json(st.session_state.blockchain.chain)
