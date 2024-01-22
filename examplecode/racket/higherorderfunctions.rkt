#lang racket
; defines a simple list for the examples
(define numbers '(1 2 3 4 5))

; demonstrates "map" and "anonymous functions"
; applies the anonymous function to each member of a list and returns new list with all the results
(define squared (map (lambda (x) (* x x)) numbers))

; demonstrates "reduce" ... condensing a list down to a single number
(define sum (foldl + 0 squared))
(define product (foldl * 1 squared))

; demonstrates filter for trimming down a list to a smaller list
(define evenNumbers (filter (lambda (number) (even? number)) numbers))
(define evenNumber2 (filter even? numbers))