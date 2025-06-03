---
date: 2024-11-29T14:50:47
publish: true
comments: true
permalink: implement-dx12-shaderlab
aliases:
---

# 基于 DX12 实现 ShaderLab

ShaderLab 是对 `ID3D12RootSignature` 和 `ID3D12PipelineState` 的封装。每次写完 Shader 就会自动生成 `RootSignature` 和 `PipelineState`，不用再人工填写那一坨参数。

<!-- more -->

大体设计如下，成员就不写了。

``` mermaid
classDiagram
    Shader --> ShaderKeywordSpace
    Shader --> "many" ShaderProperty : Contains
    Shader --> "many" ShaderPass : Contains
    ShaderPass --> ShaderPassRenderState
    ShaderPass --> "many" ShaderProgram : Contains
    ShaderProgram --> ShaderKeywordSet

    class Shader
    class ShaderProperty
    class ShaderPass
    class ShaderPassRenderState
    class ShaderProgram
    class ShaderKeywordSpace
    class ShaderKeywordSet
```

## 编译器

引擎的上层逻辑使用 C#，所以语法分析用 `antlr4` 实现，其他的方案有 `yacc` 和 `lex`。`antlr4` 可以从我的 [[Scoop|Scoop]] Bucket 快速安装，然后直接用 `antlr4` 或 `antlr4-parse` 命令，前者是生成代码的工具，后者是解释器。

``` bash
scoop install java/openjdk11
scoop install stalo/antlr4
```

- 官方样例：[antlr/grammars-v4](https://github.com/antlr/grammars-v4)
- 简单教程：[ANTLR 4简明教程](https://wizardforcel.gitbooks.io/antlr4-short-course/content/getting-started.html)

提取 `hlsl` 代码时，使用 [`#line` 指令](https://learn.microsoft.com/en-us/cpp/preprocessor/hash-line-directive-c-cpp?view=msvc-170) 增加行号信息，再给 [DXC](https://github.com/microsoft/DirectXShaderCompiler) 编译，这样出错时就能正确显示源码的位置。

``` csharp
public override int VisitHlslProgramDeclaration([NotNull] ShaderLabParser.HlslProgramDeclarationContext context)
{
    // Remove HLSLPROGRAM and ENDHLSL，但要保留换行，不要 Trim，后面要设置行号
    string code = context.HlslProgram().GetText()[11..^7];

    // 保证行号和源文件一致
    // 注意：#line 设置的是下一行的行号
    int startLineNumber = context.HlslProgram().Symbol.Line;
    CurrentPass.HlslProgram = $"#line {startLineNumber}\n" + code;

    return base.VisitHlslProgramDeclaration(context);
}
```

下面给出 ShaderLab 的一部分语法。

``` antlr4
grammar ShaderLab;

shader
    : 'Shader' StringLiteral LeftBrace shaderDeclaration* RightBrace
    ;

shaderDeclaration
    : propertiesBlock
    | tagsBlock
    | renderStateDeclaration
    | hlslIncludeDeclaration
    | passBlock
    ;

propertiesBlock
    : 'Properties' LeftBrace propertyDeclaration* RightBrace
    ;

passBlock
    : 'Pass' LeftBrace passDeclaration* RightBrace
    ;

passDeclaration
    : nameDeclaration
    | tagsBlock
    | renderStateDeclaration
    | hlslProgramDeclaration
    ;

attributeDeclaration
    : BracketLiteral
    ;

numberLiteralExpression
    : IntegerLiteral
    | FloatLiteral
    ;

vectorLiteralExpression
    : '(' numberLiteralExpression ',' numberLiteralExpression ',' numberLiteralExpression ',' numberLiteralExpression ')'
    ;

textureLiteralExpression
    : StringLiteral LeftBrace RightBrace
    ;

propertyDefaultValueExpression
    : numberLiteralExpression
    | vectorLiteralExpression
    | textureLiteralExpression
    ;

propertyTypeDeclaration
    : Float
    | Int
    | Color
    | Vector
    | Texture
    ;

propertyDeclaration
    : attributeDeclaration* Identifier '(' StringLiteral ',' propertyTypeDeclaration ')' Assign propertyDefaultValueExpression
    ;

nameDeclaration
    : 'Name' StringLiteral
    ;

renderStateDeclaration
    : cullDeclaration
    | zTestDeclaration
    | zWriteDeclaration
    | blendDeclaration
    | blendOpDeclaration
    | colorMaskDeclaration
    | stencilBlock
    ;

tagsBlock
    : 'Tags' LeftBrace tagDeclaration* RightBrace
    ;

tagDeclaration
    : StringLiteral Assign StringLiteral
    ;

cullDeclaration
    : 'Cull' (cullModeValue | BracketLiteral)
    ;

zTestDeclaration
    : 'ZTest' (Disabled | compareFuncValue | BracketLiteral)
    ;

zWriteDeclaration
    : 'ZWrite' (Off | On | BracketLiteral)
    ;

blendDeclaration
    : 'Blend' IntegerLiteral? (Off | (blendFactorValueOrBracketLiteral blendFactorValueOrBracketLiteral (',' blendFactorValueOrBracketLiteral blendFactorValueOrBracketLiteral)?))
    ;

blendOpDeclaration
    : 'BlendOp' IntegerLiteral? blendOpValueOrBracketLiteral (',' blendOpValueOrBracketLiteral)?
    ;

colorMaskDeclaration
    : 'ColorMask' IntegerLiteral                 # colorMaskInt1Declaration
    | 'ColorMask' IntegerLiteral IntegerLiteral  # colorMaskInt2Declaration
    | 'ColorMask' IntegerLiteral? Identifier     # colorMaskIdentifierDeclaration
    | 'ColorMask' IntegerLiteral? BracketLiteral # colorMaskBracketLiteralDeclaration
    ;

stencilBlock
    : 'Stencil' LeftBrace stencilDeclaration* RightBrace
    ;

stencilDeclaration
    : stencilRefDeclaration
    | stencilReadMaskDeclaration
    | stencilWriteMaskDeclaration
    | stencilCompDeclaration
    | stencilPassDeclaration
    | stencilFailDeclaration
    | stencilZFailDeclaration
    | stencilCompFrontDeclaration
    | stencilPassFrontDeclaration
    | stencilFailFrontDeclaration
    | stencilZFailFrontDeclaration
    | stencilCompBackDeclaration
    | stencilPassBackDeclaration
    | stencilFailBackDeclaration
    | stencilZFailBackDeclaration
    ;

stencilRefDeclaration
    : 'Ref' (IntegerLiteral | BracketLiteral)
    ;

stencilReadMaskDeclaration
    : 'ReadMask' (IntegerLiteral | BracketLiteral)
    ;

stencilWriteMaskDeclaration
    : 'WriteMask' (IntegerLiteral | BracketLiteral)
    ;

stencilCompDeclaration
    : 'Comp' (compareFuncValue | BracketLiteral)
    ;

stencilPassDeclaration
    : 'Pass' (stencilOpValue | BracketLiteral)
    ;

stencilFailDeclaration
    : 'Fail' (stencilOpValue | BracketLiteral)
    ;

stencilZFailDeclaration
    : 'ZFail' (stencilOpValue | BracketLiteral)
    ;

stencilCompFrontDeclaration
    : 'CompFront' (compareFuncValue | BracketLiteral)
    ;

stencilPassFrontDeclaration
    : 'PassFront' (stencilOpValue | BracketLiteral)
    ;

stencilFailFrontDeclaration
    : 'FailFront' (stencilOpValue | BracketLiteral)
    ;

stencilZFailFrontDeclaration
    : 'ZFailFront' (stencilOpValue | BracketLiteral)
    ;

stencilCompBackDeclaration
    : 'CompBack' (compareFuncValue | BracketLiteral)
    ;

stencilPassBackDeclaration
    : 'PassBack' (stencilOpValue | BracketLiteral)
    ;

stencilFailBackDeclaration
    : 'FailBack' (stencilOpValue | BracketLiteral)
    ;

stencilZFailBackDeclaration
    : 'ZFailBack' (stencilOpValue | BracketLiteral)
    ;

hlslIncludeDeclaration
    : HlslInclude
    ;

hlslProgramDeclaration
    : HlslProgram
    ;

HlslInclude
    : 'HLSLINCLUDE' .*? 'ENDHLSL'
    ;

HlslProgram
    : 'HLSLPROGRAM' .*? 'ENDHLSL'
    ;

cullModeValue
    : Off
    | Front
    | Back
    ;

blendFactorValue
    : Zero
    | One
    | SrcColor
    | OneMinusSrcColor
    | SrcAlpha
    | OneMinusSrcAlpha
    | DstAlpha
    | OneMinusDstAlpha
    | DstColor
    | OneMinusDstColor
    | SrcAlphaSaturate
    ;

blendFactorValueOrBracketLiteral
    : blendFactorValue
    | BracketLiteral
    ;

blendOpValue
    : Add
    | Sub
    | RevSub
    | Min
    | Max
    ;

blendOpValueOrBracketLiteral
    : blendOpValue
    | BracketLiteral
    ;

compareFuncValue
    : Never
    | Less
    | Equal
    | LEqual
    | Greater
    | NotEqual
    | GEqual
    | Always
    ;

stencilOpValue
    : Keep
    | Zero
    | Replace
    | IncrSat
    | DecrSat
    | Invert
    | IncrWrap
    | DecrWrap
    ;
```

## 变体

变体本质上是将动态分支放到编译期处理，在代码中声明 Keyword 就能创建变体。

``` cpp
#pragma multi_compile _ _ALPHATEST_ON
```

在编译 `hlsl` 前，用正则表达式得到代码中声明的 Keyword。

``` cpp
std::regex re(R"(^\s*#\s*pragma\s+(.*))", std::regex::ECMAScript);
auto itEnd = std::sregex_iterator();

for (auto it = std::sregex_iterator(source.begin(), source.end(), re); it != itEnd; ++it)
{
    std::string temp{};
    std::vector<std::string> args{};
    std::istringstream iss((*it)[1]);

    while (iss >> temp)
    {
        args.emplace_back(std::move(temp));
    }

    if (args.empty())
    {
        continue;
    }

    // ...

    if (args[0] == "multi_compile" && args.size() > 1)
    {
        std::unordered_set<std::string> uniqueKeywords{};

        for (size_t i = 1; i < args.size(); i++)
        {
            // _ 表示没有 Keyword，替换为空字符串
            if (std::all_of(args[i].begin(), args[i].end(), [](char c) { return c == '_'; }))
            {
                uniqueKeywords.insert("");
            }
            else
            {
                // ...

                uniqueKeywords.insert(args[i]);
            }
        }

        config.MultiCompile.emplace_back(uniqueKeywords.begin(), uniqueKeywords.end());
    }
}
```

然后，对不同的 Keyword 组合各进行一次编译。显然，随着 Keyword 数量增加，编译出来的体积会指数爆炸，对运行时的性能也会有更大的影响。Unity 的文档中有相对详细的说明：

> Unity can use up to 4,294,967,294 global shader keywords. Individual shaders and compute shaders can use up to 65,534 local shader keywords. These totals include keywords used for variants, and keywords used for dynamic branching.
>
> Every keyword declared in the shader source file and its dependencies count towards this limit. Dependencies include [Passes](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Pass.html) that the shader includes with [UsePass](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-UsePass.html), and [fallbacks](https://docs.unity3d.com/6000.0/Documentation/Manual/SL-Fallback.html).
>
> If Unity encounters a shader keyword with the same name multiple times, it only counts towards the limit once.
>
> ==If a shader uses more than 128 keywords in total, it incurs a small runtime performance penalty==; therefore, it is best to keep the number of keywords low. Unity always reserves 4 keywords per shader. [^1]

为了方便实现，我将引擎的 Keyword 数量上限定为 128，这样使用 `std::bitset<128>` 保存 Keyword 组合就行了。128 位相当于一个 `Vector4` 的大小，是可以接受的。

模仿 Unity，先实现一个类似 `namespace` 的 `ShaderKeywordSpace`，把 Keyword 映射到一个 $[0,128)$ 范围内的整数。每个 Shader 都有自己独立的 `ShaderKeywordSpace`，这样就把原本「引擎的 Keyword 数量上限为 128」变成了「每个 Shader 的 Keyword 数量上限为 128」，增加了引擎总的 Keyword 上限。

``` cpp
class ShaderKeywordSpace
{
public:
    ShaderKeywordSpace();

    ShaderKeywordSpace(const ShaderKeywordSpace&) = delete;
    ShaderKeywordSpace& operator =(const ShaderKeywordSpace&) = delete;

    enum class AddKeywordResult
    {
        Success = 0,
        AlreadyExists = 1,
        OutOfSpace = 2,
    };

    size_t GetKeywordCount() const;
    int8_t GetKeywordIndex(const std::string& keyword) const;
    const std::string& GetKeywordName(int8_t index) const;
    AddKeywordResult AddKeyword(const std::string& keyword);
    void Clear();

private:
    std::unordered_map<std::string, uint8_t> m_KeywordIndexMap;
    uint8_t m_NextIndex; // 目前最多支持 128 个 Keyword
};
```

然后封装 `ShaderKeywordSet` 用于记录 Keyword 组合。

``` cpp
class ShaderKeywordSet
{
public:
    using data_t = std::bitset<128>;

    ShaderKeywordSet();

    size_t GetEnabledKeywordCount() const;
    size_t GetMatchingKeywordCount(const ShaderKeywordSet& other) const;
    std::vector<std::string> GetEnabledKeywords(const ShaderKeywordSpace& space) const;
    const data_t& GetData() const { return m_Keywords; }

    void SetKeyword(const ShaderKeywordSpace& space, const std::string& keyword, bool value);
    void EnableKeyword(const ShaderKeywordSpace& space, const std::string& keyword);
    void DisableKeyword(const ShaderKeywordSpace& space, const std::string& keyword);
    void Clear();

private:
    data_t m_Keywords;
};
```

在运行时，我们要根据 `Material` 中启用的 Keyword 组合，寻找最匹配的一组 `ShaderProgram`。为了避免重复查找，匹配结果会缓存在 `ShaderPass` 中。

``` cpp
class ShaderPass
{
    // ...

    struct ProgramMatch
    {
        int32_t Indices[ShaderProgram::NumTypes]; // -1 表示 nullptr
        size_t Hash;
    };
    
    std::unordered_map<ShaderKeywordSet::data_t, ProgramMatch> m_ProgramMatches;
};
```

匹配就是遍历所有 `ShaderProgram`，计算其 Keyword 组合与目标组合的距离，然后选择距离最小的。

``` cpp
static size_t absdiff(size_t a, size_t b)
{
    return a > b ? a - b : b - a;
}

const ShaderPass::ProgramMatch& ShaderPass::GetProgramMatch(const ShaderKeywordSet& keywords)
{
    auto [it, isNew] = m_ProgramMatches.try_emplace(keywords.GetData());

    if (isNew)
    {
        ProgramMatch& m = it->second;
        m.Hash = HashUtils::DefaultHash;

        size_t targetKeywordCount = keywords.GetEnabledKeywordCount();

        for (int32_t i = 0; i < ShaderProgram::NumTypes; i++)
        {
            size_t minDiff = std::numeric_limits<size_t>::max();
            m.Indices[i] = -1;

            for (size_t j = 0; j < m_Programs[i].size(); j++)
            {
                const ShaderKeywordSet& ks = m_Programs[i][j]->GetKeywords();
                size_t matchingCount = ks.GetMatchingKeywordCount(keywords);
                size_t enabledCount = ks.GetEnabledKeywordCount();

                // 没 match 的数量 + 多余的数量
                size_t diff = absdiff(targetKeywordCount, matchingCount) + absdiff(enabledCount, matchingCount);

                if (diff < minDiff)
                {
                    minDiff = diff;
                    m.Indices[i] = static_cast<int32_t>(j);
                }
            }

            if (m.Indices[i] != -1)
            {
                ShaderProgram* program = m_Programs[i][m.Indices[i]].get();
                m.Hash = HashUtils::FNV1(program->GetHash(), std::size(program->GetHash()), m.Hash);
            }
        }
    }

    return it->second;
}
```

## RootSignature

在 Shader 编译完成后，可以用反射记录资源的 `shader register`、`register space` 等信息。

``` cpp
ComPtr<IDxcBlob> pReflectionData;
GFX_HR(pResults->GetOutput(DXC_OUT_REFLECTION, IID_PPV_ARGS(&pReflectionData), nullptr));
if (pReflectionData != nullptr)
{
    // Create reflection interface.
    DxcBuffer ReflectionData = {};
    ReflectionData.Encoding = DXC_CP_ACP;
    ReflectionData.Ptr = pReflectionData->GetBufferPointer();
    ReflectionData.Size = pReflectionData->GetBufferSize();

    ComPtr<ID3D12ShaderReflection> pReflection;
    context.Utils->CreateReflection(&ReflectionData, IID_PPV_ARGS(&pReflection));

    // ...
}
```

在运行时，根据记录的信息就能构建出 `ID3D12RootSignature`。在下面的示例代码中

- `g_GlobalRootSignaturePool` 是一个全局的对象池。创建 `RootSignature` 前要先序列化参数，刚好可以拿序列化的数据做 Hash，然后 Hash 相同的直接复用旧对象。我之前截帧 Unity，发现它们的 `RootSignature` 就是复用的，确实有不少 Shader 的 `RootSignature` 是一样的。
- `m_RootSignatures` 是 `ShaderPass` 中的缓存，Key 是 `ShaderPass::ProgramMatch::Hash`。

    ``` cpp
    class ShaderPass
    {
        // ...
    
        std::unordered_map<size_t, Microsoft::WRL::ComPtr<ID3D12RootSignature>> m_RootSignatures;
    };
    ```

> [!NOTE]- 关于 Hash Collision
> Hash collisions are to be expected, and they indicate a duplicate object. We avoid duplication by checking an STL map for pre-existing hash values. (Essentially a hash map.) Unexpected collisions (where two completely different series of bytes yield the same hash value), on the other hand, should be so exceedingly rare as to probably never be noticed. If unexpected collisions do arise, I'd suspect you have a different bug (such as in the hashing system itself.) [^2]

``` cpp
// RootSignature 根据 Hash 复用
static std::unordered_map<size_t, ComPtr<ID3D12RootSignature>> g_GlobalRootSignaturePool{};

static ID3D12RootSignature* CreateRootSignature(ID3DBlob* serializedData)
{
    LPVOID bufferPointer = serializedData->GetBufferPointer();
    SIZE_T bufferSize = serializedData->GetBufferSize();

    if (bufferSize % 4 != 0)
    {
        throw GfxException("Invalid root signature data size");
    }

    size_t hash = HashUtils::FNV1(static_cast<uint32_t*>(bufferPointer), bufferSize / 4);
    ComPtr<ID3D12RootSignature>& result = g_GlobalRootSignaturePool[hash];

    if (result == nullptr)
    {
        ID3D12Device4* device = GetGfxDevice()->GetD3D12Device();
        GFX_HR(device->CreateRootSignature(0, bufferPointer, bufferSize, IID_PPV_ARGS(result.GetAddressOf())));
    }

    return result.Get();
}

ID3D12RootSignature* ShaderPass::GetRootSignature(const ShaderKeywordSet& keywords)
{
    const ShaderPass::ProgramMatch& m = GetProgramMatch(keywords);

    if (auto it = m_RootSignatures.find(m.Hash); it != m_RootSignatures.end())
    {
        return it->second.Get();
    }

    std::vector<CD3DX12_ROOT_PARAMETER> params;
    std::vector<CD3DX12_STATIC_SAMPLER_DESC> staticSamplers;
    std::vector<CD3DX12_DESCRIPTOR_RANGE> srvUavRanges;
    std::vector<CD3DX12_DESCRIPTOR_RANGE> samplerRanges;

    for (int32_t i = 0; i < ShaderProgram::NumTypes; i++)
    {
        if (m.Indices[i] == -1)
        {
            continue;
        }

        ShaderProgram* program = m_Programs[i][static_cast<size_t>(m.Indices[i])].get();
        size_t srvUavStartIndex = srvUavRanges.size();
        size_t samplerStartIndex = samplerRanges.size();
        D3D12_SHADER_VISIBILITY visibility = GetShaderVisibility(static_cast<ShaderProgramType>(i));

        // ...
    }

    CD3DX12_ROOT_SIGNATURE_DESC desc(
        static_cast<UINT>(params.size()), params.data(),
        static_cast<UINT>(staticSamplers.size()), staticSamplers.data(),
        D3D12_ROOT_SIGNATURE_FLAG_ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT);

    ComPtr<ID3DBlob> serializedData = nullptr;
    ComPtr<ID3DBlob> error = nullptr;
    HRESULT hr = D3D12SerializeRootSignature(&desc, D3D_ROOT_SIGNATURE_VERSION_1, serializedData.GetAddressOf(), error.GetAddressOf());

    if (error != nullptr)
    {
        LOG_ERROR(reinterpret_cast<char*>(error->GetBufferPointer()));
    }

    GFX_HR(hr);

    ID3D12RootSignature* result = CreateRootSignature(serializedData.Get());
    m_RootSignatures[m.Hash] = result;
    return result;
}
```

## PipelineState

创建 `ID3D12PipelineState` 的参数非常多，我将它们拆成三部分。

1. 由 `Mesh` 决定的 `GfxInputDesc`

    ``` cpp
    enum class GfxSemantic
    {
        Position,
        Normal,
        Tangent,
        Color,
        TexCoord0,
        TexCoord1,
        TexCoord2,
        TexCoord3,
        TexCoord4,
        TexCoord5,
        TexCoord6,
        TexCoord7,
    
        // Aliases
        TexCoord = TexCoord0,
    };
    
    struct GfxInputElement
    {
        GfxSemantic Semantic;
        DXGI_FORMAT Format;
        uint32_t InputSlot;
        D3D12_INPUT_CLASSIFICATION InputSlotClass;
        uint32_t InstanceDataStepRate;
    
        constexpr GfxInputElement(
            GfxSemantic semantic,
            DXGI_FORMAT format,
            uint32_t inputSlot = 0,
            D3D12_INPUT_CLASSIFICATION inputSlotClass = D3D12_INPUT_CLASSIFICATION_PER_VERTEX_DATA,
            uint32_t instanceDataStepRate = 0) noexcept
            : Semantic(semantic)
            , Format(format)
            , InputSlot(inputSlot)
            , InputSlotClass(inputSlotClass)
            , InstanceDataStepRate(instanceDataStepRate) {}
    };
    
    class GfxInputDesc final
    {
    public:
        GfxInputDesc(D3D12_PRIMITIVE_TOPOLOGY topology, const std::vector<GfxInputElement>& elements);
    
        D3D12_PRIMITIVE_TOPOLOGY_TYPE GetPrimitiveTopologyType() const;
    
        D3D12_PRIMITIVE_TOPOLOGY GetPrimitiveTopology() const { return m_PrimitiveTopology; }
        const std::vector<D3D12_INPUT_ELEMENT_DESC>& GetLayout() const { return m_Layout; }
        size_t GetHash() const { return m_Hash; }
    
    private:
        D3D12_PRIMITIVE_TOPOLOGY m_PrimitiveTopology;
        std::vector<D3D12_INPUT_ELEMENT_DESC> m_Layout;
        size_t m_Hash;
    };
    ```

2. 由 `RenderGraph` 维护的 `GfxOutputDesc`

    ``` cpp
    class GfxOutputDesc final
    {
    public:
        GfxOutputDesc();
    
        void MarkDirty();
        size_t GetHash() const;
    
        bool IsDirty() const { return m_IsDirty; }
    
    public:
        std::vector<DXGI_FORMAT> RTVFormats;
        DXGI_FORMAT DSVFormat;
    
        uint32_t SampleCount;
        uint32_t SampleQuality;
    
        bool Wireframe;
    
    private:
        mutable bool m_IsDirty;
        mutable size_t m_Hash;
    };
    ```

3. 由 `Shader` 和 `Material` 决定的 `ShaderPassRenderState`

    ``` cpp
    template<typename T>
    struct ShaderPassVar
    {
        bool IsDynamic;
    
        union
        {
            int32_t PropertyId;
            T Value;
        };
    };
    
    struct ShaderPassBlendFormula
    {
        ShaderPassVar<BlendMode> Src;
        ShaderPassVar<BlendMode> Dest;
        ShaderPassVar<BlendOp> Op;
    };
    
    struct ShaderPassBlendState
    {
        bool Enable;
        ShaderPassVar<ColorWriteMask> WriteMask;
        ShaderPassBlendFormula Rgb;
        ShaderPassBlendFormula Alpha;
    };
    
    struct ShaderPassDepthState
    {
        bool Enable;
        ShaderPassVar<bool> Write;
        ShaderPassVar<CompareFunction> Compare;
    };
    
    struct ShaderPassStencilAction
    {
        ShaderPassVar<CompareFunction> Compare;
        ShaderPassVar<StencilOp> PassOp;
        ShaderPassVar<StencilOp> FailOp;
        ShaderPassVar<StencilOp> DepthFailOp;
    };
    
    struct ShaderPassStencilState
    {
        bool Enable;
        ShaderPassVar<uint8_t> Ref;
        ShaderPassVar<uint8_t> ReadMask;
        ShaderPassVar<uint8_t> WriteMask;
        ShaderPassStencilAction FrontFace;
        ShaderPassStencilAction BackFace;
    };
    
    struct ShaderPassRenderState
    {
        ShaderPassVar<CullMode> Cull;
        std::vector<ShaderPassBlendState> Blends; // 如果长度大于 1 则使用 Independent Blend
        ShaderPassDepthState DepthState;
        ShaderPassStencilState StencilState;
    };
    ```

`ShaderPassRenderState` 中存在 `Cull [_CullMode]` 这种运行时根据 `Material` 动态确定的值。

``` cpp
template<typename T, typename Intermediate>
static T& ResolveShaderPassVar(ShaderPassVar<T>& v, const std::function<Intermediate(int32_t)>& resolve)
{
    if (v.IsDynamic)
    {
        v.Value = static_cast<T>(resolve(v.PropertyId));
        v.IsDynamic = false;
    }

    return v.Value;
}

size_t GfxPipelineState::ResolveShaderPassRenderState(ShaderPassRenderState& state,
    const std::function<bool(int32_t, int32_t*)>& intResolver,
    const std::function<bool(int32_t, float*)>& floatResolver)
{
    std::function<int32_t(int32_t)> resolveInt = [&intResolver, &floatResolver](int32_t id)
    {
        if (int32_t i = 0; intResolver(id, &i)) return i;
        if (float f = 0.0f; floatResolver(id, &f)) return static_cast<int32_t>(f);
        return 0;
    };

    std::function<bool(int32_t)> resolveBool = [&intResolver, &floatResolver](int32_t id)
    {
        if (int32_t i = 0; intResolver(id, &i)) return i != 0;
        if (float f = 0.0f; floatResolver(id, &f)) return f != 0.0f;
        return false;
    };

    std::function<float(int32_t)> resolveFloat = [&intResolver, &floatResolver](int32_t id)
    {
        if (float f = 0.0f; floatResolver(id, &f)) return f;
        if (int32_t i = 0; intResolver(id, &i)) return static_cast<float>(i);
        return 0.0f;
    };

    // ...

    return hash;
}
```

Resolve 的结果会缓存在 `Material` 中。

``` cpp
const ShaderPassRenderState& Material::GetResolvedRenderState(int32_t passIndex, size_t* outHash)
{
    // ...

    auto it = m_ResolvedRenderStates.find(passIndex);

    if (it == m_ResolvedRenderStates.end())
    {
        ShaderPassRenderState rs = m_Shader->GetPass(passIndex)->GetRenderState(); // 拷贝一份
        size_t hash = GfxPipelineState::ResolveShaderPassRenderState(rs,
            [this](int32_t id, int32_t* outInt) { return GetInt(id, outInt); },
            [this](int32_t id, float* outFloat) { return GetFloat(id, outFloat); });
        it = m_ResolvedRenderStates.emplace(passIndex, std::make_pair(rs, hash)).first;
    }

    if (outHash != nullptr)
    {
        *outHash = it->second.second;
    }

    return it->second.first;
}
```

最后，把参数拼起来就能创建 `ID3D12PipelineState`。`PipelineState` 涉及非常多参数，包括编译后的 Shader 指令，不同 Shader 很难复用同一个对象（要是能复用，为什么分成两个 Shader 呢？），所以我把结果根据 Hash 缓存在 `ShaderPass` 中，有几点好处

- 不同 Shader 的 `PipelineState` 分开存，能进一步减少 Hash Collision 的可能性
- 当 Shader 被卸载时，相关的 `PipelineState` 也会被自动回收

``` cpp
class ShaderPass
{
    // ...

    std::unordered_map<size_t, Microsoft::WRL::ComPtr<ID3D12PipelineState>> m_PipelineStates;
};

ID3D12PipelineState* GfxPipelineState::GetGraphicsPSO(Material* material, int32_t passIndex, const GfxInputDesc& inputDesc, const GfxOutputDesc& outputDesc)
{
    Shader* shader = material->GetShader();
    if (shader == nullptr)
    {
        return nullptr;
    }

    ShaderPass* pass = shader->GetPass(passIndex);
    const ShaderKeywordSet& keywords = material->GetKeywords();

    size_t hash = 0;
    const ShaderPassRenderState& rs = material->GetResolvedRenderState(passIndex, &hash);
    size_t programsHash = pass->GetProgramMatch(keywords).Hash;
    hash = HashUtils::FNV1(&programsHash, 1, hash);
    size_t inputDescHash = inputDesc.GetHash();
    hash = HashUtils::FNV1(&inputDescHash, 1, hash);
    size_t outputDescHash = outputDesc.GetHash();
    hash = HashUtils::FNV1(&outputDescHash, 1, hash);

    ComPtr<ID3D12PipelineState>& result = pass->m_PipelineStates[hash];

    if (result == nullptr)
    {
        D3D12_GRAPHICS_PIPELINE_STATE_DESC psoDesc = {};

        psoDesc.pRootSignature = pass->GetRootSignature(keywords);

        // ...

        ID3D12Device4* device = GetGfxDevice()->GetD3D12Device();
        GFX_HR(device->CreateGraphicsPipelineState(&psoDesc, IID_PPV_ARGS(result.GetAddressOf())));

#ifdef ENABLE_GFX_DEBUG_NAME
        const std::string& debugName = shader->GetName() + " - " + pass->GetName();
        result->SetName(StringUtils::Utf8ToUtf16(debugName).c_str());
#endif

        LOG_TRACE("Create Graphics PSO for '%s' Pass of '%s' Shader", pass->GetName().c_str(), shader->GetName().c_str());
    }

    return result.Get();
}
```

[^1]: [Unity - Manual: Shader keyword fundamentals](https://docs.unity3d.com/6000.0/Documentation/Manual/shader-keywords.html)
[^2]: [Collision handling of PSO hash value · Issue #82 · microsoft/DirectX-Graphics-Samples](https://github.com/microsoft/DirectX-Graphics-Samples/issues/82#issuecomment-173370923)
