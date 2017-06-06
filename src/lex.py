import re

codigo = "int nome = 20;"

tokens = ["ID","NUMERO"
          "ABRE_PARENTESE","FECHA_PARENTESE",
          "ABRE_CHAVE,FECHA_CHAVE"
          "IF","WHILE",
          "PONTO_E_VIRGULA","VIRGULA",
          "EXCLAMACAO",
          "ARITMETICO","BOLEANO",
          "TIPO",]

def numero(lexema):
    token = re.match(r'\d+',lexema)
    if(token!= None):
        return "NUMERO"
    else:
        return "ERRO"
    
def tipo(lexema):
    token1 = re.match(r'\bint\b',lexema)
    token2 = re.match(r'\bbool\b',lexema)
    if(token1!= None or token2!=None):
        return "TIPO"
    else:
        return "ERRO"
    
def id(lexema):
    token = re.match(r'\D\w',lexema)
    if(token!= None ):
        return "ID"
    else:
        return "ERRO"
         
def abre_parentese(lexema):
    token = re.match(r'\b\(\b',lexema)
    if(token!= None ):
        return "ABRE_PARENTESE"
    else:
        return "ERRO"    

def fecha_parentese(lexema):
    token = re.match(r'\b\)\b',lexema)
    if(token!= None ):
        return "FECHA_PARENTESE"
    else:
        return "ERRO"

def abre_chave(lexema):
    token = re.match(r'\b\{\b',lexema)
    if(token!= None ):
        return "ABRE_CHAVE"
    else:
        return "ERRO"
    
def fecha_chave(lexema):        
    token = re.match(r'\b\}\b',lexema)
    if(token!= None ):
        return "FECHA_CHAVE"
    else:
        return "ERRO"

def ponto_e_virgula(lexema):
    token1 = re.match(r'\b;\b',lexema)
    if(token1!= None ):
        return "PONTO_E_VIRGULA"
    else:
        return "ERRO"

def virgula(lexema):
    token1 = re.match(r'\b,\b',lexema)
    if(token1!= None ):
        return "VIRGULA"
    else:
        return "ERRO"

def exclamacao(lexema):
    token1 = re.match(r'\b!\b',lexema)
    if(token1!= None ):
        return "EXCLAMACAO"
    else:
        return "ERRO"

def aritmetico(lexema):
    token1 = re.match(r"""(\b\+\b)|(\b-\b)|(\b\*\b)|
                          (\b\\\b)|
                          (\b=\b)|
                          (\b%\b)""",lexema)
    if(token1!= None ):
        return "ARITMETICO"
    else:
        return "ERRO"

lexema = "+"
    
print aritmetico(lexema)   







