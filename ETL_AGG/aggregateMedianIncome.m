clc; clear all; 

dataVectorSize = getCityListSize();

medianIncome = zeros(dataVectorSize, length(2003:1:2013));

for y = 2003:1:2013
    idx = (y-2003)+1;
    fname = '../ETL/MedianIncome/TR/medianIncome_';
    fileID = fopen( strcat(fname,int2str(y),'.csv'));
    rawData = textscan(fileID,'%s %s %f', 'Delimiter',',','HeaderLines',1);
    medianIncome(:,idx) = rawData{3};
    fclose(fileID); 
end

scaledMedianIncome = medianIncome;

scaledMedianIncome = 0.9*(scaledMedianIncome / max(max(medianIncome))); 

medIncome = struct('y_start',2003,...
                  'y_end',2013, ...
                  'y_increment',1, ...
                  'scaledData',scaledMedianIncome, ...
                  'rawData',medianIncome);
             
save('../ETL/MedianIncome/MAT/medianIncome.mat', 'medIncome')