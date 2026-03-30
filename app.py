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
    initial_sidebar_state="collapsed"
)

# ===================== CSS FINAL - PROFESIONAL =====================
st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0e0e0;}
    .title {
        font-size: 2.9rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ff9d, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .month-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .month-card {
        background: #111827;
        border: 2px solid #334155;
        border-radius: 20px;
        padding: 1.4rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .month-card:hover {
        border-color: #00ff9d;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 255, 157, 0.1);
    }
    .day-bar {
        background: #1a2338;
        border-radius: 16px;
        padding: 1rem 1.4rem;
        margin-bottom: 0.8rem;
        border: 2px solid #334155;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .profit-positive {color: #00ff9d; font-size: 1.5rem; font-weight: 700;}
    .profit-negative {color: #ff5252; font-size: 1.5rem; font-weight: 700;}
    .progress-bar {
        height: 12px;
        background: #334155;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ===================== PERSISTENCIA DE DATOS =====================
def load_records():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")
            return df.to_dict('records')
        except: return []
    return []

def save_records(records):
    pd.DataFrame(records).to_csv(CSV_FILE, index=False)

if "records" not in st.session_state:
    st.session_state.records = load_records()

# ===================== LÓGICA DE NEGOCIO (EL CORAZÓN) =====================

def get_current_week():
    """Retorna los 5 días de la semana laboral actual."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(5)]

def get_week_profit(week_dates):
    """Calcula el profit sumando los registros existentes para esas fechas."""
    records_dict = {r["Fecha"]: r["Profit"] for r in st.session_state.records}
    return sum(records_dict.get(d.strftime("%Y-%m-%d"), 0) for d in week_dates)

def get_day_record(fecha_str):
    return next((r for r in st.session_state.records if r["Fecha"] == fecha_str), None)

def get_month_days_count(año, mes):
    """Cuenta cuántos días lunes-viernes tiene el mes para la meta total."""
    _, days = calendar.monthrange(año, mes)
    return sum(1 for d in range(1, days+1) if date(año, mes, d).weekday() < 5)

def get_month_weeks_iso(año, mes):
    """
    Divide el mes en semanas basadas en el estándar ISO.
    Si una semana cruza de mes, solo devuelve los días que pertenecen a este mes.
    """
    weeks = {}
    _, num_days = calendar.monthrange(año, mes)
    for d in range(1, num_days + 1):
        dt = date(año, mes, d)
        if dt.weekday() < 5:  # Lunes a Viernes
            iso_week = dt.isocalendar()[1]
            if iso_week not in weeks: weeks[iso_week] = []
            weeks[iso_week].append(dt)
    return [weeks[w] for w in sorted(weeks.keys())]

# ===================== LOGIN =====================
if not st.session_state.get("logged_in", False):
    st.markdown('<div style="max-width:400px; margin:100px auto; padding:2rem; background:#111827; border-radius:20px; border:1px solid #334155; text-align:center;">', unsafe_allow_html=True)
    st.markdown('<p class="title" style="font-size:2rem;">Diego Tracker</p>', unsafe_allow_html=True)
    pw = st.text_input("Password", type="password")
    if st.button("Entrar", use_container_width=True, type="primary"):
        if pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ===================== INTERFAZ - SIDEBAR =====================
pagina = st.sidebar.radio("Navegación", ["Semana Actual", "Ver por Mes", "Resumen General"])

# ===================== VISTA: SEMANA ACTUAL =====================
if pagina == "Semana Actual":
    st.markdown('<p class="title">Semana Actual</p>', unsafe_allow_html=True)
    
    week_dates = get_current_week()
    total_week = get_week_profit(week_dates)
    target_week = 1750.0
    prog_val = min(max((total_week / target_week) * 100, 0), 100) if target_week > 0 else 0

    st.markdown(f"**Semana del {week_dates[0].strftime('%d %b')} al {week_dates[-1].strftime('%d %b %Y')}**")
    
    st.markdown(f"""
    <div style="background:#111827; padding:1.5rem; border-radius:15px; margin-bottom:2rem;">
        <div style="display:flex; justify-content:space-between; font-weight:bold;">
            <span>Progreso Semanal</span>
            <span>${total_week:,.2f} / ${target_week:,.0f}</span>
        </div>
        <div class="progress-bar"><div style="width:{prog_val}%; height:100%; background:linear-gradient(90deg, #00ff9d, #00ccff);"></div></div>
    </div>
    """, unsafe_allow_html=True)

    for day in week_dates:
        f_str = day.strftime("%Y-%m-%d")
        rec = get_day_record(f_str)
        val = rec["Profit"] if rec else 0.0
        txt = rec["Notas"] if rec else "Sin datos"
        
        col_c = "profit-positive" if val >= 0 else "profit-negative"
        
        st.markdown(f"""
        <div class="day-bar">
            <div style="width:120px;"><b>{day.strftime('%A')}</b><br><small>{day.strftime('%d %b')}</small></div>
            <div style="flex:1; text-align:center;" class="{col_c}">${val:,.2f}</div>
            <div style="flex:2; color:#94a3b8; font-size:0.9rem;">{txt[:80]}</div>
            <div style="width:100px;">
        """, unsafe_allow_html=True)
        if st.button("Editar", key=f"btn_{f_str}"):
            st.session_state.edit_date = f_str
            st.session_state.edit_note = txt
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    if "edit_date" in st.session_state:
        st.divider()
        with st.form("edit_form"):
            st.write(f"### Editando {st.session_state.edit_date}")
            new_p = st.number_input("Profit", value=0.0)
            new_n = st.text_area("Notas", value=st.session_state.edit_note)
            if st.form_submit_button("Guardar"):
                # Eliminar existente si hay
                st.session_state.records = [r for r in st.session_state.records if r["Fecha"] != st.session_state.edit_date]
                st.session_state.records.append({
                    "Fecha": st.session_state.edit_date,
                    "Profit": round(new_p, 2),
                    "Notas": new_n
                })
                save_records(st.session_state.records)
                del st.session_state.edit_date
                st.rerun()

# ===================== VISTA: VER POR MES =====================
elif pagina == "Ver por Mes":
    st.markdown('<p class="title">Ver por Mes</p>', unsafe_allow_html=True)
    año_sel = 2026
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    
    st.markdown('<div class="month-grid">', unsafe_allow_html=True)
    for i, nombre in enumerate(meses):
        m_num = i + 1
        d_lab = get_month_days_count(año_sel, m_num)
        target_m = d_lab * 350
        actual_m = sum(r["Profit"] for r in st.session_state.records if r["Fecha"].startswith(f"{año_sel}-{m_num:02d}"))
        
        st.markdown(f"""
        <div class="month-card">
            <h4>{nombre}</h4>
            <div style="color:#00ff9d; font-size:1.4rem; font-weight:bold;">${actual_m:,.0f}</div>
            <div style="color:#94a3b8; font-size:0.8rem;">Meta: ${target_m:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Detalle", key=f"sel_{m_num}", use_container_width=True):
            st.session_state.view_m = m_num
    st.markdown('</div>', unsafe_allow_html=True)

    if "view_m" in st.session_state:
        st.divider()
        m_idx = st.session_state.view_m
        st.subheader(f"Detalle de {meses[m_idx-1]}")
        
        weeks = get_month_weeks_iso(año_sel, m_idx)
        for j, w_days in enumerate(weeks, 1):
            w_profit = get_week_profit(w_days)
            # Meta proporcional: 350 x cantidad de días que tiene esa semana en ESTE mes
            w_target = len(w_days) * 350 
            
            with st.expander(f"SEMANA {j} ({w_days[0].strftime('%d %b')} - {w_days[-1].strftime('%d %b')}) • Total: ${w_profit:,.2f} / Meta: ${w_target:,.0f}"):
                for d in w_days:
                    r = get_day_record(d.strftime("%Y-%m-%d"))
                    p = r["Profit"] if r else 0.0
                    c = "profit-positive" if p >= 0 else "profit-negative"
                    st.write(f"**{d.strftime('%A %d')}**: :{c.split('-')[1]}[${p:,.2f}] - {r['Notas'] if r else ''}")

# ===================== VISTA: RESUMEN GENERAL =====================
else:
    st.markdown('<p class="title">Resumen</p>', unsafe_allow_html=True)
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        total = df["Profit"].sum()
        st.metric("Balance Total Acumulado", f"${total:,.2f}")
        st.line_chart(df.set_index("Fecha")["Profit"])
    else:
        st.info("No hay registros todavía.")

st.sidebar.divider()
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.logged_in = False
    st.rerun()
