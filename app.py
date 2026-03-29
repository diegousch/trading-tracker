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

# ===================== CSS PROFESIONAL =====================
st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0e0e0;}
    .stButton>button {border-radius: 16px; font-weight: 600; padding: 0.75rem 1.5rem;}
    .stButton>button:hover {transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0, 255, 157, 0.3);}
    
    .metric-card, .month-card, .week-card {
        background: #111827;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .day-card {
        background: #1a2338;
        border-radius: 18px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border: 2px solid #334155;
        transition: all 0.3s ease;
    }
    .day-card:hover {border-color: #00ff9d; transform: translateY(-3px);}
    
    .profit-positive {color: #00ff9d; font-size: 1.75rem; font-weight: 700;}
    .profit-negative {color: #ff5252; font-size: 1.75rem; font-weight: 700;}
    
    .month-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem;}
    .month-card {cursor: pointer; transition: all 0.3s ease;}
    .month-card:hover {border-color: #00ff9d; transform: scale(1.04);}
    
    .cloud {
        background: #1a2338;
        color: #00ccff;
        padding: 12px 24px;
        border-radius: 9999px;
        font-weight: 600;
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

# ===================== LOGIN =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    pw = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if pw == "1234":
            st.session_state.logged_in = True
            st.success("¡Bienvenido, Diego!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# ===================== UTILIDADES =====================
def get_current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(5)]

def get_week_profit(week_dates):
    records = {r["Fecha"]: r["Profit"] for r in st.session_state.records}
    return sum(records.get(d.strftime("%Y-%m-%d"), 0) for d in week_dates)

def get_day_record(fecha_str):
    for r in st.session_state.records:
        if r["Fecha"] == fecha_str:
            return r
    return None

def get_month_days(año, mes):
    _, num_dias = calendar.monthrange(año, mes)
    dias_laborables = sum(1 for d in range(1, num_dias+1) if date(año, mes, d).weekday() < 5)
    return dias_laborables

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

# ===================== SEMANA ACTUAL =====================
if pagina == "Semana Actual":
    st.subheader("🏠 Semana Actual")
    week_dates = get_current_week()
    week_total = get_week_profit(week_dates)
    meta_semanal = 1750
    progreso = min(max(week_total / meta_semanal * 100, 0), 100)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{week_dates[0].strftime('%d %b')} — {week_dates[4].strftime('%d %b %Y')}**")
    with col2:
        st.metric("Total Semanal", f"${week_total:,.2f}", f"${week_total - meta_semanal:,.2f}")

    st.markdown(f"""
    <div style="background:#1a2338; padding:1.8rem; border-radius:20px; margin:1rem 0;">
        <div style="display:flex;justify-content:space-between;font-weight:600;margin-bottom:8px;">
            <span>Progreso semanal</span>
            <span>${week_total:,.0f} / ${meta_semanal}</span>
        </div>
        <div style="height:14px;background:#334155;border-radius:9999px;overflow:hidden;">
            <div style="width:{progreso}%;height:100%;background:linear-gradient(90deg,#00ff9d,#00ccff);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if week_total >= meta_semanal:
        st.success("🎉 ¡Meta semanal alcanzada!")
    else:
        st.markdown(f'<div class="cloud">☁️ Faltan <strong>${meta_semanal - week_total:,.0f}</strong> para la meta semanal</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Días de la semana")

    for d in week_dates:
        fecha_str = d.strftime("%Y-%m-%d")
        record = get_day_record(fecha_str)
        profit = record["Profit"] if record else 0.0
        notas = record["Notas"] if record else "Sin notas"

        color_class = "profit-positive" if profit >= 0 else "profit-negative"

        col_d, col_p, col_n, col_b = st.columns([1.2, 1.4, 3.5, 1])
        with col_d:
            st.markdown(f"**{d.strftime('%A')}**<br><small>{d.strftime('%d %b')}</small>", unsafe_allow_html=True)
        with col_p:
            st.markdown(f"<span class='{color_class}'>${profit:,.2f}</span>", unsafe_allow_html=True)
        with col_n:
            st.caption(notas[:90] + "..." if len(notas) > 90 else notas)
        with col_b:
            if st.button("Editar", key=f"edit_w_{fecha_str}"):
                st.session_state.editing_date = fecha_str
                st.session_state.editing_profit = profit
                st.session_state.editing_notas = notas
                st.rerun()

    # Formulario de edición
    if "editing_date" in st.session_state:
        fecha = st.session_state.editing_date
        st.divider()
        st.subheader(f"✏️ Editando {fecha}")
        profit = st.number_input("Profit del día ($)", value=st.session_state.editing_profit, step=10.0)
        notas = st.text_area("Notas / Operaciones detalladas", value=st.session_state.editing_notas)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Guardar", type="primary", use_container_width=True):
                record = get_day_record(fecha)
                if record:
                    record["Profit"] = round(profit, 2)
                    record["Notas"] = notas
                else:
                    st.session_state.records.append({
                        "Fecha": fecha,
                        "Día": datetime.strptime(fecha, "%Y-%m-%d").strftime("%A"),
                        "Profit": round(profit, 2),
                        "Notas": notas
                    })
                save_records(st.session_state.records)
                st.success("Guardado correctamente")
                for key in ["editing_date", "editing_profit", "editing_notas"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        with c2:
            if st.button("Cancelar", use_container_width=True):
                for key in ["editing_date", "editing_profit", "editing_notas"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

# ===================== VER POR MES (NUEVA VERSIÓN COMPLETA) =====================
elif pagina == "Ver por Mes":
    st.subheader("📅 Ver por Mes")

    año = st.selectbox("Año", range(2025, 2029), index=1)
    meses_nombres = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    mes_seleccionado = st.selectbox("Selecciona un mes", range(1,13), format_func=lambda x: meses_nombres[x-1])

    if "selected_month" not in st.session_state or st.session_state.get("selected_month") != (año, mes_seleccionado):
        st.session_state.selected_month = (año, mes_seleccionado)
        st.session_state.show_month_detail = True

    # Grid de todos los meses (para navegación rápida)
    st.markdown("### Todos los meses del año")
    month_grid = st.columns(4)
    for i, mes_name in enumerate(meses_nombres):
        with month_grid[i % 4]:
            dias_lab = get_month_days(año, i+1)
            meta_mensual = 350 * dias_lab
            # Calcular total real del mes
            datos_mes = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{i+1:02d}")]
            total_mes = sum(r["Profit"] for r in datos_mes)
            
            color = "#00ff9d" if total_mes >= meta_mensual else "#ff5252" if total_mes < 0 else "#eab308"
            
            st.markdown(f"""
            <div class="month-card" style="border: 2px solid {color};" onclick="window.location.reload();">
                <h3 style="text-align:center;">{mes_name}</h3>
                <div style="font-size:2rem; font-weight:700; text-align:center; color:{color};">${total_mes:,.0f}</div>
                <div style="text-align:center; color:#94a3b8; font-size:0.95rem;">Meta: ${meta_mensual:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Detalle del mes seleccionado
    st.subheader(f"{meses_nombres[mes_seleccionado-1]} {año}")
    dias_lab = get_month_days(año, mes_seleccionado)
    meta_mensual = 350 * dias_lab

    datos_mes = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes_seleccionado:02d}")]
    total_mes = sum(r["Profit"] for r in datos_mes)

    delta = total_mes - meta_mensual
    st.metric("Total del mes", f"${total_mes:,.2f}", f"${delta:,.2f} vs meta")

    if total_mes >= meta_mensual:
        st.success(f"🎯 Meta mensual alcanzada (+${delta:,.0f} adicionales)")
    else:
        st.error(f"❌ Meta mensual no alcanzada (faltan ${abs(delta):,.0f})")

    # Semanas del mes
    st.subheader("Semanas del mes")
    cal = calendar.monthcalendar(año, mes_seleccionado)
    
    for semana_idx, semana in enumerate(cal):
        # Filtrar solo días válidos (no 0)
        dias_semana = [d for d in semana if d != 0]
        if not dias_semana:
            continue
            
        week_start = date(año, mes_seleccionado, dias_semana[0])
        week_end = date(año, mes_seleccionado, dias_semana[-1]) if len(dias_semana) > 1 else week_start
        
        week_dates = []
        for d in range(5):  # Lunes a Viernes
            try:
                day_date = week_start + timedelta(days=d)
                if day_date.month == mes_seleccionado and day_date.weekday() < 5:
                    week_dates.append(day_date)
            except:
                pass
        
        if not week_dates:
            continue
            
        week_total = get_week_profit(week_dates)
        
        st.markdown(f"**Semana {semana_idx+1}** ({week_start.strftime('%d %b')} - {week_end.strftime('%d %b')}) — Total: **${week_total:,.2f}**")
        
        for day in week_dates:
            fecha_str = day.strftime("%Y-%m-%d")
            record = get_day_record(fecha_str)
            profit = record["Profit"] if record else 0.0
            notas = record["Notas"] if record else "Sin registro"
            
            color_class = "profit-positive" if profit >= 0 else "profit-negative"
            
            col1, col2, col3, col4 = st.columns([1.1, 1.3, 3.8, 1])
            with col1:
                st.write(f"{day.strftime('%A')}<br><small>{day.strftime('%d %b')}</small>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span class='{color_class}'>${profit:,.2f}</span>", unsafe_allow_html=True)
            with col3:
                st.caption(notas)
            with col4:
                if st.button("Editar", key=f"edit_m_{fecha_str}"):
                    st.session_state.editing_date = fecha_str
                    st.session_state.editing_profit = profit
                    st.session_state.editing_notas = notas
                    st.rerun()

# ===================== RESUMEN GENERAL =====================
else:
    st.subheader("📊 Resumen General")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        total = df["Profit"].sum()
        dias = len(df)
        st.metric("Total Ganado", f"${total:,.2f}")
        st.metric("Días Operados", dias)
        
        import plotly.express as px
        fig = px.bar(df, x="Fecha", y="Profit", title="Profit Diario", template="plotly_dark")
        fig.add_hline(y=350, line_dash="dash", line_color="yellow", annotation_text="Mínimo diario")
        fig.add_hline(y=750, line_dash="dash", line_color="orange", annotation_text="Ideal diario")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Registra operaciones para ver gráficos.")

st.caption("💼 Diego Options Trading Journal • Versión 6.0")
