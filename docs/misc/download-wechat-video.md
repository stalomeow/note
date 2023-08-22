# 下载微信视频号的视频

!!! abstract

    下载微信视频号的视频。2023 年 8 月，该方法还有效，但是找缓存文件之类的方法已经失效了。

## 抓包

1. 把视频转发给文件传输助手。
2. 电脑上播放视频。必须在微信里点，自己的浏览器里能开网页但放不了视频！
3. 抓包。找到 Host 为 `finder.video.qq.com` 的请求，资源类型是 `video/mp4`。
4. 复制链接。

## 改链接

1. 把网址里的 20302 修改成 20304。不改链接下不了，我也不知道为啥换成 20304 就行了。
2. 直接下载，不用管文件的类型，不用管任何东西，下载完把文件后缀名强行换成 mp4 就行。

**如果想下载高清版的视频，要删掉链接里除 encfilekey 和 token 以外的所有参数。不删的话，下载的是标清的视频。** [^1]

??? example "举个例子"

    我要下载 2023 年七夕节的符玄视频。抓包拿到的链接是

    ```
    https://finder.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQAN1a6ibefGvPw1PHx7RM3ic3gFGcdj1ANdvmKX5xW7W42ibjIYEl370ltTichiccv0Aic2C2VoPMwZEFumXQVowqBQu3&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&web=1&token=cztXnd9GyrEGEialXvUYkhnSnbm1RKCM1Q2aqZMrYmMPZRxicf7W0xKmvn6dnDathvZUUA9XbBpbZemce6zACNfibEEYceAo806WkVf1wlv9WvhOKFsTukfZUEKQhILCtI7&extg=10f002e&svrbypass=AAuL%2FQsFAAABAAAAAABFfBrniHBEF4ttG2DkZBAAAADnaHZTnGbFfAj9RgZXfw6VL1b55l%2BhP%2FmOYyH2q2EYrf0Fl%2BMvkM0ksZRm1q1OjEDL&svrnonce=1692688411&fexam=1&X-snsvideoflag=xW20
    ```

    标清版视频的链接是

    ```
    https://finder.video.qq.com/251/20304/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQAN1a6ibefGvPw1PHx7RM3ic3gFGcdj1ANdvmKX5xW7W42ibjIYEl370ltTichiccv0Aic2C2VoPMwZEFumXQVowqBQu3&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&web=1&token=cztXnd9GyrEGEialXvUYkhnSnbm1RKCM1Q2aqZMrYmMPZRxicf7W0xKmvn6dnDathvZUUA9XbBpbZemce6zACNfibEEYceAo806WkVf1wlv9WvhOKFsTukfZUEKQhILCtI7&extg=10f002e&svrbypass=AAuL%2FQsFAAABAAAAAABFfBrniHBEF4ttG2DkZBAAAADnaHZTnGbFfAj9RgZXfw6VL1b55l%2BhP%2FmOYyH2q2EYrf0Fl%2BMvkM0ksZRm1q1OjEDL&svrnonce=1692688411&fexam=1&X-snsvideoflag=xW20
    ```

    高清版视频的链接是

    ```
    https://finder.video.qq.com/251/20304/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQAN1a6ibefGvPw1PHx7RM3ic3gFGcdj1ANdvmKX5xW7W42ibjIYEl370ltTichiccv0Aic2C2VoPMwZEFumXQVowqBQu3&token=cztXnd9GyrEGEialXvUYkhnSnbm1RKCM1Q2aqZMrYmMPZRxicf7W0xKmvn6dnDathvZUUA9XbBpbZemce6zACNfibEEYceAo806WkVf1wlv9WvhOKFsTukfZUEKQhILCtI7
    ```

[^1]: [怎么下载微信视频号的视频? - 知乎](https://www.zhihu.com/question/533237015/answer/3171620888)