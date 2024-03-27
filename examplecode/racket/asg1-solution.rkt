#lang racket

; calculate sum of a list
(define (sumList lis)
  (if (empty? lis) 0 (+ (car lis) (sumList (cdr lis)))))

(define (mean lis)
  (/ (sumList lis) (length lis)))