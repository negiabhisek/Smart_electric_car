t = tcpip('localhost', 7013, 'NetworkRole', 'client');
fopen(t);
pause(2);
a = readfis('car_collision');
try
    while 1
    
        data = fscanf(t);
        num = str2num(data);
        num = num/100;
        %out = cellfun(@str2num, data)
        %class(out)
        output = evalfis(num,a);
        strval = num2str(output);
        fprintf(t,strval);
    end
catch
    fclose(t);
end
fclose(t);