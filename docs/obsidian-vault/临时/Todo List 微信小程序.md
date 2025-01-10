# Todo List 微信小程序

---

## 功能

- 添加/删除/修改/完成代办事项
- 自动微信登录，将应用数据与微信账号绑定，实现多端同步

---

## 设计思想

- 界面简洁
- 功能完善

---

## 前端

![[screenshot.jpg|220]]

---

## 后端

使用 go 开发

![[backend.png|750]]

---

## 数据结构

---

代办事项的数据结构如下，用于前后端通信，能完整地实现前面提到的功能

``` go
type TodoItem struct {
	Id         string `json:"id"`
	Title      string `json:"title"`
	Desc       string `json:"desc"`
	Date       string `json:"date"` // 截止日期
	Level      int    `json:"level"`
	Completed  bool   `json:"completed"`
	CreateAt   string `json:"createAt"`   // 创建日期
	CompleteAt string `json:"completeAt"` // 完成日期
}
```

---

## 登录流程

---

小程序启动后，会自动调用微信的接口登录，后端进行校验后下发 token 给前端。

![[login.png|500]]

微信接口返回的 `openid` 是用户的唯一识别码，将用户数据与 `openid` 关联后，即可实现多端数据同步。

---

通过调用 `wx.login()`，获取登录凭证，有效期为 5 分钟，将它发给后端校验

``` ts
wx.login({
  success: async res => {
    await TodoManager.login(res.code);
    wx.reLaunch({ url: '../todo/index' });
  },
});
```

---

后端根据微信文档实现校验逻辑，获取 `openid`

``` go
type wxCode2SessionRsp struct {
    OpenId       string `json:"openid"`
    SessionKey   string `json:"session_key"`
    UnionId      string `json:"unionid"`
    ErrorCode    int32  `json:"errcode"`
    ErrorMessage string `json:"errmsg"`
}

func RequestUserId(code string) (string, error) {
    rsp, err := http.Get(fmt.Sprintf(urlFmt, appId, appSecret, code, "authorization_code"))
    if err != nil {
        return "", err
    }

    defer rsp.Body.Close()

    data := wxCode2SessionRsp{}
    err = json.NewDecoder(rsp.Body).Decode(&data)
    if err != nil {
        return "", err
    }

    if data.ErrorCode != 0 {
        return "", fmt.Errorf("error code: %d, error message: %s", data.ErrorCode, data.ErrorMessage)
    }

    // openid 是用户的唯一标识
    return data.OpenId, nil
}
```

---

后端生成 token 并返回

``` go
func (m *Manager) AddUserAndGetToken(userId string) (string, error) {
    token, err := createRandomBase64(16)
    if err != nil {
        return "", err
    }

    m.mu.Lock()
    defer m.mu.Unlock()

    if _, ok := m.userData[userId]; !ok {
        var list *todoList
        if list, err = newTodoList(); err != nil {
            return "", err
        }
        m.userData[userId] = list
    }

    m.tokens[token] = userId
    m.isChanged = true
    return token, nil
}
```

---

生成 token 时，使用了密码学安全的随机数发生器

``` go
import (
    "crypto/rand"
    "encoding/base64"
)

func createRandomBase64(len int) (string, error) {
    b := make([]byte, len)
    if _, err := rand.Read(b); err != nil {
        return "", err
    }
    return base64.StdEncoding.EncodeToString(b), nil
}
```

---

## 数据保存

---

在后端实现了一个 `Manager` 结构来管理数据，并使用 `RWMutex` 保证并发安全。

``` go
type Manager struct {
	mu       sync.RWMutex
	userData map[string]*todoList // userId -> todoList
	tokens   map[string]string    // token -> userId

	isChanged bool
	saveData  map[string][]*TodoItem // 用于保存数据
}
```

---

在启动服务端时，会先加载上次保存的数据，然后启动一个 `goroutine`，在后台定时保存数据。

``` go
func NewManager() (*Manager, error) {
	m := &Manager{
		mu:       sync.RWMutex{},
		userData: make(map[string]*todoList),
		tokens:   make(map[string]string),

		isChanged: false,
		saveData:  make(map[string][]*TodoItem),
	}

	if err := m.load(); err != nil {
		return nil, err
	}

	// 定时保存数据
	go func() {
		t := time.NewTicker(time.Millisecond * 500)
		for range t.C {
			m.save()
		}
	}()

	return m, nil
}
```

---

## 路由

---

使用 `gin` 框架实现后端 API 的路由，启动后监听 `1145` 端口，提供了登录、增删改查这类基础功能。

``` go
r := gin.Default()
r.POST("/login", login)
r.GET("/list", validateToken, listItems)
r.POST("/add", validateToken, addItem)
r.POST("/delete", validateToken, deleteItem)
r.POST("/set", validateToken, setItem)
r.Run(":1145")
```

---

利用 `gin` 中间件简化 `token` 鉴权。

``` go
func validateToken(c *gin.Context) {
	token := c.GetHeader("Authorization")

	id, ok := m.GetUserIdByToken(token)
	if !ok {
		c.AbortWithStatusJSON(http.StatusOK, gin.H{
			"success": false,
			"data":    "invalid token",
		})
		return
	}

	c.Set("id", id)
	c.Next()
}
```

---

## 前端接口

---

针对项目将 `wx.request()` 封装为异步函数，方便后续调用。

``` ts
type Method = 'GET' | 'POST' | 'PUT' | 'DELETE';

function fetchJSON<T>(method: Method, token: string, url: string, data: any): Promise<T> {
  return new Promise((resolve, reject) => wx.request({
    url,
    method,
    data,
    dataType: 'json',
    header: {
      'Content-Type': 'application/json',
      'Authorization': token,
    },
    success(res) {
      if (res.statusCode === 200) {
        let data = <any>res.data;
        if (data.success) {
          resolve(data.data);
          return;
        }
      }

      reject(res);
    },
    fail(err) {
      reject(err);
    },
  }));
}
```

---

将后端接口封装为简单的异步函数，方便程序使用。

``` ts
export class TodoItem {
  public id: string = '';
  public title: string = '';
  public desc: string = '';
  public date: string = '';
  public level: number = 0;
  public completed: boolean = false;
  public createdAt: string = '';
  public completedAt: string = '';
}

export class TodoManager {
  private static _baseUrl = 'MY_URL';
  private static _token: string = '';

  public static async login(code: string): Promise<void> {
    this._token = await fetchJSON<string>('POST', '', `${this._baseUrl}/login`, { code });
    console.log(`Token: ${this._token}`);
  }

  public static async getAll(): Promise<TodoItem[]> {
    return await fetchJSON<TodoItem[]>('GET', this._token, `${this._baseUrl}/list`, {});
  }

  public static async addItem(title: string, desc: string, date: string, level: number, completed: boolean): Promise<TodoItem> {
    return await fetchJSON<TodoItem>('POST', this._token, `${this._baseUrl}/add`, { title, desc, date, level, completed });
  }

  public static async deleteItem(id: string): Promise<void> {
    await fetchJSON<string>('POST', this._token, `${this._baseUrl}/delete`, { id });
  }

  public static async setItem(id: string, title: string, desc: string, date: string, level: number, completed: boolean): Promise<TodoItem> {
    return await fetchJSON<TodoItem>('POST', this._token, `${this._baseUrl}/set`, { id, title, desc, date, level, completed });
  }

  private static formatNumber(n: number): string {
    let s = n.toString();
    return s[1] ? s : '0' + s;
  }

  public static formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    date.toDateString()
    return [year, month, day].map(this.formatNumber).join('-');
  }
}
```

---

## 演示
