from lex import analizarLex 
"""
testado:
tipo id = id;
tipo id = id + numero;
tipo id = id + id;
tipo id = numero + id; 
tipo id = numero + numero;
tipo id = ((numero|id) + (numero|id))
tipo id = ((numero|id) + numero|id)

bug lex:
so indentifica id com mais de 1 caracter EX.: aa:aceita 
                                               a:rejeita
<sinal>: -,/ 
num<sinal>num: rejeita
num<sinal> num: rejeita
num <sinal>num: rejeita
num <sinal> num: aceita 
"""


codigo = 'int var = ((aa+bb)+cc+cc);'

def expressao(listaTokens,i=0):
    """
    <expressao>::= if(<operacao>){<expressao>}<expressao>  
                 | while(<operacao>){<expressao>}<expressao> 
                 | TIPO <declaracoes>  
                 | ID<chamada>
                 | palavra vazia
    """
    
    index = i
    if(index < len(listaTokens)):
        print 'exprecao',i,listaTokens[i]
        if(listaTokens[index][0] == 'TIPO'):
            flag,newIndex = declaracoes(listaTokens,index+1)
            index=newIndex
            return flag,index
        elif(listaTokens[index][0] == 'IF'):
            return False
        elif(listaTokens[index][0] == 'WHILE'):
            return False
        elif(listaTokens[index][0] == 'ID'):
            return False
        else:
            print 'expresao-vazio',True
            return True,index                    
    else:
        print 'expresao-fim',True
        return True,index    
      
def declaracoes(listaTokens,i=0):
    """
    <declaracoes>::= ID<declaracao>
    """
    index = i    
    if(index < len(listaTokens)):
        print 'declaracoes',i,listaTokens[i]
        if(listaTokens[index][0] == 'ID'):
            flag,newIndex = declaracao(listaTokens,index+1)
            index = newIndex            
            return flag,index
        else:
            print 'declaracoes-ID',False
            return False,index 
    else:
        print 'declaracoes-fim',False
        return False,index
        
def declaracao(listaTokens,i):
    """
    <declaracao>::= (<param>){<expressao>}<expressao>
                 | ;<exprecao> 
                | =<operacao><declaracao> 

    """
    index = i
    if(index < len(listaTokens)):
        print 'declaracao',i,listaTokens[i]
        if(listaTokens[index][1] == "="):
            flag,newIndex = operacao(listaTokens,index+1)
            index = newIndex
            if(flag):
                flag,i = declaracao(listaTokens,index+1)
                index=newIndex
                return flag,index
            else:
                print 'declaracao->atribuicao',False
                return False,index
                
        elif(listaTokens[index][0] == 'PONTO_E_VIRGULA'):
            flag,newIndex = expressao(listaTokens[index+1:])
            index=newIndex
            return flag,index
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            flag,newIndex = param(listaTokens,index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE' and 
                        listaTokens[index+2][0] == "ABRE_CHAVE"):
                
                flag,index = expressao(listaTokens,index+3)
                if(flag and listaTokens[index+1][0] == 'FECHA_CHAVE'):
                    
                    flag,newIndex = expressao(listaTokens,index+1)
                    index=newIndex
                    return flag,index
                else:
                    print 'operacao-expressao_fecha_chave',False
                    return False,index
            else:
                print 'declaracao-fecha_parentese,abre_chave',False
                return False,index
        else:
            print 'declaracao-vasio',False
            return False,index    
    else:
        print 'declaracao-fim',False
        return False,index
               
def operacao(listaTokens,i):
    """
    <operacao>::= (<operacao>) <op2>
                | ID+'<op_2>          
                | NUMERO<op_2> 
                | true    
                | false     
    """
    index=i
    if(index < len(listaTokens)):
        print 'operacao',i,listaTokens[i]
        if(listaTokens[index][0] == "NUMERO"): 
            flag,newIndex = op2(listaTokens,index+1)
            index = newIndex
            return flag,index
        elif(listaTokens[index][0] == "VALOR_BOOL"):
            return True,index
        elif(listaTokens[index][0] == "ID"):
            flag,newIndex = op2(listaTokens,index+1)
            index = newIndex
            return flag,index
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            flag,newIndex = operacao(listaTokens,index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE'):
                flag,newIndex = op2(listaTokens, index+2)
                index = newIndex
                return flag,index
            else:
                print 'operacao-fecha_parentese',False
                return False,index
        else:
            print 'operacao-vazio',False
            return False,index
    else:
        print 'operacao-fim',False
        return False,index
            
def op2(listaTokens,i):
    """
    <op_2>::= <sinal><operacao> 
            | palavra vazia  

    """
    index=i
    if(index<len(listaTokens)):
        print 'op2',i,listaTokens[i]   
        if(listaTokens[index][0] == 'OP_ARITMETICO' or 
           listaTokens[index][0] == 'OP_BOOLEANO'):
            flag,newIndex=operacao(listaTokens,index+1)
            index=newIndex
            return flag,index
        else:
            print 'op2->vazio',True
            return True,index-1  
    else:
        print 'op2-fim',True
        return True,index

def param(listaTokens,i):
    """
    <param>::= <Variavel><param> 
             | palavra vazia 
    """
    index = i
    return True,index
    
      
listaTokens = analizarLex(codigo)
flag,index =  expressao(listaTokens)

print flag