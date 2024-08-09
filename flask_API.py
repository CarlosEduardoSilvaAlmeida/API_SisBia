from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
import io
import json

app = Flask(__name__)

# Carregar o CSV com codificação 'latin1'
df = pd.read_csv('ARQUIVO_13_06_2024_17_17_31_KO (1).CSV', encoding='latin1')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    estado = request.args.get('estado')
    grupo = request.args.get('grupo')
    classe = request.args.get('classe')

    # Log dos parâmetros recebidos
    print(f"Parâmetros recebidos - Estado: {estado}, Grupo: {grupo}, Classe: {classe}")

    # Aplicar filtros condicionais
    filtered_df = df
    if estado:
        filtered_df = filtered_df[filtered_df['processo_sg_uf'] == estado]
    if grupo:
        filtered_df = filtered_df[filtered_df['no_taxon_grupo'] == grupo]
    if classe:
        filtered_df = filtered_df[filtered_df['sintax_classe'] == classe]

    # Log do DataFrame filtrado
    print(f"DataFrame filtrado:\n{filtered_df}")

    # Selecionar as colunas especificadas
    result_df = filtered_df[['ua_ponto_central_ocorrencia_longitude', 'ua_ponto_central_ocorrencia_latitude', 'sintax_ordem', 'sintax_familia', 'sintax_genero', 'bio_taxon_incerteza', 'sintax_especie', 'bio_data']]
 
    print(f"DataFrame final:\n{result_df}")

    # Converter para JSON
    resultado_json = result_df.to_json(orient='records')
    resultado_json = json.loads(resultado_json)

    # Retornar o JSON formatado
    return jsonify(resultado_json)

@app.route('/options', methods=['GET'])
def options():
    estados = df['processo_sg_uf'].dropna().unique().tolist()
    grupos = df['no_taxon_grupo'].dropna().unique().tolist()
    classes = df['sintax_classe'].dropna().unique().tolist()
    
    return jsonify({
        'estados': estados,
        'grupos': grupos,
        'classes': classes
    })

if __name__ == '__main__':
    app.run(debug=True)