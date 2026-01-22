(defrule ping
  =>
  (assert (delog
            (level TRACE)
            (source system)
            (message "Ping rule fired")
            (ref-id none)))
)

; route
(defrule edge-to-route-by-transport
  (edge 
    (from ?a)
    (to ?b)
    (distance ?d)
    (allowed-transport $?ats))
  (transport 
    (id ?mode)
    (avg-speed ?spd)
    (cost-per-km ?cpk))
    (test (member$ ?mode $?ats))
=>
  (assert (route
            (id (gensym*))
            (start-location ?a)
            (end-location ?b)
            (mode ?mode)
            (service none)
            (distance ?d)
            (base-time (* (/ ?d ?spd) 60)); km/ (km/h) -> hour -> minutes
            (base-cost (* ?d ?cpk)))))

(defrule edge-to-route-by-transport-reverse
  (edge 
    (from ?a)
    (to ?b)
    (distance ?d)
    (allowed-transport $?ats))
  (transport 
    (id ?mode)
    (avg-speed ?spd)
    (cost-per-km ?cpk))
    (test (member$ ?mode $?ats))
=>
  (assert (route
            (id (gensym*))
            (start-location ?b)
            (end-location ?a)
            (mode ?mode)
            (service none)
            (distance ?d)
            (base-time (* (/ ?d ?spd) 60)); km/ (km/h) -> hour -> minutes
            (base-cost (* ?d ?cpk)))))

; route evaluation
(defrule evaluate-route-basis
  (route
    (id ?rid)
    (base-time ?t)
    (base-cost ?c))
=>
  (assert (route-evaluation
            (route-id ?rid)
            (estimated-time ?t)
            (estimated-cost ?c)
            (risk-level low)
            (score (- 100 (+ ?t ?c))))))

; traffic congestion
(defrule traffic-congestion-penalty
  ?re <- (route-evaluation
           (route-id ?rid)
           (estimated-time ?t)
           (score ?s))
  (route (id ?rid) (start-location ?loc))
  (traffic (location-id ?loc) (congestion-level high))
=>
  (modify ?re
    (estimated-time (+ ?t 10))
    (score (- ?s 10))
    (risk-level medium)))

(defrule traffic-accident-high-risk
  ?re <- (route-evaluation
           (route-id ?rid)
           (score ?s))
  (route (id ?rid) (start-location ?loc))
  (traffic (location-id ?loc) (accident yes))
=>
  (modify ?re
    (risk-level high)
    (score (- ?s 30))))

; stations-service
(defrule expand-to-stations-service
  (line
    (mode ?m)
    (service ?s)
    (stations $? ?loc $?))
  (not
    (stations-service
      (location ?loc)
      (mode ?m)
      (service ?s)))
=>
  (assert
    (stations-service
      (location ?loc)
      (mode ?m)
      (service ?s))))


; transfer 
(defrule transfer-to-route
; (phase (name ready))
  (transfer
    (location ?loc)
    (from-mode ?m1)
    (from-service ?s1)
    (to-mode ?m2)
    (to-service ?s2)
    (time ?t))

  (stations-service
    (location ?loc)
    (mode ?m1)
    (service ?s1))
  (stations-service
    (location ?loc)
    (mode ?m2)
    (service ?s2))
=>
  (assert
    (route
      (id (gensym*))
      (start-location ?loc)
      (end-location ?loc)
      (mode ?m2)
      (service ?s2)
      (distance 0)
      (base-time ?t)
      (base-cost 0)))
  (assert
    (route
      (id (gensym*))
      (start-location ?loc)
      (end-location ?loc)
      (mode ?m1)
      (service ?s1)
      (distance 0)
      (base-time ?t)
      (base-cost 0))))





