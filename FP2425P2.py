'''
Orbito-n
2º Projeto de Fundamentos da Programação
Henrique Lhano
Número: 109281
henrique.lhano@tecnico.ulisboa.pt
'''

LETRAS = tuple('abcdefghijklmnopqrstuvwxyz')
DIFICULDADES = ('facil', 'normal')
MODOS = ('facil', 'normal', '2jogadores')

'''TAD posicao'''
#Construtor
def cria_posicao(col, lin):
    if type(col) == str and len(col) == 1 and 'a' <= col <= 'j' \
        and type(lin) == int and  1 <= lin <= 10:
            return (col, lin)   
    raise ValueError("cria_posicao: argumentos invalidos") 
'''A função cria_posicao é projetada para criar um tuplo contendo uma letra e um número inteiros como elementos.
Caso contrário, ela levanta uma exceção ValueError.'''


#Seletores
def obtem_pos_col(p):
    return p[0]

def obtem_pos_lin(p):
    return p[1]
'''Os seletores servem para obter a coluna e a linha da posição respetivamente. 
Os seletores são utilizados posteriormente para garantir que cumpro as regras de abstração da TAD posição.'''

#Reconhecedor
def eh_posicao(arg):
    return type(arg) == tuple and len(arg) == 2 \
        and type(arg[0]) == str and 'a' <= arg[0] <= 'j' \
            and type(arg[1]) == int and  1 <= arg[1] <= 10

#Teste
def posicoes_iguais(p1, p2):
    return eh_posicao(p1) and eh_posicao(p2) and obtem_pos_col(p1) == obtem_pos_col(p2) and obtem_pos_lin(p1) == obtem_pos_lin(p2)

#Transformador
def posicao_para_str(p): # Converter algo tipo ('a',2) em 'a2'
    return f'{obtem_pos_col(p)}{obtem_pos_lin(p)}'

def str_para_posicao(s): # Converter algo tipo 'a2' em ('a',2)
    return cria_posicao(s[0], int(s[1:]))  # Slicing no argumento de qualquer tipo no índice 1

# Funções de alto nível associados a este TAD
def eh_posicao_valida(p,n):
    return eh_posicao(p) and type(n) == int and 2 <= n <= 5 

def obtem_posicoes_adjacentes(p, n, d):
    if eh_posicao_valida(p, n) and type(d) == bool:
        LETRAS_LOCAL = [chr(i) for i in range(97, 97 + 2 * n)]  # LETRAS_LOCAL da 'a'(97 em ASCII) até a última coluna para o tabuleiro de 2n*2n
        def limite_direito(col):
            return col == LETRAS_LOCAL[-1]  # Verifica se a coluna está no limite direito
        def limite_esquerdo(col):
            return col == 'a'  # Verifica se a coluna está no limite esquerdo
        def limite_superior(lin):
            return lin == 1  # Verifica se está na linha superior
        def limite_inferior(lin):
            return lin == 2 * n  # Verifica se está na linha inferior
        
        if d is False:  # Adjacentes ortogonais
            move = {
                'U': lambda x: None if limite_superior(obtem_pos_lin(x)) else cria_posicao(obtem_pos_col(x), obtem_pos_lin(x)-1),  # Acima
                'R': lambda x: None if limite_direito(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))+1], obtem_pos_lin(x)),  # Direita
                'D': lambda x: None if limite_inferior(obtem_pos_lin(x)) else cria_posicao(obtem_pos_col(x), obtem_pos_lin(x)+1),  # Abaixo
                'L': lambda x: None if limite_esquerdo(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))-1], obtem_pos_lin(x))  # Esquerda
            }
            return tuple(move[d](p) for d in ('U', 'R', 'D', 'L') if move[d](p))  # Adjacências ortogonais ordenadas 
        
        if d is True:  # Todas as adjacentes
            todas = {
                'U': lambda x: None if limite_superior(obtem_pos_lin(x)) else cria_posicao(obtem_pos_col(x), obtem_pos_lin(x)-1),  # Acima
                'UR': lambda x: None if limite_superior(obtem_pos_lin(x)) or limite_direito(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))+1], obtem_pos_lin(x)-1),  # Superior direita
                'R': lambda x: None if limite_direito(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))+1], obtem_pos_lin(x)),  # Direita
                'DR': lambda x: None if limite_inferior(obtem_pos_lin(x)) or limite_direito(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))+1], obtem_pos_lin(x)+1),  # Inferior direita
                'D': lambda x: None if limite_inferior(obtem_pos_lin(x)) else cria_posicao(obtem_pos_col(x), obtem_pos_lin(x)+1),  # Abaixo
                'DL': lambda x: None if limite_inferior(obtem_pos_lin(x)) or limite_esquerdo(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))-1], obtem_pos_lin(x)+1),  # Inferior esquerda
                'L': lambda x: None if limite_esquerdo(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))-1], obtem_pos_lin(x)),  # Esquerda
                'UL': lambda x: None if limite_superior(obtem_pos_lin(x)) or limite_esquerdo(obtem_pos_col(x)) else cria_posicao(LETRAS_LOCAL[LETRAS_LOCAL.index(obtem_pos_col(x))-1], obtem_pos_lin(x)-1)  # Superior esquerda
            }
            return tuple(todas[d](p) for d in ('U', 'UR', 'R', 'DR', 'D', 'DL', 'L', 'UL') if todas[d](p))  # Todas as adjacentes ordenadas

''' Nota que eu no cálculo das adjacentes já coloco por ordem no sentido horário.
A função cria uma posição adjacente a não ser que algum dos limites seja desrespeitado.
Nota que a variável local LETRAS_LOCAL só tem as letras em codigo ASCII de 'a' a chr(97+2*n), ou seja varia consoante os limites do tabuleiro,
que dependem do n(número de órbitas) que recebe de entrada.'''


def ordena_posicoes(t, n):
    if t == ():
        return ()
    def intersecao_tuplos(tp1, tp2): # Função auxiliar que encontra a interseção entre dois tuplos de posições.
        inter = ()
        for i in tp1:
            if i in tp2:  # Verifica se o elemento de tp1 também está em tp2
                inter += (i,)  # Adiciona a posição ao tuplo de interseção
        return inter

    # Armazena as posições ordenadas.
    ordenado = ()
    tamanho_tab = 2 * n

    # Loop que percorre as órbitas começando da órbita externa.
    while n >= 1:
        # Vê as linhas dentro da órbita atual.
        for i in range(1 + (n - 1), tamanho_tab - (n - 1) + 1, 1):
            # Loop para percorrer as colunas dentro da órbita atual.
            for j in range(1 + (n - 1), tamanho_tab - (n - 1) + 1, 1):
                # Adiciona a posição (coluna, linha) ao tuplo ordenado, se ela ainda não estiver lá.
                if not (chr(96 + j), i) in ordenado:
                    ordenado += ((chr(96 + j), i),)
        n -= 1  # Vai para a órbita seguinte mais interior.
    return intersecao_tuplos(ordenado, t)


'''TAD pedra'''
#Construtores
def cria_pedra_branca():
    return 'O'

def cria_pedra_preta():
    return 'X'

def cria_pedra_neutra():
    return ' '
'''Estes construtores tal como o construtor da TAD POSICAO servem para criar a string que representa uma pedra e respeitar as regras de abstração'''

#Reconhecedores
def eh_pedra(arg):
    return arg in ('X', 'O', ' ')
        
def eh_pedra_branca(p):
    return eh_pedra(p) and p == 'O'

def eh_pedra_preta(p):
    return eh_pedra(p) and p == 'X'
'''Confirmam se o argumento de entrada corresponde a um dos construtores.'''

#Teste
def pedras_iguais(p1, p2):
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2
'''Compara dois argumentos e vê se são pedras e posteriormente se são iguais'''

#Transformador
def pedra_para_str(p):
    return p
'''Converte para uma cadeia de caracteres'''

# Funções de alto nível associados a este TAD
def eh_pedra_jogador(p):
    return eh_pedra_branca(p) or eh_pedra_preta(p)
'''Vê se o argumento é uma pedra branca ou preta'''

def pedra_para_int(p):
    if eh_pedra_branca(p):
        return -1
    if eh_pedra_preta(p):
        return 1
    if cria_pedra_neutra(): # Esta função cria uma pedra assim ' ' que é o mesmo que uma pedra neutra
        return 0
'''Esta função serve para também garantir as regras de abstração.'''

'''TAD tabuleiro'''
# Construtores
def cria_tabuleiro_vazio(n):
    if type(n) == int and 2 <= n <= 5:
        return (n, {})
    raise ValueError('cria_tabuleiro_vazio: argumento invalido')  

'''Esta função serve para criar o tabuleiro sem nenhuma pedra incluída.
O tabuleiro eu defini como um inteiro que corresponde ao número de órbitas e um dicionário,
onde a chave é a pedra e o elemento da chave é a posição onde a pedra está.'''

def cria_tabuleiro(n, tp, tb):
    if type(n) == int and 2 <= n <= 5:
        tabuleiro = cria_tabuleiro_vazio(n)
        if type(tp) == tuple and all(eh_posicao(i) and eh_posicao_valida(i,n) for i in tp) and \
            type(tb) == tuple and all(eh_posicao(i) and eh_posicao_valida(i,n) for i in tb):
            for i in tp: 
                if eh_pedra_jogador(obtem_pedra(tabuleiro, i)):
                    raise ValueError('cria_tabuleiro: argumentos invalidos')   
                coloca_pedra(tabuleiro, i, cria_pedra_preta())
            for i in tb: 
                if eh_pedra_jogador(obtem_pedra(tabuleiro, i)):
                    raise ValueError('cria_tabuleiro: argumentos invalidos')  
                coloca_pedra(tabuleiro, i, cria_pedra_branca())
            return tabuleiro
    raise ValueError('cria_tabuleiro: argumentos invalidos')  
'''Esta função serve para criar o tabuleiro com as pedras que recebe como argumento.
Caso cumpra os argumentos sejam validos, a função coloca as pedras pretas e brancas 
que estão nos tuplos que recebe de entrada e coloca no tabuleiro'''

def cria_copia_tabuleiro(t):
    return (t[0], t[1].copy())
'''Para simular a jogada do PC à frente uso este construtor para construir um tabuleiro igual onde possa simular a jogada do PC.'''

#Seletores
def obtem_numero_orbitas(t):
    return t[0]
'''Seletor que serve para definir o tamanho do tabuleiro.'''

def obtem_pedra(t, p):
    if p in t[1]:
        return t[1][p]
    else:
        return cria_pedra_neutra()
'''Seletor que obtém a pedra de uma dada posição'''
    
def obtem_linha_horizontal(t, p):
    linha_horizontal = []
    for col in range(ord('a'), ord('a') + 2 * obtem_numero_orbitas(t)):  # Percorre as colunas de 'a' até o limite das órbitas
        linha_horizontal.append((cria_posicao(chr(col), obtem_pos_lin(p)), obtem_pedra(t, cria_posicao(chr(col), obtem_pos_lin(p)))))  # Adiciona a posição e a pedra correspondente
    return tuple(linha_horizontal)
'''Irá servir para posteriormente ver k= 2*obtem_numero_orbitas(t) em linha horizontal'''


def obtem_linha_vertical(t,p):
    linha_vertical = []
    for lin in range(1, 2 * obtem_numero_orbitas(t) + 1):  # Percorre as linhas de 1 até o máximo permitido
        linha_vertical.append((cria_posicao(obtem_pos_col(p), lin), obtem_pedra(t, cria_posicao(obtem_pos_col(p), lin))))  # Adiciona a posição e a pedra correspondente
    return tuple(linha_vertical)
'''Irá servir para posteriormente ver k= 2*obtem_numero_orbitas(t) em linha vertical'''

def obtem_linhas_diagonais(t, pos):
    col_idx = ord(obtem_pos_col(pos)) - ord('a') # Converte a letra para o seu index respetivo ASCII
    lin_idx = obtem_pos_lin(pos) - 1 #Index da linha
    max_idx = 2 * obtem_numero_orbitas(t) # Máximo tamanho possível 
    diagonal_principal = []
    anti_diagonal = []

    # Diagonal principal (esquerda-superior para direita-inferior)
    for i in range(-min(lin_idx, col_idx), min(max_idx - lin_idx - 1, max_idx - col_idx - 1) + 1):
        nova_pos = cria_posicao(chr(ord('a') + col_idx + i), lin_idx + i + 1)
        diagonal_principal.append((nova_pos, obtem_pedra(t, nova_pos)))

    # Anti-diagonal (direita-superior para esquerda-inferior)
    for i in range(-min(lin_idx, max_idx - col_idx - 1), min(max_idx - lin_idx - 1, col_idx) + 1):
        nova_pos = cria_posicao(chr(ord('a') + col_idx - i), lin_idx + i + 1)
        anti_diagonal.append((nova_pos, obtem_pedra(t, nova_pos)))

    anti_diagonal_ordenada = tuple(anti_diagonal[::-1]) # Ordena da ordem correta

    # Converte as posições e pedras para strings e estas formam um tuplo
    diagonal_principal_str = tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in diagonal_principal)
    anti_diagonal_str = tuple((posicao_para_str(p), pedra_para_str(v)) for p, v in anti_diagonal_ordenada)

    return diagonal_principal_str, anti_diagonal_str
'''Nota que esta função foi muito baseada na função obtem_diagonais do projeto 1.
A diferença é que o tuplo final é constituído por posições mas convertidas para strings usando a função posicao_para_str.
Irá servir para posteriormente ver k= 2*obtem_numero_orbitas(t) em linha diagonal'''

def obtem_posicoes_pedra(t, j):
    posicoes = []
    tamanho_tabuleiro = 2 * obtem_numero_orbitas(t)  # O tabuleiro tem dimensão de 2 * número de órbitas

    # Percorre todas as posições possíveis no tabuleiro
    for col in range(ord('a'), ord('a') + tamanho_tabuleiro):
        for lin in range(1, tamanho_tabuleiro + 1):
            posicao = cria_posicao(chr(col), lin)
            pedra = obtem_pedra(t, posicao)
            # Adiciona a posição se ela contiver a pedra 'j' ou, se j é None, qualquer posição incluindo as vazias
            if (j is None and pedra == cria_pedra_neutra()) or pedras_iguais(pedra, j):
                posicoes.append(posicao)

    return ordena_posicoes(tuple(posicoes), obtem_numero_orbitas(t))
"""Retorna as posições no tabuleiro que contêm a pedra 'j'. 
Se j for None, retorna todas as posições, incluindo as vazias."""

# Modificadores
def coloca_pedra(t, p, j):
    t[1][p] = j
    return t
'''Coloca uma pedra associada a uma posição.'''

def remove_pedra(t, p):
    if p in t[1]:
        del t[1][p]
    return t 

#Reconhecedor
def eh_tabuleiro(arg):
    return type(arg) == tuple and len(arg) == 2 and type(arg[0]) == int and 2<=arg[0]<=5 \
        and type(arg[1]) == dict and all(eh_posicao(k) for k in arg[1]) and \
            all(eh_posicao_valida(k,arg[0]) for k in arg[1]) and \
                all(eh_pedra(arg[1][k]) for k in arg[1])
'''Função que permite mais à frente usar para ver se um argumento é um tabuleiro.'''

#Teste
def tabuleiros_iguais(t1, t2):
    if eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1[0] == t2[0]: 
        if sorted(t1[1].keys()) == sorted(t2[1].keys()): # mesmas chaves
            return all(pedras_iguais(t1[1][k], t2[1][k]) for k in t1[1])
    return False
'''Tal como referi, usei o eh_tabuleiro para respeitar abstração e depois comparo cada argumento do dicionario.'''

# Transformador
def tabuleiro_para_str(t):
    linhas = []  # Lista que vai armazenar as linhas do tabuleiro como strings
    
    # Cabeçalho das colunas com letras
    cabecalho = "    " + "   ".join([chr(col) for col in range(ord('a'), ord('a') + 2 * obtem_numero_orbitas(t))])
    linhas.append(cabecalho)
    
    for linha in range(1, 2 * obtem_numero_orbitas(t) + 1):
        linha_str = f"{linha:02d} "  # Adiciona o número da linha
        for coluna in range(ord('a'), ord('a') + 2 * obtem_numero_orbitas(t)):
            # Adiciona a pedra na string e o separador "-"
            linha_str += f"[{pedra_para_str(obtem_pedra(t, cria_posicao(chr(coluna), linha)))}]"
            if coluna < ord('a') + 2 * obtem_numero_orbitas(t) - 1:
                linha_str += "-"
        
        # Adiciona a linha montada à lista de linhas
        linhas.append(linha_str)
        # Adiciona o separador vertical
        if linha < 2 * obtem_numero_orbitas(t):
            separador = "    " + "|   " * (2 * obtem_numero_orbitas(t) - 1) + "|"
            linhas.append(separador)
    
    return "\n".join(linhas)  # Converte a lista em string e retorna
'''Este transformador converte o tabuleiro numa cadeia de caracteres, a representação externa de um tabuleiro para os nossos olhos.'''

# Funções de alto nível associadas a este TAD
def move_pedra(t, p1, p2):
    coloca_pedra(t, p2, obtem_pedra(t, p1))
    remove_pedra(t, p1)
    return t

'''FUNÇÕES AUXILIARES NÃO NO ENUNCIADO'''
# Função auxiliar que vê os limites da orbita exterior e devolve a posição seguinte
def posicao_limites_orbita_exterior(t,p,s):
    LETRAS_LOCAL = [chr(i) for i in range(97, 97 + 2 * obtem_numero_orbitas(t))]
    if s is False: # Sentido anti-horário
        '''Se estiver num dos cantos'''
        if obtem_pos_lin(p) == 1 and obtem_pos_col(p) == LETRAS_LOCAL[-1]: # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] # Criou apenas duas ortogonais e eu quero a última no critério de ordenação
        if obtem_pos_lin(p) == 1 and obtem_pos_col(p) == LETRAS_LOCAL[0]: # Canto superior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] 
        if obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) and obtem_pos_col(p) == LETRAS_LOCAL[0]: # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] 
        if obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) and obtem_pos_col(p) == LETRAS_LOCAL[-1]: # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] 

        if obtem_pos_lin(p) == 1 and obtem_pos_col(p) != LETRAS_LOCAL[-1] and obtem_pos_col(p) != LETRAS_LOCAL[0]: # Na linha superior sem estar nos cantos 
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2] # Posição à esquerda
        if obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) and obtem_pos_col(p) != LETRAS_LOCAL[-1] and obtem_pos_col(p) != LETRAS_LOCAL[0]: # Na linha inferior sem estar nos cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] # Posição à direita
        if obtem_pos_col(p) == LETRAS_LOCAL[0] and 1 < obtem_pos_lin(p) < 2*obtem_numero_orbitas(t): # Na coluna da esquerda sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2] # Posição abaixo 
        if obtem_pos_col(p) == LETRAS_LOCAL[-1] and 1 < obtem_pos_lin(p) < 2*obtem_numero_orbitas(t): # Na coluna da direita sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] # Posição acima 
        
    if s is True: # Sentido horário
        '''Se estiver num dos cantos'''
        if obtem_pos_lin(p) == 1 and obtem_pos_col(p) == LETRAS_LOCAL[-1]: # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] 
        if obtem_pos_lin(p) == 1 and obtem_pos_col(p) == LETRAS_LOCAL[0]: # Canto superior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] 
        if obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) and obtem_pos_col(p) == LETRAS_LOCAL[0]: # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] 
        if obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) and obtem_pos_col(p) == LETRAS_LOCAL[-1]: # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] 
        
        if obtem_pos_lin(p) == 1 and obtem_pos_col(p) != LETRAS_LOCAL[-1] and obtem_pos_col(p) != LETRAS_LOCAL[0]: # Na linha superior sem estar nos cantos 
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] # Posição à direita
        if obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) and  obtem_pos_col(p) != LETRAS_LOCAL[-1] and obtem_pos_col(p) != LETRAS_LOCAL[0]: # Na linha inferior sem estar nos cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2] # Posição à esquerda
        if obtem_pos_col(p) == LETRAS_LOCAL[0] and 1 < obtem_pos_lin(p) < 2*obtem_numero_orbitas(t): # Na linha da esquerda sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] # Posição acima 
        if obtem_pos_col(p) == LETRAS_LOCAL[-1] and 1 < obtem_pos_lin(p) < 2*obtem_numero_orbitas(t): # Na linha da direita sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] # Posição abaixo 
'''Nota que pode haver índices iguais mesmo sendo posições diferentes que quer se tem de obter.
Isso está relacionado com o tamanho do tuplo que é criado pela função obtem_intersecoes_adjacentes.
Quando a posição original é um canto, apenas tem duas adjacentes ortogonais.
Quando esta está numa linha, há três. A posição com índice do tuplo a retornar depende da posição pretendida.
Nota que eu só quero as posições adjacentes ortogonais neste caso, porque nenhuma das posições seguintes vai ser a adjacente diagonal.
Aqui nesta função vê-se a diferença dos casos da obtem_intersecoes_adjacentes, porque para a estratégia fácil, é qualquer adjacente mais próxima do centro.
Para esta função, basta a adjacente ortogonal seguinte, consoante o sentido pretendido.'''


def posicao_limites_orbita_interior(t,s,p):
    if s is False: # Sentido anti-horário
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)-1): # Canto superior esquerdo da órbita interior
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2] # Agora cria 4 ortogonais e eu quero a terceira(baixo)
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)): # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[3] 
        if obtem_pos_lin(p) == (obtem_numero_orbitas(t)+1) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)-1): # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1] 
        if obtem_pos_lin(p) == (obtem_numero_orbitas(t)+1) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)): # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] 
    if s is True: # Sentido horário
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)-1): # Canto superior esquerdo da órbita interior
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)): # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2]
        if obtem_pos_lin(p) == (obtem_numero_orbitas(t)+1) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)-1): # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0] 
        if obtem_pos_lin(p) == (obtem_numero_orbitas(t)+1) and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)): # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[3] 
'''Nota que para qualquer n, a órbita mais interior é sempre um quadrado 2*2.
Daí basta me apenas fazer verificações dos cantos.
A única diferença destes cantos para os exteriores é que estes têm 4 posições adjacentes ortogonais.'''

def posicao_limites_orbita_semiInterior(t,p,s):
    if s is False: #Sentido anti-horário
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t) + 1): # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[3]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 and obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97): # Canto superior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+2 and obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97): # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p, obtem_numero_orbitas(t), False)[1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) + 2 and obtem_pos_col(p) == chr(obtem_numero_orbitas(t) +1 +97): # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0]
        
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 and chr(obtem_numero_orbitas(t)-2+97) < obtem_pos_col(p) < chr(97+obtem_numero_orbitas(t) + 1): #linha superior sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [3]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+2 and chr(obtem_numero_orbitas(t)-2+97) < obtem_pos_col(p) < chr(obtem_numero_orbitas(t) +1 +97): # linha inferior sem cantos
            return obtem_posicoes_adjacentes(p, obtem_numero_orbitas(t), False)[1]
        if obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97) and obtem_numero_orbitas(t)-1 < obtem_pos_lin(p) <  obtem_numero_orbitas(t)+2: #coluna esquerda sem cantos
            return obtem_posicoes_adjacentes(p, obtem_numero_orbitas(t),False) [2]
        if obtem_pos_col(p) == chr(obtem_numero_orbitas(t) +1 +97) and obtem_numero_orbitas(t)-1 < obtem_pos_lin(p) < obtem_numero_orbitas(t) + 2: #coluna direita sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[0]
    
    if s is True: #Sentido horário
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 and obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t) + 1): # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[2]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 and obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97): # Canto superior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+2 and obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97): # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p, obtem_numero_orbitas(t), False)[0]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) + 2 and obtem_pos_col(p) == chr(obtem_numero_orbitas(t) +1 +97): # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[3]
        
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 and chr(obtem_numero_orbitas(t)-2+97) < obtem_pos_col(p) < chr(97+obtem_numero_orbitas(t) + 1): #linha superior sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+2 and chr(obtem_numero_orbitas(t)-2+97) < obtem_pos_col(p) < chr(obtem_numero_orbitas(t) +1 +97): # linha inferior sem cantos
            return obtem_posicoes_adjacentes(p, obtem_numero_orbitas(t), False)[3]
        if obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97) and obtem_numero_orbitas(t)-1 < obtem_pos_lin(p) <  obtem_numero_orbitas(t)+2: #coluna esquerda sem cantos
            return obtem_posicoes_adjacentes(p, obtem_numero_orbitas(t),False) [0]
        if obtem_pos_col(p) == chr(obtem_numero_orbitas(t) +1 +97) and obtem_numero_orbitas(t)-1 < obtem_pos_lin(p) < obtem_numero_orbitas(t) + 2: #coluna direita sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t), False)[2]
'''Órbita intermediária para n = 3 e segunda órbita mais interior para n=4 e n=5'''   


def posicao_limites_orbita_semiInterior2(t,p,s):
    if s is False: # Sentido anti-horário
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-2 and obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)): # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [3]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-2 and obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)): # Canto superior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[2]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+3 and obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)): # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+3 and obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)): # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [0]
        
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) - 2 and  chr(97-3+ obtem_numero_orbitas(t)) < obtem_pos_col(p) < chr(97+2+obtem_numero_orbitas(t)): #linha superior sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [3]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) +3 and chr(97-3+obtem_numero_orbitas(t)) < obtem_pos_col(p) < chr(97+2+obtem_numero_orbitas(t)): #linha inferior sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [1]
        if obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)) and obtem_numero_orbitas(t)-2 < obtem_pos_lin(p) < obtem_numero_orbitas(t)+3:#coluna esquerda sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[2]
        if obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)) and obtem_numero_orbitas(t)-2 < obtem_pos_lin(p) < obtem_numero_orbitas(t)+3: #coluna direita sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[0]

    if s is True:
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-2 and obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)): # Canto superior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [2]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)-2 and obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)): # Canto superior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+3 and obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)): # Canto inferior esquerdo
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [0]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t)+3 and obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)): # Canto inferior direito
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [3]
        
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) - 2 and  chr(97-3+ obtem_numero_orbitas(t)) < obtem_pos_col(p) < chr(97+2+obtem_numero_orbitas(t)): #linha superior sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [1]
        if obtem_pos_lin(p) == obtem_numero_orbitas(t) +3 and chr(97-3+obtem_numero_orbitas(t)) < obtem_pos_col(p) < chr(97+2+obtem_numero_orbitas(t)): #linha inferior sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False) [3]
        if obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)) and obtem_numero_orbitas(t)-2 < obtem_pos_lin(p) < obtem_numero_orbitas(t)+3:#coluna esquerda sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[0]
        if obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)) and obtem_numero_orbitas(t)-2 < obtem_pos_lin(p) < obtem_numero_orbitas(t)+3: #coluna direita sem cantos
            return obtem_posicoes_adjacentes(p,obtem_numero_orbitas(t),False)[2]
'''Segunda órbita mais exterior para n = 4 e órbita do meio para n = 5'''



def obtem_posicao_seguinte(t, p, s):
    # A órbita mais exterior para qualquer caso
    if obtem_pos_lin(p) == 1 or obtem_pos_lin(p) == 2*obtem_numero_orbitas(t) or obtem_pos_col(p) == 'a' or obtem_pos_col(p) == chr(97+2*obtem_numero_orbitas(t)-1):
        return posicao_limites_orbita_exterior(t, p, s)
    
    #verificar órbita segunda exterior para n=4 e órbita do meio para n=5
    elif obtem_pos_lin(p) == obtem_numero_orbitas(t)- 2 or obtem_pos_lin(p) == obtem_numero_orbitas(t) +3 or obtem_pos_col(p) == chr(97-3+obtem_numero_orbitas(t)) or obtem_pos_col(p) == chr(97+2+obtem_numero_orbitas(t)):
        return posicao_limites_orbita_semiInterior2(t,p,s)

    # Verificar órbita intermédia para n = 3, segunda órbita mais interior para n = 4 e para n = 5
    elif obtem_pos_lin(p) == obtem_numero_orbitas(t)-1 or obtem_pos_lin(p) == obtem_numero_orbitas(t)+2 or obtem_pos_col(p) == chr(obtem_numero_orbitas(t)-2+97) or obtem_pos_col(p) == chr(obtem_numero_orbitas(t) +1 +97):
        return posicao_limites_orbita_semiInterior(t, p, s)

    # A órbita mais interior para qualquer caso
    elif obtem_pos_lin(p) == obtem_numero_orbitas(t) or obtem_pos_lin(p) == (obtem_numero_orbitas(t)+1) or obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)) or obtem_pos_col(p) == chr(97+obtem_numero_orbitas(t)+1):
        return posicao_limites_orbita_interior(t, s, p)
'''Com o auxílio das funções auxiliares, eu chamo apenas essas funções e vejo se a linha e coluna está nessa órbita comparando.'''

def roda_tabuleiro(t):
    novas_posicoes = {}
    for posicao in t[1]:
        pedra = obtem_pedra(t, posicao)  # Obter a pedra atual
        proxima_posicao = obtem_posicao_seguinte(t, posicao, False) 
        # Guardar a pedra na nova posição
        novas_posicoes[proxima_posicao] = pedra
    # Remover todas as pedras das posições atuais
    for posicao in list(t[1].keys()):
        remove_pedra(t, posicao)
    # Colocar as pedras nas novas posições
    for posicao, pedra in novas_posicoes.items():
        coloca_pedra(t, posicao, pedra)
    return t
'''Eu guardo a pedra da posição antiga na nova posição, depois removo e coloco.
Nota que não uso o move_pedra porque mover é a mesma coisa que remover e colocar no mesmo sítio, logo não existe necessidade de chamar essa função.'''

def verifica_linha_pedras(tab, pos, jog, k):
    # Obtenha as linhas horizontais, verticais e diagonais centradas na posição pos
    linhas = [
        [x[0] for x in obtem_linha_horizontal(tab, pos)],  # Linha horizontal contendo pos
        [x[0] for x in obtem_linha_vertical(tab, pos)],    # Linha vertical contendo pos
    ] + [[x[0] for x in linha] for linha in obtem_linhas_diagonais(tab, pos)]  # Linhas diagonais

    # Ver cada linha para encontrar sublistas de k posições consecutivas
    for linha in linhas:
        if pos in linha: # Se a posição em questão está mesmo na linha a verificar
            idx = linha.index(pos)  # Índice da posição pos na linha
            for i in range(max(0, idx - k + 1), min(len(linha) - k + 1, idx + 1)): # Tentar capturar sublistas de tamanho k ao redor da posição pos
                this_line = linha[i:i + k]                
                if all(obtem_pedra(tab, p) == jog for p in this_line): # Verificar se todas as posições têm a pedra do jogador jog
                    return True
    return False
'''Função responsável por verificar se há uma linha vertical, horizontal ou diagonal com k = 2*obtem_numero_orbitas(t).'''


'''Funções Adicionais'''
def eh_vencedor(t,j):
    for posicao in obtem_posicoes_pedra(t,j):
        if verifica_linha_pedras(t,posicao,j,2*obtem_numero_orbitas(t)):
            return True
    return False    
'''Função responsável por ver se algum dos jogadores é vencedor.'''

def eh_fim_jogo(t):
    if len(obtem_posicoes_pedra(t,cria_pedra_neutra())) == 0: # Se não há posições livres, o jogo termina
        return True
    if eh_vencedor(t,cria_pedra_branca()) or eh_vencedor(t, cria_pedra_preta()):
        return True
    if eh_vencedor(t,cria_pedra_branca()) and eh_vencedor(t, cria_pedra_preta()): # Se houver dois com k = 2*n é empate e também é fim de jogo
        return True
    return False
'''Função responsável por ver as condições de um fim de jogo.
Se algum dos jogadores é vencedor, o jogo termina.
Se não houver posições livres, o jogo termina.
Se houver dois jogadores com k pedras consecutivas, o jogo termina'''

def escolhe_movimento_manual(tab):
    while True:
        num = input('Escolha uma posicao livre:') 
        if len(num) > 1 and len(num) < 4 and num[0].isalpha() and num[1:].isdigit() and 1 <= int(num[1:]) <= 2*obtem_numero_orbitas(tab):
            pos = str_para_posicao(num)
            if eh_posicao(pos) and eh_posicao_valida(pos, obtem_numero_orbitas(tab)) and not eh_pedra_jogador(obtem_pedra(tab, pos)):
                return pos
'''Esta função é um loop infinito que é responsável por o jogador escolher uma posição em formato tipo 'a1' e converte para ('a',1).
A função aceita uma string e vejo se cada parte dessa mesma string é um numero e letra.'''
       
def escolhe_movimento_auto(t, j, lvl):  # Pedra j é do jogador, não do computador
    if lvl in DIFICULDADES and eh_pedra_jogador(j) and eh_tabuleiro(t):
        if lvl == 'facil':
            print('Turno do computador (facil):')
            adjacentes_livres = set()  
            
            # Obter as posições adjacentes às pedras neutras
            for posicao in obtem_posicoes_pedra(t, cria_pedra_neutra()):
                for adj in obtem_posicoes_adjacentes(posicao, obtem_numero_orbitas(t), True):
                    if not eh_pedra_jogador(obtem_pedra(t, adj)):
                        adjacentes_livres.add(adj)
            
            # Ordenar posições adjacentes e livres restantes
            adjacentes_livres = ordena_posicoes(tuple(adjacentes_livres), obtem_numero_orbitas(t))
            
            # Retornar a primeira posição disponível
            if len(adjacentes_livres) > 0:
                return adjacentes_livres[0]
            else:
                return ordena_posicoes(obtem_posicoes_pedra(t,cria_pedra_neutra()),obtem_numero_orbitas(t))[0]  # posição livre mais interna
            
        elif lvl == 'normal':
            livres_ordenadas = ordena_posicoes(obtem_posicoes_pedra(t, cria_pedra_neutra()), obtem_numero_orbitas(t))
            adversario = cria_pedra_branca() if eh_pedra_preta(j) else cria_pedra_preta()
            melhor_posicao = None

            for pos in livres_ordenadas:
                tab_temp = cria_copia_tabuleiro(t)
                coloca_pedra(tab_temp, pos, j)
                roda_tabuleiro(tab_temp)
                seguinte = obtem_posicao_seguinte(t, pos, False)
                if verifica_linha_pedras(tab_temp, seguinte, j, 2 * obtem_numero_orbitas(t)):
                    return pos

            for pos in livres_ordenadas:
                tab_temp = cria_copia_tabuleiro(t)
                coloca_pedra(tab_temp, pos, adversario)
                seguinte2 = obtem_posicao_seguinte(tab_temp, obtem_posicao_seguinte(tab_temp, pos, False), False)
                roda_tabuleiro(tab_temp)
                roda_tabuleiro(tab_temp)
                if verifica_linha_pedras(tab_temp, seguinte2, adversario, 2 * obtem_numero_orbitas(t)):
                    melhor_posicao = pos  # Atualize melhor_posicao para o caso de bloqueio
                    return melhor_posicao

            return melhor_posicao if melhor_posicao else (livres_ordenadas[0] if livres_ordenadas else None)

'''Função responsável por escolher a posição que o computador irá jogar, consoante a dificuldade escolhida.
Na dificuldade fácil, o computador escolhe a posição adjacente livre mais próxima do centro.
Na normal determino o maior L <= K tal que o jogador consiga ganhar nessa posição após uma rotação.
Se não, jogar numa posição que impossibilita o adversário no final do seu próximo turno de obter L pedras consecutivas numa linha
que contenha essa posição.'''

def orbito(n, modo, jog):
    if type(n) != int or not 2 <= n <= 5 or modo not in MODOS or not eh_pedra_jogador(jog):
        raise ValueError('orbito: argumentos invalidos')
    if modo in DIFICULDADES and jog == cria_pedra_preta(): # Se for contra o computador e começar com as pretas
        print(f"Bem-vindo ao ORBITO-{n}.")
        print(f"Jogo contra o computador ({modo}).")
        print(f"O jogador joga com '{jog}'.")
        tab = cria_tabuleiro_vazio(n)
        print(tabuleiro_para_str(tab))
        while not eh_fim_jogo(tab):
            computador = cria_pedra_branca()
            if jog:
                print("Turno do jogador.")
                posicao = escolhe_movimento_manual(tab)
                atualizado = coloca_pedra(tab, posicao, jog)
                roda_tabuleiro(atualizado)
                print(tabuleiro_para_str(atualizado))
                if eh_vencedor(atualizado,cria_pedra_branca()) and eh_vencedor(atualizado,cria_pedra_preta()):
                    print("EMPATE")
                    return 0
                if eh_vencedor(atualizado,jog): 
                    print("VITORIA")
                    return pedra_para_int(jog)
                if len(obtem_posicoes_pedra(atualizado,cria_pedra_neutra())) == 0:
                    print('EMPATE')
                    return 0
            if computador:
                posicao_pc  = escolhe_movimento_auto(tab, computador, modo)
                apos_jogada = coloca_pedra(tab,posicao_pc,computador)
                print(tabuleiro_para_str(apos_jogada))
                if eh_vencedor(apos_jogada,computador) and eh_vencedor(apos_jogada,jog): # Se ambos tiverem k pedras consecutivas
                    print("EMPATE")
                    return 0
                if eh_vencedor(apos_jogada,computador):
                    print("DERROTA")
                    return pedra_para_int(computador)
                if len(obtem_posicoes_pedra(apos_jogada,cria_pedra_neutra())) == 0:
                    print('EMPATE')
                    return 0
                
    if modo in DIFICULDADES and jog == cria_pedra_branca(): # Se for contra o computador e começar com as brancas
        print(f"Bem-vindo ao ORBITO-{n}.")
        print(f"Jogo contra o computador ({modo}).")
        print(f"O jogador joga com '{jog}'.")
        tab = cria_tabuleiro_vazio(n)
        print(tabuleiro_para_str(tab))
        while not eh_fim_jogo(tab):
            computador = cria_pedra_preta() # Ir alternando de jogador
            posicao_pc = escolhe_movimento_auto(tab,computador,modo) # Escolhe posição do computador
            tab_bot = coloca_pedra(tab,posicao_pc, computador)
            roda_tabuleiro(tab_bot)
            print(tabuleiro_para_str(tab_bot))
            if eh_vencedor(tab_bot,cria_pedra_branca()): # Após rotação, podem surgir k pedras consecutivas minhas mesmo sendo a vez do computador 
                print("VITORIA")
                return pedra_para_int(cria_pedra_branca())
            if eh_vencedor(tab_bot,computador): # Se o computador ganhar após rotação
                print('DERROTA')
                return pedra_para_int(computador) # Devolve sempre o vencedor, mesmo que o jogador perca
            if len(obtem_posicoes_pedra(tab_bot,cria_pedra_neutra())) == 0:
                print('EMPATE')
                return 0
            
            if jog:
                print('Turno do jogador.')
                posicao = escolhe_movimento_manual(tab)
                minha_jogada = coloca_pedra(tab,posicao,jog)
                roda_tabuleiro(minha_jogada)
                print(tabuleiro_para_str(minha_jogada))
                if eh_vencedor(minha_jogada,jog):
                    print('VITORIA')
                    return pedra_para_int(jog)
                if len(obtem_posicoes_pedra(minha_jogada,cria_pedra_neutra())) == 0:
                    print('EMPATE')
                    return 0
                
    if modo == '2jogadores':
        print(f"Bem-vindo ao ORBITO-{n}.")
        print("Jogo para dois jogadores.")
        vazio = cria_tabuleiro_vazio(n)
        print(tabuleiro_para_str(vazio))
        
        # Defino o jogador inicial como pedra preta ('X')
        jog = cria_pedra_preta()
        
        while not eh_fim_jogo(vazio):
            print(f"Turno do jogador '{jog}'.")
            pos = escolhe_movimento_manual(vazio)
            jogada1 = coloca_pedra(vazio, pos, jog)
            roda_tabuleiro(jogada1)
            print(tabuleiro_para_str(jogada1))
            
            # Alternar de jogador
            jog = cria_pedra_branca() if eh_pedra_preta(jog) else cria_pedra_preta()     

            if eh_vencedor(jogada1, jog):
                print(f"VITORIA DO JOGADOR '{jog}'")
                return pedra_para_int(jog)
                
            if len(obtem_posicoes_pedra(jogada1, cria_pedra_neutra())) == 0:
                print('EMPATE')
                return 0
'''No geral, esta função cria um jogo orbito-n entre dois jogadores ou contra o computador 
e retorna -1 se o jogador branco ganhar, ou 1 se o jogador preto ganhar ou 0 se houver um empate.'''
