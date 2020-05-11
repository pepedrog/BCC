#lang plai
;; objetos como coleção de nomes
;(define o-1
;     (lambda (m)
;        (case m
;            [(add1) (lambda (x) (+ x 1))]
;            [(sub1) (lambda (x) (- x 1))])))
;
;(define (msg o m . a)
;        (apply (o m) a))
;
;(test (msg o-1 'add1 3) 4) 

;;;;;;;;;;;;;;;;;;;;;;;;;;
;; construtor
;(define (o-constr-1 x)
;        (lambda (m)
;             (case m
;                 [(addX) (lambda (y) (+ x y))])))

;(test (msg (o-constr-1 12) 'addX 34) 46)

;;;;;;;;;;;;;;;;;;;;;;;;
;; estado
;(define (o-state-1 count)
;        (lambda (m)
;            (case m
;                [(inc) (lambda () (set! count (+ count 1)))]
;                [(dec) (lambda () (set! count (- count 1)))]
;                [(get) (lambda () count)])))

;(test (let ([o (o-state-1 5)])
;        (begin (msg o 'inc)
;               (msg o 'dec)
;               (msg o 'get)))
;      5)

;(test (let ([o1 (o-state-1 3)]
;            [o2 (o-state-1 3)])
;        (begin (msg o1 'inc)
;               (msg o1 'inc)
;               (+ (msg o1 'get)
;                  (msg o2 'get))))
;      (+ 5 3))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; membros privados

;(define (o-state-2 init)
;    (let ([count init])
;       (lambda (m)
;           (case m
;              [(inc) (lambda () (set! count (+ count 1)))]
;              [(dec) (lambda () (set! count (- count 1)))]
;              [(get) (lambda () count)]))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; membros estáticos

;(define o-static-1
;   (let ([counter 0])
;      (lambda (amount)
;         (begin
;            (set! counter (+ 1 counter))
;               (lambda (m)
;                  (case m
;                     [(inc) (lambda (n) (set! amount (+ amount n)))]
;                     [(dec) (lambda (n) (set! amount (- amount n)))]
;                     [(get) (lambda () amount)]
;                    [(count) (lambda () counter)]))))))

;(test (let ([o (o-static-1 1000)])
;        (msg o 'count))
;      1)
;(test (let ([o (o-static-1 0)])
;        (msg o 'count))
;      2)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; auto referência
;(define o-self!
;   (let ([self 'dummy])
;      (begin
;          (set! self
;             (lambda (m)
;                (case m
;                   [(first) (lambda (x) (msg self 'second (+ x 1)))]
;                   [(second) (lambda (x) (+ x 1))])))
;           self)))

;(test (msg o-self! 'first 5) 7)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; com o combinador Y (simplificado)

;(define o-self-no!
;   (lambda (m)
;      (case m
;      [(first) (lambda (self x) (msg/self self 'second (+ x 1)))]
;      [(second) (lambda (self x) (+ x 1))])))

;(define (msg/self o m . a)
;  (apply (o m) o a))

;(test (msg/self o-self-no! 'first 5) 7)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; late binding
;(define (mt)
;  (let ([self 'dummy])
;    (begin
;      (set! self
;            (lambda (m)
;              (case m
;                [(add) (lambda () 0)])))
;      self)))

;(define (node v l r)
;  (let ([self 'dummy])
;    (begin
;      (set! self
;            (lambda (m)
;              (case m
;                [(add) (lambda () (+ v
;                                     (msg l 'add)
;                                     (msg r 'add)))])))
;      self)))

;(define a-tree
;  (node 10
;        (node 5 (mt) (mt))
;        (node 15 (node 6 (mt) (mt)) (mt))))

;(test (msg a-tree 'add) (+ 10 5 15 6))

