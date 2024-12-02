---
date: 2024-05-01T21:09:28
slug: windows-custom-keyboard-remap
draft: false
comments: true
---

# Windows 上自定义按键映射

针对我的奇怪需求，使用 Win API 实现了

- 禁用 `num lock`
- 将 `caps lock` 映射成 `win + space`
- 将键盘布局状态同步到 `caps lock` 的 LED 指示灯

代码开源在 [stalomeow/KeyboardRemapper](https://github.com/stalomeow/KeyboardRemapper)。

<!-- more -->

## 安装

使用 [[Scoop]] 从 [stalomeow/ScoopBucket](https://github.com/stalomeow/ScoopBucket) 安装。

``` bash
sudo scoop install stalo/kbdremap
```

开机会自动启动。如果进程意外终止，可以使用命令 `kbdremap` 重启。

## 按键映射

使用 [LowLevelKeyboardProc](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644985(v=vs.85)) 实现，代码可以借鉴 [PowerToys KeyboardManager](https://github.com/microsoft/PowerToys/tree/main/src/modules/keyboardmanager)。

## 同步指示灯

使用 [[Windows 全局钩子]] 监听键盘布局变化（`HSHELL_LANGUAGE`）事件，然后根据当前布局设置指示灯状态。

### 检查是否为中文键盘布局

``` cpp
static bool IsChineseKeyboardLayout()
{
    CHAR name[KL_NAMELENGTH];

    // https://learn.microsoft.com/en-us/globalization/keyboards/kbdus_2
    return GetKeyboardLayoutNameA(name) && strcmp(name, "00000804") == 0;
}
```

KeyboardLayoutName 就是 [Keyboard identifier](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-language-pack-default-values?view=windows-11#keyboard-identifiers)，简体中文对应的是 `"00000804"`。

### 设置指示灯

需要引入头文件 [ntddkbd.h](https://learn.microsoft.com/en-us/windows/win32/api/ntddkbd/)。具体的思路参考 [windows - Is it possible to control capslock light without actual capslocking? - Stack Overflow](https://stackoverflow.com/questions/72679665/is-it-possible-to-control-capslock-light-without-actual-capslocking)。
