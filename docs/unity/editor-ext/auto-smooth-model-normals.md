# 自动平滑模型法线

!!! abstract

    导入模型后，自动平滑法线。

在做模型描边的时候，需要平滑法线，防止硬边断裂。

我写了一个简单的资源后处理器，在模型导入到 Unity 后，自动计算平滑法线，保存到切线中。

考虑到部分模型的法线是自定义的，法线需要自己计算，然后根据角度加权平均，得到平滑法线。

!!! danger "注意"

    Unity 中的叉积使用左手定则。

## 代码

``` c# title="NormalUtility.cs"
using System;
using System.Collections.Generic;
using UnityEngine;

public static class NormalUtility
{
    public enum StoreLocation
    {
        Tangent = 0,
        Normal = 1,
        UV7 = 2
    }

    private class WeightedNormal
    {
        private Vector3 m_Normals = Vector3.zero;
        private float m_Weights = 0;

        public Vector3 Value
        {
            get
            {
                if (Mathf.Approximately(m_Weights, 0.0f))
                {
                    return Vector3.zero;
                }

                return m_Normals / m_Weights;
            }
        }

        public void UpdateWith(Vector3 normal, float weight)
        {
            m_Normals += normal * weight;
            m_Weights += weight;
        }
    }

    public static void SmoothAndStore(GameObject go, StoreLocation storeLocation, bool upload)
    {
        foreach (var renderer in go.GetComponentsInChildren<SkinnedMeshRenderer>(false))
        {
            SmoothAndStore(renderer.sharedMesh, storeLocation, upload);
            Debug.Log($"Smooth normals of {renderer.gameObject.name}.", renderer);
        }

        foreach (var filter in go.GetComponentsInChildren<MeshFilter>(false))
        {
            SmoothAndStore(filter.sharedMesh, storeLocation, upload);
            Debug.Log($"Smooth normals of {filter.gameObject.name}.", filter);
        }
    }

    public static void SmoothAndStore(Mesh mesh, StoreLocation storeLocation, bool upload)
    {
        CheckMeshTopology(mesh, MeshTopology.Triangles);

        Dictionary<Vector3, WeightedNormal> smoothNormals = new();
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
                smoothNormals.GetOrAdd(vertex).UpdateWith(normal, angle);
            }
        }

        Vector3[] normals = Array.ConvertAll(vertices, v => smoothNormals[v].Value);
        StoreNormals(normals, mesh, storeLocation, upload);
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

    private static void StoreNormals(Vector3[] normals, Mesh mesh, StoreLocation location, bool upload)
    {
        switch (location)
        {
            case StoreLocation.Tangent:
                mesh.SetTangents(Array.ConvertAll(normals, n => (Vector4)n));
                break;

            case StoreLocation.Normal:
                mesh.SetNormals(normals);
                break;

            case StoreLocation.UV7:
                mesh.SetUVs(6, normals);
                break;

            default:
                throw new NotImplementedException();
        }

        if (upload)
        {
            mesh.UploadMeshData(false);
        }
    }

    private static TValue GetOrAdd<TKey, TValue>(this Dictionary<TKey, TValue> self, TKey key)
        where TValue : class, new()
    {
        if (!self.TryGetValue(key, out TValue value))
        {
            value = new TValue();
            self.Add(key, value);
        }

        return value;
    }
}
```

``` c# title="AvatarModelPostprocessor.cs"
using System.IO;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEngine;

public class AvatarModelPostprocessor : AssetPostprocessor
{
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
        importer.importTangents = ModelImporterTangents.None;
    }

    private void OnPostprocessModel(GameObject go)
    {
        if (!IsAvatarModel)
        {
            return;
        }

        NormalUtility.SmoothAndStore(go, NormalUtility.StoreLocation.Tangent, false);
        Debug.Log("<b>[Smooth Normal]</b> " + assetPath);
    }

    public override uint GetVersion()
    {
        return 2;
    }
}
```
