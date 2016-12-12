clc; clear all; 

dataVectorSize = getCityListSize();

y_start = 2003; 
y_end = 2013; 
y_inc = 1; 

medianIncome = zeros(dataVectorSize, length(y_start:y_inc:y_end));

for y = y_start:y_inc:y_end
    idx = (y-y_start)+1;
    fname = '../MedianIncome/TR/medianIncome_';
    fileID = fopen( strcat(fname,int2str(y),'.csv'));
    rawData = textscan(fileID,'%s %s %f', 'Delimiter',',','HeaderLines',1);
    medianIncome(:,idx) = rawData{3};
    fclose(fileID); 
end

scaledMedianIncome = medianIncome;

scaledMedianIncome = 0.95*(scaledMedianIncome / max(max(medianIncome))); 

scaledMedianIncome(isnan(scaledMedianIncome)) = 0;

medIncome = struct('y_start',y_start,...
                  'y_end',y_end, ...
                  'y_increment',y_inc, ...
                  'scaledData',scaledMedianIncome, ...
                  'rawData',medianIncome);
             
save('../MedianIncome/MAT/medianIncome.mat', 'medIncome')