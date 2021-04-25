
; computes the nth fibonacci number, where n starts at 0
(def (fib n)
  (if (= n 0)
    1
    (if (= n 1)
      1
      (+ (fib (- n 1)) (fib (- n 2))))))

(fib 7)