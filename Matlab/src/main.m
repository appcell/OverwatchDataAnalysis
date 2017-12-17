clc;
close all;
clear;

%% File read-in
v = VideoReader('./../../videos/1.mp4');
v.CurrentTime = 219;
width = v.Width;
height = v.Height;
Itemp = readFrame(v);
% Only top-right corner is of interest for now
I = imcrop(Itemp, [800, 200, 355, 166]);
Gx = [-1 1];
Gy = Gx';
Igray = rgb2gray(I);
%Igray = adapthisteq(Igray, 'clipLimit', 0.6, 'Distribution', 'exponential');

%% Another gradient computation for edge detection
red = I(:,:,1);
green = I(:,:,2);
blue = I(:,:,3);
[Gmag,Gdir] = imgradient(red, 'prewitt');
maxx = max(Gmag(:));
TGmag = (Gmag > 0.2*maxx).*Gmag;
TGmag = imfill(TGmag, 'holes');
TGmag = bwareaopen(TGmag, 300, 8);

% Preprocess: remove small objs. (Somehow bwareaopen doesn't work well, thus has to customize)
TGmag = removeSmallObj(TGmag, 300, 1.0, 5.0);
BW = removeBorder(TGmag);
BW = bwareaopen(BW, 50);
BWExpanded = expandByPixel(BW);
% Display intermediate results
figure
imshowpair(I, label2rgb(bwlabel(BW, 4)), 'montage');
figure
%imshowpair(I, TGmag, 'montage');
imshowpair(I, Igray, 'montage');

%% Process each labelled obj. One obj could be either container or avatar itself, or skill icon.
regionsTemp = regionprops(BW,'Area', 'BoundingBox','PixelList');
avatars = [];
skills = [];
containers = [];
NR = numel(regionsTemp);
for k = 1:NR
    area = prod(regionsTemp(k).BoundingBox(3:4));
    if area > 500 % Region is valid if area > 500
        if regionsTemp(k).BoundingBox(3) > 50
            containers = [containers; regionsTemp(k)];
        elseif circleOrSquare(regionsTemp(k))
            avatars = [avatars; regionsTemp(k)];
        else
            skills = [skills; regionsTemp(k)];
        end     
    end
end


% %% Comparison & matching between video & given chara avatars
% % Not finished. Leave for later use
% % square   = rgb2gray(imread('../images/rectangle.png'));
% % c = normxcorr2(square, BW);
% % figure, surf(c), shading flat
% % [ypeak, xpeak] = find(c==max(c(:)));
% % yoffSet = ypeak-size(square,1);
% % xoffSet = xpeak-size(square,2);
% 
% %% Record all potential corners
% % corners = [];
% % lines = [];
% 
% %% Find horizontal/vertical lines with Hough
% [HVertical,TVertical,RVertical] = hough(BW, 'Theta',-2:2);
% rotateAngle = 33; % Since Hough doesn't work with horizontal lines well, rotation needed
% BWRotate = imrotate(BW, rotateAngle);
% [HHorizontal,THorizontal,RHorizontal] = hough(BWRotate, 'Theta', (90-rotateAngle-2):(90-rotateAngle+2));
% PVertical  = houghpeaks(HVertical,50,'threshold',ceil(0.1*max(HVertical(:))));
% PHorizontal  = houghpeaks(HHorizontal,50,'threshold',ceil(0.1*max(HHorizontal(:))));
% linesVertical = houghlines(BW,TVertical,RVertical,PVertical,'FillGap',3,'MinLength',15);
% linesHorizontal = houghlines(BWRotate,THorizontal,RHorizontal,PHorizontal,'FillGap',3,'MinLength',15);
% 
% % Rotate back?
% % Not finished. I forget rotation etc
% rotateMatrix = [cosd(rotateAngle) -sind(rotateAngle); sind(rotateAngle) cosd(rotateAngle)];
% m = size(BWRotate,2)/2;     % width/2
% n = size(BWRotate,1)/2;    % height/2
% first = [1 0 -m; 0 1 -n; 0 0 1];
% third = [1 0 m; 0 1 n; 0 0 1];
% second = [cosd(rotateAngle) -sind(rotateAngle) 0; sind(rotateAngle) cosd(rotateAngle) 0; 0 0 1];
% 
% % Show horizontal lines
% % figure, imshow(BW), hold on
% for k = 1:length(linesHorizontal)
%    lineLength = norm(linesHorizontal(k).point1 - linesHorizontal(k).point2);
%    xy = [linesHorizontal(k).point1; linesHorizontal(k).point2];
%    point1 =  xy(1,:);
%    point2 =  xy(2,:);
%    point1 = third*second*first * [point1';1];
%    point2 = third*second*first * [point2';1];
%    point1 = point1 - [8 n/2+10 1]';
%    point2 = point2 - [8 n/2+10 1]';
%    if lineLength < 30
%        corners = [corners; point1(1:2,1)'];
%        lines = [lines; point1(1:2,1)' point2(1:2,1)'];
% %        plot([point1(1,1),point2(1,1)] ,[point1(2,1),point2(2,1)],'LineWidth',2,'Color','green');
% %        plot(point1(1,1), point1(2,1),'x','LineWidth',2,'Color','yellow');
% %        plot(point2(1,1), point2(2,1),'x','LineWidth',2,'Color','red');
%    end
% end
% 
% figure, imshow(BW), hold on
% for k = 1:length(linesVertical)
%    lineLength = norm(linesVertical(k).point1 - linesVertical(k).point2);
%    xy = [linesVertical(k).point1; linesVertical(k).point2];
%    point1 =  xy(1,:);
%    point2 =  xy(2,:);
%    
%    if lineLength < 30
%        corners = [corners; point1; point2];
%        lines = [lines; point1,point2];
%        plot(xy(:,1), xy(:,2),'LineWidth',2,'Color','green');
%        plot(point1(1,1), point1(1,2),'x','LineWidth',2,'Color','yellow');
%        plot(point2(1,1), point2(1,2),'x','LineWidth',2,'Color','red');
%    end
% end
% 
% %% Find corner points with Harris, result seems noisy tho.
% C = detectHarrisFeatures(Igray, 'MinQuality', 0.1, 'FilterSize', 7);
% % figure
% % imshow(Igray);
% % hold on
% % plot(C.selectStrongest(10));
% CCorners = C.selectStrongest(80);
% for k = 1:length(CCorners)
% %      corners = [corners; CCorners(k).Location];
% end
% 
% 
% %% Given (noisy) corner points & line segments, find actual corners
% imshow(BW);
% hold on
% for k=1:size(lines, 1)
%     plot([lines(k,1), lines(k,3)], [lines(k,2), lines(k,4)],'LineWidth',2,'Color','green');
% end