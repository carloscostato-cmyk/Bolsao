from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import os
from datetime import datetime
import openpyxl

app = Flask(__name__)
app.secret_key = 'claro-fortinet-2026'
DB_PATH = os.path.join(os.path.dirname(__file__), 'sistema.db')

import logging
logging.basicConfig(level=logging.DEBUG)

def init_db():
    """Garante que o banco e as tabelas existem ao iniciar."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontos_bolsao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            point_pack_number TEXT NOT NULL UNIQUE,
            responsavel TEXT NOT NULL,
            projetos TEXT,
            pontos INTEGER NOT NULL,
            used_amount REAL DEFAULT 0,
            registration_date TEXT,
            expiration_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontos_utilizados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bolsao_id INTEGER,
            serial_number TEXT NOT NULL,
            dados_cliente TEXT,
            product_model TEXT,
            valor_pontos_dia REAL NOT NULL,
            data_aplicacao TEXT NOT NULL,
            data_fim TEXT,
            FOREIGN KEY (bolsao_id) REFERENCES pontos_bolsao (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS base_conciliacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_number TEXT NOT NULL,
            description TEXT,
            usage_date TEXT,
            points REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco ao subir a aplicação
init_db()

def get_db_connection():
    """Cria uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    """
    Tela principal (Dashboard) que consolida as informações
    de pontos, replicando a lógica da aba "Dashboard" do Excel.
    """
    conn = get_db_connection()
    
    # Lógica para buscar e calcular os dados para o Dashboard
    # Esta é uma implementação inicial. A lógica de cálculo será refinada.
    
    # Exemplo: buscar totais de pontos do bolsão
    bolsao_summary = conn.execute('''
        SELECT 
            responsavel || ' (' || projetos || ')' as grupo,
            SUM(pontos) as pontos_totais,
            SUM(used_amount) as used_totais_fortinet
        FROM pontos_bolsao
        GROUP BY grupo
    ''').fetchall()

    # Exemplo: buscar pontos utilizados calculados
    utilizados_summary = conn.execute('''
        SELECT 
            b.responsavel || ' (' || b.projetos || ')' as grupo,
            SUM(pu.valor_pontos_dia * (julianday('now') - julianday(pu.data_aplicacao))) as pontos_consumidos_calculado
        FROM pontos_utilizados pu
        JOIN pontos_bolsao b ON pu.bolsao_id = b.id
        GROUP BY grupo
    ''').fetchall()
    
    conn.close()

    # Unir os dados para a view (lógica simplificada)
    # Em um cenário real, isso seria feito com mais cuidado, talvez no próprio SQL ou com Pandas
    
    dados_dashboard = []
    utilizados_map = {item['grupo']: item['pontos_consumidos_calculado'] for item in utilizados_summary}

    for item in bolsao_summary:
        grupo = item['grupo']
        pontos_totais = item['pontos_totais']
        used_totais_fortinet = item['used_totais_fortinet']
        pontos_utilizados_calc = utilizados_map.get(grupo, 0)
        
        dados_dashboard.append({
            'grupo': grupo,
            'pontos_totais': pontos_totais,
            'used_totais_fortinet': used_totais_fortinet,
            'remaining_totais_fortinet': pontos_totais - used_totais_fortinet,
            'pontos_utilizados_analitico': pontos_utilizados_calc,
            'faltantes_analitico': pontos_totais - pontos_utilizados_calc,
            'percent_fortinet': (used_totais_fortinet / pontos_totais) * 100 if pontos_totais else 0,
            'percent_analitico': (pontos_utilizados_calc / pontos_totais) * 100 if pontos_totais else 0,
        })

    return render_template('index.html', dashboard_data=dados_dashboard)

@app.route('/pontos_bolsao')
def listar_pontos_bolsao():
    """Lista todos os pacotes de pontos (Point Packs)."""
    conn = get_db_connection()
    pontos = conn.execute('SELECT * FROM pontos_bolsao ORDER BY registration_date DESC').fetchall()
    conn.close()
    return render_template('pontos_bolsao.html', pontos=pontos)

@app.route('/pontos_bolsao/novo', methods=['GET', 'POST'])
def novo_ponto_bolsao():
    """Tela para adicionar um novo Point Pack."""
    erro = None
    if request.method == 'POST':
        try:
            pontos     = int(request.form['pontos'])
            used       = float(request.form.get('used_amount', 0) or 0)
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO pontos_bolsao (point_pack_number, responsavel, projetos, pontos, used_amount, registration_date, expiration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['point_pack_number'],
                request.form['responsavel'],
                request.form['projetos'],
                pontos,
                used,
                request.form['registration_date'],
                request.form['expiration_date']
            ))
            conn.commit()
            conn.close()
            return redirect(url_for('listar_pontos_bolsao'))
        except sqlite3.IntegrityError:
            erro = 'Número do Pack já cadastrado. Use um número diferente.'
        except Exception as e:
            erro = f'Erro ao salvar: {str(e)}'

    return render_template('novo_bolsao.html', erro=erro)

@app.route('/pontos_utilizados')
def listar_pontos_utilizados():
    """Lista todos os equipamentos e seu consumo de pontos."""
    conn = get_db_connection()
    # A query calcula os dias e pontos consumidos dinamicamente
    query = '''
        SELECT
            pu.id,
            pu.serial_number,
            pu.dados_cliente,
            pu.product_model,
            pu.valor_pontos_dia,
            pu.data_aplicacao,
            pu.data_fim,
            b.responsavel || ' (' || b.projetos || ')' as resp_projeto,
            CASE
                WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
            END as dias_consumidos,
            (CASE
                WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
            END) * pu.valor_pontos_dia as pontos_consumidos
        FROM pontos_utilizados pu
        JOIN pontos_bolsao b ON pu.bolsao_id = b.id
        ORDER BY pu.data_aplicacao DESC
    '''
    pontos = conn.execute(query).fetchall()
    conn.close()
    
    total_pontos = sum(p['pontos_consumidos'] for p in pontos)
    media_pontos = total_pontos / len(pontos) if pontos else 0
    
    return render_template('pontos_utilizados.html', data=pontos, total_pontos=total_pontos, media_pontos=media_pontos)

@app.route('/pontos_utilizados/novo', methods=['GET', 'POST'])
def novo_ponto_utilizado():
    """Tela para registrar o uso de pontos por um equipamento."""
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO pontos_utilizados (bolsao_id, serial_number, dados_cliente, product_model, valor_pontos_dia, data_aplicacao, data_fim)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['bolsao_id'],
            request.form['serial_number'],
            request.form['dados_cliente'],
            request.form['product_model'],
            float(request.form['valor_pontos_dia']),
            request.form['data_aplicacao'],
            request.form.get('data_fim') if request.form.get('data_fim') else None
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pontos_utilizados'))

    conn = get_db_connection()
    bolsoes = conn.execute("""
        SELECT id, responsavel, projetos, (pontos - used_amount) as saldo
        FROM pontos_bolsao
        ORDER BY responsavel, projetos, saldo DESC
    """).fetchall()

    # Grupos únicos — para cada responsavel+projetos, pega o pack com maior saldo
    grupos_vistos = set()
    grupos_unicos = []
    for b in bolsoes:
        chave = (b['responsavel'], b['projetos'])
        if chave not in grupos_vistos:
            grupos_vistos.add(chave)
            grupos_unicos.append(b)

    conn.close()
    return render_template('novo_ponto_utilizado.html', bolsoes=grupos_unicos)

@app.route('/conciliacao', methods=['GET', 'POST'])
def conciliacao():
    """Página para upload e visualização da conciliação com a base Fortinet."""
    conn = get_db_connection()

    if request.method == 'POST':
        arquivo = request.files.get('arquivo_conciliacao')
        if not arquivo or arquivo.filename == '':
            flash('Nenhum arquivo selecionado.', 'erro')
            return redirect(url_for('conciliacao'))

        ext = os.path.splitext(arquivo.filename)[1].lower()
        if ext not in ('.xlsx', '.xls'):
            flash('Formato inválido. Envie um arquivo .xlsx ou .xls.', 'erro')
            return redirect(url_for('conciliacao'))

        try:
            wb = openpyxl.load_workbook(arquivo, read_only=True, data_only=True)
            ws = wb.active

            # Detecta cabeçalhos na primeira linha (case-insensitive, strip)
            headers = []
            for cell in next(ws.iter_rows(min_row=1, max_row=1)):
                val = str(cell.value).strip().lower() if cell.value is not None else ''
                headers.append(val)

            def col_idx(name):
                """Retorna índice da coluna pelo nome (parcial, case-insensitive)."""
                for i, h in enumerate(headers):
                    if name.lower() in h:
                        return i
                return None

            idx_serial  = col_idx('serial')
            idx_desc    = col_idx('description')
            idx_date    = col_idx('usage date') or col_idx('date')
            idx_points  = col_idx('points')

            if idx_serial is None or idx_points is None:
                flash('Colunas obrigatórias não encontradas. Verifique se o arquivo contém "Serial Number" e "Points".', 'erro')
                return redirect(url_for('conciliacao'))

            # Limpa tabela e reinsere
            conn.execute('DELETE FROM base_conciliacao')

            rows_inseridos = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                serial = row[idx_serial] if idx_serial is not None else None
                if not serial:
                    continue
                desc   = row[idx_desc]   if idx_desc   is not None else None
                date   = row[idx_date]   if idx_date   is not None else None
                points = row[idx_points] if idx_points is not None else 0

                # Normaliza data
                if isinstance(date, datetime):
                    date = date.strftime('%Y-%m-%d')
                elif date is not None:
                    date = str(date)

                try:
                    points = float(points) if points is not None else 0.0
                except (ValueError, TypeError):
                    points = 0.0

                conn.execute(
                    'INSERT INTO base_conciliacao (serial_number, description, usage_date, points) VALUES (?, ?, ?, ?)',
                    (str(serial).strip(), str(desc).strip() if desc else '', date, points)
                )
                rows_inseridos += 1

            conn.commit()
            flash(f'Base importada com sucesso! {rows_inseridos} registros carregados.', 'sucesso')

        except Exception as e:
            flash(f'Erro ao processar o arquivo: {str(e)}', 'erro')
        finally:
            conn.close()

        return redirect(url_for('conciliacao'))

    # GET — monta tabela de conciliação cruzando pontos_utilizados × base_conciliacao
    resultado = conn.execute('''
        SELECT
            pu.serial_number,
            pu.dados_cliente,
            pu.product_model,
            b.responsavel || ' (' || b.projetos || ')' AS grupo,
            pu.valor_pontos_dia,
            pu.data_aplicacao,
            CASE
                WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
            END AS dias_consumidos,
            (CASE
                WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
            END) * pu.valor_pontos_dia AS pontos_calculados,
            COALESCE((
                SELECT SUM(bc.points)
                FROM base_conciliacao bc
                WHERE UPPER(TRIM(bc.serial_number)) = UPPER(TRIM(pu.serial_number))
            ), 0) AS pontos_fortinet
        FROM pontos_utilizados pu
        JOIN pontos_bolsao b ON pu.bolsao_id = b.id
        ORDER BY grupo, pu.serial_number
    ''').fetchall()

    # Conta registros na base de conciliação
    total_base = conn.execute('SELECT COUNT(*) as c FROM base_conciliacao').fetchone()['c']
    conn.close()

    # Calcula diferença para cada linha
    linhas = []
    for r in resultado:
        calc    = r['pontos_calculados'] or 0
        fortinet = r['pontos_fortinet'] or 0
        diff    = calc - fortinet
        status  = 'ok' if abs(diff) < 0.01 else ('acima' if diff > 0 else 'abaixo')
        linhas.append({**dict(r), 'diferenca': diff, 'status': status})

    return render_template('conciliacao.html', linhas=linhas, total_base=total_base)


@app.route('/debug/status')
def debug_status():
    """Rota temporária de diagnóstico."""
    import sys
    try:
        conn = get_db_connection()
        tabelas = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        conn.close()
        return {
            'status': 'ok',
            'python': sys.version,
            'db_path': DB_PATH,
            'db_exists': os.path.exists(DB_PATH),
            'tabelas': [t['name'] for t in tabelas]
        }
    except Exception as e:
        return {'status': 'erro', 'mensagem': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
