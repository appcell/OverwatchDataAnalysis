function res = normalizeGrayScaleImg(I)
res = double(I);
m = mean(I(:));
res = res - m;
tmp = double(I);
s = std(tmp(:));
res = res / s;

maxV = max(res(:));
minV = min(res(:));
res = (res - minV) / (maxV - minV);
minV2 = min(res(:));

end