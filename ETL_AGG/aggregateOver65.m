data = zeros(3113, length(2000:1:2009));

fname = '../ETL/Age/TR/agePlus65Raw.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*d', '%s', '%s', repmat('%f',[1,10])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for y = 1:10    
    data(:,y) = rawData{y+2};
end

data = data / 100; % convert percentage to decimal

ageData = struct('y_start',2000,...
                  'y_end',2009, ...
                  'y_increment',1, ...
                  'data',data);
             
save('../ETL/Age/MAT/percentOver65.mat', 'ageData')