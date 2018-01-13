function [charas, ability, assist] = findIconsInRow(rowNum, Itemp, charaNamesArr, iconsArr)

Ileft = imcrop(Itemp, [963, 110 + (rowNum-1)*35 - 1, 205, 37]);
Iright = imcrop(Itemp, [1130, 110 + (rowNum-1)*35 - 1, 115, 37]);


charaRight = matchIcon(Iright, charaNamesArr, iconsArr);
if charaRight.name == "empty"
    charaLeft = struct('name', "empty", 'pos', [], 'coeff', 0, 'team', 0);
    charas = {charaLeft, charaRight};
else
    charaLeft = matchIcon(Ileft, charaNamesArr, iconsArr);
    color1 = Itemp(1, 1, :);
    color2 = Itemp(1, 1280, :);
    if charaLeft.name ~= "empty"
        pos = charaLeft.pos(1:2);
        pos = pos - [5 0];
        color = double(Ileft(pos(2), pos(1), :));
        colorTemp1 = abs(double(color1) - (color + mean(color1) - mean(color)));
        colorTemp2 = abs(double(color2) - (color + mean(color2) - mean(color)));
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
        pos = pos + [charaRight.pos(3), 0] + [5 1];
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
%% Postprocess: remove potential empty rows
    Iright = imcrop(Iright, charaRight.pos + [-5 0 10 0]);
    Ileft = imcrop(Ileft, charaLeft.pos + [-5 0 10 0]);
    filledRight = edge(rgb2gray(Iright), 'Prewitt', 0.1);
    filledLeft = edge(rgb2gray(Ileft), 'Prewitt', 0.1);
    % If an recognition is valid, there must be large vertical gradient lines
    % on its left & right sides.
    sumLeft1 = sum(sum(filledLeft(:,1:7)) > (0.3*charaLeft.pos(4)));
    sumLeft2 = sum(sum(filledLeft(:,end-7:end)) > (0.3*charaLeft.pos(4)));
    if ~(sumLeft1 >= 1 && sumLeft2 >= 1)
        charaLeft.name = "empty";
    end
    
    sumRight1 = sum(sum(filledRight(:,1:5)) > (0.3*charaRight.pos(4)));
    sumRight2 = sum(sum(filledRight(:,end-5:end)) > (0.3*charaRight.pos(4)));
    if ~(sumRight1 >= 1 && sumRight2 >= 1)
        charaRight.name = "empty";
    end
    charas = {charaLeft, charaRight};
    
%%  To find the assist and ability  
    if (charaRight.pos(1)+1130-(charaLeft.pos(1)+charaLeft.pos(3)+963)>45)
        [ability,assist,assistNum]=assistAndAbility(charaLeft, charaRight,rowNum, Itemp);
    else
        ability ={"empty",0}; %the first item is hero's Name, second is ability id
        assistNum = 0;
        assist = {"empty","empty","empty","empty","empty"};
    end
    
    
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
%     imshow(edge(rgb2gray(icon), 'Prewitt', 0.1));

    % Why green? Because with other channels D.Va cannot get recognized.
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