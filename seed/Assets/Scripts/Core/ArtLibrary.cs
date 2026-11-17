using System.Collections.Generic;
using UnityEngine;

namespace Vampire
{
    /// <summary>
    /// 素材取用的唯一入口。
    /// 规则：先从 Resources/Art 里找同名 PNG（你自己画或下载的真素材），
    /// 找不到就用代码现画一个占位图 —— 这样游戏任何时候都能跑起来，
    /// 换素材时只覆盖同名 PNG，一行代码都不用改。
    /// </summary>
    public static class ArtLibrary
    {
        const int PIXELS_PER_UNIT = 64;   // 一格 = 64 像素 = 1 个世界单位
        static readonly Dictionary<string, Sprite> cache = new Dictionary<string, Sprite>();

        public static Sprite Get(string name, Color tint = default, int shape = 0)
        {
            if (cache.TryGetValue(name, out var cached) && cached != null) return cached;

            var s = Resources.Load<Sprite>("Art/" + name);
            if (s == null) s = MakeFallback(tint.a <= 0f ? Color.magenta : tint, shape);

            cache[name] = s;
            return s;
        }

        /// <summary>兜底图：0=圆 1=菱形 2=方 3=星点（子弹）</summary>
        static Sprite MakeFallback(Color color, int shape)
        {
            int n = PIXELS_PER_UNIT;
            var tex = new Texture2D(n, n, TextureFormat.RGBA32, false)
            {
                filterMode = FilterMode.Point,
                wrapMode = TextureWrapMode.Clamp
            };
            var px = new Color32[n * n];
            float c = (n - 1) * 0.5f;

            for (int y = 0; y < n; y++)
            for (int x = 0; x < n; x++)
            {
                float dx = x - c, dy = y - c;
                bool inside;
                switch (shape)
                {
                    case 1: inside = Mathf.Abs(dx) / c + Mathf.Abs(dy) / c <= 1f; break;
                    case 2: inside = Mathf.Abs(dx) <= c * 0.75f && Mathf.Abs(dy) <= c * 0.75f; break;
                    case 3: inside = dx * dx + dy * dy <= c * 0.22f; break;
                    default: inside = dx * dx + dy * dy <= c * c; break;
                }
                px[y * n + x] = inside ? (Color32)color : new Color32(0, 0, 0, 0);
            }

            tex.SetPixels32(px);
            tex.Apply();
            var sp = Sprite.Create(tex, new Rect(0, 0, n, n), new Vector2(0.5f, 0.5f), PIXELS_PER_UNIT);
            sp.name = name + "_fallback";
            return sp;
        }

        /// <summary>主界面用的中文字体：拿系统字体，避免内置字体缺汉字。</summary>
        public static Font UiFont()
        {
            var f = Font.CreateDynamicFontFromOSFont(
                new[] { "Microsoft YaHei", "微软雅黑", "SimHei", "PingFang SC", "Noto Sans CJK SC" }, 20);
            if (f != null) return f;

            // 老版本 Unity 内置字体叫 Arial.ttf，新版本叫 LegacyRuntime.ttf
            var legacy = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            return legacy != null ? legacy : Resources.GetBuiltinResource<Font>("Arial.ttf");
        }
    }
}
