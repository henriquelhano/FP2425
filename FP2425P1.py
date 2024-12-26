'''
1º Projeto de Fundamentos da Programação
Henrique Lhano
Número: 109281
henrique.lhano@tecnico.ulisboa.pt
'''

'''Variáveis Globais'''
dificuldades = ('facil','normal','dificil')
jogadores = (-1, 1)


'''Secção 2.1  Representação do Tabuleiro'''

# 2.1.1
def eh_tabuleiro(tab): 
    return isinstance(tab, tuple)  and 2 <= len(tab) <= 100 and\
        isinstance(tab[0], tuple) and 2 <= len(tab[0]) <= 100 and \
            all((type(v) == tuple and len(tab[0]) == len(v)) for v in tab) and \
            all((type(e) == int) and e in (-1,0, 1) for v in tab for e in v)
 
'''Esta maneira de verificar verifica que um tabuleiro apenas pode ser definido pelas condições 
referidas no enunciado. Um tabuleiro é um tuplo de tuplos onde os tuplos interiores apenas podem ter (-1,0,1).
O tamanho do tuplo exterior representa o número de linhas e o tamanho dos tuplos interiores representa o número de colunas.
O tabuleiro tem tamanho mínimo de 2*2 e tamanho máximo de 100*100.'''
 
# 2.1.2
def eh_posicao(arg):
    return isinstance(arg, int) and arg > 0 and arg < 10000 # Como o máximo é 100*100, o número máximo de posições é de 10000
'''Esta função apenas verifica que é um inteiro positivo, e não se está dentro dos limites'''

# 2.1.3
def obtem_dimensao(tab): 
    return (len(tab), len(tab[0]))
'''Serve para obter as dimensões do tabuleiro.'''

# 2.1.4
def obtem_valor(tab, pos): 
    num_colunas = len(tab[0])
    linha = (pos - 1) // num_colunas  # Converter a posição numérica em índice de linha
    coluna = (pos - 1) % num_colunas  # Converter a posição numérica em índice de linha
    return tab[linha][coluna]         # Devolve o número da pedra
'''Serve para obter o valor da posição, vendo a quem pertence uma determinada pedra.'''

#2.1.5
def obtem_coluna(tab, pos): 
    num_linhas, num_colunas = obtem_dimensao(tab)
    coluna = (pos - 1) % num_colunas + 1 # Calcula o índice da coluna correspondente à posição dada
    return tuple(coluna + i * num_colunas for i in range(num_linhas)) # Tuplo com a coluna onde está a pedra
'''Função que devolve a coluna completa onde a posição está.
Serve também para posteriormente verificar k pedras conscutivas em coluna'''

#2.1.6
def obtem_linha(tab, pos): 
    num_colunas = len(tab[0])
    # Calcula a linha onde a posição está
    linha = (pos - 1) // num_colunas
    inicio_linha = linha * num_colunas + 1
    return tuple(inicio_linha + i for i in range(num_colunas)) # Tuplo com a linha onde está a pedra 
'''Função que devolve a linha completa onde a posição está.
Serve também para posteriormente verificar k pedras consecutivas em linha'''

#2.1.7
def obtem_diagonais(tab, pos):
    num_linhas, num_colunas = obtem_dimensao(tab)

    # Calcula a linha e a coluna da posição fornecida
    linha = (pos - 1) // num_colunas
    coluna = (pos - 1) % num_colunas

    diagonal_principal = []
    anti_diagonal = []

    # Calcula a diagonal principal (esquerda-superior para direita-inferior)
    for i in range(-min(linha, coluna), min(num_linhas - linha, num_colunas - coluna)):
        nova_linha = linha + i # Atualiza a linha
        nova_coluna = coluna + i # Atualiza a coluna
        if 0 <= nova_linha < num_linhas and 0 <= nova_coluna < num_colunas: # Vê -se está nos limites do tabuleiro
            pos_diagonal = nova_linha * num_colunas + nova_coluna + 1 # Vê a posição a seguir da diagonal principal
            diagonal_principal.append(pos_diagonal) # Adiciona à lista

    # Calcula a antidiagonal (direita-superior para esquerda-inferior)
    for i in range(-min(linha, num_colunas - coluna - 1), min(num_linhas - linha, coluna + 1)):
        nova_linha = linha + i # Atualiza a linha
        nova_coluna = coluna - i # Atualiza a coluna
        if 0 <= nova_linha < num_linhas and 0 <= nova_coluna < num_colunas: # Vê -se está nos limites do tabuleiro
            pos_anti_diagonal = nova_linha * num_colunas + nova_coluna + 1 # Vê a posição a seguir da anti_diagonal
            anti_diagonal.append(pos_anti_diagonal) # Adiciona à lista
            anti_diagonal_ordenada = tuple(sorted(anti_diagonal, reverse=True)) # Ordena a lista da antidiagonal da maior para menor posição e de seguida converte para tuplo

    return (tuple(diagonal_principal), anti_diagonal_ordenada) # Devolve o tuplo com a diagonal principal e anti_diagonal

'''Função que devolve as diagonais completas onde a posição está.
Serve também para posteriormente verificar k pedras consecutivas em diagonal'''


def tabuleiro_para_str(tab):  
    linhas = []
    m, n = obtem_dimensao(tab)
    for i, linha in enumerate(tab):
        linha_str = ""
        for j, val in enumerate(linha):
            if val == 1: # Se a posição tiver pedra preta
                linha_str += "X"
            elif val == -1: # Se a posição tiver pedra branca
                linha_str += "O"
            else:
                linha_str += "+" # Se não tiver pedra de um jogador
            if j < n - 1:
                linha_str += "---"
        linhas.append(linha_str)
        # Adiciona linha intermediária 
        if i < m - 1:
            linhas.append("|   " * (n - 1) + "|")
    return '\n'.join(linhas)
'''Função que dá uma representação externa, uma representação para os nossos olhos de um tabuleiro'''


'''Secção 2.2  Funções de inspeção e manipulação do tabuleiro'''
# 2.2.1
def eh_posicao_valida(tab, pos): 
    if not eh_tabuleiro(tab) or not eh_posicao(pos): # Vê se tab é um tabuleiro e se pos é um inteiro positivo
        raise ValueError('eh_posicao_valida: argumentos invalidos')
    num_linhas, num_colunas = obtem_dimensao(tab)
    if pos > num_linhas * num_colunas: # Verifica se a posição está dentro dos limites do tabuleiro
        return False
    return True
'''Verifica que é uma posição e que está dentro dos limites do tabuleiro'''

#2.2.2
def eh_posicao_livre(tab, pos):  
    if not eh_tabuleiro(tab) or not eh_posicao(pos) or not eh_posicao_valida(tab,pos): # Verifica argumentos de entrada
        raise ValueError('eh_posicao_livre: argumentos invalidos')
    num_linhas, num_colunas = obtem_dimensao(tab)
    if pos > num_linhas * num_colunas:
        raise ValueError('eh_posicao_livre: argumentos invalidos')
    # Calcula a linha e coluna da posição
    linha = (pos - 1) // num_colunas
    coluna = (pos - 1) % num_colunas
    return tab[linha][coluna] == 0
'''Acede à pedra do tabuleiro. Se for 0, devolve true. Caso seja 1 ou -1 devolve false.'''

# 2.2.3
def obtem_posicoes_livres(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('obtem_posicoes_livres: argumento invalido')
    posicoes_livres = []
    num_linhas, num_colunas = obtem_dimensao(tab)
    # Percorre todas as posições do tabuleiro
    for linha in range(num_linhas):
        for coluna in range(num_colunas):
            # Calcula a posição numérica a partir da linha e coluna
            posicao = linha * num_colunas + coluna + 1
            if tab[linha][coluna] == 0: # Se a posição não tiver -1 ou 1, adiciona à lista
                posicoes_livres.append(posicao)
    return tuple(posicoes_livres)

'''Devolve um tuplo com todas as posições livres no tabuleiro.
Uma posição livre é onde nem o jogador nem o computador já jogaram.'''

# 2.2.4
def obtem_posicoes_jogador(tab, jog):
    if not eh_tabuleiro(tab) or jog not in jogadores:
        raise ValueError('obtem_posicoes_jogador: argumentos invalidos')
    posicoes_jogador = []
    num_linhas, num_colunas = obtem_dimensao(tab)
    for linha in range(num_linhas):
        for coluna in range(num_colunas):
            # Calcula a posição numérica a partir da linha e coluna
            posicao = linha * num_colunas + coluna + 1
            # Se o valor na posição for igual ao jogador, adiciona à lista
            if tab[linha][coluna] == jog:
                posicoes_jogador.append(posicao)
    
    return tuple(posicoes_jogador)
'''Devolve um tuplo com todas as posições que o jogador já jogou.
Serve posteriormente para calcular a estratégia fácil da 2.3.3'''

# 2.2.5
def obtem_posicoes_adjacentes(tab, pos):
    if not eh_tabuleiro(tab):
        raise ValueError('obtem_posicoes_adjacentes: argumentos invalidos')
    
    num_linhas, num_colunas = obtem_dimensao(tab)
    if not eh_posicao(pos) or pos > num_linhas * num_colunas: # Verifica se é uma interseção dentro dos limites
        raise ValueError('obtem_posicoes_adjacentes: argumentos invalidos')
    
    num_linhas, num_colunas = obtem_dimensao(tab)
    # Calcula a linha e coluna da posição
    linha = (pos - 1) // num_colunas
    coluna = (pos - 1) % num_colunas
    posicoes_adjacentes = []

    # Direções de movimento 
    direcoes = [
        (-1, -1), (-1, 0), (-1, 1),  # Diagonais superiores
        (0, -1),          (0, 1),     # Horizontais
        (1, -1), (1, 0), (1, 1)       # Diagonais inferiores
    ]

    # Calcula as posições adjacentes
    for d_linha, d_coluna in direcoes:
        nova_linha = linha + d_linha
        nova_coluna = coluna + d_coluna
        
        # Verifica se a nova posição está dentro dos limites do tabuleiro
        if 0 <= nova_linha < num_linhas and 0 <= nova_coluna < num_colunas:
            nova_posicao = nova_linha * num_colunas + nova_coluna + 1 # Calcula a posição com o índice linha e coluna
            posicoes_adjacentes.append(nova_posicao)
    return tuple(sorted(posicoes_adjacentes)) # Converte num tuplo, ordenado do menor para o maior
'''Função que vê as posições acima, ao lado esquerdo, direito e abaixo.
Esta função é fundamental para a estratégia livre de jogo, porque o primeiro critério desta estratégia é jogar na posição adjacente livre mais próxima do centro.'''


# 2.2.6
def ordena_posicoes_tabuleiro(tab, tup): 
    if not eh_tabuleiro(tab) or not isinstance(tup, tuple):
        raise ValueError('ordena_posicoes_tabuleiro: argumentos invalidos')
    num_linhas, num_colunas = obtem_dimensao(tab)
    for i in tup: # verificar que o tuplo contém apenas interseções válidas
        if not eh_posicao(i) or i > num_linhas * num_colunas:
            raise ValueError('ordena_posicoes_tabuleiro: argumentos invalidos')    
    
    # Calcula a posição central
    pos_central = (num_linhas // 2) * num_colunas + (num_colunas // 2) + 1
    
    def calcula_distancia(pos):
        # Função para calcular a distância de Chebyshev de uma posição ao centro
        linha_central = (pos_central - 1) // num_colunas
        coluna_central = (pos_central - 1) % num_colunas
        linha_pos = (pos - 1) // num_colunas
        coluna_pos = (pos - 1) % num_colunas
        return max(abs(linha_central - linha_pos), abs(coluna_central - coluna_pos))

    posicoes_ordenadas = sorted(tup, key=lambda pos: (calcula_distancia(pos), pos)) # lambda é uma expressão matemática algo tipo y = f(x)
    return tuple(posicoes_ordenadas)
'''A distância de Chebyshev é a maior diferença absoluta das linhas e colunas. 
Se a distância for a mesma, as posições são ordenadas por posição numérica.
Nota que usei uma função interna, porque calcula_distância é apenas útil para ordena_posicoes_tabuleiro,
mantendo a função interna para uso exclusivo e facilita também a organização de código.
Esta função serve como critério de desempate caso haja mais que uma posição que cumpra os requisitos de cada estratégia.'''

# 2.2.7
def marca_posicao(tab, pos, jog):  
    if not eh_tabuleiro(tab) or jog not in (-1, 1):
        raise ValueError('marca_posicao: argumentos invalidos')    
    num_linhas, num_colunas = obtem_dimensao(tab)
    if not eh_posicao(pos) or pos > num_linhas * num_colunas:
        raise ValueError('marca_posicao: argumentos invalidos')
    if not eh_posicao_livre(tab,pos):
        raise ValueError('marca_posicao: argumentos invalidos')
    num_linhas, num_colunas = obtem_dimensao(tab)    
    tab_lista = [list(linha) for linha in tab] # Converte o tabuleiro para lista com listas interiores porque estas são mutáveis
    pos -= 1                    # Ajusta a posição para índice de lista (começando do 0)
    linha = pos // num_colunas  
    coluna = pos % num_colunas   
    tab_lista[linha][coluna] = jog # Marca a jogada
    tab_resultante = tuple(tuple(linha) for linha in tab_lista) # Volta a converter para tuplo de tuplos
    return tab_resultante
'''Função que atualiza o tabuleiro após uma jogada de um jogador.'''

# 2.2.8
def verifica_k_linhas(tab, pos, jog, k):
    if not eh_tabuleiro(tab) or not eh_posicao(pos) or jog not in jogadores:
        raise ValueError('verifica_k_linhas: argumentos invalidos')
    if not eh_posicao(k) or not eh_posicao_valida(tab, pos):
        raise ValueError('verifica_k_linhas: argumentos invalidos')
    def conta_consecutivos(seq, pos):
        contador = 0
        max_consecutivos = 0
        inclui_posicao = False # Flag que irá garantir se a posição fornecida está na sequência
            
        for p in seq: # Percorre cada posição da sequência (linha, coluna ou diagonal)
            valor = obtem_valor(tab, p) # Vê o valor de cada posição p
            if valor == jog:
                contador += 1 # Conta pedras consecutivas do jogador
                if p == pos:  # Flag que garante se a posição fornecida está na sequência
                    inclui_posicao = True
            else:
                contador = 0  # Reinicia o contador ao encontrar outro valor diferente da do jogador em questão
            max_consecutivos = max(max_consecutivos, contador)
            
        # Só retorna o máximo de posições de um jogador se a flag estiver a True
        return max_consecutivos if inclui_posicao == True else 0

    # Verificar se uma linha tem k pedras consecutivas
    linha = obtem_linha(tab, pos)
    if conta_consecutivos(linha, pos) >= k:
        return True
    # Verificar se uma coluna tem k pedras consecutivas
    coluna = obtem_coluna(tab, pos)
    if conta_consecutivos(coluna, pos) >= k:
        return True
    # Verificar se uma diagonal principal tem k pedras consecutivas
    diagonais = obtem_diagonais(tab, pos)
    diagonal_principal = diagonais[0]
    if conta_consecutivos(diagonal_principal, pos) >= k:
        return True
    # Verificar se uma antidiagonal tem k pedras consecutivas
    anti_diagonal = diagonais[1]
    if conta_consecutivos(anti_diagonal, pos) >= k:
        return True

    return False

'''A Flag serve para garantir que k pedras consecutivas é do jogador correspondente ao argumento de entrada e não um k linha presente no tabuleiro, 
mesmo que não seja do jogador em questão.
Esta função verifica k pedras consecutivas.
Serve para ver se o jogador em questão ganha o jogo mnk.'''


'''Secção 2.3  Funções de jogo'''
# 2.3.1
def eh_fim_jogo(tab, k):  
    if not eh_tabuleiro(tab) or not eh_posicao(k):
        raise ValueError('eh_fim_jogo: argumentos invalidos')
    for jog in jogadores:
        for pos in obtem_posicoes_jogador(tab, jog):
            if verifica_k_linhas(tab, pos, jog, k): # Se houver k pedras consecutivas, o jogo termina
                return True
    livres = obtem_posicoes_livres(tab)
    if not livres: # Se não houver mais posições livres 
        return True
    return False
'''Função que verifica as condições essenciais para o jogo terminar'''

# 2.3.2
def escolhe_posicao_manual(tab):
    if not eh_tabuleiro(tab):
        raise ValueError('escolhe_posicao_manual: argumento invalido')
    
    while True:
        entrada = int(input('Turno do jogador. Escolha uma posicao livre: '))
        posicao = entrada - 1
        # Verifica se a posição está dentro dos limites do tabuleiro. Não recorro a eh_posicao_valida porque esta função só tem um argumento de entrada.
        total_posicoes = sum(len(row) for row in tab)
        if posicao < 0 or posicao >= total_posicoes:
            continue

        # Converte a posição linear para (linha, coluna)
        linha = posicao // len(tab[0])
        coluna = posicao % len(tab[0])

        # Verifica se a posição está livre
        if tab[linha][coluna] == 0:
            return posicao + 1
        else:
            continue
'''Esta função é um loop infinito que serve para o jogador escolher a posição que deseja jogar.'''

def escolhe_posicao_auto(tab, jog, k, lvl):
    if not eh_tabuleiro(tab) or jog not in jogadores:
        raise ValueError('escolhe_posicao_auto: argumentos invalidos')
    if not eh_posicao(k) or lvl not in dificuldades:
        raise ValueError('escolhe_posicao_auto: argumentos invalidos')
    num_linhas, num_colunas = obtem_dimensao(tab)
    
    if lvl == 'facil':
        print("Turno do computador (facil):")
        posicoes_livres_adjacentes = []
        for pos in obtem_posicoes_jogador(tab, jog): # vê as posições do jogador
            adjacentes = obtem_posicoes_adjacentes(tab, pos) # Vê as adjacentes à do jogador
            for adj in adjacentes:
                if eh_posicao_livre(tab, adj): # Se é adjacente e livre à do jogador adiciona à lista
                    posicoes_livres_adjacentes.append(adj)
        
        if posicoes_livres_adjacentes: # Vê a adjacente livre mais próxima do centro, primeiro critério de jogo na estratégia fácil
            return ordena_posicoes_tabuleiro(tab, tuple(posicoes_livres_adjacentes))[0]
        
        posicoes_livres = obtem_posicoes_livres(tab)
        if posicoes_livres: # Caso não haja livres adjacentes, escolhe a posição livre mais próxima do centro 
            return ordena_posicoes_tabuleiro(tab, posicoes_livres)[0]
            
    elif lvl == 'normal':       
        posicoes_livres_ordenadas = ordena_posicoes_tabuleiro(tab,obtem_posicoes_livres(tab)) # Passo 1: vê as posições livres
        # Encontra o maior L <= k
        for L in range(k, 0, -1):
            # Verifica se o computador pode completar uma linha com L pedras consecutivas
            computador = -jog  # Computador
            for pos in posicoes_livres_ordenadas:
                tab_temp = marca_posicao(tab, pos, computador) # Tabuleiro temporário que vê se o computador consegue ganhar sem alterar o tabuleiro original
                if verifica_k_linhas(tab_temp, pos, computador, L):
                    return pos  # O computador ganha
            # Verifica se o jogador pode completar uma linha com L pedras consecutivas, logo o computador tenta bloquear
            for i in posicoes_livres_ordenadas:
                tab_temp = marca_posicao(tab, i, jog) # Tabuleiro temporário que vê se o jogador pode ganhar, logo o computador tenta bloquear
                if verifica_k_linhas(tab_temp, i, jog, L):
                    return i  # Jogador pode completar L peças consecutivas, logo computador joga aqui para bloquear
        # Se nenhum dos requisitos anteriores é cumprido, joga na posição livre mais próxima do centro
        return posicoes_livres_ordenadas[0]
                
    if lvl == 'dificil':
        print("Turno do computador (dificil):")
        # Parte 2 do raciocínio(Se não consegue ganhar, tenta bloquear a nossa vitória)
        posicoes_a_bloquear = obtem_posicoes_jogador(tab,jog) #posições do jogador
        for i in range(num_linhas):
            for j in range(num_colunas):
                if len(posicoes_a_bloquear) > 1: # Se houver mais que uma 
                    posicoes_a_bloquear_ordenadas = ordena_posicoes_tabuleiro(tab, posicoes_a_bloquear)
                    if verifica_k_linhas(tab, posicoes_a_bloquear_ordenadas[0], jog, k) == True: # Se a posição do jogador levar a k_em_linha
                        return i * num_colunas + j + 1
                if len(posicoes_a_bloquear) == 1:
                    if verifica_k_linhas(tab, posicoes_a_bloquear[0], jog, k) == True:
                        return i * num_colunas + j + i
        for i in range(num_linhas):
            for j in range(num_colunas):
                if tab[i][j] == 0:
                    # Simula a jogada para o jogador atual
                    tab_temp = [list(row) for row in tab]
                    tab_temp[i][j] = jog
                    if verifica_k_linhas== True:  # Verifica se a jogada leva à vitória
                        return i * num_colunas + j + 1
                    tab_temp[i][j] = jog # Simula jogada do oponente
                    if verifica_k_linhas == True:  # Verifica se o oponente venceria
                        return i * num_colunas + j + 1
        return ordena_posicoes_tabuleiro(tab, obtem_posicoes_livres(tab))[0]

'''Esta função calcula todas as estratégias possíveis para o computador jogar o jogo mnk.
Na estratégia fácil, o primeiro critério '''

def jogo_mnk(cfg, jog, lvl):
    if not isinstance(cfg,tuple) or jog not in jogadores or lvl not in dificuldades:
        raise ValueError('jogo_mnk: argumentos invalidos')
    print('Bem-vindo ao JOGO MNK.')
    if jog == 1:
        print("O jogador joga com 'X'.")
    if jog == -1:
        print("O jogador joga com 'O'.")
        
    m, n, k = cfg  # Dimensões do tabuleiro e o valor de k para vencer
    tabuleiro = ((tuple([tuple([0] * n) for _ in range(m)])))  # Cria tabuleiro vazio
    print(tabuleiro_para_str(tabuleiro)) # Imprime tabuleiro vazio
    
    # Loop do jogo para se o jogador for as pretas
    if jog == 1:
        while True:
            computador = -jog # ir alternando de jogador
            if jog:
                posicao = escolhe_posicao_manual(tabuleiro)
                tabuleiro = marca_posicao(tabuleiro, posicao, jog)
                print(tabuleiro_para_str(tabuleiro))
                if verifica_k_linhas(tabuleiro, posicao, jog, k):
                    print("VITORIA")
                    return jog
                elif not obtem_posicoes_livres(tabuleiro):
                    print("EMPATE")
                    return 0
            if computador:
                posicao = escolhe_posicao_auto(tabuleiro, computador, k, lvl)
                tabuleiro = marca_posicao(tabuleiro, posicao, computador)
                print(tabuleiro_para_str(tabuleiro))
                if verifica_k_linhas(tabuleiro, posicao, computador, k):
                    print("DERROTA")
                    return computador
                elif not obtem_posicoes_livres(tabuleiro):
                    print("EMPATE")
                    return 0
                
    # Loop do jogo para se o jogador for as brancas
    if jog == -1: 
        computador = -jog # Ir alternando de jogador
        while True:
            posicao = escolhe_posicao_auto(tabuleiro, computador, k, lvl) # Escolhe posição do computador
            tabuleiro = marca_posicao(tabuleiro, posicao, computador) # Atualiza o tabuleiro com a jogada
            print(tabuleiro_para_str(tabuleiro)) # Representação externa do tabuleiro
            if verifica_k_linhas(tabuleiro, posicao, computador, k):
                print("DERROTA")
                return computador # Devolve sempre o vencedor, mesmo que o jogador perca
            elif not obtem_posicoes_livres(tabuleiro): # Se não houver mais posições livres é empate
                print("EMPATE")
                return 0 # Se não houver vencedor, devolve 0
            if jog:
                posicao = escolhe_posicao_manual(tabuleiro)
                tabuleiro = marca_posicao(tabuleiro, posicao, jog) # Atualiza o tabuleiro com a jogada
                print(tabuleiro_para_str(tabuleiro))
                if verifica_k_linhas(tabuleiro, posicao, jog, k):
                    print("VITORIA")
                    return jog
                elif not obtem_posicoes_livres(tabuleiro):
                    print("EMPATE")
                    return 0
                
'''Nota que o jogo começa sempre pelas pretas. 
Por isso fiz dois loops infinitos em que vejo cada um dos casos do argumento de entrada jog.
O primeiro caso vê se o jogador é as pretas.
O segundo caso vê se o computador é as pretas.
Esta função permite jogar o jogo.'''