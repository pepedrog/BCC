#lang plai-typed

#|
 | Funções simples
 | Um único argumento, que será representado por um symbol
 |
 |#

; Novo tipo, com funções.
; Precisamos de duas novas entradas: 
;     - identificador, para argumentos
;     - aplicação da função
(define-type ExprC
  [numC (n : number)]
  [idC  (s : symbol)]  ; identificador
  [appC (fun : symbol) (arg : ExprC)] ; aplicação, com o nome da função e o valor do argumento
  [plusC (l : ExprC) (r : ExprC)]
  [multC (l : ExprC) (r : ExprC)]
  [ifC   (condição : ExprC) (sim : ExprC) (não : ExprC)]
  )

; definição de função com 1 argumento
(define-type FunDefC
  [fdC (name : symbol) (arg : symbol) (body : ExprC)]
  )


; inclui funções
(define-type ExprS
  [numS    (n : number)]
  [idS     (s : symbol)] 
  [appS    (fun : symbol) (arg : ExprS)] 
  [plusS   (l : ExprS) (r : ExprS)]
  [bminusS (l : ExprS) (r : ExprS)]
  [uminusS (e : ExprS)]
  [multS   (l : ExprS) (r : ExprS)]
  [ifS     (c : ExprS) (s : ExprS) (n : ExprS)]
  )

; agora é preciso arrumar desugar interpretador e parser.

(define (desugar [as : ExprS]) : ExprC  
  (type-case ExprS as
    [numS    (n) (numC n)]
    [idS     (s) (idC s)] ; este é fácil
    [appS    (fun arg) (appC fun (desugar arg))] ; fun é um symbol, não precisa de desugar 
    [plusS   (l r) (plusC (desugar l) (desugar r))] 
    [multS   (l r) (multC (desugar l) (desugar r))]
    [bminusS (l r) (plusC (desugar l) (multC (numC -1) (desugar r)))]
    [uminusS (e)   (multC (numC -1) (desugar e))]
    [ifS     (c s n) (ifC (desugar c) (desugar s) (desugar n))]
    ))


#|
 | O interpretador precisa tratar de substituir o parâmetro pelo valor!
 | Além disso, precisa receber as definições de funções (uma lista)
 | Será necessário procurar a função na lista:
 |
 |       get-fundef : symbol * (listof FunDefC) -> FunDefC
 |
 | e fazer substituição dos symbols
 |
 |       subst : ExprC * symbol * ExprC -> ExprC
 |
 |#


; começamos pela última
; subst :  ExprC * symbol * ExprC -> ExprC
; ou (subst VALOR ID EXPRESSÃO)
; Vou manter a ordem do livro, mas vou mudar o nome dos argumentos:
; subst substitui ISSO por VALOR em EM
(define (subst [valor : ExprC] [isso : symbol] [em : ExprC]) : ExprC
  (type-case ExprC em
    [numC (n) em]   ; nada a substituir, repassa
    [idC (s) (cond  ; poderia ser 'if', mas existem coisas no futuro...
               [(symbol=? s isso) valor] ; símbolo, troque
               [else em])] ; deixa quieto
    [appC  (f a) (appC f (subst valor isso a))] ; chamada de função 
		   	  	 	   	; arruma o argumento
    [plusC (l r) (plusC (subst valor isso l) (subst valor isso r))]
    [multC (l r) (multC (subst valor isso l) (subst valor isso r))]
    [ifC (c s n) (ifC   (subst valor isso c) 
			(subst valor isso s) (subst valor isso n))]
  ))

; Agora o interpretador!

(define (interp [a : ExprC] [fds : (listof FunDefC)]) : number
  (type-case ExprC a
    [numC (n) n]
    ; Aplicação de função é que precisa de subst
    [appC (f a) 
          (local ([define fd (get-fundef f fds)]) ; pega a definição em fd
            (interp (subst a                 ; interpreta o resultado de subst
                           (fdC-arg fd)
                           (fdC-body fd)
                           )
                    fds))]
    ; Não devem sobrar idenficadores livres na expressão
    [idC (_) (error 'interp "não deveria encontrar isso!")]
    [plusC (l r) (+ (interp l fds) (interp r fds))]
    [multC (l r) (* (interp l fds) (interp r fds))]
    [ifC (c s n) (if (zero? (interp c fds)) (interp n fds) (interp s fds))]
    ))

; get-fundef
(define (get-fundef [n : symbol] [fds : (listof FunDefC)]) : FunDefC
  (cond
    [(empty? fds) (error 'get-fundef "referência para função não definida")]
    [(cons? fds) (cond
                   [(equal? n (fdC-name (first fds))) (first fds)] ; achou!
                   [else (get-fundef n (rest fds))] ; procura no resto
                   )]))


; o parser precisa tratar de chamadas
(define (parse [s : s-expression]) : ExprS
  (cond
    [(s-exp-number? s) (numS (s-exp->number s))]
    [(s-exp-list? s)
     (let ([sl (s-exp->list s)])
       (case (s-exp->symbol (first sl))
         [(+) (plusS (parse (second sl)) (parse (third sl)))]
         [(*) (multS (parse (second sl)) (parse (third sl)))]
         [(-) (bminusS (parse (second sl)) (parse (third sl)))]
         [(~) (uminusS (parse (second sl)))]
         [(call) (appS (s-exp->symbol (second sl)) (parse (third sl)))]
         [(if) (ifS (parse (second sl)) (parse (third sl)) (parse (fourth sl)))]
         [else (error 'parse "invalid list input")]))]
    [else (error 'parse "invalid input")]))

#|
 | Nesta linguagem, as funções são pré-definidas
 | Vejamos dobro, quadrado e fatorial
 |#
(define biblioteca (list 
                    [fdC 'dobro 'x (plusC (idC 'x) (idC 'x))]
                    [fdC 'quadrado 'y (multC (idC 'y) (idC 'y))]
                    [fdC 'fatorial 'n (ifC  (idC 'n) 
						 (multC (appC 'fatorial (plusC (idC 'n) (numC -1))) 
								(idC 'n))
						 (numC 1))]
                    [fdC 'narciso  'narciso (multC (idC 'narciso) (numC 1000))]
                    ))

(interp (desugar (parse '(+ -1400 (call fatorial 7)))) biblioteca)
(test (interp (desugar (parse '(call narciso (call fatorial 7)))) biblioteca) 5040000)