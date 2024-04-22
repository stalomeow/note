---
date: 2024-01-26T02:03:22
draft: false
authors:
  - stalomeow
categories:
  - Game Back-end
---

# 游戏注册、登录和鉴权

很多游戏公司都会搞一个通行证，官网、旗下所有游戏都用它登录。为了泛用性，这部分用的是 https 协议。我尝试用 golang + [gin 框架](https://github.com/gin-gonic/gin) + [MongoDB](https://www.mongodb.com/zh-cn) 搞了个类似的服务，包括注册、登录和鉴权。然后，用 C# 写了一套 SDK，方便在 Unity 里用。



## 前端大致流程

``` mermaid
flowchart TD
    A[尝试自动登录] -->|Old Token| B{后端}
    B -->|成功，返回 New Token| C[登录成功]
    B -->|失败| D[登录/注册]
    D -->|账号密码| B
```

登录成功后，每次请求 API 都带上 Token，后端会做鉴权。

## 密码传输与保存

很多人都是所有账号用一个密码，如果一个地方密码明文泄露了，黑客拿去撞库的话，一大堆账号都没了。只要明文不泄露，出意外的时候，损失就能仅仅控制在当前的站点。

传输密码的时候，用的是 https 协议，一般情况下已经足够安全了。Google 在传输密码时就没额外做加密。百度是自己又做了一次 RSA。还有些网站是前端 hash 一次，把结果作为用户的密码传给后端，不使用密码明文。

我用的是类似百度的方案。服务器启动时，会生成 RSA 密钥 + 公钥。公钥是公开的，前端直接请求后端 API 就能拿到。密码用公钥加密后传给后端，后端用密钥解密。

``` go title="后端 RSA"
var rsaPrivateKey *rsa.PrivateKey
var rsaPublicKey *rsa.PublicKey
var rsaPublicKeyB64Str string

func GenerateRSAKeys() error {
	privateKey, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		return err
	}

	rsaPrivateKey = privateKey
	rsaPublicKey = &privateKey.PublicKey

	derPkcs1 := x509.MarshalPKCS1PublicKey(rsaPublicKey)
	rsaPublicKeyB64Str = base64.StdEncoding.EncodeToString(derPkcs1)
	return nil
}

func GetRSAPublicKey() string {
	return rsaPublicKeyB64Str
}

func DecryptStringRSA(str string) (string, error) {
	data, err := base64.StdEncoding.DecodeString(str)
	if err != nil {
		return "", err
	}
	buf, err := rsa.DecryptPKCS1v15(rand.Reader, rsaPrivateKey, data)
	if err != nil {
		return "", err
	}
	return string(buf), nil
}
```

在 Unity 里，C# 部分解析 RSA 公钥的方法是不能用的，会报 `PlatformNotSupportedException`，原因不明。可以用开源的 Bouncy Castle 来解析公钥：

- [Bouncy Castle 官网](https://www.bouncycastle.org/csharp/)
- [Bouncy Castle GitHub 镜像](https://github.com/bcgit/bc-csharp)

``` csharp title="前端 RSA"
public RSA CreateRSA()
{
    var provider = new RSACryptoServiceProvider();
    provider.ImportParameters(ParsePKCS1DERPublicKey(Data));
    return provider;
}

// 解析 DER 格式的 PKCS#1 公钥
private static RSAParameters ParsePKCS1DERPublicKey(string derPublicKey)
{
    // 将 DER 编码的公钥转换为字节数组
    byte[] derBytes = Convert.FromBase64String(derPublicKey);

    // 使用 BouncyCastle 进行 DER 解码
    Asn1Object obj = Asn1Object.FromByteArray(derBytes);
    RsaPublicKeyStructure rsaPubKey = RsaPublicKeyStructure.GetInstance(obj);

    return new RSAParameters
    {
        Modulus = rsaPubKey.Modulus.ToByteArrayUnsigned(),
        Exponent = rsaPubKey.PublicExponent.ToByteArrayUnsigned()
    };
}

private static void EncryptStringRSA(RSA rsa, ref string str)
{
    byte[] data = Encoding.UTF8.GetBytes(str);
    data = rsa.Encrypt(data, RSAEncryptionPadding.Pkcs1);
    str = Convert.ToBase64String(data, Base64FormattingOptions.None);
}
```

保存密码时，不能用可逆加密，更不能直接存明文。[2011 年中国网站用户信息泄露事件](https://zh.wikipedia.org/wiki/2011%E5%B9%B4%E4%B8%AD%E5%9B%BD%E7%BD%91%E7%AB%99%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%E4%BA%8B%E4%BB%B6) 中 CSDN 就因此泄露了大量密码。

现在一般都是给密码加盐（salt）再 hash，然后存进数据库。加盐就是给密码加上一个**长长长长的随机字符串，每个用户都不一样**。这样相当于提高了密码强度，而且相同密码的不同用户的 hash 值是不一样的。黑客就很难再建立彩虹表（Rainbow table）逆向 hash。

golang 内置了 [bcrypt 算法](https://pkg.go.dev/golang.org/x/crypto/bcrypt)。

=== "生成 Hash"

    ``` go
    // bcrypt 算法将盐和 hash 结果拼在一起存进 passwordHash 里
    passwordHash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
    if err != nil {
        panic(err)
    }

    // 把 passwordHash 存进数据库里
    ```

=== "检查密码"

    ``` go
    // 从数据库里取出 passwordHash

    if bcrypt.CompareHashAndPassword(passwordHash, []byte(password)) != nil {
        // 密码错误
    }
    ```

## Token 鉴权

每次请求需要鉴权的 API 时都带上账号密码很麻烦，一般会用 Token 代替。为了安全，Token 是有过期时间的，每次登录时会刷新时间。常用 JSON Web Token，[阮一峰的博客](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html) 里讲得很清楚。

可以用开源的 [jwt-go](https://github.com/golang-jwt/jwt) 生成 Token：

``` go
func generateJWTToken(userName string, secret []byte) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": userName,
		"exp": time.Now().Add(3 * 24 * time.Hour).Unix(),
	})
	return token.SignedString(secret)
}
```

鉴权功能一般用 gin 的中间件来实现：

``` go
func parseJWTToken(tokenString string, secret []byte) (userName string, err error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return secret, nil
	})
	if err != nil {
		return "", err
	}
	if !token.Valid {
		return "", fmt.Errorf("jwt token is invalid")
	}
	return token.Claims.GetSubject()
}

func JWTAuth(jwtSecret []byte) gin.HandlerFunc {
	return func(c *gin.Context) {
		userName, err := parseJWTToken(c.GetHeader("Authorization"), jwtSecret)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, model.CommonRsp{
				ReturnCode: model.ReturnCodeInvalidAuthToken,
				Message:    "Invalid auth token",
				Data:       nil,
			})
			return
		}

		// 查询用户信息
		var user db.UserData
		err = db.GetUserAccounts().FindOne(context.TODO(), bson.D{
			{"user_name", userName},
		}).Decode(&user)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, model.CommonRsp{
				ReturnCode: model.ReturnCodeInvalidAuthToken,
				Message:    "Invalid auth token",
				Data:       nil,
			})
			return
		}

        // 之后可以直接取用 user 信息
		c.Set("UserData", user)
		c.Next()
	}
}
```

JWT 的缺点是它只保存在前端，后端不能随意废弃某一个 JWT。如果对安全性要求很高，可以自己生成 uuid 作为 Token，然后存在数据库里。还可以把用户的登录设备、IP 和 Token 关联起来，存进数据库，实现将某设备踢下线的功能。
