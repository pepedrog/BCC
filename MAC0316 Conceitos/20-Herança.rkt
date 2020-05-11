#lang plai

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Objeto original - árvores e folhas
(define (mt)
  (let ([self 'dummy])
    (begin
      (set! self
            (lambda (m)
              (case m
                [(add) (lambda () 0)])))
      self)))


(define (node v l r)
  (let ([self 'dummy])
    (begin
      (set! self
            (lambda (m)
              (case m
                [(add) (lambda () (+ v
                                     (msg l 'add)
                                     (msg r 'add)))])))
      self)))


(define ( msg o m . a )
   (apply ( o m ) a ) )


(define a-tree
  (node 10
        (node 5 (mt) (mt))
        (node 15 (node 6 (mt) (mt)) (mt))))

(test (msg a-tree 'add) (+ 10 5 15 6))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Extensão


(define (node/size parent-maker v l r)
  (let ([parent-object (parent-maker v l r)]
        [self 'dummy])
    (begin
      (set! self
            (lambda (m)
              (case m
                [(size) (lambda () (+ 1
                                      (msg l 'size)
                                      (msg r 'size)))]
                [else (parent-object m)])))
      self)))

(define (mt/size parent-maker)
  (let ([parent-object (parent-maker)]
        [self 'dummy])
    (begin
      (set! self
            (lambda (m)
              (case m
                [(size) (lambda () 0)]
                [else (parent-object m)])))
      self)))


(define a-tree/size
  (node/size node
             10
             (node/size node 5 (mt/size mt) (mt/size mt))
             (node/size node 15
                        (node/size node 6 (mt/size mt) (mt/size mt))
                        (mt/size mt))))



(test (msg a-tree/size 'add) (+ 10 5 15 6))
(test (msg a-tree/size 'size) 4)



;;; Sem mutação

(define (mt-no!)
  (lambda (m)
    (case m
      [(add) (lambda (self) 0)])))


(define (node-no! v l r)
  (lambda (m)
    (case m
      [(add) (lambda (self) (+ v
                           (msg/self l 'add)
                           (msg/self r 'add)))])))



(define (msg/self o m . a )
   (apply (o m) o a ))


(define (node/size-no! parent-maker v l r)
  (let ([parent-object (parent-maker v l r)])
    (lambda (m)
      (case m
        [(size) (lambda (self) (+ 1
                                  (msg/self l 'size)
                                  (msg/self r 'size)))]
        [else (parent-object m)]))))

(define (mt/size-no! parent-maker)
  (let ([parent-object (parent-maker)])
    (lambda (m)
      (case m
        [(size) (lambda (self) 0)]
        [else (parent-object m)])))
  )



(define o-tree/size
  (node/size-no! node-no!
             10
             (node/size-no! node-no!  5 (mt/size-no! mt-no!) (mt/size-no! mt-no!))
             (node/size-no! node-no! 15
                        (node/size-no! node-no! 6 (mt/size-no! mt-no!) (mt/size-no! mt-no!))
                        (mt/size-no! mt-no!))))



(test (msg/self o-tree/size 'add) (+ 10 5 15 6))
(test (msg/self o-tree/size 'size) 4)

