function charas = findIcons(rowNum, Itemp, charaNamesArr, iconsArr)
    iconHeight = 22;
    charaLeft = struct;
    charaRight = struct;
    Ileft = imcrop(Itemp, [963, 110 + (rowNum-1)*35 + 1 + (35-21)/2, 205, 21]);
    Iright = imcrop(Itemp, [1130, 110 + (rowNum-1)*35 + 1 + (35-21)/2, 115, 21]);  
    
    %% right
    [borderRight1, borderRight2] = findIconPosition(Iright);
    if borderRight1(1) == -1
        charaRight.name = "empty";
        charas = {struct('name',"empty"), struct('name', "empty")};
        return;
    end
    charaRightMaxCoeff = 0;
    for i=1:size(borderRight1, 2) % in case several borders are found
        border1 = borderRight1(i);
        border2 = borderRight2(i);
        iconRight = imcrop(Iright, [border1, 0, border2-border1, iconHeight]);
        tempCharaRight = matchIcon(iconRight, charaNamesArr, iconsArr);
        if tempCharaRight.coeff > charaRightMaxCoeff
            tempCharaRight.pos = [border1, 1, border2-border1, iconHeight];
            charaRight = tempCharaRight;
        end
    end
    


    %% left
    [borderLeft1, borderLeft2] = findIconPosition(Ileft);
    if borderLeft1(1) == -1
        charaLeft.name = "empty";
    else
        charaLeftMaxCoeff = 0;
        for i=1:size(borderLeft1, 2) % in case several borders are found
            border1 = borderLeft1(i);
            border2 = borderLeft2(i);
            iconLeft = imcrop(Ileft, [border1, 0, border2-border1, iconHeight]);
            tempCharaLeft = matchIcon(iconLeft, charaNamesArr, iconsArr);
            if tempCharaLeft.coeff > charaLeftMaxCoeff
                tempCharaLeft.pos = [border1, 1, border2-border1, iconHeight];
                charaLeft = tempCharaLeft;
            end
        end
    end
    

    %% Recognize team
    color1 = Itemp(1, 1, :);
    color2 = Itemp(1, 1280, :);
    if charaLeft.name ~= "empty"
        pos = charaLeft.pos(1:2);
        pos = pos - [5 0];
        color = double(Ileft(pos(2), pos(1), :));
        colorTemp1 = abs(double(color1) - ((mean(color1) - mean(color)) + color));
        colorTemp2 = abs(double(color2) - ((mean(color2) - mean(color)) + color));
        diff1 = max(colorTemp1);
        diff2 = max(colorTemp2);
        if diff1 <= diff2
            charaLeft.team = 1;
        else
            charaLeft.team = 2;
        end
    end
    if charaRight.name ~= "empty"
        pos = charaRight.pos(1:2);
        pos = pos + [charaRight.pos(3), 0] + [5 0];
        color = Iright(pos(2), pos(1), :);
        colorTemp1 = abs(double(color1) - double(color));
        colorTemp2 = abs(double(color2) - double(color));
        diff1 = max(colorTemp1);
        diff2 = max(colorTemp2);
        if diff1 <= diff2
            charaRight.team = 1;
        else
            charaRight.team = 2;
        end  
    end
    charas = {charaLeft, charaRight};
end