from flask import Flask, request, render_template, redirect, url_for, jsonify
import re
import random

app = Flask(__name__)

synonyms = {
    'rápido': ['veloz', 'ligero', 'ágil', 'pronto'],
    'feliz': ['contento', 'alegre', 'satisfecho'],
    'triste': ['melancólico', 'deprimido', 'abatido'],
    'enojado': ['irritado', 'furioso', 'molesto'],
    'hermoso': ['bello', 'bonito', 'atractivo', 'precioso', 'lindo'],
    'inteligente': ['listo', 'sabio', 'brillante'],
    'fuerte': ['robusto', 'potente', 'resistente', 'sólido'],
    'débil': ['frágil', 'delicado', 'vulnerable'],
    'grande': ['enorme', 'gigante', 'inmenso'],
    'pequeño': ['diminuto', 'reducido', 'chico'],
    'rico': ['adinerado', 'millonario'],
    'pobre': ['necesitado', 'humilde'],
    'caliente': ['ardiente', 'sofocante'],
    'frío': ['helado', 'hielado'],
    'viejo': ['anciano', 'veterano', 'mayor', 'maduro'],
    'joven': ['adolescente', 'juvenil'],
    'difícil': ['complicado', 'complejo'],
    'fácil': ['sencillo', 'simple', 'ligero', 'cómodo'],
    'limpio': ['aseado', 'higiénico'],
    'sucio': ['mugriento', 'manchado', 'ensuciado'],
    'amable': ['cortés', 'afable', 'gentil'],
    'cansado': ['fatigado', 'agotado', 'exhausto'],
    'nuevo': ['reciente', 'moderno', 'flamante'],
    'viejo': ['antiguo', 'usado', 'desgastado'],
    'claro': ['luminoso', 'iluminado', 'despejado'],
    'oscuro': ['sombrio', 'tenebroso'],
    'húmedo': ['mojado', 'empapado'],
    'seco': ['árido', 'reseco'],
    'calmado': ['tranquilo', 'sereno'],
    'nervioso': ['ansioso', 'agitado'],
    'rápido': ['expedito', 'rápido', 'veloz'],
    'lento': ['pausado', 'tardo'],
    'lleno': ['completo', 'saturado'],
    'vacío': ['desocupado', 'hueco'],
    'sabroso': ['gustoso', 'delicioso', 'exquisito'],
    'insípido': ['soso', 'sin sabor'],
    'caro': ['costoso', 'preciado'],
    'barato': ['económico', 'accesible'],
    'morir': ['fallecer', 'expirar', 'perecer', 'sucumbir']
    }

def analyze_code(code):
    tokens = []
    lines = code.split('\n')
    
    for line_number, line in enumerate(lines, start=1):
        words = re.findall(r'\b\w+\b|\S', line)
        
        for word in words:
            token = {
                'value': word,
                'sinónimo': '',
                'dígito': '',
                'símbolo': '',
                'line': line_number
            }

            if word.isdigit():
                token['dígito'] = 'X'
            elif re.match(r'\W', word):
                token['símbolo'] = 'X'
            else:
                found = False
                for key, synonyms_list in synonyms.items():
                    if word == key:
                        token['sinónimo'] = random.choice(synonyms_list)
                        found = True
                        break
                    elif word in synonyms_list:
                        token['sinónimo'] = key
                        found = True
                        break
                
                if not found:
                    token['sinónimo'] = word
            
            tokens.append(token)
    
    return tokens

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code')
    
    if not code:
        return jsonify({"error": "Por favor, ingrese texto para analizar"}), 400
    
    results = analyze_code(code)
    return render_template('index.html', results=results, code=code)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
