t = tcpip('localhost', 50004, 'NetworkRole', 'client');
fopen(t);
pause(2);
a = readfis('E:\Project\2016\Coding\Lidar_mapping_using_python\Fuzzy\Try1\socket_programming\car_collision');
try
    while 1
    
        data = fscanf(t);
        num = str2num(data);
        num = num/100
        %out = cellfun(@str2num, data)
        %class(out)
        output = evalfis(num,a)
        fprintf(t,output)
    end
catch
    fclose(t);
end