---
date: 2024-01-13T03:48:38
draft: false
authors:
  - stalomeow
categories:
  - Circuit Simulation
---

# Multisim 仿真「方向之星」控制器

数电仿真大作业。感觉运气挺好，抽到的题不太难（。

> 说明：「方向之星」是装在小汽车后窗上一组灯饰，由左右两排十余个小灯及中间一个大灯组成，起美观、提示作用。
>
> 要求：
>
> 1. 根据汽车的运行状态，控制中间大灯 —— “减速” 灯亮灭以及左边排灯、右边排灯的依次闪亮（每边排灯闪亮时每边每次只亮一个灯）。
> 2. 配套设计的一个声光提示系统，提示驾驶员在转弯结束后，及时关闭转向灯。
> 3. 左、右排灯同时闪亮时，能始终保持对称状态以求美观。
>
> 拓展要求：以最简的电路实现功能。

<!-- more -->

## 仿真图

![Multisim Screenshot](../../../assets/images/DirectionStar_Screenshot.png)

S1 打到上面时，表示正在转弯；打到下面，表示转弯结束。S2 同理。

[:material-download: 下载仿真源文件](../../../assets/files/DirectionStar.ms14){ .md-button }

## 排灯及中间大灯

两边的排灯用两个有 10 个灯的 LED Bar。要实现题中流水灯效果，可以用一片 74LS190 十进制计数器 + 一片 74LS42 十进制译码器。

考虑到 74LS42 的输出是低电平有效，LED Bar 有 A 标记的一侧直接全连高电平，另一侧分别接到 74LS42 的 10 个输出端。

- 关灯：给计数器置数 1111，这时译码器的输出全是高电平。LED Bar 两侧都是高电平，所有灯都不亮。（74LS190 是异步置数，可以立刻关灯）
- 流水灯：允许计数器计数，这时译码器只有一个输出是低电平，且是每个输出端依次变化。LED Bar 中的灯依次亮。

中间大灯用了一个 Lamp，闪烁功能就偷个懒：从 74LS42 的 10 个输出里隔一个取一个，共 5 个输出，经过一个与门连到中间大灯一端。另一端连到高电平。中间大灯相当于以排灯一半的频率在闪烁。

## 关转向灯的提示

关转向灯的提示用了一个蜂鸣器 + 一个灯泡。转弯结束后，蜂鸣器会响一段时间，灯泡会亮一段时间。

用了一片 74LS194 移位寄存器。74LS194 是异步清零和同步置数，置数需要等待 CP。如果转弯时间小于时钟周期，会检测不到。所以采用清零来实现。

转弯时，无条件清零。转弯结束后，一直左移进 $1$。当输出中同时包含 $0$ 和 $1$ 时（$Q_A Q_B Q_C Q_D$ 中有 $1$，但不全为 $1$），蜂鸣器和灯泡工作。即

$$
\overline{Q_A Q_B Q_C Q_D}(Q_A + Q_B + Q_C + Q_D)
$$

这个设计可以自启动。

## 一些坑

- 给元件打中文标签时，如果改 `RefDes` 那么电路就没法工作了。只能把中文写在下面的 `Label` 栏里。
- 蜂鸣器只能上面开口的那侧接低电平。反过来接就没法工作。
- LED Bar 只能有 A 标记的一侧连高电平。反过来接也没法工作。