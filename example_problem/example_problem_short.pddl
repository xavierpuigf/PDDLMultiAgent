(define (problem setuptable1)
(:domain virtualhome)
(:objects
    plate1 table drawer - object
    kitchen livingroom - room
    char1 - character
)
(:init
    (container drawer)
    (surface table)
    (grabable plate1)
    (inside plate1 drawer)
    (inside drawer kitchen)
    (inside table livingroom)
    (inside char1 livingroom)
)
(:goal
    (ontop plate1 table)
)
)
