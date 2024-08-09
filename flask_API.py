from flask import Flask, request, send_file, render_template
import pandas as pd
import io

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

    # Filtrar os dados
    filtered_df = df
    if estado:
        filtered_df = filtered_df[filtered_df['processo_sg_uf'] == estado]
    if grupo:
        filtered_df = filtered_df[filtered_df['no_taxon_grupo'] == grupo]
    if classe:
        filtered_df = filtered_df[filtered_df['sintax_classe'] == classe]

    # Selecionar as colunas especificadas
    result_df = filtered_df[['ua_ponto_central_ocorrencia_longitude', 'ua_ponto_central_ocorrencia_latitude', 'sintax_ordem', 'sintax_familia', 'sintax_genero', 'bio_taxon_incerteza', 'sintax_especie', 'bio_data']]

    # Gerar CSV
    output = io.BytesIO()
    result_df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, mimetype='text/csv', download_name='result.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)