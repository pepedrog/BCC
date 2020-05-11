#lang plai-typed

(define-type ArithC
   [numC  (n : number)]
   [plusC (l : ArithC) (r : ArithC)]
   [multC (l : ArithC) (r : ArithC)])

; Incluindo subtração e sinal (menos unário)
(define-type ArithS
  [numS    (n : number)]
  [plusS   (l : ArithS) (r : ArithS)]
  [bminusS (l : ArithS) (r : ArithS)]
  [uminusS (e : ArithS)]
  [multS   (l : ArithS) (r : ArithS)])
                                   
;;  Evitando recursão generativa 
(define (desugar [as : ArithS]) : ArithC
  (type-case ArithS as
    [numS    (n)   (numC n)]
    [plusS   (l r) (plusC (desugar l)
                        (desugar r))]
    [multS   (l r) (multC (desugar l)
                        (desugar r))]
    [bminusS (l r) (plusC (desugar l)
                          (multC (numC -1) (desugar r)))]
    [uminusS (e)   (multC (numC -1) (desugar e))] ;aqui

    ))



(define (interp [a : ArithC]) : number
  (type-case ArithC a
    [numC (n) n]
    [plusC (l r) (+ (interp l) (interp r))]
    [multC (l r) (* (interp l) (interp r))]))

(interp (desugar (bminusS (numS 3) (numS 2))))



