function heroOnField = detectHeroOnField(oneFrame)

charaNamesArr = {'ana', 'bastion', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier76', 'sombra', 'symmetra', 'torbjon', 'tracer', 'widowmaker', 'winston', 'zarya', 'zenyatta'};
iconsArr = {};
iconsArrG ={};
for i=1:size(charaNamesArr, 2)
    [icon, map, alpha] = imread(['./../../images/charas/',charaNamesArr{i},'.png']);
    icon = imresize(icon, 1280/1920);
    alpha = imresize(alpha, 1280/1920);
    alpha2 = zeros(size(alpha, 1), size(alpha, 2), 3);
    alpha2(:, :, 1) = alpha;
    alpha2(:, :, 2) = alpha;
    alpha2(:, :, 3) = alpha;
    iconsArrG{i, 1} = double(icon);
    iconsArrG{i, 2} = double(alpha2);
end

heroOnField = {};
width = 38;
height = 30;

%% Left
teamColor = oneFrame(1, 1, :);
bgimage = zeros(25, 32, 3);
bgimage(:, :, 1) = teamColor(1);
bgimage(:, :, 2) = teamColor(2);
bgimage(:, :, 3) = teamColor(3);
bgimage = double(bgimage);

for i = 1:6
    xmin = 62 + (i-1) * 71;
    ymin = 48;
    heroIcon = imcrop(oneFrame,[xmin,ymin,width,height]);
    for j = 1:size(charaNamesArr,2)
        icon = iconsArrG{j, 1};
        alpha = iconsArrG{j, 2};
        fusedIcon = uint8(icon.*(alpha/255) + bgimage.*((255-alpha)/255));
        corr1 = max(max(normxcorr2(fusedIcon(:, :, 1),heroIcon(:, :, 1))));
        corr2 = max(max(normxcorr2(fusedIcon(:, :, 2),heroIcon(:, :, 2))));
        corr3 = max(max(normxcorr2(fusedIcon(:, :, 3),heroIcon(:, :, 3))));
        corr = (corr1 + corr2 + corr3)/3;
        judgeGray(j) = corr;
    end
    [r2,c2] = find(judgeGray == max(judgeGray));
    heroOnField{i} = charaNamesArr{c2};
end

%% right
teamColor = oneFrame(1, 1280, :);
bgimage = zeros(25, 32, 3);
bgimage(:, :, 1) = teamColor(1);
bgimage(:, :, 2) = teamColor(2);
bgimage(:, :, 3) = teamColor(3);
bgimage = double(bgimage);

for i = 1:6
    xmin = 857 + (i-1) * 71;
    ymin = 48;
    heroIcon = imcrop(oneFrame,[xmin,ymin,width,height]);
    for j = 1:size(charaNamesArr,2)
        icon = iconsArrG{j, 1};
        alpha = iconsArrG{j, 2};
        fusedIcon = uint8(icon.*(alpha/255) + bgimage.*((255-alpha)/255));
        corr1 = max(max(normxcorr2(fusedIcon(:, :, 1),heroIcon(:, :, 1))));
        corr2 = max(max(normxcorr2(fusedIcon(:, :, 2),heroIcon(:, :, 2))));
        corr3 = max(max(normxcorr2(fusedIcon(:, :, 3),heroIcon(:, :, 3))));
        corr = (corr1 + corr2 + corr3)/3;
        judgeGray(j) = corr;        
    end
    [r2,c2] = find(judgeGray == max(judgeGray));
    heroOnField{i+6} = charaNamesArr{c2};
end

end