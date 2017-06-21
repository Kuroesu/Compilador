import re

codigo = """int limite=30;
            bool valor = false;
            int var = 4 / 2;
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
            
tokenOrder = ["TIPO","IF","WHILE","RETURN","NUMERO","VALOR_BOOL","ABRE_PARENTESE","FECHA_PARENTESE","ABRE_CHAVE",
              "FECHA_CHAVE","PONTO_E_VIRGULA","VIRGULA","EXCLAMACAO","OP_BOOLEANO","OP_ARITMETICO","ID"]

tokensDict = {"TIPO" : r'(\bint\b)|(\bbool\b)',
          "IF" : r'\bif\b',
          "WHILE" : r'\bwhile\b',
          'NUMERO' : r'\d+',
          "VALOR_BOOL": r'(\btrue\b)|(\bfalse\b)',
          "ABRE_PARENTESE" : r'\($',
          "FECHA_PARENTESE": r'\)$',
          "ABRE_CHAVE":r'\{$',
          "FECHA_CHAVE":r'\}$',
          "PONTO_E_VIRGULA":r';$',
          "VIRGULA":r',$',
          "EXCLAMACAO":r'!$',
          "OP_BOOLEANO":r'(==$)|(>=$)|(<=$)|(<$)|(>$)|(or$)|(and$)',
          "OP_ARITMETICO":r'(\+$)|(-$)|(\*$)|(/$)|(=$)|(%$)',
          "RETURN":r'\breturn\b',                
          "ID": r'\D\w'}


def analizarLex(fonte):
    tokenList = []
    #quebra a string separando os lexemas
    lexemas = separaLexemas(fonte) 
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
                        break;
                    elif(lexemas[index] == '<' and lexemas[index+1] == '='):        
                        tokenList.append(["OP_BOOLEANO",'<='])
                        index+=1
                        errLex = False #nao chama o exeption
                        break;
                    else:
                        tk = re.match(expRegular,lexemas[index])#faz o match do lexema com a expressao regular
                        if(tk is not None):
                            tokenList.append([token,lexemas[index]])#se reconhecer o lexema add na lista de tokens
                            errLex = False #nao chama o exeption
                            break
                         
                if(errLex):
                    for i in tokenList:
                        print i 
                    raise Exception("erro ao indentificar o caracter",lexemas[index],"na linha",linha)
        index+=1      
              
    for i in tokenList:
        print i                
    return tokenList    
   
def separaLexemas(fonte):
    lexemas = []
    #quebra a string separando os lexemas
    sliceFonte = re.split("([ *(^)*{^}*;*,*=*+*-*>*<*!*\\*\*])",fonte)
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
    
analizarLex(codigo)   







