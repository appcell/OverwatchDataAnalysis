function charas = getKillEvents(v)
Itemp = readFrame(v);

%% Icons read-in
charaNamesArr = ["ana", "bastion", "doomfist", "dva", "genji", "hanzo", "junkrat", "lucio", "mccree", "mei", "mercy", "moira", "orisa", "pharah", "reaper", "reinhardt", "riptire", "roadhog", "soldier76", "sombra", "symmetra", "torbjon", "tracer", "widowmaker", "winston", "zarya", "zenyatta", "meka", "shield", "supercharger", "teleporter", "turret"];
iconsArr = {};
for i=1:size(charaNamesArr, 2)
    iconsArr{i} = imread(convertStringsToChars("./../../images/icons/" + charaNamesArr(i) + ".png"));
end

%% Comparison by row, each row is 30px, 4 rows at most
charas = struct('name',{},'pos',{}, 'coeff',{});
for i = 1:4
    Irow = imcrop(Itemp, [800, 202 + (i-1)*26 - 1, 355, 28]);
    charasRow = findIconsInRow(Irow, charaNamesArr, iconsArr);
    charas(end+1, 1) = charasRow(1);
    charas(end, 2) = charasRow(2);
end

%% Output
% imshow(imcrop(Itemp, [800, 202, 355, 104]));
% for i = 1:size(charas, 1)
%     chara1 = charas(i, 1);
%     chara2 = charas(i, 2);
%     fprintf('%s, %f; %s, %f\n', chara1.name, chara1.coeff, chara2.name, chara2.coeff);
% end

end
