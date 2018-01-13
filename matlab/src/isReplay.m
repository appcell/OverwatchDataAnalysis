function replay = isReplay(oneFrame)

Itemp = rgb2gray(imcrop(oneFrame,[62,100,78,80]));

replayIcon = rgb2gray(imread(['./../../images/','replay.png']));

replayIndex = max(max(normxcorr2(normalizeGrayScaleImg(replayIcon),normalizeGrayScaleImg(Itemp))));

if replayIndex > 0.9
    replay = 1;
else 
    replay = 0;
end

end

