function y = circleOrSquare(region)
% Here the idea is: if border parts of bounding box is not occupied enough,
% then the region is not square.

x0 = ceil(region.BoundingBox(1));
y0 = ceil(region.BoundingBox(2));
h = region.BoundingBox(4);
w = region.BoundingBox(3);
tempImg = zeros(h, w);
tempImgWithBorder = zeros(h, w);
for i = 1:size(region.PixelList, 1)
    x = region.PixelList(i, 1) - x0 + 1;
    y = region.PixelList(i, 2) - y0 + 1;
    tempImg(y, x) = 1;
end
for j = 1:w
    tempImgWithBorder(1, j) = 1;
    tempImgWithBorder(h, j) = 1;
end
for i = 1:h
    tempImgWithBorder(i, 1) = 1;
    tempImgWithBorder(i, w) = 1;
end

cnt = sum(sum(tempImgWithBorder.*tempImg));
total = sum(sum(tempImgWithBorder));

y = (cnt/total) > 0.5; % If true: square; false: circle.

end