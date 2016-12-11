function [size] = getCityListSize()

fname = '../ETL/CountyLists/masterList.csv';
fileID = fopen(fname);
rawData = textscan(fileID,'%s %s','Delimiter',',','HeaderLines',1);

size = length(rawData{1});
end