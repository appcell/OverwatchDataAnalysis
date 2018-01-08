function [ults,ultsVar]= ultStates(oneFrame)
%This function is used to detect the Ultimate states for a certain 720p
%full screen shot in OWL series (S1) The visiting team is at the left top
%corner and the home team is at the top right corner.
% Input oneFrame- one shot from readFrame function(or same format)
% Output ults - 1 by 12, 1d array, from left to right , elements = 0(no
% ult) or 1 (has ult)
%        ultsVar - 1 by 12, 1d array, from left to right, elements = double
%        from (-1,1)= correlation coefficients from crossrelation algorithm(possibility to have an ult)

%set the 2 different ult icons from visiting side and home side, and scale
%them to compare with 720p video.
% visitingUlt=imresize(rgb2gray(imread('./../../images/visitingUlt.png')),0.6);
visitingUlt=imresize(imread('./../../images/visitingUlt.png'), 1);
% homeUlt=imresize(rgb2gray(imread('./../../images/homeUlt.png')),0.75);
homeUlt=imresize(imread('./../../images/homeUlt.png'),1);
%initialize ults and ultsVar
ults=[1:1:12];
ultsVar=[1:1:12];
%the rectangular area parameters used to detect the ult icon
width=30;
height=26;

%crop the top lines for detection
I=imcrop(oneFrame,[0,40,1280,60]);
IGray=rgb2gray(I);
%compare the visiting ults with visiting team members
for i = 1:6
    xmin=34+(i-1)*70;
    ymin=11;
    IRect=imcrop(IGray,[xmin,ymin,width,height]);
    C=normxcorr2(visitingUlt,IRect);
    B=max(C(:));
    %to avoid possible explosion effect
    if mean(IRect)>230
        B=1;
    end
    ultsVar(i)=gather(B);
end
%compare the home ults with home team members
for i=7:12
    xmin=835+(i-7)*70;
    ymin=11;
    IRect=imcrop(IGray,[xmin,ymin,width,height]);
    C=normxcorr2(homeUlt,IRect);
    B=max(C(:));
    if mean(IRect)>230
        B=1;
    end
    ultsVar(i)=B;
end
%return those with correlation coefficients >0.8
ults=(ultsVar>0.8);
end
