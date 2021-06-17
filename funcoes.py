# -*- coding: utf-8 -*-
import pandas as pd
from os import system, name

def union(first, begins):
    n = len(first)
    first |= begins
    return len(first) != n

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def transform2(string, lista):  # conversão e filtragem
    listanova = []
    texto = ""
    tam = len(string)
    x = 0
    while x < tam:
        texto += string[x]
        if(x < tam-1 and texto+string[x+1] in lista):
            listanova.append(texto+string[x+1])
            texto = ""
            x += 1
        elif texto in lista:
            listanova.append(texto)
            texto = ""
        x += 1
    return listanova


def tr3(string, lista):  # conversão e filtragem
    stringnova = ""
    tam = len(string)
    x = 0
    while x < tam:
        if(x < tam-1 and str(string[x]) + str(string[x+1]) in lista):
            stringnova += str(" ")+str(string[x])+str(string[x+1])+str(" ")
            x += 1
        elif(str(string[x]) in lista):
            stringnova += " "+str(string[x])+" "
        else:
            stringnova += str(string[x])
        x += 1
    return list(filter(lambda x: x != "", stringnova.split(" ")))


def verificar_palavra(string, tabela, grammar):
    lista = sorted(
        (list(grammar.terminals)+list(grammar.nonterminals)), key=len, reverse=True)
    lista1 = sorted(list(lista)+list('$'), key=len, reverse=True)
    rule = [(i, transform2(j, lista)) for i, j in grammar.rules]
    nao_terminais = list(grammar.nonterminals)
    terminais = list(grammar.terminals)
    string_pilha = transform2(string, lista)

    if '^' in rule[0][0]:
        rule.pop(0)
    rule = tuple(rule)
    nt_pilha = [rule[0][0]]

    nt_pilha.append('$')
    string_pilha.append('$')
    top = nt_pilha[0]

    verifica = set(tr3(string, lista))
    verifica2 = set(transform2(string, lista))
    if verifica != verifica2:
        return "ERRO String Inválida!!!!"

    resultado = []
    i = 0

    while True:
        if not (top == string_pilha[0]) and nt_pilha[0] in terminais:
            # i += 1
            # print("Linha {}".format(i))
            # print("Pilha: {}".format(nt_pilha))
            # print("Entrada: {}".format(string_pilha))
            # print("Ação: String Recusada")
            # print("--------------------------------------------------------------------------------")
            resultado.append([str(nt_pilha) ,str(string_pilha),"String Recusada"])
            
            return "String Recusada", resultado

        if top == '$' and string_pilha[0] == '$':
            # i += 1
            # print("--------------------------------------------------------------------------------")
            # print("Linha {}".format(i))
            # print("Pilha: {}".format(nt_pilha))
            # print("Entrada: {}".format(string_pilha))
            # print("Ação: Sentença OK")
            # print("--------------------------------------------------------------------------------")
            resultado.append([str(nt_pilha) ,str(string_pilha),"Sentença OK"])
           
            return "String Aceita", resultado
        
        if top == string_pilha[0]:
            # i += 1
            # print("--------------------------------------------------------------------------------")
            # print("Linha {}".format(i))
            # print("Pilha: {}".format(nt_pilha))
            # print("Entrada: {}".format(string_pilha))
            # print("Ação: Desempilha '{}'".format(nt_pilha[0]))
            resultado.append([str(nt_pilha), str(string_pilha),"Desempilha {}".format(nt_pilha[0])])
            
            # print("--------------------------------------------------------------------------------")
            nt_pilha.pop(0)
            string_pilha.pop(0)
            top = nt_pilha[0]
        
        if top in nao_terminais:
            # i += 1
            ant_top = top
            # print("--------------------------------------------------------------------------------")
            # print("Linha {}".format(i))
            # print("Pilha: {}".format(nt_pilha))
            # print("Entrada: {}".format(string_pilha))
            
            consulta = tabela[(top, string_pilha[0])]
            if consulta == 'ERRO':
                # print("Ação: ERRO")
                resultado.append([str(nt_pilha), str(string_pilha) ,"ERRO - String Recusada Pela Tabela"])
                
                return "ERRO - String Recusada Pela Tabela", resultado
            else:
                resultado.append([str(nt_pilha), str(string_pilha),"{} -> {}".format(ant_top, consulta)])
                nt_pilha[0] = consulta
                if len(consulta) > 1:
                    nt_pilha = [i for j in [transform2(
                        i, lista1) for i in nt_pilha] for i in j]
                if nt_pilha[0] == 'ε':
                    nt_pilha.pop(0)
                top = nt_pilha[0]
            
            # print("Ação: {} -> {}".format(ant_top, consulta))
            # print("--------------------------------------------------------------------------------")



def LL1(first, follow, grammar):
    lista = sorted(
        (list(grammar.terminals)+list(grammar.nonterminals)), key=len, reverse=True)
    rule = [(i, transform2(j, lista)) for i, j in grammar.rules]
    terminais = grammar.terminals - {'ε'}

    if not ('^' in rule[0][0]):
        valor = rule[0][0]+'$'
        rule.insert(0, ('^', valor))
        lista = list(lista) + list('$') + list('^')
        terminais |= {'$'}

    if '^' in rule[0][0]:
        rule.pop(0)
    rule = tuple(rule)

    terminais = sorted(terminais, key=len, reverse=True)

    table = {}
    for nt, expression in rule:
        for element in list(terminais):
            table[nt, element] = 'ERRO'
    for nt, expression in rule:
        first_set = first[nt]
        for element in (first_set-{'ε'}):
            for symbol in expression:
                if element in first[symbol]:
                    table[nt, element] = "".join(expression)
                    # if 'ERRO' in set(table[nt, element]):
                    #     table[nt, element] = ["".join(expression)]
                    # if not ("".join(expression) in set(table[nt, element])):
                    #     table[nt, element].append("".join(expression))
                    #     print(table[nt, element])
                    # = ["".join(expression)]
        if 'ε' in first_set:
            for element in follow[nt]:
                table[nt, element] = "".join(expression)
                # [nt+" -> "+"".join(expression)]
        if 'ε' in first[nt] and '$' in follow[nt]:
            table[nt, '$'] = "".join(expression)
            # [nt+" -> "+"".join(expression)]
    return table


def FirstAndFollow(terminais, nao_terminais, regras):
    # lista dos terminais e não terminais
    # terminais = grammar.terminals
    # nao_terminais = grammar.nonterminals
    lista = sorted((list(terminais)+list(nao_terminais)),
                   key=len, reverse=True)

    first = {i: set() for i in nao_terminais}
    first.update((i, {i}) for i in terminais)
    follow = {i: set() for i in nao_terminais}

    rule = tuple([(i, transform2(j, lista)) for i, j in regras])

    if not ('^' in rule[0][0]):
        rule = [list(i) for i in rule]
        valor = [rule[0][0], '$']
        rule.insert(0, ['^', valor])
        lista = sorted((list(lista) + list('$') + list('^')),
                       key=len, reverse=True)
        terminais |= {'$'}
        nao_terminais |= {'^'}
        rule = tuple(tuple(i) for i in rule)
        first = {i: set() for i in nao_terminais}
        first.update((i, {i}) for i in terminais)
        follow = {i: set() for i in nao_terminais}

    epsilon = {'ε'}

    while True:
        updated = False
        for nt, expression in rule:
            for symbol in expression:
                updated |= union(first[nt], first[symbol])
                if symbol not in epsilon:
                    break
                else:
                    updated |= union(epsilon, {nt})
            aux = follow[nt]
            for symbol in reversed(expression):
                if symbol in follow:
                    updated |= union(follow[symbol], aux)
                if symbol in epsilon:
                    aux = aux.union(first[symbol])
                else:
                    aux = first[symbol]

        if not updated:
            for chave, valor in follow.items():
                if 'ε' in follow[chave]:
                    follow[chave] = follow[chave] - {'ε'}
            cond1 = False
            cond2 = False
            for i in epsilon:
                if '^' in i:
                    cond1 = True
                if 'ε' in i:
                    cond2 = True

            for i in nao_terminais:
                if '^' in i:
                    first.pop(i)
                    follow.pop(i)
                if cond1 and '^' in i:
                    epsilon.remove(i)

            for i in terminais:
                # first.pop(i)
                first['$'] = '$'
                if cond2 and 'ε' in i:
                    epsilon.remove(i)
            for i in {'$'}:
                first.pop(i)

            return first, follow, epsilon


def retornar_tabela(table):
    new_table = {}

    for pair in table:
        new_table[pair[1]] = {}
    for pair in table:
        new_table[pair[1]][pair[0]] = table[pair]
    df = pd.DataFrame(new_table).fillna('ERRO')

    return df


def visualizar_tabela(table):
    print("\nTabela Sintática Preditiva \n")
    print(table)
    print("\n")


def visual_tab(table):
    table2 = {}
    for key, val in table.items():
        table2[key] = 'ERRO'
        if not ('ERRO' in val):
            table2[key] = ["{} -> {}".format(key[0], val)]

    return table2


def visualizar_first(first):
    print("First\n")

    for key, value in first.items():
        print("First({}) = {}".format(key, value))
    print("\n--------------------------------------------------------------------------------")


def visualizar_follow(follow):
    print("Follow\n")
    for key, value in follow.items():
        print("Follow({}) = {}".format(key, value))
    print("\n--------------------------------------------------------------------------------")


def visualizar_grammar(grammar):
    clear()
    print("\n\nGramatica\n")
    for i in grammar:
        print(i)
    print("\n--------------------------------------------------------------------------------")


def limpar_terminais_first(terminais, first):
    for i in terminais - {'$'}:
        if i in first:
            first.pop(i)