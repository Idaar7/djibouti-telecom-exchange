import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="East Africa Bandwidth Exchange", layout="wide")
lang = st.radio("🌐 Select Language / Choisir la langue", ["EN", "FR"], horizontal=True)

if lang == "EN":
    st.title("🌍 Telecom Capacity Arbitrage Hub — East Africa")
    st.write("Wholesale real-time bidding and brokerage platform for submarine cable landing stations and terrestrial backhaul networks.")
    sub1 = "⚡ Live Wholesale Network Capacity Feed"
    sub2 = "🛒 ISP Trading Terminal (Acquisition Platform)"
    box_label = "Select target infrastructure trunk line:"
    num_label = "Required volume allocation (Gbps):"
    name_label = "Acquiring Telecom Operator / ISP Corporate Name:"
    metric_label = "Estimated Monthly Contract Value (USD)"
    sec_label = "🔒 Transaction automated via cryptographic routing smart-contracts."
    btn_order = "Submit Network Purchase Order"
    success_order = "Purchase order confirmed. Allocating bandwidth."
    error_order = "Please enter a valid institutional corporate name."
    carrier_title = "💼 Tier-1 Carrier Gateway (Sellers)"
    mail_label = "Enter operator corporate email to list unutilized Dark Fiber / STM-64 capacity:"
    btn_liq = "Apply for Liquidity Provider Status"
    success_liq = "Partnership inquiry transmitted. Network engineering desk will reach out."
else:
    st.title("🌍 Place d'Arbitrage Télécom — Hub Est-Africain")
    st.write("Plateforme de courtage et d'enchères en temps réel pour les capacités de câbles sous-marins et réseaux terrestres.")
    sub1 = "⚡ Cours de la Capacité Réseau de Gros en Direct"
    sub2 = "🛒 Terminal de Négociation pour Fournisseurs d'Accès (FAI)"
    box_label = "Sélectionnez l'axe réseau à acquérir :"
    num_label = "Volume requis (en Gbps) :"
    name_label = "Nom de l'Opérateur / FAI acquéreur :"
    metric_label = "Estimation du Contrat Mensuel (USD)"
    sec_label = "🔒 Transaction sécurisée via smart-contract de routage automatisé."
    btn_order = "Soumettre l'Ordre d'Achat Réseau"
    success_order = "Ordre d'achat validé. Allocation de bande passante en cours."
    error_order = "Veuillez entrer le nom de votre structure télécom."
    carrier_title = "💼 Espace Opérateurs Tier-1 (Vendeurs)"
    mail_label = "Email corporate pour lister vos surplus de capacité non-utilisés (Dark Fiber / STM-64) :"
    btn_liq = "Ouvrir un compte Liquidity Provider"
    success_liq = "Demande de partenariat émise. Nos équipes d'infrastructure réseau vous recontacteront."

@st.cache_data(ttl=5)
def get_market_data():
    routes = ["Djibouti (SEA-ME-WE 5) ──► Addis Ababa", "Mombasa (TEAMS) ──► Kampala", "Mogadishu (DARE1) ──► Hargeisa", "Djibouti (AAE-1) ──► Bossaso", "Asmara ──► Khartoum"]
    data = []
    capacities = [100, 200, 400, 600, 1000]
    for r in routes:
        cap = np.random.choice(capacities)
        base_p = 1200 if "Djibouti" in r else 1500
        price = round(base_p * (1 + np.random.uniform(-0.15, 0.10)), 2)
        data.append({
            "Wholesale Network Route" if lang=="EN" else "Axe Réseau": r,
            "Available Capacity (Gbps)" if lang=="EN" else "Capacité Dispo (Gbps)": int(cap),
            "Spot Price ($/Mbps/Month)" if lang=="EN" else "Prix Spot ($/Mbps/Mois)": price,
            "Market Trend" if lang=="EN" else "Tendance": np.random.choice(["⬇️ Stable", "🔥 Bullish", "📉 Bearish"])
        })
    return pd.DataFrame(data)

market_df = get_market_data()
st.subheader(sub1)
st.dataframe(market_df, use_container_width=True)

st.write("---")
st.subheader(sub2)
col1, col2 = st.columns(2)
with col1:
    selected_route = st.selectbox(box_label, market_df.iloc[:, 0].tolist())
    requested_capacity = st.number_input(num_label, min_value=1, max_value=1000, value=10)
    fai_name = st.text_input(name_label)
with col2:
    current_price = market_df[market_df.iloc[:, 0] == selected_route].iloc[:, 2].values[0]
    total_monthly_est = round((current_price * requested_capacity * 1000), 2)
    st.metric(label=metric_label, value=f"{total_monthly_est:,.2f} $")
    st.write(sec_label)
    if st.button(btn_order):
        if fai_name: st.success(f"{success_order} ({fai_name})")
        else: st.error(error_order)

st.write("---")
st.subheader(carrier_title)
email_operator = st.text_input(mail_label)
if st.button(btn_liq):
    if email_operator: st.success(f"{success_liq} ({email_operator})")
