# bacnet

bacnet 学习手册


**python pip install BACpypes
安装模拟bacnet 模拟器，制作一个设备。


**ReadPropertyMultipleServer.py 模拟器代码

**BACpypes.ini 设备配置

**BACnetScan 扫描工具

**objtype object type  e.g. analogInput

模拟输入Analog Input 模拟传感器输入如机械开关On/Off输入


模拟输出Analog Output 模拟控制量输出


模拟值Analog Value 模拟控制设备参数如设备阀值


数字输入Binary Input 数字传感器输入如电子开关On/Off输入


数字输出Binary Output 继电器输出


数字值Binary Value 数字控制系统参数


命令Command 向多设备多对象写多值如日期设置


日历表Calender 程序定义的事件执行日期列表


时间表Schedule 周期操作时间表


事件登记Event Enrollment 描述错误状态事件如输入值超界或报警事件。通知一个设备对象，也可通过“通知类”对象通知多设备对象


文件File 允许访问（读/写）设备支持的数据文件


组Group 提供单一操作下访问多对象多属性


环Loop 提供访问一个“控制环”的标准化操作


多态输入Multi-state Output 表述多状态处理程序的状况，如制冷设备开、关和除霜循环


多态输出Multi-state Output 表述多状态处理程序的期望状态，如制冷设备开始冷却、除霜的时间


通知类Notification Class 包含一个设备列表，配合“事件登记”对象将报警报文发送给多设备


程序Program 允许设备应用程序开始和停止、装载和卸载，并报告程序当前状态


设备Device 其属性表示设备支持的对象和服务以及设备商和固件版本等信息

