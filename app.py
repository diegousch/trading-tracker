import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
import os

CSV_FILE = "trading_records.csv"

# ===================== CONFIGURACIÓN INICIAL =====================
st.set_page_config(
    page_title="Diego Options Tracker",
    page_icon="📈",
    layout="wide",          # Cambiado a wide para mejor experiencia profesional
    initial_sidebar_state="expanded"
)

# ===================== CSS PROFESIONAL (Dark Finance Theme) =====================
st.markdown("""
<style>
    /* Fondo principal y tipografía */
    .main {
        background-color: #0a0e17;
        color: #e0e0e0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Título principal */
    .stApp h1 {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #00ff9d, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    /* Sidebar */
    .css-1d391kg, section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Botones */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 255, 157, 0.3);
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #00cc66, #00ff9d);
        color: #000;
    }
    
    /* Métricas elegantes */
    .stMetric {
        background-color: #1a2338;
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .stMetric label {
        font-size: 1.05rem;
        color: #94a3b8;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Alertas y mensajes */
    .stSuccess {
        background-color: #052e16;
        border-left: 5px solid #00cc66;
    }
    .stError {
        background-color: #450a0a;
        border-left: 5px solid #ef4444;
    }
    
    /* Cards para días */
    .day-card {
        background-color: #1a2338;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border: 1px solid #334155;
        transition: all 0.2s ease;
    }
    .day-card:hover {
        border-color: #00cc66;
        transform: translateX(4px);
    }
    
    /* Títulos de sección */
    .stSubheader {
        color: #60a5fa;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Diego's Options Profit Tracker")
st.markdown("**Meta diaria:** <span style='color:#00ff9d; font-weight:600;'>$350 mínimo</span> | <span style='color:#00ccff;'>$700 ideal</span>", unsafe_allow_html=True)

# ===================== CARGAR / GUARDAR =====================
def load_records():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict('records')
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
    st.markdown("<h2 style='text-align:center; color:#60a5fa;'>🔑 Acceso al Tracker</h2>", unsafe_allow_html=True)
    col_login = st.columns([1, 2, 1])
    with col_login[1]:
        email = st.text_input("Email", "diego@example.com")
        pw = st.text_input("Contraseña", type="password", value="1234")
        if st.button("🚀 Entrar", use_container_width=True):
            if pw == "1234":
                st.session_state.logged_in = True
                st.success("¡Bienvenido de nuevo, Diego! 📈")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# ===================== SIDEBAR =====================
st.sidebar.header("📍 Navegación")
opcion = st.sidebar.radio(
    "Ir a:",
    ["Registrar Operación", "Ver por Mes", "Gráficos y Resumen"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.caption("💼 Diego Options Trading Journal")
st.sidebar.caption("Versión 4.0 • Professional Dark Mode")

# ===================== REGISTRAR OPERACIÓN =====================
if opcion == "Registrar Operación":
    st.subheader("💰 Registrar o Actualizar Día")
    
    fecha_seleccionada = st.date_input("📅 Fecha de la operación", value=date.today())
    fecha_str = fecha_seleccionada.strftime("%Y-%m-%d")
    
    registro_actual = next((r for r in st.session_state.records if r["Fecha"] == fecha_str), None)
    profit_inicial = registro_actual["Profit"] if registro_actual else 0.0
    notas_inicial = registro_actual["Notas"] if registro_actual else ""
    
    col_input1, col_input2 = st.columns([1, 2])
    with col_input1:
        profit = st.number_input("Profit del día ($)", value=profit_inicial, step=10.0, format="%.2f")
    with col_input2:
        notas = st.text_area("Notas / Operaciones detalladas", value=notas_inicial, placeholder="Ej: 3x SPY Calls 0DTE + 1x QQQ Put...")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Guardar / Actualizar Registro", type="primary", use_container_width=True):
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
            st.success(f"✅ Registro guardado correctamente: **${profit:,.2f}** el {fecha_str}")
            st.rerun()
    
    with col_btn2:
        if registro_actual and st.button("🗑️ Borrar este día", type="secondary", use_container_width=True):
            st.session_state.records = [r for r in st.session_state.records if r["Fecha"] != fecha_str]
            save_records(st.session_state.records)
            st.success("Día eliminado correctamente")
            st.rerun()

    st.divider()
    st.subheader("📋 Historial Completo")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(
            df.sort_values("Fecha", ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aún no tienes registros. ¡Comienza a registrar tus operaciones!")

# ===================== VER POR MES =====================
elif opcion == "Ver por Mes":
    st.subheader("📆 Análisis Mensual")
    
    col1, col2 = st.columns(2)
    with col1:
        año = st.selectbox("Año", range(2024, 2028), index=2)
    with col2:
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        mes_idx = st.selectbox("Mes", range(1,13), index=2, format_func=lambda x: meses[x-1])
    
    primer_dia = date(año, mes_idx, 1)
    _, num_dias = calendar.monthrange(año, mes_idx)
    
    dias_laborables = sum(1 for d in range(1, num_dias+1) if date(año, mes_idx, d).weekday() < 5)
    meta_mensual = 350 * dias_laborables
    
    st.markdown(f"""
    <div style='background:#1a2338; padding:1.5rem; border-radius:16px; text-align:center; border:1px solid #334155;'>
        <h3 style='margin:0; color:#60a5fa;'>{meses[mes_idx-1]} {año}</h3>
        <p style='margin:0.3rem 0 0 0; font-size:1.1rem;'>Meta mensual: <strong>${meta_mensual:,.0f}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    datos_mes = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes_idx:02d}")]
    total_mes = sum(r["Profit"] for r in datos_mes)
    
    delta = total_mes - meta_mensual
    st.metric(
        label="Total del mes",
        value=f"${total_mes:,.2f}",
        delta=f"${delta:,.2f} vs meta"
    )
    
    st.divider()
    st.subheader("Días del mes")
    
    for dia in range(1, num_dias + 1):
        fecha = date(año, mes_idx, dia)
        if fecha.weekday() >= 5:
            continue
            
        fecha_str = fecha.strftime("%Y-%m-%d")
        profit_dia = next((r["Profit"] for r in datos_mes if r["Fecha"] == fecha_str), 0)
        
        color = "#00cc66" if profit_dia >= 700 else \
                "#4ade80" if profit_dia >= 350 else \
                "#ef4444" if profit_dia < 0 else \
                "#eab308" if profit_dia > 0 else "#64748b"
        
        icon = "🚀" if profit_dia >= 700 else "✅" if profit_dia >= 350 else "❌" if profit_dia < 0 else "⚠️"
        
        st.markdown(f"""
        <div class="day-card">
            <span style="font-size:1.1rem; font-weight:600; color:{color};">{icon} {fecha.strftime('%d %b')} • {fecha.strftime('%A')}</span><br>
            <span style="font-size:1.6rem; font-weight:700;">${profit_dia:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

# ===================== GRÁFICOS Y RESUMEN =====================
else:
    st.subheader("📊 Resumen General y Gráficos")
    
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df = df.sort_values("Fecha")
        
        total_general = df["Profit"].sum()
        promedio = total_general / len(df) if len(df) > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ganado", f"${total_general:,.2f}", help="Suma de todos los profits")
        col2.metric("Promedio Diario", f"${promedio:,.2f}")
        col3.metric("Días Operados", len(df))
        
        # Gráfico profesional
        import plotly.express as px
        
        df["Color"] = ["#00ff9d" if p >= 0 else "#ff5252" for p in df["Profit"]]
        
        fig = px.bar(
            df, 
            x="Fecha", 
            y="Profit", 
            color="Color",
            color_discrete_map={"#00ff9d":"#00ff9d", "#ff5252":"#ff5252"},
            title="Profit Diario",
            template="plotly_dark"
        )
        
        fig.update_layout(
            plot_bgcolor="#0f172a",
            paper_bgcolor="#0a0e17",
            font=dict(color="#e0e0e0"),
            height=520,
            bargap=0.15
        )
        
        fig.add_hline(y=350, line_dash="dash", line_color="#eab308", annotation_text="Mínimo $350")
        fig.add_hline(y=700, line_dash="dash", line_color="#00ccff", annotation_text="Ideal $700")
        
        st.plotly_chart(fig, use_container_width=True, theme=None)
        
        st.dataframe(
            df[["Fecha", "Día", "Profit", "Notas"]].sort_values("Fecha", ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Registra operaciones para ver los gráficos y el resumen completo.")

# Botón de limpieza (solo para pruebas)
if st.sidebar.button("🗑️ Limpiar TODO (prueba)", type="secondary"):
    st.session_state.records = []
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    st.success("Base de datos limpiada")
    st.rerun()
