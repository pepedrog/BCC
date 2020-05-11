#lang plai-typed

#|
 | Objetos
 |#

(define-type ExprC
  [numC  (n : number)]
  [idC   (s : symbol)]
  [plusC (l : ExprC) (r : ExprC)]
  [multC (l : ExprC) (r : ExprC)]
  [lamC  (arg : symbol) (body : ExprC)]
  [appC  (fun : ExprC) (arg : ExprC)]
  [ifC   (condição : ExprC) (sim : ExprC) (não : ExprC)]
  [objC  (ns : (listof symbol)) (es : (listof ExprC))] ; objeto
  [msgC  (o : ExprC) (n : symbol)]					  ; seletor de campo
  )

; inclui os mesmos tipos
(define-type ExprS
  [numS    (n : number)]
  [idS     (s : symbol)] 
  [lamS    (arg : symbol) (body : ExprS)] ; muda de acordo
  [appS    (fun : ExprS) (arg : ExprS)] 
  [plusS   (l : ExprS) (r : ExprS)]
  [bminusS (l : ExprS) (r : ExprS)]
  [uminusS (e : ExprS)]
  [multS   (l : ExprS) (r : ExprS)]
  [ifS     (c : ExprS) (s : ExprS) (n : ExprS)]
  [letS    (id : symbol) (val : ExprS) (expr : ExprS)]
  [objS    (ns : (listof symbol)) (es : (listof ExprS))] ; objeto
  [msgS    (o : ExprS) (n : symbol) (a : ExprS)] ; pense em o.n(a), ou o->n(a)
  )


; agora é preciso tomar cuidado com as modificações
(define (desugar [as : ExprS]) : ExprC  
  (type-case ExprS as
    [numS    (n) (numC n)]
    [idS     (s) (idC s)]
    [lamS    (a b) (lamC a (desugar b))] ; idem
    [appS    (fun arg) (appC (desugar fun) (desugar arg))] 
    [plusS   (l r) (plusC (desugar l) (desugar r))] 
    [multS   (l r) (multC (desugar l) (desugar r))]
    [bminusS (l r) (plusC (desugar l) (multC (numC -1) (desugar r)))]
    [uminusS (e)   (multC (numC -1) (desugar e))]
    [ifS     (c s n) (ifC (desugar c) (desugar s) (desugar n))]
    [objS	  (ns es) (objC ns (map (lambda (e) (desugar e)) es))] ; desugar cada elemento
    [msgS    (o n a) (appC (msgC (desugar o) n) (desugar a))]
    [letS    (id val expr) (appC  (lamC id (desugar expr)) (desugar val))] ; já aplica o método
    ))


#|
 | Closure não tem mais o nome, mas precisa do environment
 |#

; Um objeto é um valor
(define-type Value
  [numV  (n   : number)]
  [closV (arg : symbol) (body : ExprC) (env : Env)]
  [objV  (ns  : (listof symbol)) (vs : (listof Value))])
  

; símbolos devem se associar ao número (ou a Value?)
(define-type Binding
      [bind (name : symbol) (val : Value)])

; A lista de associações é o environment
(define-type-alias Env (listof Binding))
(define mt-env empty)
(define extend-env cons)

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

; trata agora lamC e appC
(define (interp [a : ExprC] [env : Env]) : Value
  (type-case ExprC a
    [numC (n)   (numV n)] 
    [idC  (n)   (lookup n env)]
    [lamC (a b) (closV a b env)] ; definição de função captura o environment

    [appC (f a)
          (local ([define f-value (interp f env)]) ; f-value descreve melhor a ideia
            (interp (closV-body f-value)
                    (extend-env 
                        (bind (closV-arg f-value) (interp a env))
                        (closV-env f-value) ; não mais mt-env
                    )))]
    [plusC (l r)  (num+ (interp l env) (interp r env))]
    [multC (l r)  (num* (interp l env) (interp r env))]
    [ifC (c s n)  (if (zero? (numV-n (interp c env))) (interp n env) (interp s env))]
    [objC (ns es) (objV  ns (map (lambda (e) (interp e env)) es))] ; avalia todos os valores
	 [msgC (o n)   (lookup-msg  n (interp o env))] ; seletor
    )) 

; lookup também muda o tipo de retorno
(define (lookup [for : symbol] [env : Env]) : Value
       (cond
            [(empty? env) (error 'lookup (string-append (symbol->string for) " não foi encontrado"))] ; livre (não definida)
            [else (cond
                  [(symbol=? for (bind-name (first env)))   ; achou!
                                 (bind-val (first env))]
                  [else (lookup for (rest env))])]))        ; vê no resto

(define (lookup-msg [n : symbol] [o : Value]) : Value
	(type-case Value o
          [objV (nomes valores)
                (cond
                  [(empty? nomes) (error 'lookup-msg (string-append (symbol->string n) " não foi encontrado"))]
                  [(symbol=? n (first nomes)) (first valores)] ; achou
                  [else (lookup-msg n (objV (rest nomes) (rest valores)))])] ; cria um sub objeto para procurar
          [else (error 'lookup-msg "Valor passador não é um objeto!")]))

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
         [(func) (lamS (s-exp->symbol (second sl)) (parse (third sl)))] ; definição
         [(call) (appS (parse (second sl)) (parse (third sl)))]
         [(if)   (ifS (parse (second sl)) (parse (third sl)) (parse (fourth sl)))]
         [(:=)   (letS (s-exp->symbol (second sl)) (parse (third sl)) (parse (fourth sl)))] 
         [(obj)  (cond 
                   [(and (s-exp-list? (second sl)) (s-exp-list? (third sl))) 
                    (objS (map (λ (s) (s-exp->symbol s)) (s-exp->list (second sl))) 
                          (map (λ (e) (parse e))         (s-exp->list (third  sl))))]
                   [else (error 'parse "Objeto mal definido")])]
         [(->)   (msgS (parse (second sl)) (s-exp->symbol (third sl)) (parse (fourth sl)))]
         [else (error 'parse "invalid list input")]))]
    [else (error 'parse "invalid input")]))

; Facilitador
(define (interpS [s : s-expression]) (interp (desugar (parse s)) mt-env))

; Testes
(test (interp (plusC (numC 10) (appC (lamC '_ (numC 5)) (numC 10)))
              mt-env)
      (numV 15))
(interpS '(+ 10 (call (func x (+ x x)) 16)))

(interp (desugar (letS 'o (objS (list 'add1 'sub1)
			   (list (lamS 'x (plusS (idS 'x) (numS 1)))
					 (lamS 'x (plusS (idS 'x) (numS -1)))))
	  (msgS (idS 'o) 'add1 (numS 3)))) mt-env)

(interpS '(:= bib (obj (add1            sub1) 
                       ((func x (+ x 1)) (func x (- x 1)))
                       )
                  (-> bib add1 3)))


