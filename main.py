# -*- coding: utf-8 -*-
import re
from funcoes import *
from pathlib import Path
from os import system, name
from grammar import Grammar


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def tratarArq(lista):
    lista = " ".join(lista.split())
    lista = re.split(r' ', lista)
    return lista


def lerArquivo(dir):
    arquivo = []
    b = []
    inicio = ""
    fim = ""

    with open(dir, "r") as gramatica:
        for line in gramatica:
            arquivo.append(line.replace('Îµ', 'ε').strip().split('\n'))
    arquivo = [i for j in arquivo for i in j]

    for i in range(0, len(arquivo)):
        temp = []
        temp = tratarArq(arquivo[i])
        arquivo[i] = temp

    for i in range(0, len(arquivo)):
        tam = len(arquivo[i])
        for j in range(0, tam):
            if "|" in arquivo[i][j]:
                inicio = arquivo[i][0]+" "+arquivo[i][1]
                fim = arquivo[i][-1]
                suma = inicio+" "+fim
                arquivo.append(tratarArq(suma))

    for i in arquivo:
        b.append(" ".join(i[:3]))
    return b


def salvarArquivoFirst(first, epsilon):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    with open(outpath+'/First.txt', 'w+', encoding="utf-8") as file:
        a = "Epsilon na Gramatica = {}".format(epsilon)
        file.write(a + '\n')
        for i in first:
            a = "Primeiro({}) = {}".format(i, first[i])
            file.write(a + '\n')


def salvarArquivoFollow(follow):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    with open(outpath+'/Follow.txt', 'w+', encoding="utf-8") as file:
        a = ''
        for i in follow:
            a = "Follow({}) = {}".format(i, follow[i])
            file.write(a + '\n')


def gravarArquivo(first, follow, epsilon):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    with open(outpath+'/First.txt', 'w+', encoding="utf-8") as file:
        a = "Epsilon na Gramatica = {}".format(epsilon)
        file.write(a + '\n')
        for i in first:
            a = "Primeiro({}) = {}".format(i, first[i])
            file.write(a + '\n')
    print("\n")
    with open(outpath+'/Follow.txt', 'w+', encoding="utf-8") as file:
        a = ''
        for i in follow:
            a = "Follow({}) = {}".format(i, follow[i])
            file.write(a + '\n')


def printArquivo(dir):
    with open(dir, "r", encoding="utf-8") as file:
        for line in file:
            print(line)


def salvar_tabela(tabela):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    tabela.to_excel(outpath+'/Tabela.xls')
    # tabela.to_csv(outpath+'/Tabela.csv', sep=';', encoding='utf-8', header='true', )


def tr_terminais(terminais):
    return [i for j in [list(i) for i in terminais] for i in j]


def salvar_verificador(resultado):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    colunas = "Pilha Entrada Acão".split()
    dados = pd.DataFrame(data=resultado, columns=colunas)
    dados.to_excel(outpath+"/Verificador.xls")


def visualizar_saida(first, follow, epsilon, tabela, gramatica):
    print('--------------------------------------------------------------------------------')
    X = True
    while X:
        print("\n")
        op = input('1 - Visualizar First\n2 - Visualizar Follow\n3 - Visualizar First e Follow\n4 - Visualizar Tabela\n5 - Verificar Cadeia\n6 - Sair\n\nDigite a Opção: ')
        print('\n--------------------------------------------------------------------------------\n')
        if op == '1':
            clear()
            limpar_terminais_first(gramatica.terminals, first)
            visualizar_first(first)

            opc1 = input(
                "Deseja Salvar em Arquivo ?:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Não Salvar): ")
            if opc1 == 's':
                salvarArquivoFirst(first, epsilon)
                print("Arquivo Salvo em /output/First.txt")
            elif opc1 != 's':
                clear()
                pass

            opc = input(
                "Deseja voltar ao menu principal:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Encerrar): ")
            if opc == 's':
                clear()
                X = True
            else:
                clear()
                X = False

        if op == '2':
            clear()
            visualizar_follow(follow)

            opc1 = input(
                "Deseja Salvar em Arquivo ?:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Não Salvar): ")
            if opc1 == 's':
                salvarArquivoFollow(follow)
                print("Arquivo Salvo em /output/Follow.txt")
            elif opc1 != 's':
                clear()
                pass

            opc = input(
                "Deseja voltar ao menu principal:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Encerrar): ")
            if opc == 's':
                clear()
                X = True
            else:
                clear()
                X = False

        if op == '3':
            clear()
            limpar_terminais_first(gramatica.terminals, first)
            visualizar_first(first)
            print(
                '--------------------------------------------------------------------------------\n')
            visualizar_follow(follow)

            opc1 = input(
                "Deseja Salvar em Arquivo ?:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Não Salvar): ")
            if opc1 == 's':
                gravarArquivo(first, follow, epsilon)
                print("Arquivo Salvo em /output/First.txt")
                print("Arquivo Salvo em /output/Follow.txt")
            elif opc1 != 's':
                clear()
                pass

            opc = input(
                "Deseja voltar ao menu principal:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Encerrar): ")
            if opc == 's':
                clear()
                X = True
            else:
                clear()
                X = False

        if op == '4':
            clear()
            visualizar_tabela(retornar_tabela(visual_tab(tabela)))

            opc1 = input(
                "Deseja Salvar em Arquivo ?:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Não Salvar): ")
            if opc1 == 's':
                salvar_tabela(retornar_tabela(visual_tab(tabela)))
                print("Arquivo Salvo em /output/Tabela.xls")
            elif opc1 != 's':
                clear()
                pass

            opc = input(
                "Deseja voltar ao menu principal:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Encerrar): ")
            if opc == 's':
                clear()
                X = True
            else:
                clear()
                X = False

        if op == '5':
            clear()
            verificador = verificar_palavra(
                input("Escreva uma sentença: "), tabela, gramatica)

            if type(verificador) == tuple:
                string, pilha = verificador

                col = "Pilha Entrada Ação".split()
                dados = pd.DataFrame(data=pilha, columns=col)

                print("\n")
                print(dados.set_index(['Pilha', 'Entrada']))
                print("\n")

                opc1 = input(
                    "Deseja Salvar em Arquivo ?:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Não Salvar): ")
                if opc1 == 's':
                    salvar_verificador(pilha)
                    print("Arquivo Salvo em /output/Verificador.xls")
                elif opc1 != 's':
                    clear()
                    pass

            opc = input(
                "Deseja voltar ao menu principal:\n\t(Se Sim Digite :'s', Ou Digite Qualquer Coisa e Dê Enter para Encerrar): ")
            if opc == 's':
                clear()
                X = True
            else:
                clear()
                X = False

        if op == '6':
            clear()
            X = False


def comentarios_sobre_gramaticas(escolha):
    if escolha == 1:
        print("Sobre a Gramatica a.txt, é necessário (((comentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 2:
        print("Sobre a Gramatica b.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 3:
        print("Sobre a Gramatica c.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 4:
        print("Sobre a Gramatica d.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 5:
        print("Sobre a Gramatica e.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 6:
        print("Sobre a Gramatica f.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 7:
        print("Sobre a Gramatica g.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 8:
        print("Sobre a Gramatica h.txt, é necessário (((descomentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")
    if escolha == 9:
        print("Sobre a Gramatica i.txt, é necessário (((comentar))) \na penuntima linha da Função 'terminals' \nLocalizada em grammar.py Dentro da Classe Grammar \npara um bom funcionamento do código")


def main():
    dir = "gramaticas"

    gramatica = [dir+'/a.txt', dir+'/b.txt', dir+'/c.txt',
                 dir+'/d.txt', dir+'/e.txt', dir+'/f.txt', dir+'/g.txt', dir+'/h.txt', dir+'/i.txt']

    clear()
    print("Selecione Entre 1 até 9:\n")
    print("1 - a.txt\n2 - b.txt\n3 - c.txt\n4 - d.txt\n5 - e.txt\n6 - f.txt\n7 - g.txt\n8 - h.txt\n9 - i.txt\n\n")
    escolha = int(input('Escolha uma Gramatica: '))

    if not (escolha in [i for i in range(1, 10)]):
        print("Escolha Invalida")
        exit()

    clear()

    comentarios_sobre_gramaticas(escolha)
    confirmar = input(
        "Digite OK para Continuar ou qualquer coisa para finalizar: ")
    if confirmar != 'OK':
        clear()
        exit()
    elif confirmar == 'OK':
        pass

    clear()

    gr = lerArquivo(gramatica[escolha-1])

    visualizar_grammar(gr)

    gramatica = Grammar(gr)

    terminais, nao_terminais, regras = gramatica.terminals, gramatica.nonterminals, gramatica.rules

    first, follow, epsilon = FirstAndFollow(terminais, nao_terminais, regras)

    tabela = LL1(first, follow, gramatica)

    print("Epsilon nas Expresões \n\n{}".format(epsilon))

    visualizar_saida(first, follow, epsilon, tabela, gramatica)


if __name__ == "__main__":
    main()
