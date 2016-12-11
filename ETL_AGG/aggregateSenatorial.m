clc; clear all; 

dataVectorSize = getCityListSize();

completeDemocrat = zeros(dataVectorSize, length(1984:2:2012));
completeRepublican = zeros(dataVectorSize, length(1984:2:2012));
demVotes = zeros(dataVectorSize, length(1984:2:2012));
repVotes = zeros(dataVectorSize, length(1984:2:2012));

totalVotes = zeros(dataVectorSize, length(1984:2:2012));

for y = 1984:2:2012
    idx = (y-1984)/2+1;
    fname = '../ETL/SenatorialReturns/TR/returnsSenatorial_';
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

senData = struct('y_start',1984,...
                  'y_end',2012, ...
                  'y_increment',2, ...
                  'demPerc',completeDemocrat, ...
                  'repPerc',completeRepublican, ...
                  'totalVotes', totalVotes, ...
                  'States', rawData(1), ...
                  'Counties',rawData(2));

save('../ETL/SenatorialReturns/MAT/senatorialReturns.mat', 'senData')