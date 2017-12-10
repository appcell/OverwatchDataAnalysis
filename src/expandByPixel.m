function BW2 = expandByPixel(BW)
    BW2 = zeros(size(BW, 1), size(BW, 2));
    for i=2:size(BW, 1)-1
        for j=2:size(BW, 2)-1
            if BW(i,j) == 1
                BW2(i+1,j) = 1;
                BW2(i-1,j) = 1;
                BW2(i,j+1) = 1;
                BW2(i,j-1) = 1;
            end
        end
    end
end