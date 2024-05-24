---
slug: "240524131620"
date: 2024-05-24
---

# Windows 任务栏改成状态栏

Windows 11 平板模式的任务栏非常窄，只显示时间、电量等状态，光标放上去后才展开显示 app。

<div class="responsive-video-container">
    <iframe src="https://player.bilibili.com/player.html?isOutside=true&aid=922007803&bvid=BV1Au4y1u7q9&cid=1362259631&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

PC 上需要修改注册表才能实现

1. 在 `计算机\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer` 里新建一个 `TabletPostureTaskbar`，类型是 `DWORD`，值为 `1`
2. 在 `计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\PriorityControl` 里修改 `ConvertibleSlateMode`，类型是 `DWORD`，值为 `1`

切换 app 直接用 Alt+Tab，期间按方向键或者 Tab 键可以切换选择的窗口，按 delete/Ctrl+W 键可以关闭选择的窗口。Ctrl+Alt+Tab 可以永久打开切换 app 的界面。

可惜不能把任务栏移动到屏幕顶部。。。