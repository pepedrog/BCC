#lang plai-typed

#|
 | Environments
 |#

; Na estrutura nada muda....

(define-type ExprC
  [numC (n : number)]
  [idC  (s : symbol)]
  [appC (fun : symbol) (arg : ExprC)]
  [plusC (l : ExprC) (r : ExprC)]
  [multC (l : ExprC) (r : ExprC)]
  [ifC   (condição : ExprC) (sim : ExprC) (não : ExprC)]
  )

(define-type FunDefC
  [fdC (name : symbol) (arg : symbol) (body : ExprC)]
  )

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


(define (desugar [as : ExprS]) : ExprC  
  (type-case ExprS as
    [numS    (n) (numC n)]
    [idS     (s) (idC s)]
    [appS    (fun arg) (appC fun (desugar arg))]
    [plusS   (l r) (plusC (desugar l) (desugar r))] 
    [multS   (l r) (multC (desugar l) (desugar r))]
    [bminusS (l r) (plusC (desugar l) (multC (numC -1) (desugar r)))]
    [uminusS (e)   (multC (numC -1) (desugar e))]
    [ifS     (c s n) (ifC (desugar c) (desugar s) (desugar n))]
    ))


#|
 | O interpretador precisa de uma lista adicional de definições para os símbolos
 |#

(define-type Binding
      [bind (name : symbol) (val : number)])

; A lista de associações é o environment
(define-type-alias Env (listof Binding))
(define mt-env empty)        ; ente pronunciar "mt" em inglês e compare com "empty"
(define extend-env cons)     ; sorte, cons faz exatamente o que queremos para estender o env

; interp: todas as chamadas recursivas devem levar em conta o environment
(define (interp [a : ExprC] [env : Env] [fds : (listof FunDefC)]) : number
  (type-case ExprC a
    [numC (n) n] ; nada a fazer
    
    ; um identificador deve ser trocado pela sua associação
    [idC (n) (lookup n env)]
    
    ; aplicação ainda precisa olhar a definição da função, mas não faz mais substituições
    ; o que precisa ser feito é apenas mais uma associação
    [appC (f a) 
          (local ([define fd (get-fundef f fds)]) 
            (interp (fdC-body fd)          ; expressão
                    (extend-env 
                        (bind (fdC-arg fd) (interp a env fds))
                        env)              ; novo environment
                    fds))]
    
    ; aqui não muda quase nada, só a chamada
    [plusC (l r) (+ (interp l env fds) (interp r env fds))]
    [multC (l r) (* (interp l env fds) (interp r env fds))]
    [ifC (c s n) (if (zero? (interp c env fds)) (interp n env fds) (interp s env fds))]
    ))

; get-fundef
(define (get-fundef [n : symbol] [fds : (listof FunDefC)]) : FunDefC
  (cond
    [(empty? fds) (error 'get-fundef "referência para função não definida")]
    [(cons? fds) (cond
                   [(equal? n (fdC-name (first fds))) (first fds)] ; achou!
                   [else (get-fundef n (rest fds))] ; procura no resto
                   )]))

; lookup
(define (lookup [for : symbol] [env : Env]) : number
       (cond
            [(empty? env) (error 'lookup "name not found")] ; livre (não definida)
            [else (cond
                  [(symbol=? for (bind-name (first env)))   ; achou!
                                 (bind-val (first env))]
                  [else (lookup for (rest env))])]))        ; vê no resto


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
                    [fdC 'quadruple 'x (appC 'dobro (appC 'dobro (idC 'x)))]
                    ))

(interp (desugar (parse '(+ -1400 (call fatorial 7)))) mt-env biblioteca)
(test (interp (desugar (parse '(call narciso (call fatorial 7)))) mt-env biblioteca) 5040000)

(test (interp (plusC (numC 10) (appC 'const5 (numC 10))) mt-env (list (fdC 'const5 '_ (numC 5)))) 15)
(test (interp (plusC (numC 10) (appC 'double (plusC (numC 1) (numC 2)))) mt-env (list (fdC 'double 'x (plusC (idC 'x) (idC 'x))))) 16)
(test (interp (desugar (parse '(+ 10 (call quadruple (+ 1 2))))) mt-env biblioteca) 22)
(test (interp (plusC (numC 10) (appC 'quadruple (plusC (numC 1) (numC 2)))) mt-env biblioteca) 22)

(define (interpS [s : s-expression] [bib : (listof FunDefC)] ) (interp (desugar (parse s)) mt-env bib))
(interpS '(+ 10 (call quadruple (+ 1 2))) biblioteca)