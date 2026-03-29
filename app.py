import streamlit as st
import pandas as pd
from datetime import date
import calendar
import os

CSV_FILE = "trading_records.csv"

# ===================== CONFIGURACIÓN =====================
st.set_page_config(
    page_title="Diego Options Profit Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS PROFESIONAL (Dark Finance) =====================
st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0f2ff;}
    .stApp h1 {
        font-size: 2.9rem;
        background: linear-gradient(90deg, #00ffaa, #00d0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -1px;
    }
    .sidebar .css-1d391kg {background-color: #111827;}
    
    /* Botones premium */
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        padding: 12px 24px;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 255, 170, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 255, 170, 0.4);
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #00ffaa, #00d0ff);
        color: #000;
    }

    /* Métricas elegantes */
    .stMetric {
        background: #1a2338;
        border-radius: 16px;
        padding: 20px 15px;
        border: 1px solid #334155;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .stMetric label {color: #94a3b8; font-size: 1.1rem;}
    .stMetric .st-emotion-cache-1wivl2b {font-size: 2rem !important; font-weight: 700;}

    /* Tarjetas de días */
    .day-card {
        background: linear-gradient(145deg, #1a2338, #16203a);
        border-radius: 16px;
        padding: 18px;
        margin: 8px 0;
        border: 1px solid #334155;
        transition: all 0.3s ease;
    }
    .day-card:hover {
        border-color: #00ffaa;
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0, 255, 170, 0.15);
    }

    /* Dataframe */
    .stDataFrame {border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.5);}
</style>
""", unsafe_allow_html=True)

st.title("📈 Diego's Options Profit Tracker")
st.markdown("**Meta diaria:** <span style='color:#00ffaa; font-weight:700;'>$350 mínimo</span> | <span style='color:#00d0ff; font-weight:700;'>$700 ideal</span>", 
            unsafe_allow_html=True)

# ===================== CARGAR / GUARDAR =====================
def load_records():
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE).to_dict('records')
        except:
            return []
    return []

def save_records(records):
    pd.DataFrame(records).to_csv(CSV_FILE, index=False)

if "records" not in st.session_state:
    st.session_state.records = load_records()

# ===================== LOGIN =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;color:#00d0ff;'>🔑 Bienvenido al Tracker</h2>", unsafe_allow_html=True)
    col = st.columns([1,2,1])
    with col[1]:
        st.text_input("Email", "diego@example.com", disabled=True)
        pw = st.text_input("Contraseña", type="password", value="1234")
        if st.button("🚀 Entrar", type="primary", use_container_width=True):
            if pw == "1234":
                st.session_state.logged_in = True
                st.success("¡Bienvenido de nuevo, Diego!")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("📍 Navegación")
    opcion = st.radio(
        label="",
        options=["Registrar Operación", "Ver por Mes", "Gráficos y Resumen"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("💼 Diego Options Trading Journal")
    st.caption("Versión 4.1 • Professional Dark Mode")

# ===================== REGISTRAR OPERACIÓN =====================
if opcion == "Registrar Operación":
    st.subheader("💰 Registrar o Actualizar Día")
    
    fecha_seleccionada = st.date_input("📅 Fecha", value=date.today())
    fecha_str = fecha_seleccionada.strftime("%Y-%m-%d")
    
    registro_actual = next((r for r in st.session_state.records if r["Fecha"] == fecha_str), None)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        profit = st.number_input("Profit del día ($)", 
                               value=registro_actual["Profit"] if registro_actual else 0.0,
                               step=10.0, format="%.2f")
    with col2:
        notas = st.text_area("Notas / Operaciones detalladas", 
                           value=registro_actual["Notas"] if registro_actual else "",
                           placeholder="Ej: 3x SPY Calls 0DTE + 1x QQQ Put...")
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
    with col_btn1:
        if st.button("💾 Guardar / Actualizar", type="primary", use_container_width=True):
            if registro_actual:
                registro_actual["Profit"] = round(profit, 2)
                registro_actual["Notas"] = notas
            else:
                st.session_state.records.append({
                    "Fecha": fecha_str,
                    "Día": fecha_seleccionada.strftime("%A"),
                    "Profit": round(profit, 2),
                    "Notas": notas
                })
            save_records(st.session_state.records)
            st.success(f"✅ Guardado: ${profit:,.2f} el {fecha_str}")
            st.rerun()
    
    with col_btn2:
        if registro_actual and st.button("🗑️ Borrar este día", type="secondary", use_container_width=True):
            st.session_state.records = [r for r in st.session_state.records if r["Fecha"] != fecha_str]
            save_records(st.session_state.records)
            st.success("Día eliminado")
            st.rerun()

    st.divider()
    st.subheader("📋 Historial Completo")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df.sort_values("Fecha", ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay registros. ¡Empieza a operar!")

# ===================== VER POR MES =====================
elif opcion == "Ver por Mes":
    st.subheader("📆 Análisis Mensual")
    
    col_a, col_m = st.columns(2)
    with col_a:
        año = st.selectbox("Año", range(2024, 2028), index=2)
    with col_m:
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        mes = st.selectbox("Mes", range(1,13), index=2, format_func=lambda x: meses[x-1])
    
    _, num_dias = calendar.monthrange(año, mes)
    dias_laborables = sum(1 for d in range(1, num_dias+1) if date(año, mes, d).weekday() < 5)
    meta_mensual = 350 * dias_laborables
    
    # Tarjeta del mes
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,#1a2338,#16203a);padding:25px;border-radius:20px;text-align:center;border:1px solid #334155;margin:20px 0;">
        <h2 style="margin:0;color:#00d0ff;">{meses[mes-1]} {año}</h2>
        <p style="margin:8px 0 0 0;font-size:1.3rem;color:#94a3b8;">Meta mensual: <strong style="color:#00ffaa;">${meta_mensual:,.0f}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    datos_mes = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes:02d}")]
    total_mes = sum(r["Profit"] for r in datos_mes)
    
    st.metric("Total del mes", f"${total_mes:,.2f}", f"${total_mes - meta_mensual:,.2f} vs meta")
    
    st.subheader("Días del mes")
    for dia in range(1, num_dias + 1):
        fecha = date(año, mes, dia)
        if fecha.weekday() >= 5: continue
        fecha_str = fecha.strftime("%Y-%m-%d")
        profit_dia = next((r["Profit"] for r in datos_mes if r["Fecha"] == fecha_str), 0)
        
        if profit_dia >= 700:
            color, icon = "#00ffaa", "🚀"
        elif profit_dia >= 350:
            color, icon = "#4ade80", "✅"
        elif profit_dia < 0:
            color, icon = "#ff5252", "❌"
        elif profit_dia > 0:
            color, icon = "#ffcc00", "⚠️"
        else:
            color, icon = "#64748b", "📅"
        
        st.markdown(f"""
        <div class="day-card">
            <span style="font-size:1.3rem; font-weight:700; color:{color};">{icon} {fecha.strftime('%d %b')} • {fecha.strftime('%A')}</span><br>
            <span style="font-size:2.2rem; font-weight:800;">${profit_dia:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

# ===================== GRÁFICOS =====================
else:
    st.subheader("📊 Resumen General y Gráficos")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df = df.sort_values("Fecha")
        
        total = df["Profit"].sum()
        prom = total / len(df) if len(df) > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Ganado", f"${total:,.2f}")
        c2.metric("Promedio Diario", f"${prom:,.2f}")
        c3.metric("Días Operados", len(df))
        
        import plotly.express as px
        df["Color"] = ["#00ffaa" if p >= 0 else "#ff5252" for p in df["Profit"]]
        
        fig = px.bar(df, x="Fecha", y="Profit", color="Color",
                     color_discrete_map={"#00ffaa":"#00ffaa", "#ff5252":"#ff5252"},
                     title="Profit Diario", template="plotly_dark")
        fig.update_layout(plot_bgcolor="#0a0e17", paper_bgcolor="#0a0e17", height=550)
        fig.add_hline(y=350, line_dash="dash", line_color="#ffcc00", annotation_text="Mínimo $350")
        fig.add_hline(y=700, line_dash="dash", line_color="#00d0ff", annotation_text="Ideal $700")
        
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df[["Fecha", "Día", "Profit", "Notas"]], use_container_width=True, hide_index=True)
    else:
        st.info("Registra operaciones para ver gráficos y estadísticas.")

# Botón de limpieza (solo prueba)
if st.sidebar.button("🗑️ Limpiar TODO (prueba)", type="secondary"):
    st.session_state.records = []
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    st.success("Todo borrado")
    st.rerun()
