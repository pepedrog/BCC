#lang plai-typed

#|
 | Construindo aritmética com subtração
 | Usamos um outro tipo, ArithS, onde o sinal é apenas açúcar sintático
 | O interpretador chamará uma função para converter ArithS em ArithC
 |#

(define-type ArithC
  [numC (n : number)]
  [plusC (l : ArithC) (r : ArithC)]
  [multC (l : ArithC) (r : ArithC)])



; Agora incluindo subtração
(define-type ArithS
  [numS    (n : number)]
  [plusS   (l : ArithS) (r : ArithS)]
  [bminusS (l : ArithS) (r : ArithS)]
  [multS   (l : ArithS) (r : ArithS)])

; o açúcar sintático fará a seguinte transformação:
; (- a b) -> (+ a (* -1 b))
; ArithS      ArithC

; Precisamos de uma função "desugar", 
; poderíamos chamar também de ArithS->ArithC, mas vou seguir o livro


(define (desugar [as : ArithS]) : ArithC  ; recebe ArithS e devolve ArithC
  (type-case ArithS as
    [numS    (n)   (numC n)]              ; conversão direta
    [plusS   (l r) (plusC (desugar l)     ; todas as sub-árvores devem ter o açúcar retirado
                         (desugar r))] 
    [multS   (l r) (multC (desugar l)
                        (desugar r))]
    [bminusS (l r) (plusC (desugar l)     ; aqui é feita a transformação
                      (multC (numC -1) (desugar r)))]
    ))


; O interpretador é o mesmo, pois no final temos ArithC
(define (interp [a : ArithC]) : number
  (type-case ArithC a
    [numC (n) n]
    [plusC (l r) (+ (interp l) (interp r))]
    [multC (l r) (* (interp l) (interp r))]))


; o parser muda para gerar ArithS
(define (parse [s : s-expression]) : ArithS
  (cond
    [(s-exp-number? s) (numS (s-exp->number s))]
    [(s-exp-list? s)
     (let ([sl (s-exp->list s)])
       (case (s-exp->symbol (first sl))
         [(+) (plusS (parse (second sl)) (parse (third sl)))]
         [(*) (multS (parse (second sl)) (parse (third sl)))]
         ; agora temos o '-'
         [(-) (bminusS (parse (second sl)) (parse (third sl)))]
         [else (error 'parse "invalid list input")]))]
    [else (error 'parse "invalid input")]))

(define (ArithS->ArithC [as : ArithS]) (desugar as))
(test (interp (desugar (bminusS (numS 3) (numS 2)))) 1)


; já que estamos aqui, podemos criar um interpS
(define (interpS [a : ArithS]) (interp (desugar a)))

(interpS (plusS (numS 45) (bminusS  (multS (numS 2) (numS 1)) (numS 5))))

(parse '(+ (* 1 2) (+ 2 3)))

(interpS (parse '(+ (* 1 2) (+ 2 3))))
