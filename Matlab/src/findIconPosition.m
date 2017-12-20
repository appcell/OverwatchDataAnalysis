function [leftBorder, rightBorder] = findIconPosition(I)
    iconHeight = size(I, 1);
    edgeI = edge(rgb2gray(I), 'Prewitt', 0.1);
    matZero = zeros(iconHeight, 1);
    edgeIShifted = [matZero, edgeI(:, 1:(end-1))];
    sum1 = sum(edgeIShifted + edgeI);
    sum2 = sum1 > 0.8*iconHeight;
    indArr = find(sum2 == 1);
    if isempty(indArr)
        leftBorder = -1;
        rightBorder = -1;
        return;
    end
    indArr2 =  [indArr, 0] - [0, indArr];
    ind = find(indArr2(2:end-1) >= 30 & (indArr2(2:end-1) <= 40));
    if isempty(ind)
        leftBorder = -1;
        rightBorder = -1;
        return;
    end
    leftBorder = indArr(ind);
    rightBorder = indArr(ind+1);
    
end