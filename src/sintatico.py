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
tipo id = funcao(0)

"""
from webbrowser import Opera

codigo = '''
            if(a < 5){
                print(a);
            }else if(a){
                if(a){
                    print(a)
                }
            }
            '''    
#             int func(int a, bool valor){
#                 while(valor){
#                     int b = 3;
#                     int c = b+a;
#                     if(a<b){
#                         c = b-a;
#                         func(a,true,43,342,false);
#                     }
#                 }
#             }'''

listaTokens = analizarLex(codigo)
print listaTokens

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
        print 'expressao',tokenIndex,listaTokens[tokenIndex]
        
        #-----TIPO <declaracoes>
        if(listaTokens[index][0] == 'TIPO'):
            flag,newIndex = declaracoes(index+1)
            index=newIndex
            print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----if(<operacao>){<expressao>}<expressao>
        elif(listaTokens[index][0] == 'IF' and listaTokens[index+1][0]=='ABRE_PARENTESE'):
            flag,newIndex = operacao(index+2)
            index = newIndex
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" and 
               listaTokens[index+2][0] == 'ABRE_CHAVE'):
                flag,newIndex = expressao(index+3)
                index = newIndex
                print "lalalal",listaTokens[index+1][0]
                if(flag and listaTokens[index+1][0] == "FECHA_CHAVE"):
                    flag,newIndex = Else(index+1)
                    index=newIndex
                    print "retorno",flag,index,"expressao"
                    return flag,index
                else:
                    print 'expresao-if-fecha_chave',True
                    return False,index
            else:
                print 'expresao-if-fecha_parentese',False
                return False,index    
            
        #-----while(<operacao>){<expressao>}<expressao>          
        elif(listaTokens[index][0] == 'WHILE' and listaTokens[index+1][0]=='ABRE_PARENTESE'):
            flag,newIndex = operacao(index+2)
            index = newIndex
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" and 
               listaTokens[index+2][0] == 'ABRE_CHAVE'):
                flag,newIndex = expressao(index+3)
                index=newIndex
                if(flag and listaTokens[index+1][0] == "FECHA_CHAVE"):
                    flag,newIndex = expressao(index+1)
                    print "retorno",flag,index,"expressao"
                    return flag,index
                else:
                    print 'expresao-while-fecha_chave',False
                    return False,index
                
        #-----ID<chamada>            
        elif(listaTokens[index][0] == 'ID'):
            flag,newIndex = chamada(index+1)
            index = newIndex
            return flag,index
        
        #-----void <procedimento> 
        elif(listaTokens[index][0] == "VOID"):
            flag,index = declaProcedimento(index+1)
            print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----print<print>
        elif(listaTokens[index][0] == "PRINT"):
            flag,index = Print(index+1)
            print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----break;<expressao>
        elif(listaTokens[index][0] == "BREAK" and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
            flag,index = expressao(index+2)
            print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----continue;<expressao> 
        elif(listaTokens[index][0] == "CONTINUE" and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
            flag,index = expressao(index+2)
            print "retorno",flag,index,"expressao"
            return flag,index
        
        #-----return <operacao>;<expressao>
        elif(listaTokens[index][0] == "RETURN"):
            flag,index=operacao(index+1)
            if(flag and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
                flag,index = expressao(index+2)
                print "retorno",flag,index,"expressao"
                return flag,index
            else:
                print "expressao-RETURN-ponto e virgula"
                return False,index
        #-----palavra vazia    
        else:
            print 'expresao-vazio',True
            print "retorno",True,index-1
            return True,index-1                    
    else:
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
        print 'expressao',index,listaTokens[index]
        if(listaTokens[index][0] == "ELSE"):
            flag,index= condicional(index+1)
            print "retorno",flag,index,"else"
            return flag,index
        else:
            flag,index = expressao(index)
            print "retorno",flag,index,"else"
            return flag,index
    else:
        print "else-fim"
        return flag,index
        
def condicional(i):
    '''
    <condicional> ::= (<operacao>){expressao}expressao    
                   |  if(<operacao>){<expressao>}<else>
    '''
    index=i
    if(index<len(listaTokens)):
        print 'expressao',index,listaTokens[index]
        #-----if(<operacao>){<expressao>}<else>
        if(listaTokens[index][0] == 'IF' and listaTokens[index+1][0]=='ABRE_PARENTESE'):
            flag,newIndex = operacao(index+2)
            index = newIndex
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" and 
               listaTokens[index+2][0] == 'ABRE_CHAVE'):
                flag,newIndex = expressao(index+3)
                index = newIndex
                
                if(flag and listaTokens[index+1][0] == "FECHA_CHAVE"):
                    flag,newIndex = Else(index+1)
                    index=newIndex
                    print "retorno",flag,index,"condicional"
                    return flag,index
                else:
                    print 'expresao-if-fecha_chave',True
                    return False,index
            else:
                print 'expresao-if-fecha_parentese',False
                return False,index 
            
        #-----(<operacao>){expressao}expressao 
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            flag,newIndex = arg(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE' and 
                        listaTokens[index+2][0] == "ABRE_CHAVE"):
                
                flag,index = expressao(index+3)
                if(flag and listaTokens[index+1][0] == 'FECHA_CHAVE'):
                    
                    flag,newIndex = expressao(index+2)
                    index=newIndex
                    print "retorno",flag,index,"condicional"
                    return flag,index
                else:
                    print 'operacao-expressao_fecha_chave',False
                    return False,index
            else:
                print 'declaracao-fecha_parentese,abre_chave',False
                return False,index   
    else:
        print "condicional-fim"
        return False,index                    
              
def declaracoes(i=0):
    """
    <declaracoes>::= ID<declaracao>
    """
    index = i    
    if(index < len(listaTokens)):
        print 'declaracoes',i,listaTokens[i]
        if(listaTokens[index][0] == 'ID'):
            flag,newIndex = declaracao(index+1)
            index = newIndex          
            print "retorno",flag,index,"declaracoes"  
            return flag,index
        else:
            print 'declaracoes-ID',False
            return False,index 
    else:
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
        print 'declaracao',i,listaTokens[i]
        if(listaTokens[index][0] == "ATRIBUICAO"):
            flag,newIndex = operacao(index+1)
            index = newIndex
            if(flag):
                flag,newIndex = declaracao(index+1)
                index=newIndex
                print "retorno",flag,index,"declaracao"
                return flag,index
            else:
                print 'declaracao->atribuicao',False
                return False,index
                
        elif(listaTokens[index][0] == 'PONTO_E_VIRGULA'):
            flag,newIndex = expressao(index+1)
            index=newIndex
            print "retorno",flag,index,"declaracao"
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
                    print "retorno",flag,index,"declaracao"
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
               
def operacao(i):
    """
    <operacao>::= (<operacao>)<op2>
                | ID+'<op_2>          
                | NUMERO<op_2> 
                | true    
                | false     
    """
    index=i
    if(index < len(listaTokens)):
        print 'operacao',i,listaTokens[i]
        if(listaTokens[index][0] == "NUMERO"): 
            flag,newIndex = op2(index+1)
            index = newIndex
            print "retorno",flag,index,"operacao"
            return flag,index
        elif(listaTokens[index][0] == "VALOR_BOOL"):
            print "retorno",True,index,"operacao"
            return True,index
        elif(listaTokens[index][0] == "ID"):
            flag,newIndex = op2(index+1)
            index = newIndex
            print "retorno",flag,index,"operacao"
            return flag,index
        elif(listaTokens[index][0] == 'ABRE_PARENTESE'):
            flag,newIndex = operacao(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == 'FECHA_PARENTESE'):
                flag,newIndex = op2(index+2)
                index = newIndex
                print "retorno",flag,index,"operacao"
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
            
def op2(i):
    """
    <op_2>::= <sinal><operacao> 
            | palavra vazia  

    """
    index=i
    if(index<len(listaTokens)):
        print 'op2',i,listaTokens[i]   
        if(listaTokens[index][0] == 'OP_ARITMETICO' or 
           listaTokens[index][0] == 'OP_BOOLEANO'):
            flag,newIndex=operacao(index+1)
            index=newIndex
            print "retorno",flag,index,"op2"
            return flag,index
        else:
            print 'op2->vazio',True
            print "retorno",True,index-1
            return True,index-1  
    else:
        print 'op2-fim'
        print "retorno",flag,index
        return True,index

def param(i):
    """
<param>::= TIPO ID<param2>
        | palavra vazia
    """
    print 'param',i,listaTokens[i] 
    index = i
    if(index < len(listaTokens)):
        if(listaTokens[index][0] == "TIPO"):
            print listaTokens[index+1]
            if(listaTokens[index+1][0] == "ID"):
                flag,newIndex = param2(index+2)
                index = newIndex
                print "retorno",flag,index,"param"
                return flag,index
            else: 
                print "param erro id"
                return False,index    
        else:
            print "retorno",True,index,"param"
            return True,index-1
    else:
        print "param-fim" 
        print "retorno",False,index   
        return False,index

def param2(i):
    """
    <param2> ::= ,<param>
                | palavra vazia

    """
    print 'param2',i,listaTokens[i] 
    index = i
    if(index < len(listaTokens)):
        if(listaTokens[index][0] == 'VIRGULA'):
            flag,newIndex = param(index+1)
            index=newIndex
            print "retorno",flag,index,"param2"
            return flag,index
        else:
            print "retorno",True,index,"param2"    
            return True,index-1
            
    else:
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
        print 'chamada',i,listaTokens[i]
        if(listaTokens[index][0] == "ABRE_PARENTESE"):
            flag,newIndex = arg(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" 
               and listaTokens[index+2][0] == "PONTO_E_VIRGULA"):
                flag,newIndex = expressao(index+3)
                index = newIndex
                print "retorno",flag,index,"chamada"
                return flag,index
            else:
                print "chamada fecha_parentese"
                return False,index
        elif(listaTokens[index][0] == "ATRIBUICAO"):
            flag,newIndex = operacao(index+1)
            index = newIndex
            if(flag and listaTokens[index+1][0] == "PONTO_E_VIRGULA"):
                flag,newIndex = expressao(index+2)
                index=newIndex
                print 'retorno',flag,index,"chamada"
                return flag,index
            else:
                print "chamada-ponto e virgula"
                return False,index
        else:
            print "chamada abre_parentese"
            return False,index
    else:
        print "chamada-fim"
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
        print 'arg',i,listaTokens[i]
        if(listaTokens[index][0] == "ID"):
            flag,index = arg2(index+1)
            print "retorno",flag,index,"arg"
            return flag,index
        elif(listaTokens[index][0]=="NUMERO"):
            flag,index = arg2(index+1)
            print "retorno",flag,index,"arg"
            return flag,index
        elif(listaTokens[index][0]=="VALOR_BOOL"):
            flag,index = arg2(index+1)
            print "retorno",flag,index,"arg"
            return flag,index
        else:
            print "arg-vazio",True
            return True,index-1
    else:
        print "arg-fim"
        return False,index
        
def arg2(i):
    '''    
    <arg2> ::= ,<arg>
            | palavra vazia
    '''    
    index = i
    if(index<len(listaTokens)):
        print 'arg2',i,listaTokens[i]
        if(listaTokens[index][0] == "VIRGULA"):
            flag,index = arg(index+1)
            print "retorno",flag,index,"arg2"
            return flag,index
        else:
            print "arg2-vazio",True
            return True,index-1
    else:
        print "arg2-fim"
        return False,index     

def declaProcedimento(i):
    """
    <declaProcedimento>::= ID<procedimento>
    """
    index = i    
    if(index < len(listaTokens)):
        print 'declaProcedimento',i,listaTokens[i]
        if(listaTokens[index][0] == 'ID'):
            flag,newIndex = declaracao(index+1)
            index = newIndex          
            print "retorno",flag,index,"declaProcedimento"  
            return flag,index
        else:
            print 'declaProcedimento-ID',False
            return False,index 
    else:
        print 'declaProcedimento-fim',False
        return False,index

def procedimento(i):
    '''
    <procedimento>::= ;<exprecao>
                    | (<param>){<expressao>}<expressao> 
    '''
    index = i
    
    if(index<len(listaTokens)):
        print 'procedimento',i,listaTokens[i]
        if(listaTokens[index][0] == 'PONTO_E_VIRGULA'):
            flag,newIndex = expressao(index+1)
            index=newIndex
            print "retorno",flag,index,"procedimento"
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
                    print "retorno",flag,index,"procedimeto"
                    return flag,index
                else:
                    print 'operacao-expressao_fecha_chave',False
                    return False,index
            else:
                print 'procedimento-fecha_parentese,abre_chave',False
                return False,index
        else:
            print 'procedimento-vazio',False
            return False,index    
    else:
        print 'procedimento-fim',False
        return False,index
   
def Print(i):  
    '''
    <print> ::= (<operacao>);<expressao>
    '''
    index = i  
    if(index<len(listaTokens)):
        print 'Print',i,listaTokens[i]
        if(listaTokens[index][0]=="ABRE_PARENTESE"):
            flag,index = operacao(index+1)
            if(flag and listaTokens[index+1][0] == "FECHA_PARENTESE" 
               and listaTokens[index+2][0] == "PONTO_E_VIRGULA"):
                flag,index = expressao(index+3)
                print "retorno",flag,index,"print"
                return flag,index
            else:
                print "print-fecha parentese"
                return flag,index
    else:
        print "print-fim"
        return False,index

flag,index =  expressao(0)

print flag
















