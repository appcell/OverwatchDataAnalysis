# Overwatch Replay Analyzer (ORA) v0.1 Beta

## Introduction

Overwatch Replay Analyzer (ORA) v0.1 Beta is a free software developed by a bunch of fans of competitive Overwatch games. ORA can extract a timeline of events from a third-person perspective replay video, and then output to an Excel file. Currenly our effort is limited to OWL videos only. In our latest version, a timeline includes:

1. Elimination(Killer, killed player, ability, assis players)
2. Resurrection (Resurrector, resurrected player)
3. Ult charged/ult used
4. Chara switching

The released binaries & source code of ORA are published under GPL v3 license. It's free for all to redistribute and modify under the terms of the GPL v3.

## Environment requirements

OS: Windows 7, 8 & 10

## Usage

1. Download & extract to a directory, then double click on `main.exe` to run
2. Choose the video file to be analysed in `Video path`
3. Choose the output path in `Save to`
4. Input team names: team on left side in `Team A`, team on right side in `Team B`
5. Input player names (1-6, 7-12 from left to right)
6. Click on `Analyze` and wait

### Video file requirements

_The video has to be full-screened without any watermark during the match._

_Resolution should be no less than 720p._

All events in the same video will be outputed to the same timeline. Thus _it's strongly recommended not to include more than 1 matches in one video_.

## Bug report

If the program doesn't run, or its output isn't what you expect, please submit a new issue in:
https://github.com/appcell/OverwatchDataAnalysis/issues

An issue usually includes:
1. problem description
2. name & version of your operating system
3. specify the match or the video file you analyze, and when the problem happens
4. the outputed `.xlsx` file (if exists)
5. contact info (if you don't check your email that often)

Thank you for your help & support!


* * *


# 守望先锋录像分析器 v0.1 公测版

Overwatch Replay Analyzer (ORA) v0.1 Beta

## 软件简介

守望先锋录像分析器v0.1公测版（以下简称 ORA ）是由守望先锋电竞数据爱好者自发组织开发的自由软件。该软件可以根据守望先锋的比赛 ob 视角录像 __（目前仅限 OWL 比赛视频）__ 提取事件时间轴，并将时间轴输出到 Excel 表格。当前版本（v0.1公测版）中，时间轴包括以下内容：

1. 击杀事件（击杀者，被击杀者，击杀所用技能，助攻）
2. 复活事件（复活者，被复活者）
3. 大招充能完毕及大招使用事件
4. 当前玩家所用英雄，及英雄切换事件

ORA的发行版及其源码遵从 GPL v3 许可，免费供所有爱好者获取和使用。商业性使用请参阅源码中附带的 GPL v3 许可协议以获取法律信息。

## 运行环境

GUI版本： Windows 8, Windows 10

命令行版本： 待定

## 使用方法

1. 双击运行程序后，在Video path中选择需要分析的视频文件
2. 在 Save to 中选择分析结果的保存路径
3. 在“A 队”文本框中输入左边一队的队名，“B 队”输入右边一队的队名
4. 在红色玩家名输入框内按照从左至右的顺序输入左边一队的玩家名
5. 在蓝色玩家名输入框内按照从左至右的顺序输入右边一队的玩家名
6. 点击 “Analyze” 按钮，等待分析结果生成

### 视频文件要求： 

录像需为全屏且左右上角无水印，清晰度不小于720p，长宽比为16：9。

一个视频只能包含一张地图的比赛，且不支持攻防互换。

## Bug 反馈

如遇到程序无法运行，或分析结果与预期不符，请在 https://github.com/appcell/OverwatchDataAnalysis/issues 提交新的issue。

Issue应包括：
1. 问题描述
1. 所用操作系统
2. 所用视频文件（或OWL比赛场次信息）及错误发生所在视频时间
3. （如有）生成的.xlsx分析结果
4. 联系信息

感谢您的使用和测试！
