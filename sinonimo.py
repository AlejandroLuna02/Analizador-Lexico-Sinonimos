from flask import Flask, request, render_template, redirect, url_for, jsonify
import re
import random

app = Flask(__name__)

synonyms = {
    'rápido': ['veloz', 'ligero', 'ágil', 'pronto', 'expedito'],
    'feliz': ['contento', 'alegre', 'satisfecho', 'radiante', 'eufórico'],
    'triste': ['melancólico', 'deprimido', 'abatido', 'sombrío', 'desolado'],
    'enojado': ['irritado', 'furioso', 'molesto', 'indignado', 'exasperado'],
    'hermoso': ['bello', 'bonito', 'atractivo', 'precioso', 'lindo', 'encantador'],
    'inteligente': ['listo', 'sabio', 'brillante', 'astuto', 'perspicaz'],
    'fuerte': ['robusto', 'potente', 'resistente', 'sólido', 'firme'],
    'débil': ['frágil', 'delicado', 'vulnerable', 'debilitado', 'flojo'],
    'grande': ['enorme', 'gigante', 'inmenso', 'colosal', 'vasto'],
    'pequeño': ['diminuto', 'reducido', 'chico', 'minúsculo', 'pequeñito'],
    'rico': ['adinerado', 'millonario', 'opulento', 'acomodado', 'próspero'],
    'pobre': ['necesitado', 'humilde', 'miserable', 'indigente', 'destituido'],
    'caliente': ['ardiente', 'sofocante', 'abrasador', 'caluroso', 'tórrido'],
    'frío': ['helado', 'hielado', 'glacial', 'frígido', 'congelado'],
    'viejo': ['anciano', 'veterano', 'mayor', 'maduro', 'longevo'],
    'joven': ['adolescente', 'juvenil', 'jovial', 'novel', 'reciente'],
    'difícil': ['complicado', 'complejo', 'arduó', 'espinoso', 'laborioso'],
    'fácil': ['sencillo', 'simple', 'ligero', 'cómodo', 'accesible'],
    'limpio': ['aseado', 'higiénico', 'pulcro', 'impecable', 'limpísimo'],
    'sucio': ['mugriento', 'manchado', 'ensuciado', 'sucísimo', 'empolvado'],
    'amable': ['cortés', 'afable', 'gentil', 'bondadoso', 'amigable'],
    'cansado': ['fatigado', 'agotado', 'exhausto', 'rendido', 'extenuado'],
    'nuevo': ['reciente', 'moderno', 'flamante', 'novedoso', 'fresco'],
    'viejo': ['antiguo', 'usado', 'desgastado', 'obsoleto', 'decaído'],
    'claro': ['luminoso', 'iluminado', 'despejado', 'transparente', 'evidente'],
    'oscuro': ['sombrio', 'tenebroso', 'oscurecido', 'apagado', 'sombrío'],
    'húmedo': ['mojado', 'empapado', 'húmedo', 'saturado', 'encharcado'],
    'seco': ['árido', 'reseco', 'seco', 'desecado', 'escaso'],
    'calmado': ['tranquilo', 'sereno', 'sosegado', 'apacible', 'plácido'],
    'nervioso': ['ansioso', 'agitado', 'inquieto', 'excitado', 'tense'],
    'lento': ['pausado', 'tardo', 'lento', 'languideciente', 'remolón'],
    'lleno': ['completo', 'saturado', 'repleto', 'cargado', 'abundante'],
    'vacío': ['desocupado', 'hueco', 'vano', 'desierto', 'vacuo'],
    'sabroso': ['gustoso', 'delicioso', 'exquisito', 'apetitoso', 'suculento'],
    'insípido': ['soso', 'sin sabor', 'insulso', 'inodoro', 'insípido'],
    'caro': ['costoso', 'preciado', 'carísimo', 'valioso', 'exorbitante'],
    'barato': ['económico', 'accesible', 'baratillo', 'módico', 'razonable'],
    'morir': ['fallecer', 'expirar', 'perecer', 'sucumbir', 'extinguirse'],
    'contento': ['feliz', 'satisfecho', 'complacido', 'radiante'],
    'molesto': ['irritado', 'enojado', 'indignado', 'ofuscado'],
    'claro': ['lúcido', 'obvio', 'evidente', 'transparente'],
    'oscuro': ['sombrío', 'obscuro', 'tenebroso', 'misterioso'],
    'aburrido': ['tedioso', 'monótono', 'soporífero', 'insulso'],
    'emocionante': ['excitante', 'thrilling', 'conmovedor', 'estimulante'],
    'confuso': ['perplejo', 'desconcertado', 'desorientado', 'indescifrable'],
    'seguro': ['cierto', 'confiable', 'firme', 'estable'],
    'inseguro': ['incerto', 'dudoso', 'temeroso', 'vacilante'],
    'rico': ['opulento', 'lujoso', 'próspero', 'abundante'],
    'saludable': ['sano', 'vigoroso', 'robusto', 'salubre'],
    'enfermo': ['indispuesto', 'afebril', 'débil', 'enfermizo'],
    'fuerte': ['robusto', 'duradero', 'sólido', 'resistente'],
    'debil': ['frágil', 'débil', 'indefenso', 'delicado'],
    'rápido': ['rápido', 'veloz', 'ágil', 'expedito'],
    'lento': ['tardo', 'pausado', 'lento', 'moroso'],
    'cálido': ['caluroso', 'tibio', 'templado', 'ardiente'],
    'frío': ['gélido', 'frígido', 'helado', 'fresco'],
    'brillante': ['luminoso', 'resplandeciente', 'radiante', 'destellante'],
    'opaco': ['mate', 'apagado', 'oscuro', 'nublado']
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
