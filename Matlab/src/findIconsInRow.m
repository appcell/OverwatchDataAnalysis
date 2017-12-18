function charas = findIconsInRow(rowNum, Itemp, charaNamesArr, iconsArr)

Iright = imcrop(Itemp, [1145, 110 + (rowNum-1)*35 - 1, 100, 37]);
charaRight = matchIcon(Iright, charaNamesArr, iconsArr);
if charaRight.name == "empty"
    charaLeft = struct('name', "empty", 'pos', [], 'coeff', 0, 'team', 0);
    charas = {charaLeft, charaRight};
else
    Ileft = imcrop(Itemp, [963, 110 + (rowNum-1)*35 - 1, 205, 37]);
    charaLeft = matchIcon(Ileft, charaNamesArr, iconsArr);
    color1 = Itemp(1, 1, :);
    color2 = Itemp(1, 1280, :);
    if charaLeft.name ~= "empty"
        pos = charaLeft.pos(1:2);
        pos = pos - [5 0];
        color = Ileft(pos(2), pos(1), :);
        colorTemp1 = abs(double(color1) - double(color));
        colorTemp2 = abs(double(color2) - double(color));
        diff1 = max(colorTemp1);
        diff2 = max(colorTemp2);
        if diff1 <= diff2
            charaLeft.team = 1;
        else
            charaLeft.team = 2;
        end
    end
    if charaRight.name ~= "empty"
        pos = charaRight.pos(1:2);
        pos = pos + [charaRight.pos(3), 0] + [5 0];
        color = Iright(pos(2), pos(1), :);
        colorTemp1 = abs(double(color1) - double(color));
        colorTemp2 = abs(double(color2) - double(color));
        diff1 = max(colorTemp1);
        diff2 = max(colorTemp2);
        if diff1 <= diff2
            charaRight.team = 1;
        else
            charaRight.team = 2;
        end  
    end
    charas = {charaLeft, charaRight};
end

end

function res = isInImage(pos, w, h)
    res = 0;
    x = pos(1);
    y = pos(2);
    iw = pos(3);
    ih = pos(4);
    if x >= 5 && x <= w ...
            && y >= 0 && y <= h ...
            && x + iw >= 0 && x + iw <= w ...
            && y + ih >= 0 && y + ih <= h
        res = 1;
    end
end

function charas = matchIcon(I, charaNamesArr, iconsArr)
w = size(I, 2);
h = size(I, 1);

totalIconsNum = size(iconsArr, 2);
coeffArr = zeros(totalIconsNum, 1);
posArr = zeros(totalIconsNum, 4);
for i = 1:totalIconsNum
    icon = iconsArr{i};
    icon = imresize(icon,21/size(icon, 1));

    IGreen = I(:,:,2);
    iconGreen = icon(:, :, 2);
    c2 = normxcorr2(normalizeGrayScaleImg(iconGreen),normalizeGrayScaleImg(IGreen));
    c2Max = max(c2(:));
    
%     IRed = I(:,:,1);
%     IBlue = I(:,:,3);
%     iconRed = icon(:, :, 1);
%     iconBlue = icon(:, :, 3);
%     c1 = normxcorr2(normalizeGrayScaleImg(iconRed),normalizeGrayScaleImg(IRed));
%     c3 = normxcorr2(normalizeGrayScaleImg(iconBlue),normalizeGrayScaleImg(IBlue));
%     c1Max = max(c1(:));
%     c3Max = max(c3(:));
%     meanC = (c1Max + c2Max + c3Max) / 3;

    meanC = c2Max;
    [ypeak, xpeak] = find(c2==max(c2(:)));
    
    yoffSet = ypeak - size(icon,1);
    xoffSet = xpeak - size(icon,2);
    if isInImage([xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)], w, h)
        posArr(i, :) = [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)];
        coeffArr(i) = meanC;
    else
        posArr(i, :) = [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)];
        coeffArr(i) = 0;
    end
end

[sortedCoeffs, sortedInds] = sort(coeffArr(:),'descend');
top1 = sortedInds(1:1);
charas = [];
% Choose only top 1 icon
for i = 1:1
    if coeffArr(top1(i)) > 0.65
        charas(i).name = charaNamesArr(top1(i));
        charas(i).pos = posArr(top1(i), :);
        charas(i).coeff = coeffArr(top1(i));
        charas(i).team = 0;
    else
        charas(i).name = "empty";
        charas(i).pos = posArr(top1(i), :);
        charas(i).coeff = coeffArr(top1(i));
        charas(i).team = 0;
    end
end

end