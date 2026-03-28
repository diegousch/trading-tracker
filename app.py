import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Trading Profit Tracker", page_icon="📈", layout="centered")

st.title("📊 Mi Tracker de Profit en Opciones")
st.markdown("**Meta diaria:** Mínimo $350 | Ideal $700 | Semanal ideal: $1,750")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔑 Iniciar sesión")
    email = st.text_input("Email", value="diego@example.com")
    password = st.text_input("Contraseña", type="password", value="1234")
    if st.button("Entrar"):
        if password == "1234":
            st.session_state.logged_in = True
            st.success("¡Bienvenido, Diego!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

if "records" not in st.session_state:
    st.session_state.records = []

page = st.sidebar.radio("Ir a:", ["Registrar Día", "Ver Semana"])

if page == "Registrar Día":
    st.subheader("📅 Registrar Profit del Día")
    today = datetime.now().strftime("%Y-%m-%d (%A)")
    st.write(f"**Hoy:** {today}")
    
    profit = st.number_input("Profit del día ($)", value=0.0, step=10.0)
    notes = st.text_area("Notas", placeholder="Ej: Gané en SPY calls a las 10am...")
    
    if st.button("💾 Guardar Día"):
        if profit != 0:
            st.session_state.records.append({
                "Fecha": today,
                "Profit": round(profit, 2),
                "Notas": notes
            })
            st.success(f"¡Guardado! Profit hoy: ${profit:,.2f}")
        else:
            st.warning("Pon el profit del día")

elif page == "Ver Semana":
    st.subheader("📋 Registro de la Semana")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)
        
        total = df["Profit"].sum()
        dias = len(df)
        promedio = total / dias if dias > 0 else 0
        
        st.metric("Total Semana", f"${total:,.2f}")
        st.metric("Promedio Diario", f"${promedio:,.2f}")
        st.metric("Meta Semanal ($1,750)", f"${total - 1750:,.2f}")
        
        for _, row in df.iterrows():
            p = row["Profit"]
            if p >= 700:
                st.success(f"✅ {row['Fecha']}: ${p:,.2f} → ¡Día excelente!")
            elif p >= 350:
                st.info(f"✅ {row['Fecha']}: ${p:,.2f} → Mínimo cumplido")
            else:
                st.warning(f"⚠️ {row['Fecha']}: ${p:,.2f} → Falta para el mínimo")
    else:
        st.info("Aún no tienes registros esta semana. Ve a 'Registrar Día'.")

if st.sidebar.button("🗑️ Limpiar datos (solo prueba)"):
    st.session_state.records = []
    st.success("Datos borrados")
