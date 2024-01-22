#lang racket

; calculate sum of a list
(define (sumList lis)
  (if (empty? lis) 0 (+ (car lis) (sumList (cdr lis)))))

(sumList '(1 2 3 4 5))