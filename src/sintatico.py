from lex import analizarLex
from semantico import declararVar, analizarExpressao
from semantico import analizarFuncao
from semantico import atualizarVar
from semantico import printExpressao
import estruturas
from estruturas import *



debug = False

varInicio = None # guarda o incio da declaracao de uma variavel
funcInicio = None # guarda o incio de uma declaracao de funcao
chamadaInicio = None# guarda o inicio de uma chamada de funcao ou variavel
resultadoCondicao = True


def analizarSintaxe(codigo):
    global listaTokens,tabela_de_simbolos,lista_de_funcoes,escopoAtual
    listaTokens,tabela_de_simbolos = analizarLex(codigo)
    print "lexico OK"
    if debug:
        print listaTokens
        for i in tabela_de_simbolos:
            print i
    escopoAtual = funcaoGlobal               
    flag,index= expressao(0)
    return flag

def expressao(tokenIndex=0):
    """
    <expressao>::= if(<operacao>){<expressao>}<expressao>  
                 | while(<operacao>){<expressao>}<expressao> 
                 | TIPO <declaracoes>
                 | void <procedimento>  
                 | ID<chamada>
                 | palavra vazia
                 | print<print>
                 | break;<expressao>
                 | continue;<expressao>
                 | return <operacao>;<expressao> 
    """
    
    index = tokenIndex
     
    if(index < len(listaTokens)):
        if debug :
            print 'expressao',tokenIndex,listaTokens[tokenIndex]
        
        #-----TIPO <declaracoes>
        if(listaTokens[index][0] == 'TIPO'):
            flag,index = declaracoes(index+1)
            if debug :
                print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----if(<operacao>){<expressao>}<expressao>
        elif(listaTokens[index][0] == 'IF' and listaTokens[index+1][0]=='ABRE_PARENTESE'):
            if(resultadoCondicao):
                global escopoAtual,escopoAnterior,resultadoCondicao
        
                escopoIf = {"ESCOPO_PAI":escopoAtual,"TIPO":"IF","EXPRESSOES":[],"VARS":escopoAtual["VARS"],"ESCOPO":[]}
            
                escopoAtual["ESCOPO"].append(escopoIf)        
                escopoAtual = escopoIf
            
            flag,newIndex = operacao(index+2)
            if(resultadoCondicao):
                resultadoCondicao = analizarExpressao("bool",listaTokens[index+2:newIndex+1],escopoAtual["VARS"])
            index = newIndex
            
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" and 
               listaTokens[index+2][0] == 'ABRE_CHAVE'):
                flag,newIndex = expressao(index+3)
                index = newIndex
                if(flag and listaTokens[index+1][0] == "FECHA_CHAVE"):
                    if(resultadoCondicao):         
                        escopoAtual = escopoAtual["ESCOPO_PAI"]
                        resultadoCondicao = True
                    flag,newIndex = Else(index+2)
                    index=newIndex
                    if debug :
                        print "retorno",flag,index,"expressao"
                    return flag,index
                else:
                    if debug :
                        print 'expresao-if-fecha_chave',True
                    return False,index
            else:
                if debug :
                    print 'expresao-if-fecha_parentese',False
                return False,index    
            
        #-----while(<operacao>){<expressao>}<expressao>          
        elif(listaTokens[index][0] == 'WHILE' and listaTokens[index+1][0]=='ABRE_PARENTESE'):
            if(resultadoCondicao):
                global escopoAtual,escopoAnterior,resultadoCondicao
                escopoWhile = {"ESCOPO_PAI":escopoAtual,"TIPO":"WHILE","EXPRESSOES":[],"VARS":escopoAtual["VARS"],"ESCOPO":[]}
                escopoAtual["ESCOPO"].append(escopoWhile)        
                escopoAtual = escopoWhile
                inicioOperacao = index+2
                
            flag,newIndex = operacao(index+2)
            index = newIndex
            if(resultadoCondicao):
                resultadoCondicao = analizarExpressao("bool", listaTokens[inicioOperacao:index+1], escopoAtual["VARS"])
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" and 
               listaTokens[index+2][0] == 'ABRE_CHAVE'):
                
                flag,newIndex = expressao(index+3)
                index=newIndex
                if(flag and listaTokens[index+1][0] == "FECHA_CHAVE"):
                    if(resultadoCondicao):
                        escopoAtual = escopoAtual["ESCOPO_PAI"]
                        resultadoCondicao = True
                        
                    flag,newIndex = expressao(index+1)
                    if debug :
                        print "retorno",flag,index,"expressao"
                    return flag,index
                else:
                    if debug :
                        print 'expresao-while-fecha_chave',False
                    return False,index
                
        #-----ID<chamada>            
        elif(listaTokens[index][0] == 'ID'):
            global chamadaInicio
            chamadaInicio = index
            flag,newIndex = chamada(index+1)
            index = newIndex
            return flag,index
        
        #-----void <procedimento> 
        elif(listaTokens[index][0] == "VOID"):
            flag,index = declaProcedimento(index+1)
            if debug :
                print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----print<print>
        elif(listaTokens[index][0] == "PRINT"):
            flag,index = Print(index+1)
            if debug :
                print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----break;<expressao>
        elif(listaTokens[index][0] == "BREAK" and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
            flag,index = expressao(index+2)
            if debug :
                print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----continue;<expressao> 
        elif(listaTokens[index][0] == "CONTINUE" and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
            flag,index = expressao(index+2)
            if debug :
                print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----return <operacao>;<expressao>
        elif(listaTokens[index][0] == "RETURN"):
            flag,index=operacao(index+1)
            if(flag and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
                flag,index = expressao(index+2)
                if debug :
                    print "retorno",flag,index,"expressao"
                return flag,index
            else:
                if debug :
                    print "expressao-RETURN-ponto e virgula"
                return False,index
        #-----palavra vazia    
        else:
            if debug :
                print 'expresao-vazio',True
                print "retorno",True,index-1
            return True,index-1
    #-----fim da palavra                        
    else:
        if debug :
            print 'expresao-fim',True
            print "retorno",True,(index-1)
        return True,index-1   

def Else(i):
    '''
    <else> ::= else<condicional>
              |<expressao>
    '''
    index = i
    if(index < len(listaTokens)):
        global escopoAtual,resultadoCondicao
        if debug :
            print 'expressao',index,listaTokens[index]
        if(listaTokens[index][0] == "ELSE"):
            if(resultadoCondicao):
                escopoElse = {"ESCOPO_PAI":escopoAtual,"TIPO":"ELSE","EXPRESSOES":[],"VARS":escopoAtual["VARS"],"ESCOPO":[]}
        
                escopoAtual["ESCOPO"].append(escopoElse)        
                escopoAtual = escopoElse
            flag,index= condicional(index+1)
            
            if debug :
                print "retorno",flag,index,"else"
            return flag,index
        else:
            resultadoCondicao = True
            flag,index = expressao(index)
            if debug :
                print "retorno",flag,index,"else"
            return flag,index
    else:
        if debug :
            print "else-fim"
        return flag,index
        
def condicional(i):
    '''
    <condicional> ::= {expressao}expressao    
                   |  if(<operacao>){<expressao>}<else>
    '''
    index=i
    if(index<len(listaTokens)):
        if debug :
            print 'expressao',index,listaTokens[index]
        #-----if(<operacao>){<expressao>}<else>
        if(listaTokens[index][0] == 'IF' and listaTokens[index+1][0]=='ABRE_PARENTESE'):
            if(resultadoCondicao):
                global escopoAtual,escopoAnterior,resultadoCondicao
        
                escopoIf = {"ESCOPO_PAI":escopoAtual,"TIPO":"IF","EXPRESSOES":[],"VARS":escopoAtual["VARS"],"ESCOPO":[]}
            
                escopoAtual["ESCOPO"].append(escopoIf)        
                escopoAtual = escopoIf
            
            flag,newIndex = operacao(index+2)
            if(resultadoCondicao):
                resultadoCondicao = analizarExpressao("bool",listaTokens[index+2:newIndex+1],escopoAtual["VARS"])
            
            index = newIndex
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" and 
               listaTokens[index+2][0] == 'ABRE_CHAVE'):
            
                flag,newIndex = expressao(index+3)
                index = newIndex
                if(flag and listaTokens[index+1][0] == "FECHA_CHAVE"):
                    if(resultadoCondicao):
                        escopoAtual = escopoAtual["ESCOPO_PAI"]
                    flag,newIndex = Else(index+1)
                    index=newIndex
                    if debug :
                        print "retorno",flag,index,"condicional"
                    return flag,index
                else:
                    if debug :
                        print 'expresao-if-fecha_chave',True
                    return False,index
            else:
                if debug :
                    print 'expresao-if-fecha_parentese',False
                return False,index 
            
        #-----{expressao}expressao 
        elif(listaTokens[index][0] == 'ABRE_CHAVE'):
            global resultadoCondicao

            if(resultadoCondicao):
                resultadoCondicao = not resultadoCondicao
            else:
                resultadoCondicao = not resultadoCondicao
            flag,newIndex = expressao(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_CHAVE'):
                if(resultadoCondicao):
                    resultadoCondicao = True            
                    escopoAtual = escopoAtual["ESCOPO_PAI"]
                flag,index = expressao(index+3)
                return flag,index
            else:
                if debug :
                    print 'condicional-fecha_chave',False
                return False,index   
    else:
        if debug :
            print "condicional-fim"
        return False,index                    
              
def declaracoes(i=0):
    """
    <declaracoes>::= ID<declaracao>
    """
    index = i    
    if(index < len(listaTokens)):
        if debug :
            print 'declaracoes',i,listaTokens[i]
        if(listaTokens[index][0] == 'ID'):
            
            flag,newIndex = declaracao(index+1)
            index = newIndex          
            if debug :
                print "retorno",flag,index,"declaracoes"  
            return flag,index
        else:
            if debug :
                print 'declaracoes-ID',False
            return False,index 
    else:
        if debug :
            print 'declaracoes-fim',False
        return False,index
        
def declaracao(i):
    """
    <declaracao>::= (<param>){<expressao>}<expressao>
                 | ;<exprecao> 
                 | =<operacao><declaracao> 

    """
   
    index = i
    if(index < len(listaTokens)):
        if debug :
            print 'declaracao',i,listaTokens[i]
        if(listaTokens[index][0] == "ATRIBUICAO"):
            global varInicio
            varInicio = index-2
            flag,index = operacao(index+1)
            if(flag):
                flag,newIndex = declaracao(index+1)
                index=newIndex
                if debug :
                    print "retorno",flag,index,"declaracao"
                return flag,index
            else:
                if debug :
                    print 'declaracao->atribuicao',False
                return False,index
                
        elif(listaTokens[index][0] == 'PONTO_E_VIRGULA'):
            global resultadoCondicao
            if(resultadoCondicao):# verifica se o codigo depois do while sera executado
                declaVar = None
                if(listaTokens[index-2][0] == "TIPO"):
                    #declaracao de variavel sem atribuicao
                    
                    declaVar = listaTokens[index-2:index+1]
                else:
                    #declaracao de variavel com atribuicao
                   
                    declaVar = listaTokens[varInicio:index+1]
                escopoAtual["VARS"].append(declararVar(declaVar,escopoAtual["VARS"]))
            flag,newIndex = expressao(index+1)
            index=newIndex
            if debug :
                print "retorno",flag,index,"declaracao"
            return flag,index
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            funcInicio = index-2
            flag,newIndex = param(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE' and 
                        listaTokens[index+2][0] == "ABRE_CHAVE"):
                
#                 global escopoAtual,escopoAnterior
#                 escopoFunc = analizarFuncao(listaTokens[funcInicio:index+2], escopoAtual)
#                 escopoAtual["FUNCS"].append(escopoFunc)
#                 escopoAnterior = escopoAtual
#                 escopoAtual = escopoFunc
                
                flag,index = expressao(index+3)
                if(flag and listaTokens[index+1][0] == 'FECHA_CHAVE'):
                    flag,newIndex = expressao(index+2)
                    index=newIndex
                    if debug :
                        print "retorno",flag,index,"declaracao"
                    return flag,index
                else:
                    if debug :
                        print 'operacao-expressao_fecha_chave',False
                    return False,index
            else:
                if debug :
                    print 'declaracao-fecha_parentese,abre_chave',False
                return False,index
        else:
            if debug :
                print 'declaracao-vasio',False
            return False,index    
    else:
        if debug :
            print 'declaracao-fim',False
        return False,index
               
def operacao(i):
    """
    <operacao>::= (<operacao>)<op2>
                | ID'<op_2>          
                | NUMERO<op_2> 
                | true    
                | false     
    """
    index=i
    if(index < len(listaTokens)):
        if debug :
            print 'operacao',i,listaTokens[i]
        if(listaTokens[index][0] == "NUMERO"): 
            flag,newIndex = op2(index+1)
            index = newIndex
            if debug :
                print "retorno",flag,index,"operacao"
            return flag,index
        elif(listaTokens[index][0] == "VALOR_BOOL"):
            if debug :
                print "retorno",True,index,"operacao"
            return True,index
        elif(listaTokens[index][0] == "ID"):
            flag,newIndex = op2(index+1)
            index = newIndex
            if debug :
                print "retorno",flag,index,"operacao"
            return flag,index
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            flag,newIndex = operacao(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE'):
                flag,newIndex = op2(index+2)
                index = newIndex
                if debug :
                    print "retorno",flag,index,"operacao"
                return flag,index
            else:
                if debug :
                    print 'operacao-fecha_parentese',False
                return False,index
        else:
            if debug :
                print 'operacao-vazio',False
            return False,index
    else:
        if debug :
            print 'operacao-fim',False
        return False,index
#IMPLEMENTAR PRODUCAO PARA CHAMADA DE FUNCAO EM OPERACAO            
def op2(i):
    """
    <op_2>::= <sinal><operacao> 
            |(<arg>);<expressao>
            | palavra vazia  

    """
    index=i
    if(index<len(listaTokens)):
        if debug :
            print 'op2',i,listaTokens[i]   
        if(listaTokens[index][0] == 'OP_ARITMETICO' or 
           listaTokens[index][0] == 'OP_BOOLEANO'):
            flag,newIndex=operacao(index+1)
            index=newIndex
            if debug :
                print "retorno",flag,index,"op2"
            return flag,index
        else:
            if debug :
                print 'op2->vazio',True
                print "retorno",True,index-1
            return True,index-1  
    else:
        if debug :
            print 'op2-fim'
            print "retorno",flag,index
        return True,index

def param(i):
    """
<param>::= TIPO ID<param2>
        | palavra vazia
    """
    if debug :
        print 'param',i,listaTokens[i] 
    index = i
    if(index < len(listaTokens)):
        if(listaTokens[index][0] == "TIPO"):
            if debug :
                print listaTokens[index+1]
            if(listaTokens[index+1][0] == "ID"):
                flag,newIndex = param2(index+2)
                index = newIndex
                if debug :
                    print "retorno",flag,index,"param"
                return flag,index
            else: 
                if debug :
                    print "param erro id"
                return False,index    
        else:
            if debug :
                print "retorno",True,index,"param"
            return True,index-1
    else:
        if debug :
            print "param-fim" 
            print "retorno",False,index   
        return False,index

def param2(i):
    """
    <param2> ::= ,<param>
                | palavra vazia

    """
    if debug :
        print 'param2',i,listaTokens[i] 
    index = i
    if(index < len(listaTokens)):
        if(listaTokens[index][0] == 'VIRGULA'):
            flag,newIndex = param(index+1)
            index=newIndex
            if debug :
                print "retorno",flag,index,"param2"
            return flag,index
        else:
            if debug :
                print "retorno",True,index,"param2"    
            return True,index-1
            
    else:
        if debug :
            print "param2-fim"
            print "retorno",False,index    
        return False,index

def chamada(i):
    """
    <chamada>::= (<param>);<expressao>
            | = <operacao>;<expressao>

    """
     
    index = i
    if(index < len(listaTokens)):
        if debug :print 'chamada',i,listaTokens[i]
        if(listaTokens[index][0] == "ABRE_PARENTESE"):
            flag,newIndex = arg(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" 
               and listaTokens[index+2][0] == "PONTO_E_VIRGULA"):
                flag,newIndex = expressao(index+3)
                index = newIndex
                if debug :print "retorno",flag,index,"chamada"
                return flag,index
            else:
                if debug :print "chamada fecha_parentese"
                return False,index
        elif(listaTokens[index][0] == "ATRIBUICAO"):
            
            flag,newIndex = operacao(index+1)
            index = newIndex
            
            atualizarVar(listaTokens[chamadaInicio][1], listaTokens[chamadaInicio+2:index+1], escopoAtual["VARS"])
            
            
            if(flag and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
                flag,newIndex = expressao(index+2)
                index=newIndex
                if debug :print 'retorno',flag,index,"chamada"
                return flag,index
            else:
                if debug :print "chamada-ponto e virgula"
                return False,index
        else:
            if debug :print "chamada abre_parentese"
            return False,index
    else:
        if debug :print "chamada-fim"
        print False,index        

def arg(i):
    '''
    <arg> ::= ID<arg2>
          |VALOR_BOOL<arg2>
          |NUMERO<arg2>
          | palavra vazia
    '''
    index = i
    if(index < len(listaTokens)):
        if debug :print 'arg',i,listaTokens[i]
        if(listaTokens[index][0] == "ID"):
            flag,index = arg2(index+1)
            if debug :print "retorno",flag,index,"arg"
            return flag,index
        elif(listaTokens[index][0]=="NUMERO"):
            flag,index = arg2(index+1)
            if debug :print "retorno",flag,index,"arg"
            return flag,index
        elif(listaTokens[index][0]=="VALOR_BOOL"):
            flag,index = arg2(index+1)
            if debug :print "retorno",flag,index,"arg"
            return flag,index
        else:
            if debug :print "arg-vazio",True
            return True,index-1
    else:
        if debug :print "arg-fim"
        return False,index
        
def arg2(i):
    '''    
    <arg2> ::= ,<arg>
            | palavra vazia
    '''    
    index = i
    if(index<len(listaTokens)):
        if debug :print 'arg2',i,listaTokens[i]
        if(listaTokens[index][0] == "VIRGULA"):
            flag,index = arg(index+1)
            if debug :print "retorno",flag,index,"arg2"
            return flag,index
        else:
            if debug :print "arg2-vazio",True
            return True,index-1
    else:
        if debug :print "arg2-fim"
        return False,index     

def declaProcedimento(i):
    """
    <declaProcedimento>::= ID<procedimento>
    """
    index = i    
    if(index < len(listaTokens)):
        if debug :print 'declaProcedimento',i,listaTokens[i]
        if(listaTokens[index][0] == 'ID'):
            flag,newIndex = declaracao(index+1)
            index = newIndex          
            if debug :print "retorno",flag,index,"declaProcedimento"  
            return flag,index
        else:
            if debug :print 'declaProcedimento-ID',False
            return False,index 
    else:
        if debug :print 'declaProcedimento-fim',False
        return False,index

def procedimento(i):
    '''
    <procedimento>::= ;<exprecao>
                    | (<param>){<expressao>}<expressao> 
    '''
    index = i
    
    if(index<len(listaTokens)):
        if debug :print 'procedimento',i,listaTokens[i]
        if(listaTokens[index][0] == 'PONTO_E_VIRGULA'):
            flag,newIndex = expressao(index+1)
            index=newIndex
            if debug :print "retorno",flag,index,"procedimento"
            return flag,index
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            flag,newIndex = param(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE' and 
                        listaTokens[index+2][0] == "ABRE_CHAVE"):
                
                flag,index = expressao(index+3)
                if(flag and listaTokens[index+1][0] == 'FECHA_CHAVE'):
                    
                    flag,newIndex = expressao(index+2)
                    index=newIndex
                    if debug :print "retorno",flag,index,"procedimeto"
                    return flag,index
                else:
                    if debug :print 'operacao-expressao_fecha_chave',False
                    return False,index
            else:
                if debug :print 'procedimento-fecha_parentese,abre_chave',False
                return False,index
        else:
            if debug :print 'procedimento-vazio',False
            return False,index    
    else:
        if debug :print 'procedimento-fim',False
        return False,index
   
def Print(i):  
    '''
    <print> ::= (<operacao>);<expressao>
    '''
    index = i  
    if(index<len(listaTokens)):
        if debug :print 'Print',i,listaTokens[i]
        if(listaTokens[index][0]=="ABRE_PARENTESE"):
            inicioPrint = index+1
            flag,index = operacao(index+1)
            if(resultadoCondicao):
                p = printExpressao("int", listaTokens[inicioPrint:index+1], escopoAtual["VARS"])
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" 
               and listaTokens[index+2][0] == "PONTO_E_VIRGULA"):
                if(resultadoCondicao):
                    global console
                    console.append(p)
                flag,index = expressao(index+3)
                if debug :print "retorno",flag,index,"print"
                return flag,index
            else:
                if debug :print "print-fecha parentese"
                return flag,index
    else:
        if debug :print "print-fim"
        return False,index

# flag,index =  expressao(0)

# print flag
















