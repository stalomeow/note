---
date: 2024-05-01T21:09:28
slug: windows-capslock-ime
categories:
  - Misc
draft: false
comments: true
---

# Windows 上用 CapsLock 切换中英文

<!-- more -->

微软输入法切换中英文的按键选择有 Ctrl、Shift、Ctrl+Space，但它们都是其他软件常用的修饰符/快捷键，肯定没法用。后来，我用一个纯英文键盘布局和一个纯中文键盘布局，靠 Win+Space 切换，但这个快捷键按着也挺麻烦。

受 MacOS 的启发，我决定改用 CapsLock 切换中英文。恰好，我平时切换大小写用的都是 Shift。CapsLock 放在那么好的位置却不用，很可惜。

## 按键映射

使用 [[Windows PowerToys]] 的键盘管理器映射 CapsLock 到 Win+Space。


## 同步指示灯

按键都重映射了，指示灯放着不用也怪可惜的。我笔记本键盘上 CapsLock 指示灯就在这个按键右上角，改成中英文指示灯刚好。灯亮时就是中文模式，灯暗时就是英文模式。

代码开源在 GitHub 上：[stalomeow/CapsLockLed-IME](https://github.com/stalomeow/CapsLockLed-IME)。特地用纯 C 写的，几乎没有什么开销。大体思路：依靠 [[Windows 全局钩子]] 监听键盘布局变化（`HSHELL_LANGUAGE`）事件，然后根据当前布局设置指示灯状态。

### 检查是否为中文键盘布局

``` c
BOOL IsChineseKeyboardLayout()
{
    CHAR name[KL_NAMELENGTH];

    if (GetKeyboardLayoutNameA((LPSTR)&name))
    {
        // https://learn.microsoft.com/en-us/globalization/keyboards/kbdus_2
        if (strcmp(name, "00000804") == 0)
        {
            return TRUE;
        }
    }

    return FALSE;
}
```

KeyboardLayoutName 就是 [Keyboard identifier](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-language-pack-default-values?view=windows-11#keyboard-identifiers)，简体中文对应的是 `"00000804"`。

### 设置指示灯

需要引入头文件  [ntddkbd.h](https://learn.microsoft.com/en-us/windows/win32/api/ntddkbd/)。

具体的思路参考 [windows - Is it possible to control capslock light without actual capslocking? - Stack Overflow](https://stackoverflow.com/questions/72679665/is-it-possible-to-control-capslock-light-without-actual-capslocking)。

