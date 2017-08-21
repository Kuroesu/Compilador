from estruturas import *
debug = False

def analizarLoop(expressao,escopo):
    resultado = analizarExpressao("bool", expressao, escopo["VARS"])

def analizarSemantico(resultadoSintatico,codigo):
    if(resultadoSintatico):
        print "sintatico OK"
        print "---escopo__GLOBAL---"
        for ID,ATR in funcaoGlobal.items():
            if(ID == "ESCOPO"):
                print ID,":"
                for escopo in ATR:
                    print "    ",escopo
            else:        
                print ID,ATR
        print ">>>>CONSOLE<<<<"
        for linha in console:
            print ">>",linha        
    else:
        raise Exception("erro sixtaxe")
                            
def atualizarVar(ID,expressao,escopoAtual):
    varNaoDecla = True
    for var in escopoAtual:
        if(var["ID"] == ID):
            varNaoDecla = False
            var["VALOR"] = analizarExpressao(var["TIPO"], expressao, escopoAtual)
    if(varNaoDecla):
        raise Exception("variavel",var["ID"],"nao foi declarada")
                               
def declararVar(declaracao,escopoAtual):
#     print declaracao
    var = {}
    var["TIPO"] = declaracao[0][1]
    var["ID"] = declaracao[1][1]
    for varDecla in escopoAtual:
        if(var["ID"] == varDecla["ID"]):
            raise Exception("variavel",var["ID"],"ja declarada")

    if(declaracao[2][0] == "ATRIBUICAO"):
        var["VALOR"] = analizarExpressao(var["TIPO"],declaracao[3:-1],escopoAtual)
    else:
        var["VALOR"] = None
    return var        
            
def analizarExpressao(tipo, expressao, escopoVar):
    expr = ""
    temp = ""
    d = True
    for token in expressao:
        if(token[0] == "ID"):
            for var in escopoVar:
                if(var["ID"] == token[1]):  
                    d = False         
                    if(var["TIPO"] == 'bool'):
                        temp = "%d" % var["VALOR"]
                        expr +=temp
                        if(debug):
                            print "temp:",temp
                            print "expr:",expr
                    else:
                        if(var["VALOR"] == None):
                            temp = "%d" % 0
                            expr +=temp
                            if(debug):
                                print "temp:",temp
                                print "expr:",expr
                        else:
                            temp = "%d" % var["VALOR"]
                            expr +=temp
                            if(debug):
                                print "temp:",temp
                                print "expr:",expr
            if(d):
                raise Exception("variavel",token[1],"nao declarada")               
        else:
            temp = "%s" % token[1]
            expr+=temp
            if(debug):
                print "@temp:",temp
                print "@expr:",expr
    print "-------------"           
    return eval(expr)

def printExpressao(tipo,expressao,escopoVar):
    expr = ""
    temp = ""
    d = True
    for token in expressao:
        if(token[0] == "ID"):
            for var in escopoVar:
                if(var["ID"] == token[1]):  
                    d = False         
                    if(var["TIPO"] == 'bool'):
                        temp = "%s" % var["VALOR"]
                        expr +=temp
                        if(debug):
                            if(debug):
                                print "temp:",temp
                                print "expr:",expr
                    else:
                        if(var["VALOR"] == None):
                            temp = "%d" % 0
                            expr +=temp
                            if(debug):
                                print "temp:",temp
                                print "expr:",expr
                        else:
                            temp = "%d" % var["VALOR"]
                            expr +=temp
                            if(debug):
                                print "temp:",temp
                                print "expr:",expr
            if(d):
                raise Exception("variavel",token[1],"nao declarada")
        elif(token[0] == "VALOR_BOOL"):
            if(token[1] == "true"):
                temp = "%d" % True
                expr+=temp
            else:
                temp = "%d" % False
                expr+=temp            
        else:
            temp = "%s" % token[1]
            expr+=temp
            if(debug):
                print "@temp:",temp
                print "@expr:",expr
    print "-------------"           
    return eval(expr)    
                
def analizarParametros(listaParam):
    params = []
    var = {}
    for token,lexema in listaParam:
        if(token == "VIRGULA" or token == "FECHA_PARENTESE"):
            var["VALOR"] = None
            params.append(var)
            var = {}
        else:    
            var[token] = lexema
    return params    
        
def analizarFuncao(declaracao,escopoAtual):
    #int func( int a)
    funcao = {"TIPO":"void",#tipo da funcao
               "PARAM":[],#lista de parametros
               "VARS":[],#lista de variaveis
               "FUNCS":[],#lista de funcoes
               "ESCOPO":[]}#arvore de escopos

    funcao["TIPO"] = declaracao[0]
    funcao["ID"] = declaracao[1]
    funcao["PARAM"] = analizarParametros(declaracao[2:])
    
 



