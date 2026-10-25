module RomanNumerals exposing (toRoman)


numeralTable : List ( Int, String )
numeralTable =
    [ ( 1000, "M" )
    , ( 900, "CM" )
    , ( 500, "D" )
    , ( 400, "CD" )
    , ( 100, "C" )
    , ( 90, "XC" )
    , ( 50, "L" )
    , ( 40, "XL" )
    , ( 10, "X" )
    , ( 9, "IX" )
    , ( 5, "V" )
    , ( 4, "IV" )
    , ( 1, "I" )
    ]


toRoman : Int -> String
toRoman number =
    toRomanUsing numeralTable number


toRomanUsing : List ( Int, String ) -> Int -> String
toRomanUsing table remaining =
    case table of
        [] ->
            ""

        ( value, symbol ) :: smallerEntries ->
            if remaining >= value then
                symbol ++ toRomanUsing table (remaining - value)

            else
                toRomanUsing smallerEntries remaining
