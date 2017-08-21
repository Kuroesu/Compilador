import re
from estruturas import *


codigo = """int limite=30;
            bool valor = false;
            int var = 4- 2;
            bool func(int num,bool valor){
                if(num == 20){
                    return true;
                }
                if(num!=20 or valor){
                    return false;
                }    
            }
            int count=0;
            
            while(count< limite){
                count = count+1;
                valor =func(count);
            }
            """
            
detected_type = False 
            
tokenOrder = ["TIPO","IF","ELSE","WHILE","RETURN","NUMERO","VALOR_BOOL","ABRE_PARENTESE","FECHA_PARENTESE","ABRE_CHAVE",
              "FECHA_CHAVE","PONTO_E_VIRGULA","VIRGULA","BREAK","VOID","PRINT","CONTINUE","EXCLAMACAO","ATRIBUICAO","RETURN",
              "OP_BOOLEANO","OP_ARITMETICO","ID"]

tokensDict = {"TIPO" : r'(\bint\b)|(\bbool\b)|(\bvoid\b)',
          "IF" : r'\bif\b',
          "ELSE" : r'\belse\b',
          "WHILE" : r'\bwhile\b',
          'NUMERO' : r'\d+$',
          "VALOR_BOOL": r'(\btrue\b)|(\bfalse\b)',
          "ABRE_PARENTESE" : r'\($',
          "FECHA_PARENTESE": r'\)$',
          "ABRE_CHAVE":r'\{$',
          "FECHA_CHAVE":r'\}$',
          "PONTO_E_VIRGULA":r';$',
          "VIRGULA":r',$',
          "EXCLAMACAO":r'!$',
          "OP_BOOLEANO":r'(==$)|(>=$)|(<=$)| (!=$) |(<$)|(>$)|(or$)|(and$)',
          "OP_ARITMETICO":r'(\+$)|(-$)|(\*$)|(/$)|(%$)',
          "ATRIBUICAO":r'=',
          "VOID":r'\bvoid\b',
          "RETURN":r'\breturn\b',
          "BREAK":r'\bbreak\b',
          "CONTINUE":r'\bcontinue\b',
          "PRINT":r'\bprint\b',                
          "ID": r'\w'}


def analizarLex(fonte):
    tokenList = []
    
    lexemas = separaLexemas(fonte)#quebra a string separando os lexemas 
    
    linha = 1 # marca linha atual
    index = 0
    while(index < len(lexemas)):
        errLex = True; #lanca um erro caso o lexema n seja reconhecido
        if(lexemas[index] != '' and lexemas[index] != ' ' and len(lexemas[index])>0):
            
            if(lexemas[index] == '\n'):#conta a linha atual
                linha+=1    
            else:  
                for token in tokenOrder:#itera sobre as keys do dicionario 
              
                    expRegular = tokensDict[token]#seleciona a expressao regular
                    
                    if((lexemas[index] == '=') and (lexemas[index+1] == '=')):
                        tokenList.append(["OP_BOOLEANO",'=='])
                        index+=1     
                        errLex = False #nao chama o exeption
                        break
                    elif(lexemas[index] == '>' and lexemas[index+1] == '='):
                        tokenList.append(["OP_BOOLEANO",'>='])
                        index+=1
                        errLex = False #nao chama o exeption
                        break
                    elif(lexemas[index] == '<' and lexemas[index+1] == '='):        
                        tokenList.append(["OP_BOOLEANO",'<='])
                        index+=1
                        errLex = False #nao chama o exeption
                        break
                    elif(lexemas[index] == '!' and lexemas[index+1] == '='):
                        tokenList.append(["OP_BOOLEANO",'!='])
                        index+=1
                        errLex = False
                        break
                    else:
                        tk = re.match(expRegular,lexemas[index])#faz o match do lexema com a expressao regular
                        if(tk is not None):
                            
                            tokenList.append([token,lexemas[index]])#se reconhecer o lexema add na lista de tokens
                            if(token == "TIPO"):
                                global detected_type
                                tipoBuffer = ""
                                tipoBuffer = lexemas[index]
                                detected_type = True
                            if(token == "ID" and detected_type):
                                global detected_type
                                tabela_de_simbolos.append({"ID":lexemas[index],"TIPO":tipoBuffer})
                                detected_type = False    
 
                            errLex = False #nao chama o exeption
                            break
                         
                if(errLex):
                    for i in tokenList:
                        print i
                    raise Exception("erro ao indentificar o caracter",lexemas[index],"na linha",linha)
        index+=1      
                             
    return tokenList,tabela_de_simbolos    
   
def separaLexemas(fonte):
    lexemas = []
    #quebra a string separando os lexemas
    sliceFonte = re.split("([ *(^)*{^}*;*,*=*+*\-*>*<*!*/*\*])",fonte)
    for lex in sliceFonte:
        if(lex != '' and lex != ' ' and len(lex)>0):
            lexemas.append(lex)
    return lexemas
    
     
            
# token = re.match(r'\breturn\b','ret')
# print token
# if(token != None):
#     print "detectado"
# else:    
#     print "ERRO"
    
# a,tab = analizarLex(codigo)

# print a
# for i in a:
#     print i   







