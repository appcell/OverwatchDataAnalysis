
close all;
clear;

%% File read-in
v = VideoReader('./../../videos/1.mp4');
% Icons read-in
charaNamesArr = ["ana", "bastion", "doomfist", "dva", "genji", "hanzo", "junkrat", "lucio", "mccree", "mei", "mercy", "moira", "orisa", "pharah", "reaper", "reinhardt", "riptire", "roadhog", "soldier76", "sombra", "symmetra", "torbjon", "tracer", "widowmaker", "winston", "zarya", "zenyatta", "meka", "shield", "supercharger", "teleporter", "turret"];
iconsArr = {};
iconHeight = 22;
for i=1:size(charaNamesArr, 2)
    icon = imread(convertStringsToChars("./../../images/icons/" + charaNamesArr(i) + ".png"));
    iconsArr{i} = imresize(icon,iconHeight/size(icon, 1));
end
v.CurrentTime = 10;
Itemp = readFrame(v);
Itemp = imresize(Itemp, 1280/size(Itemp, 2)); % Rescale to width = 1280, currently consider 16:9 only
% figure;imshow(Itemp);

tic;
for rowNum = 1:6
    Ileft = imcrop(Itemp, [963, 110 + (rowNum-1)*35 + 1 + (35-21)/2, 205, 22]);
    Iright = imcrop(Itemp, [1130, 110 + (rowNum-1)*35 + 1 + (35-21)/2, 115, 22]);
    % left
    chara1 = struct;
    chara2 = struct;
    [borderLeft1, borderLeft2] = findIconPosition(Ileft);
    if borderLeft1 ~= -1
        iconLeft = imcrop(Ileft, [borderLeft1, 0, borderLeft2-borderLeft1, iconHeight]);
        chara1 = matchIcon(iconLeft, charaNamesArr, iconsArr);
    else
        chara1.name = "empty";
    end
    
    % right
    [borderRight1, borderRight2] = findIconPosition(Iright);
    if borderRight1 ~= -1
        iconRight = imcrop(Iright, [borderRight1, 0, borderRight2-borderRight1, iconHeight]);
        chara2 = matchIcon(iconRight, charaNamesArr, iconsArr);
    else
        chara2.name = "empty";
    end
    
    if chara1.name == "empty" && chara2.name == "empty" && rowNum > 1
        break;
    end
end
toc