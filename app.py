import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import os

CSV_FILE = "trading_records.csv"

st.set_page_config(
    page_title="Diego Options Profit Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS PROFESIONAL DARK FINANCE =====================
st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0e0e0;}
    .stButton>button {
        border-radius: 16px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0, 255, 157, 0.3);}
    
    .metric-card {
        background: #111827;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .day-card {
        background: #111827;
        border-radius: 20px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        border: 2px solid #334155;
        transition: all 0.3s ease;
    }
    .day-card:hover {
        border-color: #00ff9d;
        transform: translateY(-4px);
    }
    .profit-positive {color: #00ff9d; font-size: 1.8rem; font-weight: 700;}
    .profit-negative {color: #ff5252; font-size: 1.8rem; font-weight: 700;}
    .week-progress {
        height: 12px;
        background: #334155;
        border-radius: 9999px;
        overflow: hidden;
        margin: 12px 0;
    }
    .cloud {
        background: #1a2338;
        color: #00ccff;
        padding: 12px 24px;
        border-radius: 9999px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 15px rgba(0, 204, 255, 0.25);
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Diego's Options Profit Tracker")
st.markdown("**Metas** — Diario: **$350** mínimo | **$750** ideal | Semanal: **$1,750**")

# ===================== CARGAR / GUARDAR =====================
def load_records():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")
            return df.to_dict('records')
        except:
            return []
    return []

def save_records(records):
    pd.DataFrame(records).to_csv(CSV_FILE, index=False)

if "records" not in st.session_state:
    st.session_state.records = load_records()

# ===================== LOGIN SIMPLE =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    pw = st.text_input("Contraseña", type="password", value="")
    if st.button("Entrar"):
        if pw == "1234":   # Cambia esto por una contraseña más segura en producción
            st.session_state.logged_in = True
            st.success("¡Bienvenido, Diego!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# ===================== FUNCIONES ÚTILES =====================
def get_current_week():
    today = date.today()
    # Encontrar el lunes de esta semana
    monday = today - timedelta(days=today.weekday())
    days = []
    for i in range(5):  # Lunes a Viernes
        day = monday + timedelta(days=i)
        days.append({
            "fecha": day.strftime("%Y-%m-%d"),
            "dia_nombre": day.strftime("%A"),
            "dia_corto": day.strftime("%d %b"),
            "fecha_obj": day
        })
    return days

def get_week_profit(week_days):
    records = {r["Fecha"]: r for r in st.session_state.records}
    total = 0
    for day in week_days:
        if day["fecha"] in records:
            total += records[day["fecha"]]["Profit"]
    return round(total, 2)

def get_day_record(fecha_str):
    for r in st.session_state.records:
        if r["Fecha"] == fecha_str:
            return r
    return None

# ===================== SIDEBAR =====================
st.sidebar.header("Navegación")
pagina = st.sidebar.radio("Ir a:", ["Semana Actual", "Ver por Mes", "Resumen General"])

st.sidebar.divider()
if st.sidebar.button("🗑️ Limpiar TODO (prueba)"):
    st.session_state.records = []
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    st.success("Datos borrados")
    st.rerun()

st.sidebar.caption("Versión 5.0 • Professional Trading Journal")

# ===================== PÁGINA: SEMANA ACTUAL =====================
if pagina == "Semana Actual":
    st.subheader("🏠 Semana Actual")
    
    week_days = get_current_week()
    week_total = get_week_profit(week_days)
    progreso = min(max(week_total / 1750 * 100, 0), 100)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{week_days[0]['dia_corto']} — {week_days[4]['dia_corto']}**")
    with col2:
        st.metric("Total Semanal", f"${week_total:,.2f}", f"${week_total - 1750:,.2f}")
    
    # Barra de progreso
    st.markdown(f"""
    <div style="background:#1a2338; padding:1.5rem; border-radius:20px; margin:1rem 0;">
        <div style="display:flex; justify-content:space-between; font-weight:600; margin-bottom:8px;">
            <span>Progreso semanal</span>
            <span>${week_total:,.0f} / $1,750</span>
        </div>
        <div class="week-progress"><div style="width:{progreso}%; height:100%; background:linear-gradient(90deg, #00ff9d, #00ccff);"></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    if week_total >= 1750:
        st.success("🎉 ¡Meta semanal alcanzada!")
    elif 1750 - week_total > 0:
        st.markdown(f"""
        <div class="cloud">
            ☁️ Aún faltan <strong>${1750 - week_total:,.0f}</strong> para completar la meta semanal
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("Días de la semana")
    
    for day in week_days:
        record = get_day_record(day["fecha"])
        profit = record["Profit"] if record else 0.0
        notas = record["Notas"] if record else "Sin registro aún"
        
        color_class = "profit-positive" if profit >= 0 else "profit-negative"
        
        with st.container():
            col_dia, col_profit, col_notas, col_btn = st.columns([1.2, 1.3, 3, 1])
            with col_dia:
                st.markdown(f"**{day['dia_nombre'].capitalize()}**<br><small>{day['dia_corto']}</small>", unsafe_allow_html=True)
            with col_profit:
                st.markdown(f"<span class='{color_class}'>${profit:,.2f}</span>", unsafe_allow_html=True)
            with col_notas:
                st.caption(notas[:80] + "..." if len(notas) > 80 else notas)
            with col_btn:
                if st.button("Editar", key=f"edit_{day['fecha']}"):
                    st.session_state.editing_date = day["fecha"]
                    st.session_state.editing_profit = profit
                    st.session_state.editing_notas = notas
                    st.rerun()
    
    # Formulario de edición (modal)
    if "editing_date" in st.session_state:
        fecha_edit = st.session_state.editing_date
        st.divider()
        st.subheader(f"✏️ Editando: {fecha_edit}")
        
        profit = st.number_input("Profit del día ($)", value=st.session_state.editing_profit, step=10.0)
        notas = st.text_area("Notas / Operaciones detalladas", value=st.session_state.editing_notas)
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("💾 Guardar", type="primary", use_container_width=True):
                # Actualizar o crear
                record = get_day_record(fecha_edit)
                if record:
                    record["Profit"] = round(profit, 2)
                    record["Notas"] = notas
                else:
                    st.session_state.records.append({
                        "Fecha": fecha_edit,
                        "Día": datetime.strptime(fecha_edit, "%Y-%m-%d").strftime("%A"),
                        "Profit": round(profit, 2),
                        "Notas": notas
                    })
                save_records(st.session_state.records)
                st.success("Guardado correctamente")
                del st.session_state.editing_date
                st.rerun()
        with col_cancel:
            if st.button("Cancelar", use_container_width=True):
                del st.session_state.editing_date
                st.rerun()

# ===================== PÁGINA: VER POR MES =====================
elif pagina == "Ver por Mes":
    st.subheader("📅 Análisis por Mes")
    
    año = st.selectbox("Año", range(2025, 2028), index=1)
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    mes = st.selectbox("Mes", range(1,13), format_func=lambda x: meses[x-1])
    
    # Aquí puedes expandir más adelante con grid de semanas del mes
    st.info("Vista de mes en desarrollo. Por ahora muestra el resumen básico.")
    
    # Placeholder para futuro desarrollo (semanas dentro del mes)
    st.write("Próximamente: Grid de semanas + detalle día a día del mes seleccionado.")

# ===================== PÁGINA: RESUMEN GENERAL =====================
else:
    st.subheader("📊 Resumen General")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        total = df["Profit"].sum()
        dias = len(df)
        promedio = total / dias if dias > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ganado", f"${total:,.2f}")
        col2.metric("Promedio Diario", f"${promedio:,.2f}")
        col3.metric("Días Registrados", dias)
        
        import plotly.express as px
        fig = px.bar(df, x="Fecha", y="Profit", title="Profit Diario", template="plotly_dark")
        fig.add_hline(y=350, line_dash="dash", line_color="yellow")
        fig.add_hline(y=750, line_dash="dash", line_color="orange")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Registra operaciones en 'Semana Actual' para ver el resumen.")

st.caption("💼 Diego Options Trading Journal • Datos guardados permanentemente")
