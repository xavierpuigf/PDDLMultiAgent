(define (domain virtualhome)
(:requirements :typing :action-costs :negative-preconditions :fluents)


(:types character room object)
(:predicates

    ; States objects
    (on ?x - object)
    (open ?x - object)
    (hot ?x - object)
    (free ?x - object) 
    
    ; Character has something to do
    (sitting ?z - character ?x - object)
    (grabbed ?z - character ?x - object)
    (found ?z - character ?x - object)
    (observable ?z - character ?x)
    
    ; Object relationships
    (close ?x ?y - object)
    (facing ?x ?y - object)
    (inside ?x ?y - object)
    (ontop ?x ?y - object)

    ; Attributes objects can have
    (grabable ?x - object)
    (sittable ?x - object)
    (surface ?x - object)
    (container ?x - object)
)

(:action walk
 :parameters (
    ?room_arg - room
    ?char_arg - character
 )
 :effect
    (and (inside ?char_arg ?room_arg)
	; We are not in another room anymore
	(forall (?other_room - room)
		(when (not (= ?other_room ?room_arg)) 
		      (not (inside ?char_arg ?other_room))))
	; If we are in a room, everything in the room is observable
	(forall (?y - object)
	    (when (and (inside ?y ?room_arg) 
		       (not (forall (?container - object) 
				    (and (container ?container)
					 (inside ?y ?container) 
					 (open ?container)))))
		  (observable ?char_arg ?y)
	    )
	)
	; Everything out of the room is not observable anymore
	; Note. Except for what we are grabbing
	(forall (?y - object)
	    (when (and (not (inside ?y ?room_arg)) (not (grabbed ?char_arg ?y)))
		  (and (not (observable ?char_arg ?y))
		       (not (close ?char_arg ?y))
		  )
	    )
	)
    )
)

(:action walk
 :parameters (
    ?obj_arg - object
    ?char_arg - character
 )
 :precondition
    (observable ?char_arg ?obj_arg)
  :effect
    ; Note: this planner does not consider that you may also be close 
    ; to other objects, hopefully the RL system should learn that
    (and 
	(close ?char_arg ?obj_arg)
	(forall (?other_obj - object)
		(when (or (ontop ?obj_arg ?other_obj) (inside ?obj_arg ?other_obj))
		      (close ?char_arg ?other_obj))
	)
	(found ?char_arg ?obj_arg)
	; If we are in a room, everything in the room is observable
    )
)

(:action grab
 :parameters (
    ?obj - object
    ?char_arg - character
 )
 :precondition
    (and (not (grabbed ?char_arg ?obj))
	 (found ?char_arg  ?obj)
	 (close ?char_arg ?obj)
	 (grabable ?obj))
  :effect
    (and (grabbed ?char_arg ?obj) 
	 (forall (?obj_dest - object) 
		 (when (or (inside ?obj ?obj_dest) (ontop ?obj ?obj_dest))
		       (and (not (inside ?obj ?obj_dest)) (not (ontop ?obj ?obj_dest)))
		 )
	 )
    )
)


(:action put 
 :parameters (
    ?object_grabbed ?object_dest - object
    ?char_arg - character
    )
 :precondition
    (and (grabbed ?char_arg ?object_grabbed)
	 (close ?char_arg ?object_dest)
	 (found ?char_arg ?object_dest)
	 (or (surface ?object_dest) (container ?object_dest))
     )
  :effect
    (and 
	(not (grabbed ?char_arg ?object_grabbed))
	(ontop ?object_grabbed ?object_dest)
    )
)


(:action putin 
 :parameters (
    ?object_grabbed ?object_dest - object
    ?char_arg - character
    )
 :precondition
    (and (grabbed ?char_arg ?object_grabbed)
	 (close ?char_arg ?object_dest)
	 (found ?char_arg ?object_dest)
	 (and (container ?object_dest) (open ?object_dest))
     )
  :effect
    (and (not (grabbed ?char_arg ?object_grabbed))
    (inside ?object_grabbed ?object_dest)
    )
)


(:action open 
 :parameters (
    ?object_dest - object
    ?char_arg - character
 )
 :precondition
    (and (close ?char_arg ?object_dest)
	 (found ?char_arg ?object_dest)
	 (and (container ?object_dest) (not (open ?object_dest)))
     )
  :effect
    (and (open ?object_dest)
	 (forall (?obj - object)
		 (when (inside ?obj ?object_dest) (observable ?char_arg ?obj))
	 )
    )
)

(:action close
 :parameters (
    ?object_dest - object
    ?char_arg - character
 )
 :precondition
    (and (close ?char_arg ?object_dest)
	 (found ?char_arg ?object_dest)
	 (and (container ?object_dest) (open ?object_dest))
     )
  :effect
    (and (not (open ?object_dest))
	 (forall (?obj - object)
		 (when (inside ?obj ?object_dest) (not (observable ?char_arg ?obj)))
	 )
     )
)


(:action standup
 :parameters (
    ?from_sit - object
    ?char_arg - character
 )
 :precondition
    (sitting ?char_arg ?from_sit)
 :effect
    (not (sitting ?char_arg ?from_sit))
)
)
