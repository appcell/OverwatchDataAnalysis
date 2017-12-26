function reply = replayOrNot(oneFrame)

Itemp = rgb2gray(imcrop(oneFrame,[62,100,78,80]));

replyIcon = rgb2gray(imread(['./../../images/','reply.png']));

replyIndex = max(max(normxcorr2(normalizeGrayScaleImg(replyIcon),normalizeGrayScaleImg(Itemp))));

if replyIndex > 0.9
    reply = 1;
else 
    reply = 0;
end

end

