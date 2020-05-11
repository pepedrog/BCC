#lang racket

( 
 (
 (λ (m) (m m))
 (λ (f) (λ (n) (if (zero? n) 1 (* n ((f f) (- n 1)))))))
 5)


;(
; (λ (p)
;   (
;    (λ (m) (m m))
;    (λ (f) (p (f f)))) ; (f f) será chamado antes da hora gerando recursão infinita
;   )
; (λ (g) (λ (n) (if (zero? n) 1 (* n (g (- n 1)))))))

(
 (; isto tudo é o fatorial
  (λ (p)
    ( ; combinador Y
     (λ (m) (m m)) ; aplica m em ele mesmo 
     (λ (f) (p (λ (a) ((f f) a)))) ; m -> gerador de chamada, a é só para segurar o (f f)
     ))
  (λ (g) (λ (n) (if (zero? n) 1 (* n (g (- n 1)))))) ; p (=fatorial) (g é (f f) "segurado")
  )
 5) 