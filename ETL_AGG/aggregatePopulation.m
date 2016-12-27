clc; clear all; 

dataVectorSize = getCityListSize();
y_start = 1960; 
y_end = 2010; 
y_inc = 10; 

numDatasets = length(y_start:y_inc:y_end); 
completePopulation = zeros(dataVectorSize, numDatasets);

fname = '../Population/TR/rawPopulation.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*s', '%*s', repmat('%d',[1,numDatasets])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for i=1:length(rawData)
    completePopulation(:,i) = rawData{i};
end

completePopulation(isnan(completePopulation) | (completePopulation == 1)) = 0;

popData = struct('y_start',1960,...
                  'y_end',2010, ...
                  'y_increment',10, ...
                  'data',completePopulation);
              
save('../Population/MAT/populationData.mat', 'popData')