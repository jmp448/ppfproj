function afterHop = rowHop(curr,hops)
    fin = length(curr);
    afterHopRow = str2double(curr(2:fin))+hops;
    if afterHopRow<1
        error('Problem with row hopping, tried to hop above first row.')
    end
    afterHopRow = num2str(afterHopRow);
    afterHop = strcat(curr(1),afterHopRow);
end