% This function hops between columns in an excel spreadsheet

% Input:
% curr: the current cell, as a string
% hops: the number of hops to the right that are desired.  If the desired
%       hop is to the left, then make the number negative

% Output: the cell that is the desired number of hops away from curr, as a
%         string
% Example: columnHop('H13',-2) will return 'F13'
%          columnHop('A2',3) will return 'D2'

function afterHop = columnHop(curr,hops)
    if isstring(curr)
        curr = char(curr);
    end
    afterHopCol = addLetter(curr(1),hops);
    fin = length(curr);
    afterHop = strcat(afterHopCol,curr(2:fin));
end
