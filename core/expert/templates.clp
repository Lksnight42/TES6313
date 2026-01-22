(deftemplate transport
    (slot id)
    (slot type)
    (slot avg-speed)
    (slot capacity)
    (slot cost-per-km)
    (slot flexibility)
    (slot has-service); yes / no
)

(deftemplate location
    (slot id)
    (slot name)
    (slot level); region / city / area / node
    (slot parent)
)

(deftemplate edge
    (slot from)
    (slot to)
    (multislot allowed-transport)
    (slot distance)
)

(deftemplate route
    (slot id)
    (slot start-location)
    (slot end-location)
    (slot mode)
    (slot service); optional: line / route-id / null
    (slot distance); km
    (slot base-time); minutes
    (slot base-cost); RM
)


(deftemplate transfer
  (slot location)
  (slot from-mode); transport type
  (slot from-service); line-id / route / none
  (slot to-mode)
  (slot to-service)
  (slot time)
)

(deftemplate traffic
    (slot location-id)
    (slot congestion-level); low / medium / high
    (slot accident); yes / no
    (slot peak-hour); yes / no
)

(deftemplate user
    (slot id)
    (slot start-location)
    (slot end-location)
    (slot preference); fastest / cheapest 
    (slot budget-limit); optional
    (slot avoid); traffic / transfer / night
    (slot flexibility); low / medium / high
)

; rule system interface
(deftemplate route-evaluation
    (slot route-id)
    (slot score)
    (slot estimated-time)
    (slot estimated-cost)
    (slot risk-level)
)

(deftemplate line
  (slot mode)
  (slot service)
  (multislot stations)
)

(deftemplate stations-service
    (slot location)
    (slot mode)
    (slot service)
)

(deftemplate time-context
    (slot time-of-day); morning / evening / night
    (slot day-type); weekday/ weekeed
    (slot urgency); low /medium / high
)

(deftemplate delog
  (slot level)        ; TRACE / DEBUG / INFO / WARN / ERROR
  (slot source)       ; loader / rule / system / user
  (slot message)      ; human-readable text
  (slot ref-id)       ; optional: location-id / rule-name / etc
)

(deftemplate phase(slot name))

; uncertainty(optional)
(deftemplate weather
    (slot location-id)
    (slot condition); clear /rain / storm
    (slot severity); low /medium / high
    (slot uncertainty); 0.0 - 1.0
)

