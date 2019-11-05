(define (problem setuptable1)
(:domain virtualhome)
(:objects
    plate1, plate2, plate3, table drawer - object
    kitchen livingroom - room
    char1 - character
)
(:init
    (= (objects_grabbed) 0)
    (container drawer)
    (surface table)
    (grabable plate1)
    (grabable plate2)
    (grabable plate3)
    (inside plate1 drawer)
    (inside plate2 drawer)
    (inside plate3 drawer)
    (inside drawer kitchen)
    (inside table livingroom)
    (inside char1 livingroom)
)
(:goal
    (and (ontop plate1 table) (ontop plate3 table))
)
)
