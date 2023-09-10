# 自动平滑模型法线

!!! abstract

    导入模型后，自动平滑法线。

在做模型描边的时候，需要平滑法线，防止硬边断裂。

我写了一个简单的资源后处理器，在模型导入到 Unity 后，自动计算平滑法线，保存到切线中。

原始的法线数据需要自己计算，不能用模型自带的（因为有些模型里的法线是自定义的），然后根据角度加权平均，得到平滑法线。

## 代码

``` c# title="NormalUtility.cs"
using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Rendering;

public static class NormalUtility
{
    public enum StoreMode
    {
        ObjectSpaceTangent = 0,
        ObjectSpaceNormal = 1,
        ObjectSpaceUV7 = 2,
        TangentSpaceUV7 = 3
    }

    public static void SmoothAndStore(GameObject go, StoreMode storeMode, bool upload,
        List<GameObject> outModifiedObjs = null)
    {
        foreach (var renderer in go.GetComponentsInChildren<SkinnedMeshRenderer>(false))
        {
            SmoothAndStore(renderer.sharedMesh, storeMode, upload);
            outModifiedObjs?.Add(renderer.gameObject);
        }

        foreach (var filter in go.GetComponentsInChildren<MeshFilter>(false))
        {
            SmoothAndStore(filter.sharedMesh, storeMode, upload);
            outModifiedObjs?.Add(filter.gameObject);
        }
    }

    public static void SmoothAndStore(Mesh mesh, StoreMode storeMode, bool upload)
    {
        CheckMeshTopology(mesh, MeshTopology.Triangles);

        Vector3[] vertices = mesh.vertices;
        List<int> indices = new();
        Vector3[] normals = new Vector3[vertices.Length];
        Dictionary<Vector3, Vector3> weightedNormals = new();

        // 一些 MMD 模型有背面顶点，如果整个 Mesh 一起计算平滑法线，正反法线会相互抵消，最后变成零向量
        // 有背面顶点是因为材质、法线和正面的不一样，所以背面顶点和对应的正面顶点不在一个 SubMesh 里
        // 下面，以 SubMesh 为单位分开计算
        for (int subMeshIndex = 0; subMeshIndex < mesh.subMeshCount; subMeshIndex++)
        {
            // SubMeshDescriptor subMesh = mesh.GetSubMesh(subMeshIndex);
            mesh.GetIndices(indices, subMeshIndex, applyBaseVertex: true); // subMesh.baseVertex

            for (int i = 0; i <= indices.Count - 3; i += 3)
            {
                for (int j = 0; j < 3; j++)
                {
                    // Unity 中满足左手定则
                    (int offset1, int offset2) = j switch
                    {
                        0 => (1, 2),
                        1 => (2, 0),
                        2 => (0, 1),
                        _ => throw new NotSupportedException() // Unreachable
                    };

                    Vector3 vertex = vertices[indices[i + j]];
                    Vector3 vec1 = vertices[indices[i + offset1]] - vertex;
                    Vector3 vec2 = vertices[indices[i + offset2]] - vertex;
                    Vector3 normal = GetWeightedNormal(vec1, vec2);

                    // 这里应该可以直接用 Vector3 当 Key
                    // TODO: 如果有精度问题再改
                    weightedNormals.TryAdd(vertex, Vector3.zero);
                    weightedNormals[vertex] += normal;
                }
            }

            // for (int i = 0; i < subMesh.vertexCount; i++)
            // {
            //     int vertexIndex = subMesh.firstVertex + i;
            //     Vector3 vertex = vertices[vertexIndex];
            //
            //     // 看 Unity 官方文档
            //     // 顶点可能不在当前 SubMesh 里
            //     // 顶点也可能同时在多个 SubMesh 里
            //
            //     if (weightedNormals.TryGetValue(vertex, out Vector3 n))
            //     {
            //         normals[vertexIndex] += n;
            //     }
            // }

            foreach (int vertexIndex in indices.Distinct())
            {
                Vector3 vertex = vertices[vertexIndex];
                normals[vertexIndex] += weightedNormals[vertex];
            }

            indices.Clear();
            weightedNormals.Clear();
        }

        for (int i = 0; i < normals.Length; i++)
        {
            // 没必要除以所有权重之和，它不会改变方向。直接归一化就行
            normals[i] = normals[i].normalized;
        }

        StoreNormals(normals, mesh, storeMode, upload);
    }

    private static Vector3 GetWeightedNormal(Vector3 vec1, Vector3 vec2)
    {
        // Vector3 在归一化的时候有做精度限制
        // 模型太小时，直接用 Vector3 算出来会有很多零向量
        // 这里用 double 先放大数倍然后再算
        const double scale = 1e8;

        double x1 = vec1.x * scale;
        double y1 = vec1.y * scale;
        double z1 = vec1.z * scale;
        double len1 = Math.Sqrt(x1 * x1 + y1 * y1 + z1 * z1);

        double x2 = vec2.x * scale;
        double y2 = vec2.y * scale;
        double z2 = vec2.z * scale;
        double len2 = Math.Sqrt(x2 * x2 + y2 * y2 + z2 * z2);

        // normal = cross(vec1, vec2)
        double nx = y1 * z2 - z1 * y2;
        double ny = z1 * x2 - x1 * z2;
        double nz = x1 * y2 - y1 * x2;
        double lenNormal = Math.Sqrt(nx * nx + ny * ny + nz * nz);

        // angle between vec1 and vec2
        double angle = Math.Acos((x1 * x2 + y1 * y2 + z1 * z2) / (len1 * len2));

        // normalize & weight
        nx = nx * angle / lenNormal;
        ny = ny * angle / lenNormal;
        nz = nz * angle / lenNormal;
        return new Vector3((float)nx, (float)ny, (float)nz);
    }

    private static void CheckMeshTopology(Mesh mesh, MeshTopology topology)
    {
        for (int i = 0; i < mesh.subMeshCount; i++)
        {
            if (mesh.GetTopology(i) != topology)
            {
                throw new InvalidOperationException(
                    $"Invalid mesh topology (SubMesh {i}). Expected is {topology}.");
            }
        }
    }

    private static void StoreNormals(Vector3[] newNormals, Mesh mesh, StoreMode mode, bool upload)
    {
        switch (mode)
        {
            case StoreMode.ObjectSpaceTangent:
                mesh.SetTangents(Array.ConvertAll(newNormals, n => (Vector4)n));
                break;

            case StoreMode.ObjectSpaceNormal:
                mesh.SetNormals(newNormals);
                break;

            case StoreMode.ObjectSpaceUV7:
                mesh.SetUVs(6, newNormals);
                break;

            case StoreMode.TangentSpaceUV7:
            {
                Vector4[] tangents = mesh.tangents;
                Vector3[] normals = mesh.normals;

                for (int i = 0; i < newNormals.Length; i++)
                {
                    Vector3 normal = normals[i];
                    Vector3 tangent = tangents[i];
                    Vector3 binormal = (Vector3.Cross(normal, tangent) * tangents[i].w).normalized;

                    // tbn 是正交矩阵
                    Matrix4x4 tbn = new(tangent, binormal, normal, Vector4.zero);
                    newNormals[i] = tbn.transpose.MultiplyVector(newNormals[i]);
                }

                goto case StoreMode.ObjectSpaceUV7;
            }

            default:
                throw new NotImplementedException();
        }

        if (upload)
        {
            mesh.UploadMeshData(false);
        }
    }
}
```

``` c# title="AvatarModelPostprocessor.cs"
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEngine;

public class AvatarModelPostprocessor : AssetPostprocessor
{
    public static readonly ModelImporterTangents ImportTangents = ModelImporterTangents.None;
    public static readonly NormalUtility.StoreMode NormalStoreMode = NormalUtility.StoreMode.ObjectSpaceTangent;
    public static readonly uint Version = 10u;

    private bool IsAvatarModel
    {
        get
        {
            string modelName = Path.GetFileNameWithoutExtension(assetPath);
            return Regex.IsMatch(modelName, @"^Avatar_.+_00$");
        }
    }

    private void OnPreprocessModel()
    {
        if (!IsAvatarModel)
        {
            return;
        }

        ModelImporter importer = (ModelImporter)assetImporter;
        importer.importTangents = ImportTangents;
    }

    private void OnPostprocessModel(GameObject go)
    {
        if (!IsAvatarModel)
        {
            return;
        }

        List<GameObject> modifiedObjs = new();
        NormalUtility.SmoothAndStore(go, NormalStoreMode, false, modifiedObjs);
        string subObjList = string.Join('\n', modifiedObjs.Select(o => o.name));
        Debug.Log($"<b>[Smooth Normal]</b> {assetPath}\n" + subObjList);
    }

    public override uint GetVersion()
    {
        return Version;
    }
}
```
