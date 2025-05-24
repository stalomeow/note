---
date: 2025-04-25T22:05:42
aliases: 
draft: true
---

# GPU 崩溃

## TDR

Windows Display Driver Model（WDDM）有一个 TDR 机制（Timeout Detection and Recovery）。

> TDR is a feature in Windows that detects when the graphics card is taking longer than expected to complete an operation. It then resets the graphics card to prevent the entire system from becoming unresponsive.
>
> One of the most common stability problems in graphics occurs when a computer appears to "hang" or be completely "frozen" when it's actually processing an end-user command or operation. Many users wait a few seconds and then decide to reboot the computer. The frozen appearance of the computer frequently occurs because the GPU is busy processing intensive graphical operations, typically during game play, and hence doesn't update the display screen. TDRs enable the operating system to detect that the UI isn't responsive.
>
> ![[Pasted image 20250426002624.png|the TDR process]]
>
> The OS attempts to detect situations in which computers appear to be "frozen". The OS then attempts to dynamically recover from the frozen situations so that desktops are responsive again, alleviating the situation where end users needlessly reboot their systems.

## 常见崩溃类型

## 工具

## 参考

- [WDDM Support for Timeout Detection and Recovery (TDR) - Windows drivers | Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/drivers/display/timeout-detection-and-recovery)
