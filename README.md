# AutoSEU

[![Release Version](https://img.shields.io/github/release/TimeLeSsROMO/AutoSEU)](https://github.com/TimeLeSsROMO/AutoSEU/releases/)

------------------------------------------------------------------------------------------------------------------------------------

21年5月02日提示：打卡系统里明确了每天1-15点为打卡时间，其他时间均无法进行打卡操作。代码已经改好了，明天通过了测试就更新一版。

21年4月24日提示：学校果然改版了，增加了疫苗接种情况，因为时间、地点每个人都不一样，老规矩，自行填写一次，后续不会有问题（我就是懒）。Repeat，大家自行去系统中进行一次完整上报，后续不会有问题。

------------------------------------------------------------------------------------------------------------------------------------

目前新版win10标配了Edge chromium的浏览器，每个人都有，使用起来更方便，chrome对部分人可能需要另外安装，从1.9.10版本开始，这里将只更新Edge版，chrome后续不再更新，周知

注意：学校的系统改版很勤，服务器稳定性也很差，各种状况时有发生（比如进不去、网页跳错、健康申报没事干加个新问题、销假会不会直接批、不销假能不能请假、请假是人工批还是直接批等等等…），真的让人神烦。我只是一个人，各种事很多，更新不会特别快，大家自行判断

自动进行东南大学的每日健康申报以及次日的出校审批

一个自动每日健康申报以及次日出校审批的python脚本，基于Python-Selenium，Chrome-Chromedriver（1.9.10版改为Edge-webdriver，系统自带，无需下载其他浏览器）

基于[StephenHoo/AutoLogin](https://github.com/StephenHoo/AutoLogin)，但是分支不过去，是我自己太憨了…只能自己新建一个项目了，请谅解。部分内容可以参见这位老哥的内容，普通使用只需要在这里下载，点开即可。

如果您想自己编译python代码，则需要：

python3

安装selenium库

与浏览器对应的Webdriver

正常使用请前往[Releases](https://github.com/TimeLeSsROMO/AutoSEU/releases)下载最新版本安装包并解压，确保文件夹中的chromedriver.exe（1.9.10改为msedgedriver.exe）与AutoSEU.exe在同一文件夹即可（chromedriver or msedgedriver需要与chrome or edge浏览器版本对应，压缩包中自带的是目前的最新版，如有更新请自行前往对应网站[chrome，chromedriver](http://npm.taobao.org/mirrors/chromedriver)，[edge，msedgedriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)下载）。
直接点击exe文件运行程序，第一次运行需要输入您的一卡通号、密码、家长、辅导员等信息（完全保存个人计算机本地，并不会泄露给任何人），之后不需要再进行此操作。

需要安装好chrome浏览器，最好是安装在默认位置，否则操作会比较麻烦（1.9.10版不再需要）

请确保在现版系统中进行过至少一次健康申报和出校审批，否则可能出现奇怪的错误导致无法正常运行

------------------------------------------------------------------------------------------------------------------------------------

Version 1.9.10Edge更新日志：

1.换用Edge chromium浏览器，不需要特别安装chrome

2.细节优化

没有大的逻辑调整，和上一版本质区别很小，所有需要注意的点也一样，目前学校系统的最终版。

压缩包里的edgedriver是Edge chromium 89.0.774.63版的，如果不适配你的，按上述说明下载对应版本Microsoft Webdriver

为了普适性，以后有更新也会只更新Edge版，chrome版没得咯

------------------------------------------------------------------------------------------------------------------------------------

Version 1.9.9更新日志：

1.提高整体运行速度，提速约50%

2.优化整体架构，效率和成功率大幅提升（碰到了服务器的大锅就没办法）

3.细节调整，算是目前学校系统的最终版

注意！！！3月8日起学校执行白名单政策，只需每日上报体温即可出校，无需进行出校审批，在特殊情况下再使用出校审批的功能！！！

------------------------------------------------------------------------------------------------------------------------------------

Version 1.9.1更新日志：

只是一个小调整的版本：

1.紧急修复服务器波动导致的加载失败

2.其他微调

------------------------------------------------------------------------------------------------------------------------------------

Version 1.9更新日志：

修改代码，适用于最新改版的学校系统；

程序精简，优化多余代码；

优化加速整个脚本的运行速度；

优化改善销假的判断逻辑；

改变申请销假的逻辑（学校系统中申请销假抽风中，目前是采取撤回操作，否则无法请假）。

PS：

如果打不开可以尝试将exe同目录下的loginData.json删除后再试；

自带的chromedriver是windows，版本号88.0.4324.96，适不适配你的chrome看一下你的版本号，对不上不能运行的自行去下载，和exe放同一目录即可；

学校的销假系统基本过几天就会抽一次筋，发一次疯，申请后不会直接通过，影响请假。如果有问题的话自己进系统中把所有没有销的假都撤销掉（点进去，拉到最下面点撤销——确定），后续使用本脚本不会再有此问题。

学校健康申报系统中新增一个“近14天内有无与新型冠状病毒感染患者或无症状感染者（核酸检测阳性者）有接触史？”，大家第一次使用请先在系统中选择一次“否”，后续使用本脚本就不会有问题，就偷个小懒（狗头）

------------------------------------------------------------------------------------------------------------------------------------

Version 1.6更新日志：

1.重写了60%以上的代码（很谨慎的描述），精简部分无用代码，各功能在目前的新版网站上完美运行

2.新增更多人性化选项，可以单独进行健康申报或者出校审批

3.新增检测是否处在健康申报和出校审批的时间段功能

4.新增出校审批是否通过的检测，完善检测是否已经进行健康申报的逻辑

5.新增销假功能，用于顺利进行出校审批（2天前新改版的内容，无语）

6.完善每日体温参数；可自定义请假理由

7.完善申报失败，网站故障时的提醒功能（东大的网站稳定性真的呵呵）

8.增加更多提醒内容，增加易用性

Tips：

校区仅支持丁家桥校区，毕竟之前其他校区的老哥们也是这么搞的，只支持自己校区~其他校区可联系我进行修改

为啥直接叫1.6，因为觉得好听~而且之前漏洞比较大（判断是否进行健康申报的逻辑是看有没有新增按钮……不应该是检查新增申报的日期吗。。放心，类似的都改了）；代码比较乱，很多无用和冗余的内容；憨憨学校网页改版太大，之前的基本都废了。So，1.3 to 1.6应该不过分吧
