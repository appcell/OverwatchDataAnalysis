function heroList = getHeroList(heroOnField, teamContent)

heroList = teamContent;

for i = 1:12
    if teamContent(i).team == 1
        for j = 1:6
            if strcmp(heroOnField{j},teamContent(i).name)
                heroList(i).playerId = j;
                break;
            end
        end
    else
        for j = 7:12
            if strcmp(heroOnField{j},teamContent(i).name)
                heroList(i).playerId = j;
                break;
            end
        end
    end
end

end
