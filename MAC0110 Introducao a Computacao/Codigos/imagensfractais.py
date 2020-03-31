# Esse script deve ser rodado no terminal,
# com a saída redirecionada para um arquivo PNM,
# usando a sintaxe: python3 imagensfractais.py > imagemNN.pnm

# escolha um dos exemplos entre 0 e 12
exemplo = 0
assert exemplo in range(13)

# escolha uma densidade para a imagem:
# quanto maior, mais resolução e também mais tempo de processamento.
N = 100

# Exemplos com imagens, método de Newton e Fractais

#### Nos exemplos a seguir veremos como adaptar o código da função gráfico, que gerava imagens ASCII com '*'s e ' 's, para gerar imagens PNM, e depois explorar algumas aplicações envolvendo métodos numéricos aplicados no plano complexo, observando a convergência do método de Newton para raízes do número 1 e também o uso de iteradores para a construção do conjunto de Mandelbrot e variantes. Os detalhes do formato PNM podem ser vistos na página [Formato Netpbm](https://en.wikipedia.org/wiki/Netpbm_format).

## A função abaixo é a adaptação da função gráfico vista em aula:

def imagem(X1,X2,Y1,Y2,M,N,padrão,expressão):
    """ Gera uma imagem percorrendo o retângulo [X1,X2)x[Y1,Y2)
        discretizado com M pontos na largura e N pontos na altura,
        avaliando uma expressão que determina a cor do pixel (x,y).
        A string padrão ("RGB" ou "cinza") determina se a imagem
        será em níveis de cinza ou colorida.
    """

    # gera o cabeçalho do arquivo PNM (=PBM, PGM ou PPM)
    if padrão=="RGB": print("P3")
    else: print("P2")
    print(M,N)
    print(255)
    
    # o laço externo percorre os valores de Y em ordem decrescente
    for n in range(N):
        y = Y2-n*(Y2-Y1)/N

        # o laço interno percorre os valores de X em ordem crescente
        for m in range(M):
            x = X1+m*(X2-X1)/M

            # imprime o pixel correspondente
            print(eval(expressão),end=" ")
            
        # pula a linha para o próximo valor de y
        print("")

#### Essa função pode ser usada para computar imagens parecidas com aquelas que vimos em aula, porém ela nos oferece mais recursos, permitindo a geração não somente de imagens em preto-e-branco, mas também em níveis de cinza e coloridas no padrão RGB. Como exemplo de adaptação de um dos exemplos vistos em aula, a chamada a seguir produz uma imagem em que o gráfico da função y=x**3-x é "esfumaçado":

if exemplo==0:
    imagem(-2,2,-4,4,N,N,"cinza","round(255*(1-abs(y-x**3+x)/14)**10)")
#![Exemplo 0](exemplo0.jpg)
    
## Raízes complexas da unidade

#### Chamamos de raíz complexa da unidade um número complexo z que satisfaz uma equação da forma $z^k=1$. Nos $z$ reais, para qualquer $k$ inteiro as únicas soluções possíveis para essa equação são $z=+1$ (para qualquer $k$) e $z=-1$ (para $k$ ímpar). Quando $z=x+yi$ (onde $i=\sqrt{-1}$) a situação fica muito mais interessante, como veremos a seguir. Desse ponto em diante, usaremos nosso plano $(x,y)$ como um plano complexo $x+yi$.

#### Antes de mais nada, vamos definir o método de Newton, que vimos pela primeira vez como método iterativo para calcular a raiz quadrada de um número real positivo. Numa forma um pouco mais geral, ele serve para calcular raízes de funções, ou seja, pontos $z$ que satisfazem $f(z)=0$. A iteração de Newton tem a forma $z_{n+1}=z_n-\frac{f(z_n)}{f'(z_n)}$, que pode ser calculada a partir de um $z_0$ qualquer _desde que $f'(z_n)\neq 0$_ em todas as iterações. Essa iteração corresponde a encontrar a raiz da linearização da função $f(\cdot)$ calculada no ponto $z=z_n$, como ilustra a figura abaixo.

#![Método de Newton](NewtonIteration_Ani.gif)

def Newton(z0,função,derivada):
    """ Calcula a raiz de uma função f(z) de uma variável complexa z
        a partir de z0 (=x+y*1j) pelo método de Newton, devolvendo uma
        estimativa da raiz (z) e o número de iterações (k) do método.
        As strings função e derivada contém as representações analíticas
        de f(z) e f'(z). O método usa tolerância de 1e-8 para a parada e
        um limite de 255 iterações. Caso f'(z)=0 em algum momento, o
        método para e devolve z = 0 e k = maxiter.        
    """
    eps = 1e-8
    maxiter = 255

    # inicialização do método
    z = z0
    # testa viabilidade da iteração de Newton (f'(z)!=0)
    if abs(eval(derivada))<eps: return 0,maxiter
    # aplica o passo de Newton a partir de z0
    z = z0-eval(função)/eval(derivada)

    k=1 # contador de iterações
    while abs(z-z0)>eps and k<maxiter:
        z0 = z # guarda iterado anterior
        if abs(eval(derivada))<eps: return 0,maxiter # testa viabilidade
        z = z0-eval(função)/eval(derivada) # aplica o passo de Newton
        k += 1 # mais uma iteração
    return z,k

## Mapa de cinzas:

#### A função a seguir vai facilitar a geração das cores dos pixels, fazendo uma regrinha de três simples para mapear um valor $f\in[f_\min,f_\max]$ em um valor inteiro entre 0 e 255, compatível com os pixels das imagens em nível de cinza.

def mapadecinzas(f,fmin,fmax):
    """ Converte o valor f (teoricamente entre fmin e fmax) em uma
        representação de um pixel no modelo "cinza", cuidando para que
        os valores produzidos sejam sempre inteiros entre 0 e 255.
    """
    # faz um mapeamento linear do valor f em [fmin,fmax] no intervalo [0,1]
    x = (f-fmin)/(fmax-fmin)
    # cuida do caso em que f não estava no intervalo
    if x<0: x = 0
    if x>1: x = 1
    # leva para o intervalo [0,255]
    pix = round(255*x)
    return pix

## Primeiro exemplo de aplicação do método de Newton: $\sqrt{1}$

#### Nesse primeiro exemplo didático, usaremos o método de Newton para calcular $\sqrt{1}$ a partir de um ponto inicial complexo genérico (dentro de um retângulo dado). Sabemos que as únicas raízes quadradas de 1 são -1 e +1, mas o exemplo serve para mais do que reconfirmar isso: ele mostrará quais são os pontos iniciais que conduzem o método de Newton para a raiz -1 e quais pontos iniciais conduzem o método para a raiz +1.

def exemplo1(x,y):
    """ Calcula uma raiz quadrada de 1 pelo método de Newton
        a partir do ponto inicial z0=x+yi.
        Usada como expressão na função imagem.
    """
    função = "z**2-1"
    derivada = "2*z"
    z,k = Newton(x+y*1j,função,derivada)
    fmin, fmax = -1, +1 # limites dos valores encontrados
    pix = mapadecinzas(z.real,fmin,fmax)
    return pix

if exemplo==1:
    imagem(-1.5,1.5,-1.5,1.5,N,N,"cinza","exemplo1(x,y)")
#![Exemplo 1](exemplo1.jpg)

#### Essa é uma imagem fácil de interpretar: todos os pontos z=x+yi com x>0 levam à raiz z=+1, e todos os pontos com x<0 levam à raiz z=-1. Talvez seja possível observar uma linha vertical cinza separando os dois hemisférios: para pontos com x=0 o método não converge, pois todos os iterados possuem também x=0.

#### Uma informação adicional interessante pode ser obtida ao se incluir na imagem a informação do número de iterações que o método levou para terminar. Usando um fator $2^\frac{-k}{10}$ para alterar a tonalidade do preto ou do branco (em direção a um tom intermediário) podemos ver que quanto mais longe estiver o ponto inicial está da raiz, mais lenta será a convergência do método:

def exemplo2(x,y):
    """ Calcula uma raiz quadrada de 1 pelo método de Newton
        a partir do ponto inicial z0=x+yi.
        Usada como expressão na função imagem.
    """
    função = "z**2-1"
    derivada = "2*z"
    z,k = Newton(x+y*1j,função,derivada)
    fmin, fmax = -1, +1 # limites dos valores encontrados
    pix = mapadecinzas(z.real*2**(-k/10),fmin,fmax)
    return pix

if exemplo==2:
    imagem(-1.5,1.5,-1.5,1.5,N,N,"cinza","exemplo2(x,y)")
#![Exemplo 2](exemplo2.jpg)

## Exemplos coloridos:

#### Os próximos exemplos gerarão imagens em cores, e para isso criaremos um mapeamento específico para o padrão RGB, que leva o intervalo $[f_\min,f_\max]$ numa sequência de cores, começando em vermelho e passando por amarelo, verde, ciano, azul, magenta e terminando em vermelho de novo. Esse mapeamento "circular" será adotado para permitir a codificação dos ângulos dos números complexos, que estão entre $[-\pi,+\pi]$ mas cujas extremidades correspondem à mesma direção no plano complexo (o eixo que vai do 0 em direção aos números negativos).

def mapadecores(f,fmin,fmax,a):
    """ Converte o valor f (teoricamente entre fmin e fmax) em uma
        representação de um pixel em um espaço de cor "RGB".
        O parâmetro a é usado para escurecer a cor no modelo "RGB".
    """
    # mapeia o valor f em [fmin,fmax] no intervalo [0,1]
    x = (f-fmin)/(fmax-fmin)
    if x<0: x=0
    if x>1: x=1
    # localiza esse número em um espaço RGB por interpolação
    # linear, a partir dos pontos de controle:
    # 0 = R, 0.16 = R+G, 0.33 = G, 0.5 = G+B, 0.66 = B, 0.83 = B+R, 1 = R
    R = round(a*255*min(1,max(0,2-6*x,6*x-4)))
    G = round(a*255*max(0,min(1,4-6*x,6*x)))
    B = round(a*255*max(0,min(1,6-6*x,6*x-2)))
    return str(R)+" "+str(G)+" "+str(B)

# traz da biblioteca cmath a constante pi e a função que obtém o ângulo de um número complexo
from cmath import pi,phase

## O exemplo a seguir calcula as raízes quartas da unidade ($\sqrt[4]{1}$) usando o método de Newton. Além de $z=+1$ e $z=-1$, podemos observar que nesse caso os valores $z=i$ e $z=-i$ também são soluções de $z^4=1$, já que $i^2=-1$ e portanto $i^4=(-1)^2=1$ e $(-i)^4=(-1)^4*i^4=1$. Usaremos como mapeamento o ângulo da solução alcançada, onde poderemos ver claramente quais pontos do plano conduzem o método de Newton para as raízes +1, +i, -1 e -i.

def exemplo3(x,y):
    """ Calcula raízes quartas de 1.
    """
    função = "z**4-1"
    derivada = "4*z**3"
    z,k = Newton(x+y*1j,função,derivada)
    fmin, fmax = -pi, +pi
    pix = mapadecores(phase(z),fmin,fmax,1) # usa a=1 para não considerar o k
    return pix

if exemplo==3:
    imagem(-1.5,1.5,-1.5,1.5,N,N,"RGB","exemplo3(x,y)")
#![Exemplo 3](exemplo3.jpg)

#### Como vemos, algo de muito mais complexo ocorre nas fronteiras entre as regiões de convergência do método: para os pontos próximos de +1, +i, -1 e -i o método sempre converge para a raiz correspondente, porém para pontos próximos às duas diagonais um fenômeno novo ocorre. Há microrregiões nas diagonais que conduzem o método a todas as demais raízes, e o padrão dessas microrregiões é bastante complexo, com características de autosimilaridade, pois os mesmos padrões aparecem encaixados uns nos outros, e uma espécie de recursividade nos padrões que leva a níveis infinitesimalmente pequenos de detalhes. Tais propriedades são típicas dos objetos conhecidos como fractais.

#### Repetindo o exemplo anterior, mas usando o número de iterações como "profundidade de cor":
    
def exemplo4(x,y):
    """ calcula raízes quartas de 1, atribuindo profundidade de cor aos pixels
        conforme o número de iterações até a convergência do método de Newton.
    """
    função = "z**4-1"
    derivada = "4*z**3"
    z,k = Newton(x+y*1j,função,derivada)
    fmin, fmax = -pi, +pi
    pix = mapadecores(phase(z),fmin,fmax,2**(-k/10))
    return pix

if exemplo==4:
    imagem(-1.5,1.5,-1.5,1.5,N,N,"RGB","exemplo4(x,y)")
#![Exemplo 4](exemplo4.jpg)

## Raízes nonas da unidade:
    
#### O próximo exemplo ilustra a convergência do método de Newton para as raízes nonas de 1, ou seja, para as soluções da equação $z=\sqrt[9]{1}$. Aqui seria necessário um pouco de análise complexa para entender a forma geral da solução, que tem como representação polar a expressão $z_n=e^{i2\pi n/9}$, ou ainda a representação Cartesiana $z_n=\cos(2\pi n/9)+i\mbox{sen}(2\pi n/9)$. Essa última forma deve permitir a interpretação das diversas regiões que aparecem no gráfico.
    
def exemplo5(x,y):
    """ Calcula raízes nonas de 1, relacionando
        o número de iterações à profundidade de cor.
    """
    função = "z**9-1"
    derivada = "9*z**8"
    z,k = Newton(x+y*1j,função,derivada)
    fmin, fmax = -pi, +pi
    pix = mapadecores(phase(z),fmin,fmax,2**(-k/10))
    return pix

if exemplo==5:
    imagem(-1.5,1.5,-1.5,1.5,N,N,"RGB","exemplo5(x,y)")
#![Exemplo 5](exemplo5.jpg)

#### Alguns recortes menores da imagem anterior, ilustrando a fractalidade:

if exemplo==6:
    imagem(0.5,1.0,1.0,1.5,N,N,"RGB","exemplo5(x,y)")
#![Exemplo 6](exemplo6.jpg)

if exemplo==7:
    imagem(0.75,0.875,1.25,1.375,N,N,"RGB","exemplo5(x,y)")
#![Exemplo 7](exemplo7.jpg)

## Conjunto de Mandelbrot

#### Um outro exemplo muito conhecido de fractal é obtido por um mecanismo similar, ainda que mais simples, das iterações do método de Newton vistas nos últimos exemplos. Nesse caso uma única iteração é repetida a partir de um ponto inicial, a fim de testar se a sequência gerada permanece limitada numa região pequena próxima da origem, ou se a sequência sai dessa região, o que determinaria a sua divergência. O operador de Mandelbrot é o mapa $z_{n+1}=z_n^2+z_0$, aplicado a partir de $z_0=0$. Isso gera a sequência $z_0, z_0^2+z_0, (z_0^2+z_0)^2+z_0 = z_0^4+2z_0^3+z_0^2+z_0, \ldots$.

#### A função a seguir aplica um iterador genérico a partir de $z_0$ enquanto a condição for satisfeita, devolvendo o número de iterações:

def itera(z0,iterador,condição):
    """ Aplica o iterador a partir de z0 e enquanto satisfizer a condição.
        Devolve o índice da iteração que violou a condição, ou maxiter
        se a condição não foi violada até esse limite de iterações.
    """
    maxiter = 255 # se chegar nesse número de iterações, interrompe a sequência.
    z = z0 # ponto inicial
    k = 0 # contador de iterações
    while eval(condição) and k<maxiter:
        z = eval(iterador)
        k += 1
    return k

#### Aplica o iterador de Mandelbrot a partir dos pontos z0=x+yi no plano (x,y)

def exemplo8(x,y):
    """ Aplica iterador "z**2+z0" com z0 = x+y*1j, testando quantas
        iterações leva até a sequência sair do círculo de raio 2.
    """
    z0 = x+y*1j
    iterador = "z**2+z0"
    condição = "abs(z)<=2"
    k = itera(z0,iterador,condição)
    fmin, fmax = 0, (255**0.5)*6/4 # força o mapeamento entre vermelho e azul
    pix = mapadecores(k**0.5,fmin,fmax,1)
    return pix

#### Gera o conjunto de Mandelbrot e vários recortes:

if exemplo==8:
    imagem(-2,1.5,-1.5,1.5,N,N,"RGB","exemplo8(x,y)")
#![Exemplo 8](exemplo8.jpg)
if exemplo==9:
    imagem(-2,-0.5,-0.75,0.75,N,N,"RGB","exemplo8(x,y)")
#![Exemplo 9](exemplo9.jpg)
if exemplo==10:
    imagem(-2,-1.25,-0.375,0.375,N,N,"RGB","exemplo8(x,y)")
#![Exemplo 10](exemplo10.jpg)
if exemplo==11:
    imagem(-1.82,-1.72,-0.05,0.05,N,N,"RGB","exemplo8(x,y)")
#![Exemplo 11](exemplo11.jpg)
if exemplo==12:
    imagem(-0.65,-0.4,0.45,0.7,N,N,"RGB","exemplo8(x,y)")
#![Exemplo 12](exemplo12.jpg)

## O argumento a seguir explica por que a sequência necessariamente diverge quando algum iterado sai do círculo de raio 2.

## Teorema: se $|z|>2$ e $|c|\le 2$ então a sequência de Mandelbrot diverge.
####
#### Note que se $|z| > 2$ e $|c|\le 2$ entao existe um $\varepsilon>0$ (e <1)
#### tal que $|c| < (1-\varepsilon)*|z|$, logo
####
####     $|z^2+c| \ge |z^2|-|c|$ (desigualdade triangular)
####             $>  2*|z|-(1-\varepsilon)*|z|$
####             $=  (1+\varepsilon)*|z|$
####          
#### Além disso a propriedade acima é preservada pelo iterador:
####
####     $(1-\varepsilon)*|z^2+c| > (1-\varepsilon)*(1+\varepsilon)*|z|$
####                     $= (1-\varepsilon^2)*|z|$
####                     $> (1-\varepsilon)*|z|$         (pois $\varepsilon<1$)
####                     $> |c|$
####
#### o que permite afirmar que $|z(k)| > (1+\varepsilon)^k|z(0)|$
#### de onde a sequência diverge sempre que $|z|>2$.
