;(deffacts test-uset-sample1
;  (user-context
;    (id u1)
;    (start-location 42)
;    (end-location 43)
;    (preference fastest)
;    (flexibility medium)))

(deffacts test-user-multi-hop
  (user-context
    (id u2)
    (start-location 42)
    (end-location 80)
    (preference fastest)
    (flexibility high))
)

;(deffacts test-user-multi-hop
;  (user-context
;    (id u2)
;    (start-location 42)
;    (end-location 80)
;    (preference cheapest)
;    (flexibility high))
;)

;(deffacts test-user-invalid-transfer
;  (user-context
;    (id u4)
;    (start-location 42)
;    (end-location 42)
;    (preference fastest)
;    (flexibility medium))
;)

;(deffacts user-fastest
;  (user-fastest
;    (preference fastest))
;)

;(deffacts user-cheapest
;  (user-cheapest
;    (preference cheapest))
;)
