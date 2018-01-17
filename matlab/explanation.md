# Killfeed 识别

killfeed 识别的代码分散在main.m, getKillEvents.m 和 findIconsInRow.m

## main.m

17行开始循环读入帧， getKillEvents获取当前帧的killfeed，记在nx2的矩阵里。
23-42行 将当前帧的killfeed加上当前时间写入到视频总表eventList中。如果一行的右边的角色识别失败（name == "empty"), 该行视为无效，不记入eventList

## getKillEvents.m
画面上同时最多有6条killfeed，其高度固定。killfeed更新时，从顶端插入新的feed，旧feed依次下移直到移出第6行。所以这里的逻辑是，从上往下依次识别，如果某一行的feed和eventList中最新事件相同，说明下方的feed都是前一帧已有的旧feed，在这里中断循环避免重复识别。
在视频刚被读取之后，eventList被初始化成1x2的矩阵。所以如果size(eventList, 1) == 1说明eventList是空的，此时直接用findIconsInRow识别图标并记入charas。
如果eventList非空，则判断一下当前行是否和eventList底部重复，根据上述逻辑判断是否需要中止循环。

## findIconsInRow.m

3-4行切图，各个尺寸都是经验位置，考虑了英文选手名的长度（3-12）。切完图后用matchIcon来找图中的icon并识别。
如果右方的chara没识别出来，说明该行feed无效，直接返回。

识别出两个chara以后，根据icon周围的颜色来判断一下chara处于哪个队。一个全屏录像左上和右上两个角分别是两个队在本场比赛中的代表色。

这里的“周围”指的是左边图标的左上角往左数5px，右边图标的右上角往右数5px。另外考虑到feed背景框是半透明的，像素颜色受光照影响，19-20行对color做了（某种意义上的）normalization。normalize以后的color和代表色做比较，颜色更接近的队伍就是chara所属的队。

43行起有一个postprocess，用来去除无中生有的识别结果（有时在空画面里也能以较大的几率识别出英雄）。一个正确的识别结果至少应该在方框内，而方框的左右两侧都会在edge图上有一条直线， 所以如果左右两侧没有直线那么就认为识别出的头像的位置是错的。

注意这里的逻辑反过来是不成立的，i.e. 有头像之后可以通过两侧有直线来判断头像位置识别有效，但是不能通过寻找直线来判断头像的位置，因为有些英雄（比如猩猩/堡垒）的头像自带直线型edge。（如果这个问题能解决，那么matlab版本就不用优化了）

matchIcon： 将每个icon和当前切好的图做一次卷积，寻找cross-correlation的最大值。最大值最大的icon就是识别出的chara的icon。（这个部分很慢，起码要多线程解决，能放到gpu上是坠吼的）识别出来以后记录下icon对应的角色，icon在图中的位置等等信息。

