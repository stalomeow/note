---
slug: "240524131620"
date: 2024-05-24
---

# Windows 任务栏改成状态栏

> [!warning]
> Windows 11 的可折叠任务栏有 bug，经常卡住，不推荐用了。


Windows 11 平板模式的任务栏非常窄，只显示时间、电量等状态，光标放上去后才展开显示 app。

## 修改方法

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=922007803&bvid=BV1Au4y1u7q9&cid=1362259631&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

PC 上需要修改注册表才能实现

1. 在 `计算机\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer` 里新建一个 `TabletPostureTaskbar`，类型是 `DWORD`，值为 `1`
2. 在 `计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\PriorityControl` 里修改 `ConvertibleSlateMode`，类型是 `DWORD`，值为 `1`
3. 可以顺便去设置里开一下「自动隐藏任务栏」

切换 app 直接用 Alt+Tab，期间按方向键或者 Tab 键可以切换选择的窗口，按 delete/Ctrl+W 键可以关闭选择的窗口。Ctrl+Alt+Tab 可以永久打开切换 app 的界面。

可惜不能把任务栏移动到屏幕顶部。。。

## 还原方法

不要按照上面的逆过程还原，文件资源管理器会出 bug：文件复选框关不掉。

正确方法是去任务栏设置里，关闭「当此设备用作平板电脑时，优化任务栏以进行触控交互」。
