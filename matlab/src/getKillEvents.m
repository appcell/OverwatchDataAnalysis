function charas = getKillEvents(Itemp, eventList, charaNamesArr, iconsArr)

%% Comparison by row, each row is 30px, 4 rows at most
charas = {};
if size(eventList, 1) > 1
    for i = 1:6
        charasRow = findIconsInRow(i, Itemp, charaNamesArr, iconsArr);
        lastChara1 = eventList{end, 1};
        lastChara2 = eventList{end, 2};
        if charasRow{1}.name == "empty" && charasRow{2}.name == "empty" && i>1
            break;
        end
        if charasRow{1}.name == lastChara1.name && charasRow{2}.name == lastChara2.name...
                && charasRow{1}.team == lastChara1.team && charasRow{2}.team == lastChara2.team...
            break;
        end
        charas{end+1, 1} = charasRow{1};
        charas{end, 2} = charasRow{2};

    end
else
    for i = 1:6
        [charasRow, ability, assist] = findIconsInRow(i, Itemp, charaNamesArr, iconsArr);
        charas{end+1, 1} = charasRow{1};
        charas{end, 2} = charasRow{2};
        charas{end, 3} = ability;
        charas{end, 4} = assist;
        if charasRow{1}.name == "empty" && charasRow{2}.name == "empty" && i>1
            break;
        end
    end
end


%% Output
% imshow(Itemp);
% for i = 1:size(charas, 1)
%     chara1 = charas(i, 1);
%     chara2 = charas(i, 2);
%     fprintf('%s, %f; %s, %f\n', chara1.name, chara1.coeff, chara2.name, chara2.coeff);
% end

end
