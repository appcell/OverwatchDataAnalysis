function [ability,assist,assistNum]=assistAndAbility(charaLeft, charaRight,rowNum, Itemp)

% charas(i).name = charaNamesArr(top1(i));
% charas(i).pos = posArr(top1(i), :);
% charas(i).coeff = coeffArr(top1(i));
% charas(i).team = 0;
ability = {"empty",0};
assistNum = 0;

charaNamesArr = {'ana', 'bastion', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier76', 'sombra', 'symmetra', 'torbjon', 'tracer', 'widowmaker', 'winston', 'zarya', 'zenyatta'};


distance = charaRight.pos(1)+1130-(charaLeft.pos(1)+charaLeft.pos(3)+963)-3
assistName = {'ana','genji','junkrat','mccree','mei','mercy','orisa','reinhardt','roadhog','sombra','zarya','zenyatta'};
assistIcon = {};% all 19x28 size
assist = {};
% Ileft = imcrop(Itemp, [963, 110 + (rowNum-1)*35 - 1, 205, 37]);
% Iright = imcrop(Itemp, [1130, 110 + (rowNum-1)*35 - 1, 115, 37]);
I = imcrop(Itemp,[(963+charaLeft.pos(1)+charaLeft.pos(3)),(110+(rowNum-1)*35),distance,37]);
IAbility = imcrop(Itemp,[(965+charaLeft.pos(1)+charaLeft.pos(3)+distance-50),(115+(rowNum-1)*35),26,26]);
% imshow(IAbility);


corr = zeros(12,2);
corr(:,2) = 1:12;


for i = 50:10:160
    if distance>=(i-4) && distance<=(i+4)
        if mod(round(i/10),2)==1        
            ability{1} = "empty";
            ability{2} = 0;
            assistNum = (round(i/10)-3)/2;
        else
            assistNum = (round(i/10)-6)/2;
            ability{1} = charaLeft.name;
            abilityNum =[2,1,4,4,2,3,4,1,2,1,1,2,1,2,1,3,2,2,0,1,1,1,1,2,1,0];
            for j = 1:size(charaNamesArr,2)
                if charaNamesArr{j}==ability{1}
                    ability{2} = abilityNum(1,j);
                    if abilityNum(1,j)~=1 && abilityNum(1,j)~=0
                        abilityCorr = zeros(abilityNum(1,j),2);
                        abilityCorr(:,2) = 1:abilityNum(1,j);
                        corrAb = zeros(abilityNum(j));
                        for k = 1:abilityNum(j)
                            abilityOfHeroT = imread(convertStringsToChars("./../../images/abilities/" + ability{1} + "/"+int2str(k)+".png"));
                            abilityOfHero = double(imresize(abilityOfHeroT,22/size(abilityOfHeroT,2)));
                            corr1 = max(max(normxcorr2(abilityOfHero(:, :, 1),IAbility(:, :, 1))));
                            corr2 = max(max(normxcorr2(abilityOfHero(:, :, 2),IAbility(:, :, 2))));
                            corr3 = max(max(normxcorr2(abilityOfHero(:, :, 3),IAbility(:, :, 3))));
                            abilityCorr(k,1) = corr1 + corr2 + corr3;
                        end
                        abilityCorrSort = sortrows(abilityCorr,1,'descend');
                        ability{2} = abilityCorrSort(1,2);
                    end
                    
                end
            end
        end
        if assistNum~=0
            for j = 1:size(assistName,2)
                assistIcon{j} = (imread(convertStringsToChars("./../../images/assists/"+assistName{j}+'.png')));
                
                for k = 1:assistNum
                    Im = imresize(imcrop(I,[21*(k-1)+7,11,11,17]),28/18);
                    corrT(k) = ssim(Im,assistIcon{j});
                end
                corr(j,1) = max(corrT);
            end
            corrSort = sortrows(corr,1,'descend');
            
            for j = 1:assistNum
                assist{j} = assistName{corrSort(j,2)};
            end
        end
    break; 
    end

end

end
    
    
                