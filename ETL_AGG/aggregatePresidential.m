clc; clear all; 

dataVectorSize = getCityListSize();

completeDemocrat = zeros(dataVectorSize, length(1984:4:2012));
completeRepublican = zeros(dataVectorSize, length(1984:4:2012));
demVotes = zeros(dataVectorSize, length(1984:4:2012));
repVotes = zeros(dataVectorSize, length(1984:4:2012));

totalVotes = zeros(dataVectorSize, length(1984:4:2012));

for y = 1984:4:2012
    idx = (y-1984)/4+1;
    fname = '../PresidentialReturns/TR/presidentialReturns_';
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

presData = struct('y_start',1984,...
                  'y_end',2012, ...
                  'y_increment',4, ...
                  'demPerc',completeDemocrat, ...
                  'repPerc',completeRepublican, ...
                  'totalVotes', totalVotes, ...
                  'States', rawData(1), ...
                  'Counties',rawData(2));

save('../ETL/PresidentialReturns/MAT/presidentialReturns.mat', 'presData')