# Overwatch Replay Analyzer (ORA) v0.1.1

## Introduction

Overwatch Replay Analyzer (ORA) v0.1.1 is a free software developed by OWDATA.ORG, a free organization devoted to competitive Overwatch data analysis. ORA can extract a timeline of events from a third-person perspective replay video. Currenly our effort is limited to  __non-Asian__ custom games(*) and OWL videos only. In v0.1.1, a timeline includes:

1. Elimination(Killer, killed player, ability, assist players, critical shot)
2. Resurrection (Resurrector, resurrected player)
3. Ult charged/ult used
4. Ult charge percentage
4. Chara switching

The released binaries & source code of ORA are published under GPL v3 license. It's free for all to redistribute and modify under the terms of the GPL v3.

__Feel free to join us on Discord:__ https://discord.gg/hnvc3yG

(*): Since Asian Overwatch game UI uses a different font from non-Asian ones, issues might rise during recognition. Hopefully we will fix it in the next release.

## Change log

* Added support for custom games replay videos
* Added support for OWL stage 3-4 replay videos
* Updated elimination ability & assist recognition
* Added ult charge percentage recognition
* Added support for Brigitte, Moira and new Hanzo
* Added automatic update
* Added JSON output for further analysis and sharing
* Bugs fixed

## Environment requirements

OS: Windows 7, 8 & 10, MacOS & Linux

## Usage

1. Download & extract to a directory, then double click on `main.exe` to run
2. Choose the video file to be analysed in `Video path`
3. Choose the output path in `Save to`
4. Input team names: team on left side in `Team A`, team on right side in `Team B`
5. Input player names (1-6, 7-12 from left to right)
6. Input start & end time, game type, analysis FPS and stage number (for OWL replays only)
6. Click on `Analyze` and wait

### Video file requirements

_The video has to be full-screened without watermark during the match._

_Resolution should be no less than 720p._

All events in the same video will be outputed to the same timeline. Thus _it's strongly recommended not to include more than 1 matches in one run_.

## Bug report

If the program doesn't run, or the output isn't what you expect, please rise a new issue in:
https://github.com/appcell/OverwatchDataAnalysis/issues

An issue usually includes:
1. problem description
2. name & version of your operating system
3. specify the match or the video file you analyze, and when the problem happens
4. the outputed `.xlsx` file and '.zip' file (if exists)
5. contact info (if you don't check your email that often)

## Join us

You can join us on Discord: https://discord.gg/hnvc3yG

Or for contacting, send an email to: info@owdata.org

Thank you for your help & support!


* * *


# 守望先锋录像分析器  v0.1.1

Overwatch Replay Analyzer (ORA) v0.1.1

## 软件简介

守望先锋录像分析器v0.1.1（以下简称 ORA）是由OWDATA.ORG开发的自由软件。该软件可以根据守望先锋的比赛 ob 视角录像 __（目前仅限 非亚洲语言的自定义比赛视频与OWL 比赛视频）__ 提取事件时间轴，并将时间轴输出到 Excel 表格。当前版本（v0.1.1）中，时间轴包括以下内容：

1. 击杀事件（击杀者，被击杀者，击杀所用技能，助攻，是否暴击）
2. 复活事件（复活者，被复活者）
3. 大招充能完毕及大招使用事件
4. 大招能量
4. 当前玩家所用英雄，及英雄切换事件

ORA的发行版及其源码遵从 GPL v3 许可，免费供所有爱好者获取和使用。商业性使用请参阅源码中附带的 GPL v3 许可协议以获取法律信息。

__欢迎加入我们的Discord群组：__ https://discord.gg/hnvc3yG


## 更新日志

* 加入对自定义比赛视频的支持
* 加入对OWL第3-4阶段比赛视频的支持
* 改进了技能和助攻的识别
* 增加了大招能量的识别和记录
* 增加了对布里吉塔，莫伊拉和新版半藏的支持
* 增加了程序自动更新
* 增加了JSON格式输出以便后续分析和数据共享
* 修复了一些已知bug


## 运行环境

操作系统： Windows 7，8，10， MacOS， Linux

## 使用方法

1. 双击运行程序后，在Video path中选择需要分析的视频文件
2. 在 Save to 中选择分析结果的保存路径
3. 在“A 队”文本框中输入左边一队的队名，“B 队”输入右边一队的队名
4. 在红色玩家名输入框内按照从左至右的顺序输入左边一队的玩家名
5. 在蓝色玩家名输入框内按照从左至右的顺序输入右边一队的玩家名
6. 输入视频中比赛的开始/结束时间（以秒为单位），按提示输入视频类型。OWL视频需输入阶段数。
6. 点击 “Analyze” 按钮，等待分析结果生成

### 视频文件要求： 

录像需为全屏且左右上角无水印，清晰度不小于720p，长宽比为16：9。

一个视频只能包含一张地图的比赛，暂不支持攻防互换。

## Bug 反馈

如遇到程序无法运行，或分析结果与预期不符，请在 https://github.com/appcell/OverwatchDataAnalysis/issues 提交新的issue。

Issue应包括：
1. 问题描述
1. 所用操作系统
2. 所用视频文件（或OWL比赛场次信息）及错误发生所在视频时间
3. （如有）生成的.xlsx和.zip分析结果
4. 联系信息

## 联系我们

您可以加入我们的Discord群组: https://discord.gg/hnvc3yG

或发邮件至: info@owdata.org



感谢您的使用和测试！
