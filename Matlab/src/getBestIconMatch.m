function res = getBestIconMatch(I, iconsArr)
res = -10;
maxSS = 0;
% figure;imshow(I);

ssArr = zeros(1, size(iconsArr, 2));
for i=1:size(iconsArr, 2)
    Itemp = I;
    icon = iconsArr{i};
    if size(icon,2) < size(I,2)
        diff = size(I,2) - size(icon,2);
        if mod(diff, 2) == 0
            Itemp = Itemp(:, (diff/2)+1:(end-(diff/2)), :);
        else
            Itemp = Itemp(:, floor(diff/2)+1:floor(end-(diff/2)), :);
        end
    elseif size(icon,2) > size(I,2)
        diff = size(icon,2) - size(I,2);
        if mod(diff, 2) == 0
            icon = icon(:, (diff/2)+1:(end-(diff/2)), :);
        else
            icon = icon(:, floor(diff/2)+1:floor(end-(diff/2)), :);
        end       
    end
    ssimval = ssim(Itemp,icon);
    ssArr(i) = ssimval;
    if ssimval > maxSS
        maxSS = ssimval;
        res = i;
    end
end


end