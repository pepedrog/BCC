#lang plai-typed

#|
 | Funções como valores
 |#

(define-type ExprC
  [numC (n : number)]
  [idC  (s : symbol)]
  [plusC (l : ExprC) (r : ExprC)]
  [multC (l : ExprC) (r : ExprC)]
  [fdC (name : symbol) (arg : symbol) (body : ExprC)] ; declaração faz parte da expressão
  [appC (fun : ExprC) (arg : ExprC)] ; a aplicação recebe uma função
  [ifC   (condição : ExprC) (sim : ExprC) (não : ExprC)]
  )

; inclui funções
(define-type ExprS
  [numS    (n : number)]
  [idS     (s : symbol)] 
  [fdS (name : symbol) (arg : symbol) (body : ExprS)] ; declaração faz parte da expressão
  [appS    (fun : ExprS) (arg : ExprS)] 
  [plusS   (l : ExprS) (r : ExprS)]
  [bminusS (l : ExprS) (r : ExprS)]
  [uminusS (e : ExprS)]
  [multS   (l : ExprS) (r : ExprS)]
  [ifS     (c : ExprS) (s : ExprS) (n : ExprS)]
  )


; agora é preciso tomar cuidado com as modificações
(define (desugar [as : ExprS]) : ExprC  
  (type-case ExprS as
    [numS    (n) (numC n)]
    [idS     (s) (idC s)]
    [fdS     (n a b)  (fdC n a (desugar b))] ; precisamos converter o corpo
    [appS    (fun arg) (appC (desugar fun) (desugar arg))] 
    [plusS   (l r) (plusC (desugar l) (desugar r))] 
    [multS   (l r) (multC (desugar l) (desugar r))]
    [bminusS (l r) (plusC (desugar l) (multC (numC -1) (desugar r)))]
    [uminusS (e)   (multC (numC -1) (desugar e))]
    [ifS     (c s n) (ifC (desugar c) (desugar s) (desugar n))]
    ))


#|
 | O interpretador precisa de um tipo especial para retornar
 |#

(define-type Value
  [numV (n : number)]
  [funV (name : symbol) (arg : symbol) (body : ExprC)])

; símbolos devem se associar ao número (ou a Value?)
(define-type Binding
      [bind (name : symbol) (val : Value)])

; A lista de associações é o environment
(define-type-alias Env (listof Binding))
(define mt-env empty)        ; ente pronunciar "mt" em inglês e compare com "empty"
(define extend-env cons)     ; sorte, cons faz exatamente o que queremos para estender o env

; novos operadores
(define (num+ [l : Value] [r : Value]) : Value
    (cond
        [(and (numV? l) (numV? r))
             (numV (+ (numV-n l) (numV-n r)))]
        [else
             (error 'num+ "Um dos argumentos não é número")]))

(define (num* [l : Value] [r : Value]) : Value
    (cond
        [(and (numV? l) (numV? r))
             (numV (* (numV-n l) (numV-n r)))]
        [else
             (error 'num* "Um dos argumentos não é número")]))

; Não precisamos mais da lista de funções, pelo menos por enquanto....
(define (interp [a : ExprC] [env : Env]) : Value
  (type-case ExprC a
    [numC (n) (numV n)] ; garantir o retorno do tipo esperado
    [idC (n) (lookup n env)]
    [fdC (n a b) (funV n a b)] ; a função se auto-representa

    [appC (f a) ; some a procura!
          (local ([define fd (interp f env)]) 
            (interp (funV-body fd)
                    (extend-env 
                        (bind (funV-arg fd) (interp a env))
                        mt-env)
                    ))]
    [plusC (l r) (num+ (interp l env) (interp r env))]
    [multC (l r) (num* (interp l env) (interp r env))]
    [ifC (c s n) (if (zero? (numV-n (interp c env))) (interp n env) (interp s env))]
    ))

; lookup também muda o tipo de retorno
(define (lookup [for : symbol] [env : Env]) : Value
       (cond
            [(empty? env) (error 'lookup (string-append (symbol->string for) " não foi encontrado"))] ; livre (não definida)
            [else (cond
                  [(symbol=? for (bind-name (first env)))   ; achou!
                                 (bind-val (first env))]
                  [else (lookup for (rest env))])]))        ; vê no resto

; o parser permite definir funções...
(define (parse [s : s-expression]) : ExprS
  (cond
    [(s-exp-number? s) (numS (s-exp->number s))]
    [(s-exp-symbol? s) (idS (s-exp->symbol s))] ; pode ser um símbolo livre nas definições de função
    [(s-exp-list? s)
     (let ([sl (s-exp->list s)])
       (case (s-exp->symbol (first sl))
         [(+) (plusS (parse (second sl)) (parse (third sl)))]
         [(*) (multS (parse (second sl)) (parse (third sl)))]
         [(-) (bminusS (parse (second sl)) (parse (third sl)))]
         [(~) (uminusS (parse (second sl)))]
         [(func) (fdS (s-exp->symbol (second sl)) (s-exp->symbol (third sl)) (parse (fourth sl)))] ; definição
         [(call) (appS (parse (second sl)) (parse (third sl)))]
         [(if) (ifS (parse (second sl)) (parse (third sl)) (parse (fourth sl)))]
         [else (error 'parse "invalid list input")]))]
    [else (error 'parse "invalid input")]))

; Facilitador
(define (interpS [s : s-expression]) (interp (desugar (parse s)) mt-env))

; Testes
(test (interp (plusC (numC 10) (appC (fdC 'const5 '_ (numC 5)) (numC 10)))
              mt-env)
      (numV 15))
(interpS '(+ 10 (call (func dobra x (+ x x)) 16)))