function out = xlrd(file,this)
    [~,out]=xlsread(file,str2cell(this));
    out = string(out);
end