module RomanNumeralsTest exposing (suite)

import Expect
import RomanNumerals exposing (toRoman)
import Test exposing (Test, describe, test)


expectRoman : Int -> String -> Test
expectRoman number expected =
    test (String.fromInt number ++ " is " ++ expected) <|
        \_ ->
            Expect.equal expected (toRoman number)


suite : Test
suite =
    describe "toRoman"
        [ describe "repeating I"
            [ expectRoman 1 "I"
            , expectRoman 2 "II"
            , expectRoman 3 "III"
            ]
        , describe "subtracting before V and X"
            [ expectRoman 4 "IV"
            , expectRoman 9 "IX"
            ]
        , describe "adding after V and X"
            [ expectRoman 5 "V"
            , expectRoman 6 "VI"
            , expectRoman 10 "X"
            , expectRoman 14 "XIV"
            ]
        , describe "tens"
            [ expectRoman 40 "XL"
            , expectRoman 49 "XLIX"
            , expectRoman 90 "XC"
            ]
        , describe "hundreds"
            [ expectRoman 400 "CD"
            , expectRoman 900 "CM"
            ]
        , describe "full numbers"
            [ expectRoman 1994 "MCMXCIV"
            , expectRoman 3999 "MMMCMXCIX"
            ]
        ]
