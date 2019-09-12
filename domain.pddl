(define (domain virtualhome)

(:types table sit tv stove microwave)
(:predicates 
    (facing ?x ?y)
    (ontop ?x ?y)
    (inside ?x ?y)
    (on ?x)
    (open ?x)
    (hot ?x)
    (sitting ?x - sit)
    (grabbed ?x)
    (found ?x)
    (facing ?x ?y)
    (close ?x)
    (free ?x)
    
    (sittable ?x)
    (room ?x)
    (grabbable ?x)
    (surface ?x)
)

(:action walk
 :parameters
    (?x)
 :precondition
    (or
	(room ?x)
	(found ?x)
    )
  :postcondtion:
    (close ?x))

(:action grab
 :parameters
    (?x)
 :precondition
    (and (not (grabbed ?x))
	 (close ?x)
	 (grababble ?x))
  :postcondtion
    (grabbed ?x))


(:action put 
 :parameters
    (?x ?y)
 :precondition
    (and (grabbed ?x)
	 (close ?y)
	 (surface ?y))
  :postcondtion
    (not grabbed ?x)
    (ontop ?x ?y))
