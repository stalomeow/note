---
slug: "240425200801"
date: 2024-04-25
---

# 写一个简易 jQuery


用 TypeScript 实现一个简易版的 jQuery。

## 动机

- 现在浏览器提供的 API 已经足够取代 jQuery 了，没必要再导入它（占用带宽、延长响应时间）。GitHub 也已经把 jQuery 移除了。
- jQuery 的设计我个人感觉有点不合理。比如 `$('.abc')` 匹配的元素数量可能是 0 个或任意多个。代码的意图不明确，有时候容易出 bug。
- 浏览器的 API 用起来有点麻烦。

## 代码实现

### 扩展浏览器 API

封装几个简单实用的方法。

声明：

``` ts
declare interface Element {
  addClass(...classNames: string[]): this;
  removeClass(...classNames: string[]): this;
  toggleClass(...classNames: string[]): this;
  hasClass(className: string): boolean;

  attr(qualifiedName: string): string | null;
  attr(qualifiedName: string, value: string | null): this;
}

declare interface HTMLElement {
  top(): number;
  left(): number;

  css(propertyName: string): string;
  css(propertyName: string, value: string | null): this;
  css(properties: Record<string, string | null>): this;

  wrap(container: HTMLElement): this;
}

declare interface Array<T> {
  peek(): T | undefined;
}
```

实现：

``` ts
Object.assign(Element.prototype, {
  attr: function (qualifiedName: string, value?: string | null): string | null | Element {
    const e = this as unknown as Element;

    if (typeof value === 'undefined') {
      return e.getAttribute(qualifiedName);
    }

    if (typeof value === 'string') {
      e.setAttribute(qualifiedName, value);
      return e;
    }

    // null
    e.removeAttribute(qualifiedName);
    return e;
  },
  addClass: function (...classNames: string[]): Element {
    const e = this as unknown as Element;
    classNames.forEach(v => e.classList.add(v));
    return e;
  },
  removeClass: function (...classNames: string[]): Element {
    const e = this as unknown as Element;
    classNames.forEach(v => e.classList.remove(v));
    return e;
  },
  toggleClass: function (...classNames: string[]): Element {
    const e = this as unknown as Element;
    classNames.forEach(v => e.classList.toggle(v));
    return e;
  },
  hasClass: function (className: string): boolean {
    const e = this as unknown as Element;
    return e.classList.contains(className);
  }
});

Object.assign(HTMLElement.prototype, {
  top: function (): number {
    const e = this as unknown as HTMLElement;
    let result = e.offsetTop;
    let parent = e.offsetParent as (HTMLElement | null);

    while (parent) {
      result += parent.offsetTop;
      parent = parent.offsetParent as (HTMLElement | null)
    }

    return result;
  },
  left: function (): number {
    const e = this as unknown as HTMLElement;
    let result = e.offsetLeft;
    let parent = e.offsetParent as (HTMLElement | null);

    while (parent) {
      result += parent.offsetLeft;
      parent = parent.offsetParent as (HTMLElement | null)
    }

    return result;
  },
  css: function (
    propertyNameOrProperties: string | Record<string, string | null>,
    value?: string | null
  ): string | HTMLElement {
    const e = this as unknown as HTMLElement;

    if (typeof propertyNameOrProperties === 'string') {
      if (typeof value === 'undefined') {
        const style = getComputedStyle(e);
        return style.getPropertyValue(propertyNameOrProperties);
      }

      e.style.setProperty(propertyNameOrProperties, value);
    } else {
      for (const propertyName in propertyNameOrProperties) {
        const value = propertyNameOrProperties[propertyName];
        e.style.setProperty(propertyName, value);
      }
    }

    return e;
  },
  wrap: function (container: HTMLElement): HTMLElement {
    const e = this as unknown as HTMLElement;
    const parent = e.parentElement!;

    parent.insertBefore(container, e);
    parent.removeChild(e);
    container.appendChild(e);
    return e;
  }
});

Object.assign(Array.prototype, {
  peek: function (): unknown {
    const array = this as unknown[];

    if (array.length === 0) {
      return undefined;
    }

    return array[array.length - 1];
  }
});
```

### 美元符号

不同于 jQuery，我规定 `$()` 只能用来选择元素并且**只选择一个**，如果元素不存在那么会返回 `null`。

``` ts title="$()"
const a = $('a');
// 上一行等价于 document.querySelector<Element>('a');

const b = $<HTMLElement>('b', a);
// 上一行等价于 a.querySelector<HTMLElement>('b');
```

考虑到 `$()` 在元素不存在时会返回 `null`，但有时我就是希望这个元素存在，并且我也不想在后面对 `null` 的情况做处理，那么可以考虑使用 `$.assert()`。正如函数名所言，这个函数除了选择一个元素外还有断言功能。如果元素不存在，那么会直接抛出异常。

``` ts title="$.assert()"
const a = $.assert('a'); // 假装这个元素存在
// a 为一个 <a> 元素

const b = $.assert<HTMLElement>('b', a); // 假装这个元素不存在
// error
```

剩下的 API 都比较简单，就不在这里解释了，代码实现里有注释。

``` ts title="Implementation of $.ts"
/**
 * 选择一个符合条件的元素
 * @param selectors 选择器
 * @param root 根元素
 * @returns 符合条件的元素
 */
export default function $<E extends Element>(selectors: string, root?: ParentNode): E | null {
  return (root || document).querySelector<E>(selectors);
}

/**
 * 选择一个符合条件的元素，并断言其一定存在。如果不存在则报错
 * @param selectors 选择器
 * @param root 根元素
 * @returns 符合条件的元素
 */
$.assert = function <E extends Element>(selectors: string, root?: ParentNode): E {
  const result = $<E>(selectors, root);

  if (!result) {
    throw new Error('can not find element matching (' + selectors + ') in ' + (root || document));
  }
  return result;
}

/**
 * 选择所有符合条件的元素
 * @param selectors 选择器
 * @param root 根元素
 * @returns 由符合条件的元素组成的列表
 */
$.all = function <E extends Element>(selectors: string, root?: ParentNode): NodeListOf<E> {
  return (root || document).querySelectorAll<E>(selectors);
};

/**
 * 遍历所有符合条件的元素
 * @param selectors 选择器
 * @param callback 回调函数
 * @param root 根元素
 */
$.each = function <E extends Element>(
  selectors: string,
  callback: (item: E, index: number, list: NodeListOf<E>) => void,
  root?: ParentNode
): void {
  $.all<E>(selectors, root).forEach(callback);
};

/**
 * 创建一个元素
 * @param tagName 新元素的标签名称
 * @param attributes 新元素的所有 attribute
 * @returns 新元素
 */
$.create = function <K extends keyof HTMLElementTagNameMap>(
  tagName: K,
  attributes?: Record<string, string>
): HTMLElementTagNameMap[K] {
  const result = document.createElement(tagName);

  if (attributes) {
    for (const key in attributes) {
      result.attr(key, attributes[key]);
    }
  }

  return result;
}
```
