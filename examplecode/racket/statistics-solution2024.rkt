#lang racket
(define (mean lis)
  (/ (foldl + 0 lis) (length lis)))

; base case i is 0, return first item in list
; recursive step, make the recursive call on i-1 and cdr lis
(define (member-at i lis)
  (if (= i 0) (car lis) (member-at (- i 1) (cdr lis))))

(define (median lis)
  (let
      [
       (sortedlis (sort lis <))
      ]
    0))
;      (if (even? (length lis)) (helper1 sortedlis) (helper2 sortedlis))))


; base case - list is empty 
(define (countAppearances atm lis)
  (cond
    [(empty? lis) 0]
    [(equal? atm (car lis)) (+ 1 (countAppearances atm (cdr lis)))]
    [else (countAppearances atm (cdr lis))]))

; countAll lis1 lis2
;   lis1 will be traversed recursively
;   lis2 will never change
;   returns a list of how many times each item in lis1 appear in lis2
(define (countAll lis1 lis2)
  (if (= (length lis1) 1)
      (list (cons (car lis1) (countAppearances (car lis1) lis2)))
      (append (list (cons (car lis1) (countAppearances (car lis1) lis2))) (countAll (cdr lis1) lis2))))


(define (pairorder a b)
  (> (cdr a) (cdr b)))

(define (mode lis)
  (let
      [
       (listcounts (countAll (remove-duplicates lis) lis)) 
      ]
    (car (car (sort listcounts pairorder))))