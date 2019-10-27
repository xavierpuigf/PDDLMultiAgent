(define (problem setuptable1)
(:domain virtualhome)
(:objects
    a1
    plate1 plate2 plate3 table drawer - object
    kitchen livingroom - room
    char1 - character
)
(:init
    (container drawer)
    (surface table)
    (grabable plate1)
    (grabable plate2)
    (grabable plate3)
    (ontop plate1 drawer)
    (inside plate2 drawer)
    (inside plate3 drawer)
    (inside drawer kitchen)
    (inside table livingroom)
    (inside char1 livingroom)
)
(:goal
    (and (observable char1 plate1) (close char1 plate1))
)
)
