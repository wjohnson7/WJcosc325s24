#lang racket

; factorial recursive implementation
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

; classic head-tail recursion
(define (sumlist lis)
  (if (= (length lis) 0)
      0
      (+ (car lis) (sumlist (cdr lis)))))