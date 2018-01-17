% short script for cutting icons from screenshot
for i=1:28
    filename = "./1 ("+i+").jpg";
    f = imread(convertStringsToChars(filename));
    f2 = imcrop(f, [1722, 45, 48, 33]);
    imwrite(f2, convertStringsToChars("./"+i+".png"));
end