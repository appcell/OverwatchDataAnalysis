skillNum =[2,1,4,4,2,3,4,1,2,1,1,2,1,2,1,3,2,2,1,1,1,1,2,1];
charaNamesArr = {'ana', 'bastion', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier', 'symmetra', 'torbjon', 'tracer', 'widowmaker', 'winston', 'zarya'};

boundary=4;
for i =1:24
    for j = 1:skillNum(i)
        [icon, map, alpha] =  imread([charaNamesArr{i},'/',num2str(j),'.png']);
        l1 = size(icon,1);
        l2 = size(icon,2);
        alpha = ones(l1,l2);
        for m = 1:l1
            for n = 1:l2
                if abs(double(icon(m,n,1))-77)<boundary && abs(double(icon(m,n,2))-92)<boundary && abs(double(icon(m,n,3))-123)<boundary
                    icon(m,n,1)=0;
                    icon(m,n,2)=0;
                    icon(m,n,3)=0;
                    alpha(m,n)=0;
                end
            end
        end
        imwrite(icon,[charaNamesArr{i},'/',num2str(j),'t.png'],'Alpha',alpha);

    end
end
