t = tcpip('localhost', 7016, 'NetworkRole', 'client');
fopen(t);
pause(2);
'Start'
a = readfis('car_collision_paper_alternate_change');
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
    'closed'
    fclose(t);
end