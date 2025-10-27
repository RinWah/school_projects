; coding comments

; common lisp function named myList which creates a list that has 
; (4 (7 22) "art" ("math" (8) 99) 100) and returns it
(defun myList()
    (list 4 (list 7 22) "art" (list "math" (list 8) 99) 100))

; common lisp function named leap year which takes no required parameters
; and returns an ordered list containing all leap years from 1800 through 2025.
; the list of leapyears must be calculated, no points will be given for a 
; hard-coded list.
(defun leapYear (&optional (start 1800) (end 2025) (leaps '()))
  (if (> start end)
      (reverse leaps) ; reverse list so it's in order when printed out
      (let* ((divisible-by-4   (zerop (mod start 4))) ; multiple of 4
             (divisible-by-100 (zerop (mod start 100))) ; multiple of 100
             (divisible-by-400 (zerop (mod start 400))) ; multiple of 400
             (is-leap (or (and divisible-by-4 (not divisible-by-100)) 
                          divisible-by-400))) ; gregorian, ok by 4 not by 100
        (leapYear (1+ start) end ; recursive call to defun again
                  (if is-leap (cons start leaps) leaps)))) ; if leap year, add to leaps, if not don't change it. 
)

; takes two list parameters. returns a single list which contains the separate unique entities from both lists, 
; w. no dupes.
; not allowed to use predefined union function.
; cons means to add to beginning of list, so reverse and then add to keep everything in order.
(defun union- (list-one list-two &optional (combo '())) ; uses - so that it doesn't use union built in
    (if (and (null list-one) (null list-two)) ;stops when both inputs are fully traversed
    (reverse combo) ; again reverse list so it's in order when printed out
    (if (null list-one) ; if it's empty only go to list-two only
        (let ((x (car list-two))) ; put x to the beginning of list-two
            (union- NIL (cdr list-two) ; go through all of list-two while keeping list=one at null/false
                (if (member x combo :test #'equal) combo (cons x combo)))) ; if x is already there, keep combo, 
                ; otherwise cons x
        (let ((x (car list-one))) ; otherwise if list-one also has stuff, bind x to the beginning here too
            (union- (cdr list-one) list-two ; go through all of list one and leave list two by itself
                (if (member x combo :test #'equal) combo (cons x combo)))))) ; cons x to combo as well just like ^
)

; give mean of numbers in aList or return NIL
(defun avg (aList &optional (sum 0) (count 0)) 
    (if (null aList) ;stop when list is empty
        (if (zerop count) NIL (/ sum count)) ;stop when count is 0 and find avg by sum/count
        (avg (cdr aList) (+ sum (car aList)) (1+ count)))
)

;true if data type matches what it's supposed to be, otherwise false.
(defun isType (dataType)
    (lambda (value) (typep value dataType))
)

;params limit rate values
;limit rate nums
;values list
;return list with same elements and order of values except element that is greater than limit is multiplied
;by rate
;assume all elements in values list are numbers
;bonus: tail recursive +5 points
(defun taxCalculator (limit rate values &optional (taxes '())) 
    (if (null values) ;no numbers left
    (reverse taxes) ;original list ordering
    (let* ((x (car values)) ;get first num and set it to x
        (y (if (> x limit) (* x rate) x))) ;if x > limit, multiply y w. rate for tax, 
        ;otherwise leave price. 
        (taxCalculator limit rate (cdr values) (cons y taxes)))) ;tail recursive, bonus 
        ;points. basically put y item in front 
        ;of list.
)

;clean list of sublists
;clean sublists
;any empty sublists get deleted
(defun clean (aFunc aList &optional (acc '()))
  (if (null aList) ;when list is empty
      (reverse acc) ;reverse original order
      (let ((x (car aList))) ;x to first element of list
        (if (listp x) ;if x is a list in a list
            (clean aFunc (cdr aList) (cons (clean aFunc x) acc)) ;clean sublist, put 
            ;sublist back into main list, tail recursion to beginning of list
            (if (funcall aFunc x) ;if x isn't a list in a list, see if you need it
                (clean aFunc (cdr aList) (cons x acc)) ;if it's not empty, keep it
                (clean aFunc (cdr aList) acc)))))) ;delete x

;basically if else but three ways with no cond
(defmacro threeWayBranch (x y z)
  `(if ,(car x) ;look at x
       (progn ,@(cdr x)) ;take everything but x
       (if ,(car y) ;if x is NIL, look at y
           (progn ,@(cdr y)) ;if y is true, do y
           (if ,(car z) ;if y is NIL, look at z
               (progn ,@(cdr z)) ;do z if true
               nil)))) ;if none are true just return NIL (false)


