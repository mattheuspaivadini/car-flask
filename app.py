from flask import Flask, render_template, request, redirect, url_for, session, flash

# Criar a aplicação Flask
app = Flask(__name__)

# Chave secreta para sessões (em produção, use uma chave mais segura)
app.secret_key = 'banana1234'

# Configuração dos produtos (simulando um banco de dados)
app.config['PRODUTOS'] = {
    1: {
        'id': 1, 
        'nome': 'Desodorante', 
        'preco': 23.00, 
        'imagem_url': 'https://pngimg.com/d/deodorant_PNG54.png'
    },
    2: {
        'id': 2, 
        'nome': 'Ouroboros', 
        'preco': 5000000000.00, 
        'imagem_url': 'https://i.pinimg.com/originals/10/68/b2/1068b2cb7bfbc883fd3e211af6e1bf7e.png'
    },
    3: {
        'id': 3, 
        'nome': 'Persona 3 Reload', 
        'preco': 350.00, 
        'imagem_url': 'https://cdn.mobygames.com/covers/18191503-persona-3-reload-windows-apps-front-cover.jpg'
    },
    4: {
        'id': 4, 
        'nome': 'Gameboy Original', 
        'preco': 780.00, 
        'imagem_url': 'https://images.launchbox-app.com/Platforms/6df33ae4-8087-4db1-9f7b-965ddcba11de.png'
    },
    5: {
        'id': 5, 
        'nome': 'Máquina para secar roupa via raios ultravioletas', 
        'preco': 990.00, 
        'imagem_url': 'https://www.decorfacil.com/wp-content/uploads/2022/03/20220321tipos-de-varal-4-750x499.jpg'
    },
    6: {
        'id': 6, 
        'nome': 'Átomo de água', 
        'preco': 0.01, 
        'imagem_url': 'https://cdn.pixabay.com/photo/2013/07/12/18/15/atom-nucleus-153152_960_720.png'
    },
}

# Rota principal - Lista de produtos
@app.route('/')
def index():
    produtos = app.config['PRODUTOS']
    return render_template('index.html', produtos=produtos)

# Rota para o sobre da página
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para adicionar produto ao carrinho
@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    produtos = app.config['PRODUTOS']
    
    # Recuperar carrinho da sessão (ou criar lista vazia)
    carrinho = session.get('carrinho', [])
    
    # Adicionar produto ao carrinho
    carrinho.append(produtos[produto_id])
    
    # Salvar carrinho na sessão
    session['carrinho'] = carrinho
    
    # Mensagem de feedback
    flash('Produto adicionado ao carrinho!')
    
    return redirect(url_for('index'))

# Rota para visualizar o carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    
    # Calcular total
    total = sum(item['preco'] for item in carrinho)
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Rota para remover produto do carrinho
@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    
    # Procurar e remover produto
    for produto in carrinho:
        if produto['id'] == produto_id:
            carrinho.remove(produto)
            session['carrinho'] = carrinho
            flash('Produto removido do carrinho!')
            break
    else:
        flash('Produto não encontrado no carrinho.')
    
    return redirect(url_for('carrinho'))

# Rota para limpar o carrinho
@app.route('/limpar_carrinho', methods=['POST'])
def limpar_carro():
    session['carrinho'] = []
    flash('O carrinho foi limpado com sucesso!')
    return redirect(url_for('carrinho'))

# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)