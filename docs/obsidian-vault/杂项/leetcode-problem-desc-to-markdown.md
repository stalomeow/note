---
date: 2024-03-21T23:04:02
draft: false
authors:
  - stalomeow
categories:
  - Misc
---

# LeetCode 题目描述转 Markdown

为什么官方不能像洛谷一样支持这个功能？现在只能临时搞个油猴脚本支持一下。



代码改自 [https://github.com/tonngw/leetcode-helper](https://github.com/tonngw/leetcode-helper)，适配了最新的 UI，并且删掉了没用的功能，主打一个能用就行。

## 代码

``` js
// ==UserScript==
// @name         leetcode-helper
// @namespace    https://github.com/stalomeow
// @version      1.0.0
// @description  复制 LeetCode 题目描述
// @author       stalomeow
// @run-at       document-end
// @match        https://leetcode.cn/problems/*
// @require      https://unpkg.com/turndown/dist/turndown.js
// @grant        GM_registerMenuCommand
// @grant        GM_setClipboard
// @license 	 MIT
// ==/UserScript==

(function () {
    'use strict';

    // 初始化 html to markdown 转换工具
    const turndownService = new TurndownService();
    addTurndownServiceRules();

    // 注入菜单
    GM_registerMenuCommand("复制 LeetCode 题目为 Markdown，并存入剪切板", copy);

    // 添加复制按钮
    const copyBtn = document.createElement("button");
    copyBtn.id = "copyBtn";
    copyBtn.innerHTML = '复制';
    copyBtn.style.alignSelf = "center";
    copyBtn.title = "复制题目为 Markdown 格式";

    window.onload = setTimeout(function () {
        var x = document.getElementsByClassName("text-title-large font-semibold text-text-primary dark:text-text-primary")[0];
        x.parentNode.appendChild(copyBtn);
        console.log("I was invoked...");
    }, 1500);

    // 为复制按钮绑定点击功能
    copyBtn.onclick = function (e) {
        e.preventDefault();
        copy();
    };

    // 题目复制功能实现
    function copy() {
        var contentDom = document.querySelector('.elfjS').outerHTML;
        var contentMd = handleHtml(contentDom);

        GM_setClipboard(contentMd);

        window.alert('复制成功');
    }

    function addTurndownServiceRules() {
        turndownService.addRule('strikethrough', {
            filter: ['pre'],
            replacement: function (content, node) {
                // console.log(node.innerText);
                return '\n```\n' + node.innerText.trim() + '\n```\n\n';
            }
        });
        turndownService.addRule('strikethrough', {
            filter: ['strong'],
            replacement: function (content) {
                return '**' + content + "**"
            }
        });
        turndownService.addRule('strikethrough', {
            filter: ['code'],
            replacement: function (content) {
                return '<code>' + content + "</code>"
            }
        });
        turndownService.addRule('strikethrough', {
            filter: ['sup'],
            replacement: function (content) {
                return '<sup>' + content + "</sup>"
            }
        });
    }

    function handleHtml(html) {
        var lines = turndownService.turndown(html).split('\n');
        var markdown = '';
        for (var i = 0; i < lines.length; i++) {
            var l = lines[i];
            if (i > 0) markdown += '\n';
            if (l.length > 0) markdown += '> ' + l;
        }
        var problemTitle = document.getElementsByClassName('no-underline hover:text-blue-s dark:hover:text-dark-blue-s truncate cursor-text whitespace-normal hover:!text-[inherit]')[0].textContent;
        return `> [${problemTitle}](${window.location.href})\n\n` + markdown
    }
})();
```
