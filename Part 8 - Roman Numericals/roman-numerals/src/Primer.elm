module Primer exposing (describeNumber, double, doubleAll, firstOrZero, sumAll)


doublingFactor : Int
doublingFactor =
    2


double : Int -> Int
double number =
    number * doublingFactor


describeNumber : Int -> String
describeNumber number =
    if number < 0 then
        "negative"

    else if number == 0 then
        "zero"

    else
        "positive"


doubleAll : List Int -> List Int
doubleAll numbers =
    List.map double numbers


sumAll : List Int -> Int
sumAll numbers =
    case numbers of
        [] ->
            0

        first :: rest ->
            first + sumAll rest


firstOrZero : List Int -> Int
firstOrZero numbers =
    List.head numbers |> Maybe.withDefault 0