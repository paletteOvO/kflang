# Something Else...
# What does this lang look like
```lisp
(def x 1)
(print ((fn (y) x) 1)) ; print 1
(set x (lazy (do (print "x") 2))) ; 延時求值, 不可重複定義
x ; print "x", return 2
x ; return 2
(def (f) x)
(def (g x) (f))
(g 1) ; return 2, 閉包
(def (k ...) (apply + ...)) ; 可變長參數
(k 1 2 3) ; return 6
(def (f1 $expr) (do (print "f1") (eval expr))) ; fexpr
(f1 (print "f1,2")) ; print "f1", print "f1,2"
(def define def) ; 一切東西都是函數
(define lambda fn)
(define Y (lambda (f) 
           ((lambda (u) (u u))
            (lambda (g)
                (f (lambda (x) ((g g) x)))))))
((Y (lambda (f)
        (lambda (x)
            (if (= x 0)
                1
                (* x (f (- x 1)))))))
 5) ; return 120
(eval '(print "\n")) ; print new line ; Quote
(+ 0.1 0.2) ; return 0.30000000000000004 ;)
(def (pwr b p) ; 快速幂
  (do
    (def ans 1)
    (while (!= p 0)
           (do
             (if (= (& p 1) 1) ; 位運算
                 (set ans (* ans b))
                 )
             (set b (* b b))
             (set p (shr p 1))
             )
           )
    ans
    )
  )
(pwr 3 6) ; return 729
;快排
  (def (quicksort lst)
    (if (= (. lst __len__) 0)
        '()
        (let ([frist (. lst __getitem__ 0)]
             [rest (split lst 1)])
    (+ (quicksort (filter (fn (x) (< x frist)) rest))
       '(,(do frist))
       (quicksort (filter (fn (x) (>= x frist)) rest)))
    )
  ))
(quicksort '(5 4 46 465 1 8 58 5 41 81 6 84 1 8))
; return '(1, 1, 4, 5, 5, 6, 8, 8, 41, 46, 58, 81, 84, 465)
```
