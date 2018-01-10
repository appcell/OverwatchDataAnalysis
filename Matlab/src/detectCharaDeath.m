function deathArr = detectCharaDeath(oneFrame)

deathArr = zeros(1, 12);
%% Left
for i=1:6
    centerX = 59 + (i-1)*71;
    centerY1 = 98;
    centerY2 = centerY1 + 5;
    
    potentialCross1 = imcrop(oneFrame,[centerX-8,centerY1-5,14,10]);
    potentialCross2 = imcrop(oneFrame,[centerX-8,centerY2-5,14,10]);

    if isCrossImg(potentialCross1, oneFrame) || isCrossImg(potentialCross2, oneFrame)
        deathArr(i) = 1;
    end
end

%% Right
for i=7:12
    centerX = 871 + (i-7)*71;
    centerY1 = 98;
    centerY2 = centerY1 + 5; 
    potentialCross1 = imcrop(oneFrame,[centerX-8,centerY1-5,14,10]);
    potentialCross2 = imcrop(oneFrame,[centerX-8,centerY2-5,14,10]);
%     imshow(potentialCross1);
    if isCrossImg(potentialCross1, oneFrame) || isCrossImg(potentialCross2, oneFrame)
        deathArr(i) = 1;
    end
end
end

function res = isCrossImg(img, I)
    w = 9;
    h = 6;
    centerArea = imcrop(img, [w-3, h-3, 6, 6]);
    meanR = mean(mean(centerArea(:, :, 1)));
    meanG = mean(mean(centerArea(:, :, 2)));
    meanB = mean(mean(centerArea(:, :, 3)));
    if (meanR-meanG)>50 && (meanR-meanB)>50 
%     if max(max(std(double(centerArea)))) < 30 && (meanR-meanG)>40 && (meanR-meanB)>40 
        res = 1;
    else
        res = 0;
    end
end