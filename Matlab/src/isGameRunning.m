function flag = isGameRunning(oneFrame, charas)
    flag = 0;
    for i=1:size(charas,1)
        if charas{i, 1} ~= "dead" && charas{i, 2}[1] > 0.85
            flag = 1;
        end
    end
    
    topLeftCorner = imcrop(oneFrame,[1,1,70,15]);
    currentStd = max(max(std(double(topLeftCorner))));
    currentMean = mean(double(topLeftCorner(:)));
    if currentStd < 3 && currentMean > 230
        flag = 1;
    else
        flag = 0;
    end
end