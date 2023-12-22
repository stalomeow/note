# 将内存中数据下载为文件

!!! abstract

    原生 js 实现：将内存中数据下载为文件。

## 实现

借助 `HTMLAnchorElement` 实现。

``` js
function downloadAsFile(fileName, obj) {
    const a = document.createElement('a');

    a.download = fileName;
    a.style.display = 'none';
    a.href = URL.createObjectURL(obj);

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
```

## 例子

例如，要将 `data` 保存为 json 文件。可以创建一个 `Blob` 再调用上面的函数实现。

``` js
const blob = new Blob([JSON.stringify(data)], {
    type: "application/json",
});

// 上面指定了 blob 的 MIME type 是 json，所以文件扩展名可以不写
downloadAsFile('data', blob);
```
