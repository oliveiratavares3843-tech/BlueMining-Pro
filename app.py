import streamlit as st
import hashlib
import json
import requests
from time import time

# --- LOGICA DA BLOCKCHAIN ---
class BlueChain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=100, previous_hash='0000000000000000')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'reward': 50 
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

# --- INTERFACE VISUAL ---
st.title("⛏️ BlueChain Mining System")

# Painel de Saldo em destaque
st.subheader(f"Carteira: {st.session_state.saldo_sats} SATS")

# Botão de Mineração (Aumenta o saldo)
if st.button("🚀 CLIQUE PARA MINERAR", use_container_width=True):
    bc = st.session_state.blockchain
    ultimo_bloco = bc.chain[-1]
    hash_anterior = bc.hash(ultimo_bloco)
    novo_bloco = bc.create_block(proof=ultimo_bloco['proof'] + 1, previous_hash=hash_anterior)
    
    st.session_state.saldo_sats += 50
    st.success(f"Bloco #{novo_bloco['index']} minerado! +50 Satoshis na conta.")

st.divider()

# --- SEÇÃO DE ENVIO ---
st.subheader("📲 Enviar Satoshis para BlueWallet")

# Campos de entrada
endereco_wallet = st.text_input("Endereço da sua BlueWallet (Lightning ou BTC):", placeholder="bc1... ou lnbc...")
valor_para_enviar = st.number_input("Quantidade para enviar:", min_value=0, step=1)

# O BOTÃO DE ENVIO
if st.button("📤 ENVIAR AGORA", type="primary", use_container_width=True):
    if st.session_state.saldo_sats <= 100:
        st.error("Você não tem saldo para enviar! Minere alguns blocos primeiro.")
    elif valor_para_enviar <= 100:
        st.warning("Insira um valor maior que zero.")
    elif valor_para_enviar > st.session_state.saldo_sats:
        st.error("Saldo insuficiente para esta transferência.")
    elif not endereco_wallet:
        st.warning("Por favor, insira o endereço da sua carteira.")
    else:
        # Lógica de sucesso simulada
        st.session_state.saldo_sats -= valor_para_enviar
        st.balloons() # Efeito de festa na tela
        st.success(f"Sucesso! {valor_para_enviar} Satoshis enviados para {endereco_wallet}")
        st.info("Nota: Em uma rede real, a transação seria enviada para a LndHub da BlueWallet.")

# Rodapé com histórico
if st.checkbox("Mostrar Histórico da Blockchain"):
    st.json(st.session_state.blockchain.chain)
