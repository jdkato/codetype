# let square x = x * x;;
val square : int -> int = <fun>
# square 3;;
- : int = 9
# let rec fact x =
    if x <= 1 then 1 else x * fact (x - 1);;
val fact : int -> int = <fun>
# fact 5;;
- : int = 120
# square 120;;
- : int = 14400