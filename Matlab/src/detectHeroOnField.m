function [heroOnField,heroDeath] = detectHeroOnField(oneFrame)

charaNamesArr = {'ana', 'bastion', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'riptire', 'roadhog', 'soldier76', 'sombra', 'symmetra', 'torbjon', 'tracer', 'widowmaker', 'winston', 'zarya', 'zenyatta'};
iconsArr = {};
iconsArrG ={};
for i=1:size(charaNamesArr, 2)
    iconsArr{i} = im2double(imresize(imread([charaNamesArr{i},'.png']), [30,40]));
    iconsArrG{i} = im2double(rgb2gray(imresize(imread([charaNamesArr{i},'.png']), [30,40])));
end


k1 = 1;

%% get the pca for each RGB matrix
% for i = 1:size(charaNamesArr,2)
%     
%     for j = 1:k1
%     %% R
%         iconR = iconsArr{i}(:,:,1);
%         [COEFF, SCORE] = pca(iconR);
%         pcaR{i}(:,j) = COEFF(:,j)./sqrt(sum(COEFF(:,j).^2));
%     %% G
%         iconG = iconsArr{i}(:,:,2);
%         [COEFF, SCORE] = pca(iconG);
%         pcaG{i}(:,j) = COEFF(:,j)./sqrt(sum(COEFF(:,j).^2));
%     %% B
%         iconB = iconsArr{i}(:,:,3);
%         [COEFF, SCORE] = pca(iconB);
%         pcaB{i}(:,j) = COEFF(:,j)./sqrt(sum(COEFF(:,j).^2));
%     end
% 
% end

for i = 1:size(charaNamesArr,2)
    %% R
    iconR = iconsArr{i}(:,:,1);
    meanR(1,i) = sum(sum(iconR)')/1200;
    %% G
    iconG = iconsArr{i}(:,:,2);
    meanG(1,i) = sum(sum(iconG)')/1200;
    %% B
    iconB = iconsArr{i}(:,:,3);
    meanB(1,i) = sum(sum(iconB)')/1200;
end

% k2 = 1;
% 
% for i = 1:size(charaNamesArr,2)    
%     for j = 1:k2
%         icon = iconsArrG{i};
%         [COEFF, SCORE] = pca(icon);
%         pcaGray{i}(:,j) = COEFF(:,j)./sqrt(sum(COEFF(:,j).^2));
%     end
% end
for i = 1:size(charaNamesArr,2)    
    iconGray = iconsArrG{i};
    meanGray(1,i) = sum(sum(iconGray)')/1200;
end

heroOnField = {};
heroDeath = 12;

width = 42;
height = 26;

for i = 1:6
    xmin = 62 + (i-1) * 72;
    ymin = 48;
    heroIcon = imcrop(oneFrame,[xmin,ymin,width,height]);
%     figure
%     imshow(heroIcon)
    heroIconMatrix = im2double(imresize(heroIcon, [30,40]));
    heroIconR = sum(sum(heroIconMatrix(:,:,1))')/1200;
    heroIconG = sum(sum(heroIconMatrix(:,:,2))')/1200;
    heroIconB = sum(sum(heroIconMatrix(:,:,3))')/1200;
    heroIconGray = sum(sum(im2double(rgb2gray(imresize(heroIcon, [30,40]))))')/1200;
    
    judgeMeanR = abs(heroIconR*ones(1,size(charaNamesArr,2)) - meanR);
    judgeMeanG = abs(heroIconG*ones(1,size(charaNamesArr,2)) - meanG);
    judgeMeanB = abs(heroIconB*ones(1,size(charaNamesArr,2)) - meanB);
    judgeMeanGray = abs(heroIconGray*ones(1,size(charaNamesArr,2)) - meanGray);
    
    judgeRGB = judgeMeanR + judgeMeanG + judgeMeanB;
    
    [r1,c1] = find(judgeRGB == min(judgeRGB));
    [r2,c2] = find(judgeMeanGray == min(judgeMeanGray));
    heroOnField{i} = charaNamesArr{c2};
    
%     if judgeMeanGray(c2)*3 <judgeRGB(c1)
%         heroOnField{i} = charaNamesArr{c2};
%         heroDeath(i) = 1;
%     else
%         heroOnField{i} = charaNamesArr{c1};
%     end

end

for i = 1:6
    xmin = 862 + (i-1) * 72;
    ymin = 48;
    heroIcon = imcrop(oneFrame,[xmin,ymin,width,height]);
%     figure
%     imshow(heroIcon)
    heroIconMatrix = im2double(imresize(heroIcon, [30,40]));
    heroIconR = sum(sum(heroIconMatrix(:,:,1))')/1200;
    heroIconG = sum(sum(heroIconMatrix(:,:,2))')/1200;
    heroIconB = sum(sum(heroIconMatrix(:,:,3))')/1200;
    heroIconGray = sum(sum(im2double(rgb2gray(imresize(heroIcon, [30,40]))))')/1200;
    
    judgeMeanR = abs(heroIconR*ones(1,size(charaNamesArr,2)) - meanR);
    judgeMeanG = abs(heroIconG*ones(1,size(charaNamesArr,2)) - meanG);
    judgeMeanB = abs(heroIconB*ones(1,size(charaNamesArr,2)) - meanB);
    judgeMeanGray = abs(heroIconGray*ones(1,size(charaNamesArr,2)) - meanGray);
    
    judgeRGB = judgeMeanR + judgeMeanG + judgeMeanB;
    
    [r1,c1] = find(judgeRGB == min(judgeRGB));
    [r2,c2] = find(judgeMeanGray == min(judgeMeanGray));
    heroOnField{i+6} = charaNamesArr{c2};
%     
%     if judgeMeanGray(c2)*3 <judgeRGB(c1)
%         heroOnField{i+6} = charaNamesArr{c2};
%         heroDeath(i+6) = 1;
%     else
%         heroOnField{i+6} = charaNamesArr{c1};
%     end
end


% AC = zeros(i,j);
% 
% for i = 1:size(charaNamesArr,2)
%     for j = 1:size(charaNamesArr,2)
%         for m = 1:k
%         AC(i,j) = abs(pcaR{i}(:,m)'*pcaR{j}(:,m)) + abs(pcaG{i}(:,m)'*pcaG{j}(:,m)) + abs(pcaB{i}(:,m)'*pcaB{j}(:,m));
%         end
%     end
% end
% 
% AC
% 
% for i = 1:size(charaNamesArr,2)
%     AC(i,i) = 0;
% end
% 
% 
% max(AC)
meanR
meanG
meanB
meanGray
end