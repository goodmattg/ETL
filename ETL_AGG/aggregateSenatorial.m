clc; clear all; 

dataVectorSize = getCityListSize();

y_start = 1984; 
y_end = 2012; 
y_inc = 2; 

completeDemocrat = zeros(dataVectorSize, length(y_start:y_inc:y_end));
completeRepublican = zeros(dataVectorSize, length(y_start:y_inc:y_end));
demVotes = zeros(dataVectorSize, length(y_start:y_inc:y_end));
repVotes = zeros(dataVectorSize, length(y_start:y_inc:y_end));

totalVotes = zeros(dataVectorSize, length(y_start:y_inc:y_end));

for y = y_start:y_inc:y_end
    idx = (y-y_start)/y_inc+1;
    fname = '../SenatorialReturns/TR/returnsSenatorial_';
    fileID = fopen( strcat(fname,int2str(y),'.csv'));
    rawData = textscan(fileID,'%s %s %d %d', 'Delimiter', ',','HeaderLines',1);
    dem = double(rawData{3});
    rep = double(rawData{4});
    tot = double(dem + rep);
    pDem = dem ./ tot; 
    pRep = rep ./ tot;
    completeDemocrat(:,idx) = pDem;
    completeRepublican(:,idx) = pRep;
    demVotes(:,idx) = dem;
    repVotes(:,idx) = rep;
    totalVotes(:,idx) = tot;
    fclose(fileID); 
end

completeRepublican(isnan(completeRepublican) | (completeRepublican == 1)) = 0;
completeDemocrat(isnan(completeDemocrat) | (completeDemocrat == 1)) = 0;

senData = struct('y_start',y_start,...
                  'y_end',y_end, ...
                  'y_increment',y_inc, ...
                  'demPerc',completeDemocrat, ...
                  'repPerc',completeRepublican, ...
                  'totalVotes', totalVotes, ...
                  'States', rawData(1), ...
                  'Counties',rawData(2));

save('../SenatorialReturns/MAT/senatorialReturns.mat', 'senData')