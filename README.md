# Mix-Timer
![CIstatus](https://img.shields.io/badge/version-1.1.2-brightgreen.svg)

一个简易的倒计时定时器，可以定时自动保存/电子书阅读器自动翻页/定时提醒及更多功能   
A simple countdown timer, which could be used for auto-saving for softwares, auto-flip for ebook readers and so on.

# 项目简介

1.此项目基于python - pyqt库编写  
2.最初用于电子书软件自动翻页以及工图自动保存，后续加入其他扩展功能  
3.由于没有找到类似功能的小工具，只能自己开发，初学者水平有限，欢迎大家给出建议。  
4.当前版本功能比较简单，但常用功能都已支持，后续更多功能等待开发(≧▽≦)

# 使用方法：
![主界面](https://i.postimg.cc/9FrY66F8/image.png)

1. 在主界面中设置倒计时时间，默认为15秒，可以通过点击"+","-"按钮改变时间，或直接输入修改
2. 输入的时间支持两种格式：
    * 若输入为正整数，倒计时长为输入的时间
    * 若输入为小数，如1.5，则倒计时长为1分钟5秒，即65秒
    * 倒计时的最小单位是秒，暂不支持毫秒级倒计时
    * 其他格式暂不支持
3. 在执行动作中，可以选择具体的键盘快捷键，如win/cmd对应Windows系统的win按键，自动保存对应ctrl+s快捷键
4. 在设置中，可以修改倒计时执行次数，有三种选项：
    * 无限循环：除非点击退出或关闭工具，否则指令将不断定时执行
    * 执行一次：倒计时结束执行一次目标指令，然后自动停止倒计时
    * 自定义：可以自己设定执行次数

# 问题反馈
由于项目目前处于demo阶段，可能存在潜在bug，欢迎大家积极指正，感谢您的支持！
1. 工具及源码发布地址：
    * https://github.com/Eddingtong/MixTimer
2. QQ群：790010416, 密码：github

# 支持作者
如果您想要支持作者，可以扫描下方二维码~

![赞助码](https://i.postimg.cc/bvr904Sf/zanshang.jpg)

感谢大佬的支持(≧▽≦)~


