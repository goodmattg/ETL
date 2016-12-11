data = zeros(3113, length(1960:10:2010));

fname = '../ETL/Population/TR/populationRaw.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*d', '%s', '%s', repmat('%d',[1,6])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for y = 1:6    
    data(:,y) = rawData{y+2};
end

totalPopulationData = struct('y_start',1960,...
                  'y_end',2010, ...
                  'y_increment',10, ...
                  'data',data);
              
save('../ETL/Population/MAT/totalPopulation.mat', 'totalPopulationData')