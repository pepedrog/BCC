#lang plai-typed

#|
 | Incluindo troca de sinal: - unário, uminus
 | Mais açúcar?
 |#

(define-type ArithC
  [numC (n : number)]
  [plusC (l : ArithC) (r : ArithC)]
  [multC (l : ArithC) (r : ArithC)])




; Incluindo o sinal negativo
(define-type ArithS
  [numS    (n : number)]
  [plusS   (l : ArithS) (r : ArithS)]
  [bminusS (l : ArithS) (r : ArithS)]
  [uminusS (e : ArithS)]
  [multS   (l : ArithS) (r : ArithS)])


; Nova "desugar", ou quase

(define (desugar [as : ArithS]) : ArithC  
  (type-case ArithS as
    [numS    (n)   (numC n)]
    [plusS   (l r) (plusC (desugar l) (desugar r))] 
    [multS   (l r) (multC (desugar l) (desugar r))]
    [bminusS (l r) (plusC (desugar l) (multC (numC -1) (desugar r)))]
    ; tentativas para o - unário

    ; pode-se fazer (- 0 e)
    ;[uminusS (e)   (desugar (bminusS (numS 0) e))]
    ; esta solução é perigosa, pois estamos fazendo a recursão em no mesmo 'e'
    ; isto é, recursão "generativa", ou não estutural:
    ; o argumento da recursão é uma função, e não uma subparte, do argumento original
    
    ; Isto resoveria,mas coloca outro problema (qual?)
    ;[uminusS (e)   (bminusS (numS 0) (desugar e))]
    
    ; a solução (ainda bem que existe) também se fixa apenas nas primitivas
    [uminusS (e)   (multC (numC -1) (desugar e))]
    ))


; O interpretador é o mesmo, pois no final ainda temos ArithC
(define (interp [a : ArithC]) : number
  (type-case ArithC a
    [numC (n) n]
    [plusC (l r) (+ (interp l) (interp r))]
    [multC (l r) (* (interp l) (interp r))]))


; o parser muda mais um pouco
(define (parse [s : s-expression]) : ArithS
  (cond
    [(s-exp-number? s) (numS (s-exp->number s))]
    [(s-exp-list? s)
     (let ([sl (s-exp->list s)])
       (case (s-exp->symbol (first sl))
         [(+) (plusS (parse (second sl)) (parse (third sl)))]
         [(*) (multS (parse (second sl)) (parse (third sl)))]
         [(-) (bminusS (parse (second sl)) (parse (third sl)))]
         ; para o parser precisamos um sinal negativo...
         [(~) (uminusS (parse (second sl)))]
         [else (error 'parse "invalid list input")]))]
    [else (error 'parse "invalid input")]))

(test (interp (desugar (uminusS (numS 3) ))) -3)


(define (interpS [a : ArithS]) (interp (desugar a)))

(interpS (parse '(+ 5 (~ 3))))


