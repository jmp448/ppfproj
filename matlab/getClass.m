function class = getClass(file,row,labels)
    
    DEPT_COL = labels(2);
    NUM_COL = labels(3);
    GRADE_COL = labels(4);
    CREDS_COL = labels(5);
    
    if ~isstring(row)
        row = num2str(row);
    end
    
    deptLoc = strcat(DEPT_COL,row);
    dept = xlrd(file,deptLoc);
    
    numLoc = strcat(NUM_COL,row);
    num = xlsread(file,str2cell(numLoc));
    num = num2str(num);
    
    gradeLoc = strcat(GRADE_COL,row);
    grade = xlrd(file,gradeLoc);
    
    credsLoc = strcat(CREDS_COL,row);
    creds = xlsread(file,str2cell(credsLoc));
    creds = num2str(creds);
    
    class = Class;
    if isempty(dept)
        class.name = "empty row";
    else
        class.name = char(strcat(dept,num));
    end
    class.grade = grade;
    class.creds = creds;
    
end