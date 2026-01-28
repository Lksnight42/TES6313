(deffacts base-transports
  (transport
    (id car)
    (type car)
    (avg-speed 60)
    (capacity 4)
    (cost-per-km 0.6)
    (flexibility high)
    (has-service no)
  ) 

  (transport
    (id motorcycle)
    (type motorcycle)
    (avg-speed 70)
    (capacity 2)
    (cost-per-km 0.4)
    (flexibility very-high)
    (has-service no)
  ) 

  (transport
    (id bus)
    (type bus)
    (avg-speed 40)
    (capacity 40)
    (cost-per-km 0.25)
    (flexibility low)
    (has-service yes)
  ) 


  (transport
    (id walk)
    (type walk)
    (avg-speed 5)
    (capacity 1)
    (cost-per-km 0)
    (flexibility very-high)
    (has-service no)
  ) 
  (transport
    (id mrt)
    (type mrt)
    (avg-speed 50)
    (capacity 800)
    (cost-per-km 0.05)
    (flexibility medium)
    (has-service yes)
  ) 
)

; test fact instances

;(traffic
;  (location-id A)
;  (congestion-level high)
;  (accident no))

