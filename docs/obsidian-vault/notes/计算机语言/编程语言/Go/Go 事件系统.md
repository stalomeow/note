---
slug: "240512160330"
date: 2024-05-12
---

# Go 事件系统

基于反射实现的事件系统，参考：[grafana/pkg/bus/bus.go at main · grafana/grafana (github.com)](https://github.com/grafana/grafana/blob/main/pkg/bus/bus.go)。

## 使用

我在某项目里用事件实现了一套 api 系统，避免不同服务直接耦合。比如我要查询玩家的 uid：

``` go
playerUidQuery := api.GetPlayerUidQuery{
    AuthToken:         req.AuthToken,
    GameBiz:           "hkrpg_cn",
    CreateIfNotExists: true,
}
if err := api.Dispatch(&playerUidQuery); err != nil {
    log.Error().Err(err).Str("token", req.AuthToken).Any("addr", addr).Msg("invalid auth token")
    return
}
playerUid := playerUidQuery.Result
```

## 注册事件

刚才的 api 的处理函数如下：

``` go
func GetPlayerUidQueryHandler(query *api.GetPlayerUidQuery) error {
    // ...
}
```

参数是负载对象的指针，返回值是 `error`，这个格式是固定的！把函数传给 `api.Register()` 就能注册成功。

``` go
api.Register(GetPlayerUidQueryHandler)
```

## 实现

``` go
package api

import (
	"fmt"
	"reflect"
	"sync"
)

type HandlerFunc any
type Payload any

var apiHandlerMap = make(map[string][]HandlerFunc)
var mu = sync.RWMutex{}

func Register(handlers ...HandlerFunc) {
	mu.Lock()
	defer mu.Unlock()

	for _, handler := range handlers {
		handlerType := reflect.TypeOf(handler)
		apiName := handlerType.In(0).Elem().Name()

		if _, ok := apiHandlerMap[apiName]; !ok {
			apiHandlerMap[apiName] = make([]HandlerFunc, 0)
		}
		apiHandlerMap[apiName] = append(apiHandlerMap[apiName], handler)
	}
}

func Dispatch(payload Payload) error {
	mu.RLock()
	defer mu.RUnlock()

	apiName := reflect.TypeOf(payload).Elem().Name()

	if handlers, ok := apiHandlerMap[apiName]; ok {
		params := []reflect.Value{reflect.ValueOf(payload)}
		if err := callHandlers(handlers, params); err != nil {
			return err
		}
	} else {
		return fmt.Errorf("no handler for api '%s'", apiName)
	}

	return nil
}

func callHandlers(handlers []HandlerFunc, params []reflect.Value) error {
	for _, handler := range handlers {
		ret := reflect.ValueOf(handler).Call(params)

		e := ret[0].Interface()
		if e != nil {
			if err, ok := e.(error); ok {
				return err
			}
			return fmt.Errorf("expected api-handler to return an error, got '%T'", e)
		}
	}
	return nil
}
```
