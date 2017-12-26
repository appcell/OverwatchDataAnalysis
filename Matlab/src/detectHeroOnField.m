function heroOnField = detectHeroOnField(oneFrame)

charaNamesArr = {'ana', 'bastion', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'riptire', 'roadhog', 'soldier76', 'sombra', 'symmetra', 'torbjon', 'tracer', 'widowmaker', 'winston', 'zarya', 'zenyatta'};
iconsArr = {};
iconsArrG ={};
for i=1:size(charaNamesArr, 2)
    icons = (imread(['./../../images/icons/',charaNamesArr{i},'.png']));
    iconsArrG{i} = im2double(rgb2gray(icons));
end

heroOnField = {};

width = 42;
height = 26;


%% Judge Team Left
for i = 1:6
    xmin = 61 + (i-1) * 72;
    ymin = 48;
    heroIcon = imcrop(oneFrame,[xmin,ymin,width,height]);
%     figure
%     imshow(heroIcon)
%     icons = imresize(heroIcon, [30,40]);
    heroIconMatrix = im2double(rgb2gray(imcrop(heroIcon,[13,2,20,20])));

    for j = 1:size(charaNamesArr,2)
        judgeGray(j) = max(max(normxcorr2(normalizeGrayScaleImg(heroIconMatrix),normalizeGrayScaleImg(iconsArrG{j}))));
    end
    [r2,c2] = find(judgeGray == max(judgeGray));
    heroOnField{i} = charaNamesArr{c2};
    
end


%%Judge Team right
for i = 1:6
    xmin = 862 + (i-1) * 72;
    ymin = 48;
    heroIcon = imcrop(oneFrame,[xmin,ymin,width,height]);
%     figure
%     imshow(heroIcon)
%     icons = imresize(heroIcon, [30,40]);
    heroIconMatrix = im2double(rgb2gray(imcrop(heroIcon,[13,2,20,20])));
    for j = 1:size(charaNamesArr,2)
        judgeGray(j) = max(max(normxcorr2(normalizeGrayScaleImg(heroIconMatrix),normalizeGrayScaleImg(iconsArrG{j}))));
    end
    [r2,c2] = find(judgeGray == max(judgeGray));
    heroOnField{i+6} = charaNamesArr{c2};
end

end