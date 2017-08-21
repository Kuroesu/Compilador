

funcaoGlobal = {"ESCOPO_PAI":None,
                "TIPO":"void",#tipo da funcao
                "PARAM":[],#lista de parametros
                "VARS":[],#lista de variaveis
                "FUNCS":[],#lista de funcoes
                "ESCOPO":[]}#arvore de escopos
                   

varGenerica = {"ID":"",
               "TIPO":"",
               "VALOR":None}

# exprGenrerica = {"TIPO":"",
#                  "OPERACAO":[]}

escopoGenerico = {"ESCOPO_PAI":None,
                  "TIPO":"",
                  "EXPRESSOES":[],#lista de expressoes
                  "VARS":[],
                  "ESCOPO":[]}

                                                       
escopoAnterior = []
escopoAtual = []
lista_de_funcoes = []
listaTokens = []
tabela_de_simbolos = []
console = []

