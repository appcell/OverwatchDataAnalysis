clc;
close all;
clear;

%% File read-in
v = VideoReader('./../../videos/1.mp4');
v.CurrentTime = 60;
width = v.Width;
height = v.Height;

%% Elimination evens analysis
charas = getKillEvents(v);
Itemp = readFrame(v);

% === Output ===
imshow(imcrop(Itemp, [800, 202, 355, 104]));
for i = 1:size(charas, 1)
    chara1 = charas(i, 1);
    chara2 = charas(i, 2);
    fprintf('%s eliminated %s (accuracy: %.2f, %.2f)\n', chara1.name, chara2.name, chara1.coeff, chara2.coeff);
end