data = zeros(3113, length(1980:10:2010));

fname = '../ETL/PopulationDensity/TR/populationDensityRaw.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*d', '%s', '%s', repmat('%d',[1,4])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for y = 1:4    
    data(:,y) = rawData{y+2};
end

populationDensityData = struct('y_start',1980,...
                  'y_end',2010, ...
                  'y_increment',10, ...
                  'data',data);
              
save('../ETL/PopulationDensity/MAT/populationDensityData.mat', 'populationDensityData')