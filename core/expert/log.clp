(defrule system-started
 =>
 (assert (delog
    (level INFO)
    (source system)
    (message "engine started")
    (ref-id null)))
)

(defrule breathing 
=>
  (assert (delog
            (level TRACE)
            (source system)
            (message "breathing")
            (ref-id null)
  ))
)
; location debug
(defrule location-loaded
  (location (id ?id) (level ?lv1))
=>
  (assert (delog
            (level TRACE)
            (source loader)
            (message "Location loaded")
            (ref-id ?id)))
)


(defrule location-has-parent
  (location (id ?id) (parent ?p))
=>
  (assert (delog
            (level TRACE)
            (source system)
            (message "location has parent")
            (ref-id ?id)))
)

(defrule invalid-location-level
  (location (id ?id) (level ?lv1&:(not (member$ ?lv1 (create$ region city area node)))))
=>
  (assert (delog
            (level ERROR)
            (source system)
            (message "Invalid location level")
            (ref-id ?id)))
)
; transport
(defrule transport-loaded
  (transport (id ?tid))
=>
  (assert
    (delog
      (level TRACE)
      (source system)
      (message "Transport loaded")
      (ref-id ?tid))))

; edge 
(defrule edge-loaded
  (edge (from ?f) (to ?t))
=> 
  (assert (delog
            (level TRACE)
            (source loader)
            (message "Edge loaded")
            (ref-id (str-cat ?f "->" ?t)))))

(defrule edge-without-transport
  (edge
    (from ?f)
    (to ?t)
    (allowed-transport $?at&:(= (length$ $?at) 0)))
=>
  (assert
    (delog
      (level ERROR)
      (source system)
      (message "Edge has no allowed transport")
      (ref-id (str-cat ?f "->" ?t))
    )
  )
)
(defrule edge-invalid-transport
  (edge
    (from ?f)
    (to ?t)
    (allowed-transport $?ats))
  (test
    (not
      (subsetp
        $?ats
        (create$ car bus mrt walk motorcycle))))
=>
  (assert
    (delog
      (level ERROR)
      (source system)
      (message "Edge contains invalid transport type")
      (ref-id (str-cat ?f "->" ?t))
    )
  )
)
(defrule edge-invalid-distance
  (edge (from ?f) (to ?t) (distance ?d&:(<= ?d 0)))
=>
  (assert
    (delog
      (level ERROR)
      (source system)
      (message "Edge distance must be positive")
      (ref-id (str-cat ?f "->" ?t))
    )
  )
)

(defrule edge-from-location-missing
  (edge (from ?f))
  (not (location (id ?f)))
=>
  (assert
    (delog
      (level ERROR)
      (source system)
      (message "Edge 'from' location not found")
      (ref-id ?f)
    )
  )
)
(defrule edge-to-location-missing
  (edge (to ?t))
  (not (location (id ?t)))
=>
  (assert
    (delog
      (level ERROR)
      (source system)
      (message "Edge 'to' location not found")
      (ref-id ?t)
    )
  )
)

; route
(defrule route-created
  (route (id ?rid) (mode ?m))
=>
  (assert (delog
    (level INFO)
    (source rule)
    (message "Route created")
    (ref-id (str-cat ?rid ":" ?m)))))

(defrule best-route
  (route-evaluation (route-id ?rid) (score ?s))
  (not (route-evaluation (score ?s2&:(> ?s2 ?s))))
=>
  (assert (delog
    (level INFO)
    (source system)
    (message "Best route selected")
    (ref-id ?rid))))

; route evaluation
(defrule route-evaluation-start
  (route (id ?rid))
  (not (route-evaluation (route-id ?rid)))
=>
  (assert (delog
    (level DEBUG)
    (source rule)
    (message "Evaluating route")
    (ref-id ?rid))))

(defrule route-evaluation-created
  (route-evaluation
    (route-id ?rid)
    (score ?s)
    (estimated-time ?t)
    (estimated-cost ?c))
=>
  (assert (delog
    (level INFO)
    (source rule)
    (message
      (str-cat "Route evaluated: score="
                ?s ", time=" ?t ", cost=" ?c))
    (ref-id ?rid))))

; traffic
(defrule traffic-congestion-triggered
  (route-evaluation (route-id ?rid))
  (route (id ?rid) (start-location ?loc))
  (traffic (location-id ?loc) (congestion-level high))
=>
  (assert (delog
    (level WARN)
    (source system)
    (message "Traffic congestion penalty applied")
    (ref-id ?rid))))

(defrule traffic-accident-triggered
  (route-evaluation (route-id ?rid))
  (route (id ?rid) (start-location ?loc))
  (traffic (location-id ?loc) (accident yes))
=>
  (assert (delog
    (level ERROR)
    (source system)
    (message "Traffic accident detected, risk elevated")
    (ref-id ?rid))))

; line
(defrule line-loaded
  (line
    (mode ?m)
    (service ?s)
    (stations $?stops))
=>
  (assert
    (delog
      (level TRACE)
      (source line)
      (message
        (str-cat
          "[LOAD][LINE] "
          ?m " / " ?s
          " stations=" (length$ ?stops)))
      (ref-id ?s))))

; station-service
(defrule station-service-loaded
  (stations-service
    (location ?loc)
    (mode ?m)
    (service ?s))
=>
  (assert
    (delog
      (level INFO)
      (source station-service)
      (message
        (str-cat
          "[STATION][SERVICE] "
          " Location id under " ?m " service " ?s))
      (ref-id ?loc))))

(defrule transfer-defined
  (transfer 
    (location ?loc)
    (from-mode ?m1)
    (from-service ?s1)
    (to-mode ?m2)
    (to-service ?s2)
    (time ?t))
=>
  (assert
    (delog
      (level TRACE)
      (source transfer)
      (message
        (str-cat
          "[TRANSFER][DEFINE] at "
          ?loc ": "
          ?m1 "/" ?s1 " <-> "
          ?m2 "/" ?s2
          " time=" ?t))
      (ref-id ?loc))))

(defrule transfer-route-created
  (route
    (start-location ?loc)
    (end-location ?loc)
    (distance 0)
    (mode ?m)
    (service ?s))
=>
  (assert
    (delog
      (level INFO)
      (source route)
      (message
        (str-cat
          "[ROUTE][TRANSFER][CREATED] at "
          ?loc " switch to "
          ?m "/" ?s))
      (ref-id ?loc))))

(defrule invalid-transfer-service
  (phase (name ready))
  (transfer
    (location ?loc)
    (to-mode ?m)
    (to-service ?s))
  (not
    (stations-service
      (location ?loc)
      (mode ?m)
      (service ?s)))
=>
  (assert
    (delog
      (level ERROR)
      (source transfer)
      (message
        (str-cat
          "[TRANSFER][ERROR] "
          ?loc " has no service "
          ?m "/" ?s))
      (ref-id ?loc))))
; user-context

(defrule user-context-loaded
  (user-context
    (id ?uid)
    (start-location ?s)
    (end-location ?e))
=>
  (assert
    (delog
      (level INFO)
      (source user)
      (message
        (str-cat
          "[USER][CONTEXT] request loaded: "
          ?s " -> " ?e))
      (ref-id ?uid))))


; metric
(defrule metric-created
  (route-metric (route-id ?rid))
=>
  (assert
    (delog
      (level TRACE)
      (source metric)
      (message (str-cat "metric created for route " ?rid))
      (ref-id ?rid))))

(defrule policy-selected
  (scoring-policy (policy-id ?pid))
=>
  (assert
    (delog
      (level INFO)
      (source policy)
      (message (str-cat "scoring policy selected: " ?pid))
      (ref-id ?pid))))

(defrule final-score
  (route-evaluation
    (route-id ?rid)
    (score ?s))
    (estimated-time ?t)
    (estimated-cost ?c)
=>
  (assert
    (delog
      (level INFO)
      (source scoring)
      (message
      (str-cat "Route evaluated: score="
                ?s ", time=" ?t ", cost=" ?c))
      (ref-id ?rid))))

 




;=============================
;           ABANDON
;=============================
;(defrule edge-invalid-base-time
;  (edge (from ?f) (to ?t) (base-time ?t0&:(<= ?t0 0)))
;=>
;  (assert
;    (delog
;      (level ERROR)
;      (source system)
;      (message "Edge base-time must be positive")
;      (ref-id (str-cat ?f "->" ?t))
;    )
;  )
;)

