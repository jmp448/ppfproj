function letter = addLetter(curr,num)
    letterMap = containers.Map({'A' 'B' 'C' 'D' 'E' 'F' 'G' 'H' 'I' 'J' 'K' 'L' 'M' 'N' 'O' 'P' 'Q' 'R' 'S' 'T' 'U' 'V' 'W' 'X' 'Y' 'Z'}, ...
        [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26]);
    
    ans = letterMap(convertStringsToChars(curr))+num;
    
    if ~((ans > 1) && (ans < 27))
        error('Problem with column hopping. Tried to go to the left of A or the right of Z');
    end
    
    alphabet = convertCharsToStrings(keys(letterMap));
    letter = alphabet(ans);
    
end