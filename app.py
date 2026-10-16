import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="East Africa Bandwidth Exchange", layout="wide")
st.title("🌍 Place d'Arbitrage Télécom — Hub Est-Africain")
st.write("Plateforme de courtage et d'enchères en temps réel pour les capacités de câbles sous-marins et réseaux terrestres (Djibouti, Somalie, Kenya, Éthiopie, Soudans, Érythrée, Ouganda).")

# Simulation de flux de données de marché en direct
@st.cache_data(ttl=5)
def get_market_data():
    routes = [
        "Djibouti (SEA-ME-WE 5) ──► Addis-Abeba Landline",
        "Mombasa (TEAMS) ──► Kampala Backhaul",
        "Mogadiscio (DARE1) ──► Hargeisa Link",
        "Djibouti (AAE-1) ──► Bossaso Coastal Line",
        "Asmara Terrestrial ──► Khartoum Backbone"
    ]
    data = []
    for r in routes:
        cap = np.random.choice([10, 40, 100, 400]) # Gbps
        base_p = 1200 if "Djibouti" in r else 1500
        price = round(base_p * (1 + np.random.uniform(-0.15, 0.10)), 2)
        data.append({
            "Axe de Distribution": r,
            "Capacité Disponible (Gbps)": cap,
            "Prix Actuel ($/Mbps/Mois)": price,
            "Tendance": np.random.choice(["⬇️ Stable", "🔥 En Hausse", "📉 En Baisse"])
        })
    return pd.DataFrame(data)

market_df = get_market_data()

# Affichage des cours du marché de gros
st.subheader("⚡ Cours de la Capacité Réseau de Gros en Direct")
st.dataframe(market_df, use_container_width=True)

# Interface d'achat d'arbitrage pour les FAI
st.write("---")
st.subheader("🛒 Terminal de Négociation pour Fournisseurs d'Accès (FAI)")

col1, col2 = st.columns(2)
with col1:
    selected_route = st.selectbox("Sélectionnez l'axe réseau à acquérir :", market_df["Axe de Distribution"].tolist())
    requested_capacity = st.number_input("Volume requis (en Gbps) :", min_value=1, max_value=1000, value=10)
    fai_name = st.text_input("Nom de l'Opérateur / FAI acquéreur :")

with col2:
    current_price = market_df[market_df["Axe de Distribution"] == selected_route]["Prix Actuel ($/Mbps/Mois)"].values[0]
    total_monthly_est = round((current_price * requested_capacity * 1000), 2)
    
    st.metric(label="Estimation du Contrat Mensuel (USD)", value=f"{total_monthly_est:,.2f} $")
    st.write("🔒 Transaction sécurisée via smart-contract de routage automatisé.")
    
    if st.button("Soumettre l'Ordre d'Achat Réseau"):
        if fai_name:
            st.success(f"Ordre d'achat validé pour {fai_name}. Allocation de {requested_capacity} Gbps sur l'axe {selected_route} en cours de provisionnement.")
        else:
            st.error("Veuillez entrer le nom de votre structure télécom.")

st.write("---")
st.subheader("💼 Espace Opérateurs Tier-1 (Vendeurs : Orange, EthioTelecom, Djibouti Telecom...)
email_operator = st.text_input("Email corporate pour lister vos surplus de capacité non-utilisés (Dark Fiber / STM-64) :")
if st.button("Ouvrir un compte Liquidity Provider"):
    if email_operator:
        st.success(f"Demande de partenariat émise pour {email_operator}. Nos équipes d'infrastructure réseau vous recontacteront.")
