clc; clear all; 

dataVectorSize = getCityListSize();
y_start = 1960; 
y_end = 2010; 
y_inc = 10; 

numDatasets = length(y_start:y_inc:y_end); 
completeRace = zeros(dataVectorSize, numDatasets);

fname = '../Race/TR/rawRace.csv';
fileID = fopen(fname);
rawData = textscan(fileID,['%*s', '%*s', repmat('%d',[1,numDatasets])], 'Delimiter',',','HeaderLines',1);
fclose(fileID);

for i=1:length(rawData)
    completeRace(:,i) = rawData{i};
end

completeRace(isnan(completeRace) | (completeRace == 1)) = 0;

raceData = struct('y_start',1960,...
                  'y_end',2010, ...
                  'y_increment',10, ...
                  'data',completeRace);
              
save('../Race/MAT/raceData.mat', 'raceData')