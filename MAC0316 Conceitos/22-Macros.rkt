#lang plai
;(define-syntax my-let-1
;  (syntax-rules () 
;    [(my-let-1 (var val) body)
;     ((lambda (var) body) val)]))
;(my-let-1 (pi 3.12) (+ pi 5))
;
;(define-syntax my-let-2
;  (syntax-rules ()
;    [(my-let-2 ([var val] ...) body)
;     ((lambda (var ...) body) val ...)]))
;
;(my-let-2 ([um 1] [dois 2] [três 3]) (+ um (* dois três)))
;
;(define-syntax (my-let-3 x)
;  (syntax-case x () 
;    [(my-let-3 (var val) body)
;     #'((lambda (var) body) val)]))
;
;(my-let-3 (pi 3.12) (+ pi 5))
;
;(define-syntax (my-let-4 x)
;  (syntax-case x () 
;    [(my-let-3 (var val) body)
;     (identifier? #'var)
;     #'((lambda (var) body) val)]))
;
;(my-let-4 (pi 3.12) (+ pi 5))


;(define-syntax (my-or-1 x)
;  (syntax-case x ()
;    [(my-or-1 e0 e1 ...)
;     #'(if e0
;           e0
;           (my-or-1 e1 ...))]))

;(my-or-1 #f #t)

;
;(define-syntax (my-or-2 x)
;  (syntax-case x ()
;    [(my-or-2) #'#f]
;    [(my-or-2 e0 e1 ...)
;     #'(if e0
;           e0
;           (my-or-2 e1 ...))]))
;
;(my-or-2 #f #t)
;
;(define-syntax (my-or-3 x)
;  (syntax-case x ()
;    [(my-or-3) #'#f]
;    [(my-or-3 e0) #'e0]
;    [(my-or-3 e0 e1 ...)
;     #'(if e0
;           e0
;           (my-or-3 e1 ...))]))
;
;(my-or-3  #t)
;
;(let ([init #f])
;  (my-or-3 (begin (set! init (not init))
;                  init)
;           #f))

;(define-syntax (my-or-4 x)
;  (syntax-case x ()
;    [(my-or-4)
;     #'#f]
;    [(my-or-4 e)
;     #'e]
;    [(my-or-4 e0 e1 ...)
;     #'(let ([v e0])
;         (if v
;             v
;             (my-or-4 e1 ...)))]))
;
;(let ([init #f])
;  (my-or-4 (begin (set! init (not init))
;                  init)
;           #f))
;
;

(define (msg o m . a)
  (apply (o m) a))

;(define os-1
;  (object/self-1
;   [first (x) (msg self 'second (+ x 1))]
;   [second (x) (+ x 1)]))
;
;
;(define-syntax object/self-1
;  (syntax-rules ()
;    [(object [mtd-name (var) val] ...)
;     (let ([self (lambda (msg-name)
;                   (lambda (v) (error 'object "nothing here")))])
;       (begin
;         (set! self
;               (lambda (msg)
;                 (case msg
;                   [(mtd-name) (lambda (var) val)]
;                   ...)))
;         self))]))

;(define os-2
;  (object/self-2 self
;                 [first (x) (msg self 'second (+ x 1))]
;                 [second (x) (+ x 1)]))
;
;(define-syntax object/self-2
;  (syntax-rules ()
;    [(object self [mtd-name (var) val] ...)
;     (let ([self (lambda (msg-name)
;                   (lambda (v) (error 'object "nothing here")))])
;       (begin
;         (set! self
;               (lambda (msg)
;                 (case msg
;                   [(mtd-name) (lambda (var) val)]
;                   ...)))
;         self))]))


(define-syntax (object/self-3 x)
  (syntax-case x ()
    [(object [mtd-name (var) val] ...)
     (with-syntax ([self (datum->syntax x 'self)])
       #'(let ([self (lambda (msg-name)
                       (lambda (v) (error 'object "nothing here")))])
           (begin
             (set! self
                   (lambda (msg-name)
                     (case msg-name
                       [(mtd-name) (lambda (var) val)]
                       ...)))
             self)))]))


(define os-3
  (object/self-3
   [first (x) (msg self 'second (+ x 1))]
   [second (x) (+ x 1)]))
