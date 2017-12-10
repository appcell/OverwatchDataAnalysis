function res = removeBorder(BW)
labels = bwlabel(BW, 4);
res = BW;
w = size(BW, 2);
h = size(BW, 1);
for i = 2:(h-1)
    tbl = tabulate(labels(i, :));
    if size(tbl, 1) < 3
        for j = 1:w
            res(i, j) = 0;
        end
    end
end
end