from sintatico import analizarSintaxe
from semantico import analizarSemantico
'''
declaracao de variavel com e sem atribuicao
atualizacao de variavel

erro de tipo
erro de variavel nao declarada e ja declarada

'''
            
codigo = ''' 
           
            bool z = 7>=9;
            print(2+true);
            if(z){
                int a = 2;
                print(a);
            }else{
                int a = 4;
                print(a);
            }
            '''

result = analizarSintaxe(codigo)
analizarSemantico(result,codigo)