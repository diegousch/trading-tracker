<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diego's Options Profit Tracker</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        :root {
            --bg: #0a0e17;
            --card: #111827;
            --accent: #00ff9d;
            --accent2: #00ccff;
            --text: #e0e0e0;
            --text-light: #94a3b8;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: linear-gradient(180deg, #0a0e17 0%, #111827 100%);
            color: var(--text);
            min-height: 100vh;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .title {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00ff9d, #00ccff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: var(--text-light);
            margin-top: 8px;
        }
        
        .meta-bar {
            background: #1a2338;
            border-radius: 9999px;
            padding: 12px 24px;
            display: inline-flex;
            align-items: center;
            gap: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin: 0 auto;
            display: block;
            max-width: 420px;
        }
        
        .week-container {
            background: #111827;
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 255, 157, 0.1);
            margin-bottom: 2rem;
        }
        
        .week-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid #334155;
            padding-bottom: 1rem;
        }
        
        .progress-container {
            background: #1a2338;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .day-card {
            background: #1a2338;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .day-card:hover {
            border-color: #00ff9d;
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(0, 255, 157, 0.2);
        }
        
        .day-name {
            font-size: 1.4rem;
            font-weight: 600;
            min-width: 110px;
        }
        
        .profit-number {
            font-size: 2rem;
            font-weight: 700;
            flex: 1;
        }
        
        .positive { color: #00ff9d; }
        .negative { color: #ff5252; }
        
        .notes-preview {
            font-size: 0.95rem;
            color: var(--text-light);
            flex: 2;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .form-card {
            background: #1a2338;
            border-radius: 20px;
            padding: 2rem;
            border: 2px solid #00ccff;
            margin-top: 2rem;
        }
        
        .month-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }
        
        .month-card {
            background: #111827;
            border-radius: 20px;
            padding: 1.8rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid #334155;
            cursor: pointer;
        }
        
        .month-card:hover {
            border-color: #00ff9d;
            transform: scale(1.04);
        }
        
        .month-name {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .streak {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(0, 255, 157, 0.1);
            color: #00ff9d;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .cloud {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #1a2338;
            color: #00ccff;
            padding: 10px 20px;
            border-radius: 9999px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0, 204, 255, 0.3);
            margin: 1rem 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">
            📈 Diego's Options Profit Tracker
        </div>
        <div class="subtitle">Tu tracker profesional de opciones • Meta diaria $350 mínimo • $750 ideal</div>
        
        <div class="meta-bar" style="margin-top: 1.5rem;">
            <span><strong>Meta semanal:</strong> <span style="color:#00ff9d;">$1,750</span></span>
            <span style="color:#334155;">|</span>
            <span><strong>Meta diaria:</strong> <span style="color:#00ff9d;">$350</span> mínimo • <span style="color:#00ccff;">$750</span> ideal</span>
        </div>
    </div>

    <!-- SEMANA ACTUAL -->
    <div class="week-container">
        <div class="week-header">
            <h2>🏠 Semana Actual • 30 Mar - 3 Abr 2026</h2>
            <div class="streak">🔥 3 días consecutivos con profit</div>
        </div>

        <!-- Progress semanal -->
        <div class="progress-container">
            <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-weight:600;">
                <span>Progreso semanal</span>
                <span><strong>$1,691</strong> / $1,750</span>
            </div>
            <div style="height:18px; background:#334155; border-radius:9999px; overflow:hidden;">
                <div style="width:96.6%; height:100%; background:linear-gradient(90deg, #00ff9d, #00ccff);"></div>
            </div>
            <div class="cloud" style="margin-top:1rem;">
                ☁️ Faltan <strong>$59</strong> para completar la meta semanal
            </div>
        </div>

        <!-- Días de la semana -->
        <h3 style="margin-bottom:1rem; color:#60a5fa;">Días de la semana</h3>
        
        <!-- Lunes -->
        <div class="day-card">
            <div class="day-name">Lunes<br><span style="font-size:0.95rem; font-weight:400; color:#94a3b8;">30 Mar</span></div>
            <div class="profit-number positive">$450</div>
            <div class="notes-preview">3x SPY Calls 0DTE + 1x QQQ Put...</div>
            <button onclick="editDay('2026-03-30')" style="background:#00ff9d; color:#000; border:none; padding:12px 24px; border-radius:12px; font-weight:600; cursor:pointer;">Editar</button>
        </div>
        
        <!-- Martes -->
        <div class="day-card">
            <div class="day-name">Martes<br><span style="font-size:0.95rem; font-weight:400; color:#94a3b8;">31 Mar</span></div>
            <div class="profit-number positive">$550</div>
            <div class="notes-preview">2x NVDA Calls...</div>
            <button onclick="editDay('2026-03-31')" style="background:#00ff9d; color:#000; border:none; padding:12px 24px; border-radius:12px; font-weight:600; cursor:pointer;">Editar</button>
        </div>
        
        <!-- Miércoles -->
        <div class="day-card">
            <div class="day-name">Miércoles<br><span style="font-size:0.95rem; font-weight:400; color:#94a3b8;">01 Abr</span></div>
            <div class="profit-number negative">-$359</div>
            <div class="notes-preview">Stop loss en TSLA...</div>
            <button onclick="editDay('2026-04-01')" style="background:#00ff9d; color:#000; border:none; padding:12px 24px; border-radius:12px; font-weight:600; cursor:pointer;">Editar</button>
        </div>
        
        <!-- Jueves -->
        <div class="day-card">
            <div class="day-name">Jueves<br><span style="font-size:0.95rem; font-weight:400; color:#94a3b8;">02 Abr</span></div>
            <div class="profit-number positive">$850</div>
            <div class="notes-preview">Gran día en QQQ...</div>
            <button onclick="editDay('2026-04-02')" style="background:#00ff9d; color:#000; border:none; padding:12px 24px; border-radius:12px; font-weight:600; cursor:pointer;">Editar</button>
        </div>
        
        <!-- Viernes -->
        <div class="day-card">
            <div class="day-name">Viernes<br><span style="font-size:0.95rem; font-weight:400; color:#94a3b8;">03 Abr</span></div>
            <div class="profit-number positive">$200</div>
            <div class="notes-preview">Cierre de posiciones...</div>
            <button onclick="editDay('2026-04-03')" style="background:#00ff9d; color:#000; border:none; padding:12px 24px; border-radius:12px; font-weight:600; cursor:pointer;">Editar</button>
        </div>

        <!-- Resultado final de la semana (solo viernes) -->
        <div style="margin-top:2rem; background:#052e16; border-radius:20px; padding:1.5rem; text-align:center; border:2px solid #00ff9d;">
            <strong style="color:#00ff9d; font-size:1.3rem;">🎉 Meta semanal alcanzada</strong><br>
            <span style="font-size:2.2rem; font-weight:700; color:#00ff9d;">+$1,691</span><br>
            <span style="color:#94a3b8;">Superaste la meta de $1,750 por <strong style="color:#ff5252;">-$59</strong> (casi listo)</span>
        </div>
    </div>

    <!-- FORMULARIO DE EDICIÓN (aparece al hacer clic) -->
    <div id="editForm" class="form-card" style="display:none;">
        <h3 id="editingTitle" style="margin-bottom:1rem;">Editando: Lunes 30 Mar 2026</h3>
        
        <div style="display:grid; grid-template-columns:1fr 2fr; gap:2rem;">
            <div>
                <label style="display:block; margin-bottom:8px; font-weight:500;">Profit del día ($)</label>
                <input type="number" id="profitInput" value="450" step="10" style="width:100%; padding:14px; border-radius:12px; background:#1a2338; border:1px solid #334155; color:white; font-size:1.4rem;">
            </div>
            <div>
                <label style="display:block; margin-bottom:8px; font-weight:500;">Notas / Operaciones detalladas</label>
                <textarea id="notesInput" rows="3" style="width:100%; padding:14px; border-radius:12px; background:#1a2338; border:1px solid #334155; color:white; resize:none;">3x SPY Calls 0DTE + 1x QQQ Put...</textarea>
            </div>
        </div>
        
        <div style="margin-top:2rem; display:flex; gap:1rem;">
            <button onclick="saveEdit()" style="flex:1; background:linear-gradient(90deg,#00ff9d,#00ccff); color:#000; border:none; padding:16px; border-radius:16px; font-size:1.1rem; font-weight:700;">💾 GUARDAR CAMBIOS</button>
            <button onclick="cancelEdit()" style="flex:1; background:#334155; color:white; border:none; padding:16px; border-radius:16px; font-size:1.1rem;">Cancelar</button>
        </div>
    </div>

    <!-- MES VIEW (ejemplo de cómo se vería el grid) -->
    <h2 style="margin:3rem 0 1.5rem; color:#60a5fa;">📅 Resumen por Mes • 2026</h2>
    <div class="month-grid">
        <!-- Marzo -->
        <div class="month-card" onclick="viewMonth(3)">
            <div class="month-name">Marzo</div>
            <div style="font-size:2.2rem; font-weight:700; color:#00ff9d;">$8,420</div>
            <div style="margin:8px 0; color:#94a3b8;">Meta mensual: $7,700</div>
            <div style="height:8px; background:#334155; border-radius:9999px;"><div style="width:109%; height:100%; background:#00ff9d;"></div></div>
            <div style="margin-top:12px; color:#00ff9d; font-weight:600;">+9% sobre la meta</div>
        </div>
        
        <!-- Abril -->
        <div class="month-card" onclick="viewMonth(4)">
            <div class="month-name">Abril</div>
            <div style="font-size:2.2rem; font-weight:700; color:#ff5252;">$1,240</div>
            <div style="margin:8px 0; color:#94a3b8;">Meta mensual: $8,050</div>
            <div style="height:8px; background:#334155; border-radius:9999px;"><div style="width:15%; height:100%; background:#ff5252;"></div></div>
            <div style="margin-top:12px; color:#ff5252; font-weight:600;">-85% (en progreso)</div>
        </div>
        
        <!-- Mayo (y así sucesivamente) -->
        <div class="month-card" onclick="viewMonth(5)">
            <div class="month-name">Mayo</div>
            <div style="font-size:2.2rem; font-weight:700;">$0</div>
            <div style="margin:8px 0; color:#94a3b8;">Meta mensual: $7,350</div>
            <div style="height:8px; background:#334155; border-radius:9999px;"></div>
            <div style="margin-top:12px; color:#64748b;">Aún no registrado</div>
        </div>
    </div>

    <script>
        function editDay(date) {
            document.getElementById('editForm').style.display = 'block';
            document.getElementById('editingTitle').innerHTML = `Editando: ${date}`;
            // Aquí iría la lógica real de prellenado desde Python/Streamlit
        }
        
        function saveEdit() {
            alert('✅ Cambios guardados correctamente (en la versión real de Streamlit se actualiza el CSV y recarga la página)');
            document.getElementById('editForm').style.display = 'none';
            // En la app real: st.rerun()
        }
        
        function cancelEdit() {
            document.getElementById('editForm').style.display = 'none';
        }
        
        function viewMonth(mes) {
            alert(`Abriendo detalle completo del mes ${mes} (semanas + días + resumen detallado)`);
            // En Streamlit real: session_state.selected_month = mes; st.rerun()
        }
    </script>
</body>
</html>
