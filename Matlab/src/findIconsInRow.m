function charas = findIconsInRow(I, charaNamesArr, iconsArr)
totalIconsNum = size(iconsArr, 2);
coeffArr = zeros(totalIconsNum, 1);
posArr = zeros(totalIconsNum, 4);
w = size(I, 2);
h = size(I, 1);
for i = 1:totalIconsNum
    icon = iconsArr{i};
    icon = imresize(icon,17/size(icon, 1));
%     icon = rgb2gray(imresize(icon,17/size(icon, 1)));
    IRed = I(:,:,1);
    IGreen = I(:,:,2);
    IBlue = I(:,:,3);
    iconRed = icon(:, :, 1);
    iconGreen = icon(:, :, 2);
    iconBlue = icon(:, :, 3);
%     I = normalizeGrayScaleImg(I);
%     icon = normalizeGrayScaleImg(icon);
    c1 = normxcorr2(normalizeGrayScaleImg(iconRed),normalizeGrayScaleImg(IRed));
    c2 = normxcorr2(normalizeGrayScaleImg(iconGreen),normalizeGrayScaleImg(IGreen));
    c3 = normxcorr2(normalizeGrayScaleImg(iconBlue),normalizeGrayScaleImg(IBlue));
    c1Max = max(c1(:));
    c2Max = max(c2(:));
    c3Max = max(c3(:));
    meanC = (c1Max + c2Max + c3Max) / 3;
%     imshow(iconRed);figure;imshow(IRed);
    [ypeak, xpeak] = find(c1==max(c1(:)));
    
    yoffSet = ypeak - size(icon,1);
    xoffSet = xpeak - size(icon,2);
    if isInImage([xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)], w, h)
        posArr(i, :) = [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)];
        coeffArr(i) = meanC;
    else
        posArr(i, :) = [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)];
        coeffArr(i) = 0;
    end
    

%     imrect(gca, [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)]);
%     figure
%     imshow(I);
%     imrect(gca, [xoffSet+1, yoffSet+1, size(icon,2) , size(icon,1)]);
end

[sortedCoeffs, sortedInds] = sort(coeffArr(:),'descend');
top2 = sortedInds(1:2);
charas = [];
% Choose only top 2 icons
for i = 1:2
    charas(i).name = charaNamesArr(top2(i));
    charas(i).pos = posArr(top2(i), :);
    charas(i).coeff = coeffArr(top2(i));
%     figure
%     imshow(I);
%     imrect(gca, charas(i).pos);
end

if charas(1).pos(1) > charas(2).pos(1)
    charas([1 2]) = charas([2 1]);
end

end

function res = isInImage(pos, w, h)
    res = 0;
    x = pos(1);
    y = pos(2);
    iw = pos(3);
    ih = pos(4);
    if x > 0 && x< w ...
            && y > 0 && y< h ...
            && x+iw > 0 && x+iw< w ...
            && y+ih > 0 && y+ ih < h
        res = 1;
    end
end