function status = readTranscript()
    tic
    % Get column headers
    curr = 'A1';
    tag = xlrd('transcript',curr);
    
    while tag ~= ""
        if tag == "Effdt Primary Name"
            tmp = char(curr);
            NAME_COL = tmp(1);
        elseif tag == "Subject"
            tmp = char(curr);
            DEPT_COL = tmp(1);
        elseif tag == "Catalog Nbr"
            tmp = char(curr);
            NUM_COL = tmp(1);
        elseif tag == "Official Grade"
            tmp = char(curr);
            GRADE_COL = tmp(1);
        elseif tag == "Unt Taken"
            tmp = char(curr);
            CREDS_COL = tmp(1);
        end
        
        curr = columnHop(curr,1);
        tag = xlrd('transcript',curr);
    end
    
    % Create map of course requirements
    labels = [NAME_COL,DEPT_COL,NUM_COL,GRADE_COL,CREDS_COL];
    cm = mapInit();
    
    % Read off classes from transcript
    currRow = 2;
    class = getClass('transcript',currRow,labels);
    while (class.name~="empty row")
        % Record which course requirements are satisfied by the classes
        % taken
        if isKey(cm,class.name) %TODO add conditional for getting the minimum required grade
            reqSat = cm(class.name);
            reqSat.course = class.name;
            reqSat.taken = true;
            reqSat.grade = class.grade;
            reqSat.creds = class.creds;
            cm(class.name)=reqSat;
        end
        currRow = currRow+1;
        class = getClass('transcript',currRow,labels);
    end
    
    classes = values(cm,keys(cm));
    taken = [];
    
    for i=1:numel(classes)
        course = classes{i};
        course
        if course.taken == true
            fprintf('%s was satisfied by %s \n',course.req,course.course);
            taken = [taken course];
        end
    end
    toc
end