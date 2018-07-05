% math1910grade = {'A+'};
% math1910creds = 4;

% boxMath1910creds = 'K12:K12';

% xlswrite('poppj.xlsx',math1910creds,boxMath1910creds)

% [success,message] = copyfile('blankPPF.xlsx','roddyboi.xlsx');

%{
Excel = actxserver ('Excel.Application'); 
File='blankPPF.xlsx';
exist(File,'file') 
if ~exist(File,'file') 
    fprintf('this')
    ExcelWorkbook = Excel.workbooks.Add; 
    ExcelWorkbook.SaveAs(File,1); 
    ExcelWorkbook.Close(false); 
end 
invoke(Excel.workbooks,'Open',File); 
%}

c=[1,2,3];
d=[4,5,6];
e=[c,d];

a = [this,that,other];