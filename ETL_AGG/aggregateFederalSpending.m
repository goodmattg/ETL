data = zeros(3113, length(1983:1:2010));

fname = '../ETL/FederalSpending/TR/rawFederalSpending.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*d', '%s', '%s', repmat('%d',[1,28])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for y = 1:28    
    data(:,y) = rawData{y+2};
end

federalSpendingData = struct('y_start',1983,...
                  'y_end',2010, ...
                  'y_increment',1, ...
                  'data',data);
             
save('../ETL/FederalSpending/MAT/federalSpending.mat', 'federalSpendingData')