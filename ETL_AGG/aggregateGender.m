data = zeros(3113, length(2000:1:2009));

fname = '../ETL/Gender/TR/genderRaw.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*d', '%s', '%s', repmat('%f',[1,10])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for y = 1:10    
    data(:,y) = rawData{y+2};
end

data = data / 100; % convert percentage to decimal

genderData = struct('y_start',2000,...
                  'y_end',2009, ...
                  'y_increment',1, ...
                  'data',data);
             
save('../ETL/Gender/MAT/percentFemale.mat', 'genderData')