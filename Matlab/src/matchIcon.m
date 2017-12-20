function charas = matchIcon(I, charaNamesArr, iconsArr)
w = size(I, 2);
h = size(I, 1);
Itemp = I;
totalIconsNum = size(iconsArr, 2);
coeffArr = zeros(totalIconsNum, 1);
posArr = zeros(totalIconsNum, 4);
for i = 1:totalIconsNum
    icon = iconsArr{i};
    IGreen = Itemp(:,:,2);
    iconGreen = icon(:, :, 2);
    if size(iconGreen,2) < size(IGreen,2)
        diff = size(IGreen,2) - size(iconGreen,2);
        if mod(diff, 2) == 0
            IGreen = IGreen(:, (diff/2)+1:(end-(diff/2)), :);
        else
            IGreen = IGreen(:, floor(diff/2)+1:floor(end-(diff/2)), :);
        end
    elseif size(iconGreen,2) > size(IGreen,2)
        diff = size(iconGreen,2) - size(IGreen,2);
        if mod(diff, 2) == 0
            iconGreen = iconGreen(:, (diff/2)+1:(end-(diff/2)), :);
        else
            iconGreen = iconGreen(:, floor(diff/2)+1:floor(end-(diff/2)), :);
        end       
    end
    
    
    
    
    c2 = normxcorr2(normalizeGrayScaleImg(iconGreen),normalizeGrayScaleImg(IGreen));
    c2Max = max(c2(:));


    meanC = c2Max;
    [ypeak, xpeak] = find(c2==max(c2(:)));
    
    yoffSet = ypeak - size(icon,1);
    xoffSet = xpeak - size(icon,2);
%     if isInImage([xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)], w, h)
        posArr(i, :) = [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)];
        coeffArr(i) = meanC;
%     else
%         posArr(i, :) = [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)];
%         coeffArr(i) = 0;
%     end
end
[sortedCoeffs, sortedInds] = sort(coeffArr(:),'descend');
top1 = sortedInds(1:1);
charas = [];
% Choose only top 1 icon
for i = 1:1
    if coeffArr(top1(i)) > 0.65
        charas(i).name = charaNamesArr(top1(i));
        charas(i).coeff = coeffArr(top1(i));
        charas(i).team = 0;
    else
        charas(i).name = "empty";
        charas(i).coeff = coeffArr(top1(i));
        charas(i).team = 0;
    end
end

end