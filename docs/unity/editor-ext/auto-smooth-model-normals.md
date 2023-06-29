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
using UnityEngine;

public static class NormalUtility
{
    public enum StoreMode
    {
        ObjectSpaceTangent = 0,
        ObjectSpaceNormal = 1,
        ObjectSpaceUV7 = 2,
        TangentSpaceUV7 = 3
    }

    public static void SmoothAndStore(GameObject go, StoreMode storeMode, bool upload, List<GameObject> outModifiedObjs = null)
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

        Dictionary<Vector3, Vector3> weightedNormals = new();
        Vector3[] vertices = mesh.vertices;
        int[] triangles = mesh.triangles;

        for (int i = 0; i <= triangles.Length - 3; i += 3)
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

                Vector3 vertex = vertices[triangles[i + j]];
                Vector3 vec1 = (vertices[triangles[i + offset1]] - vertex).normalized;
                Vector3 vec2 = (vertices[triangles[i + offset2]] - vertex).normalized;

                Vector3 normal = Vector3.Cross(vec1, vec2).normalized;
                float angle = Mathf.Acos(Vector3.Dot(vec1, vec2));

                weightedNormals.TryAdd(vertex, Vector3.zero);
                weightedNormals[vertex] += normal * angle;
            }
        }

        // 没必要除以所有权重之和，它不会改变方向。直接归一化就行
        Vector3[] newNormals = Array.ConvertAll(vertices, v => weightedNormals[v].normalized);
        StoreNormals(newNormals, mesh, storeMode, upload);
    }

    private static void CheckMeshTopology(Mesh mesh, MeshTopology topology)
    {
        for (int i = 0; i < mesh.subMeshCount; i++)
        {
            if (mesh.GetTopology(i) != topology)
            {
                throw new InvalidOperationException($"Invalid mesh topology (SubMesh {i}). Expected is {topology}.");
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
    public static readonly uint Version = 5u;

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
