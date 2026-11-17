#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序化占位素材生成器（无第三方依赖，纯标准库）

用法：  python tools/gen_art.py
输出：  seed/Assets/Resources/Art/*.png   （64x64，带透明通道，像素风）

为什么先程序化生成：
1. 不用等找素材，今天就能跑起来一个能看的画面；
2. 尺寸/描边/配色统一，替换真素材时不用改代码（同名覆盖即可）；
3. 全部是我自己画的，零版权风险，能直接放进公开 GitHub 仓库。

真素材接入方式：把同名 PNG 覆盖到同一目录，游戏里自动生效（见 ArtLibrary.cs）。
"""

import os
import struct
import zlib
import math

SIZE = 64
ART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "seed", "Assets", "Resources", "Art")


class Canvas:
    """极简 RGBA 画布"""

    def __init__(self, w=SIZE, h=SIZE):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 4)  # 全透明

    def set(self, x, y, color, alpha=255):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        i = (y * self.w + x) * 4
        if alpha >= 255:
            self.px[i:i + 4] = bytes((color[0], color[1], color[2], 255))
        elif alpha > 0:
            # 简单 alpha 混合（铺在已有像素上）
            a = alpha / 255.0
            sr, sg, sb, sa = self.px[i], self.px[i + 1], self.px[i + 2], self.px[i + 3]
            da = sa / 255.0
            oa = a + da * (1 - a)
            if oa <= 0:
                return
            self.px[i] = int((color[0] * a + sr * da * (1 - a)) / oa)
            self.px[i + 1] = int((color[1] * a + sg * da * (1 - a)) / oa)
            self.px[i + 2] = int((color[2] * a + sb * da * (1 - a)) / oa)
            self.px[i + 3] = int(oa * 255)

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter type 0
            raw += self.px[y * self.w * 4:(y + 1) * self.w * 4]

        def chunk(tag, data):
            c = struct.pack(">I", len(data)) + tag + data
            return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        png += chunk(b"IEND", b"")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(png)


def blend(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def shade(edge, body, t):
    """t=0 靠近中心(body)，t=1 靠近边缘(edge)"""
    return blend(body, edge, t)


def draw_blob(cv, cx, cy, r, body, edge, wobble=0.0, seed=0):
    """画一个带描边和径向渐变的圆/水滴，wobble>0 时做轻微不规则"""
    for y in range(cv.h):
        for x in range(cv.w):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = math.hypot(dx, dy)
            if wobble:
                ang = math.atan2(dy, dx)
                d *= 1.0 + wobble * math.sin(ang * 3 + seed) * 0.5
            if d <= r:
                t = max(0.0, min(1.0, (d / r - 0.55) / 0.45))
                col = shade(edge, body, t)
                # 左上高光
                hl = (-0.45 * r, -0.45 * r)
                if math.hypot(dx - hl[0], dy - hl[1]) < r * 0.35:
                    col = blend(col, (255, 255, 255), 0.35)
                cv.set(x, y, col)
            elif d <= r + 1.6:
                cv.set(x, y, (edge[0] // 3, edge[1] // 3, edge[2] // 3), 170)


def draw_diamond(cv, cx, cy, r, body, edge):
    for y in range(cv.h):
        for x in range(cv.w):
            dx, dy = abs(x + 0.5 - cx), abs(y + 0.5 - cy)
            d = dx / r + dy / (r * 1.15)
            if d <= 1.0:
                t = max(0.0, min(1.0, (d - 0.45) / 0.55))
                col = shade(edge, body, t)
                if dx < r * 0.3 and dy < r * 0.5:
                    col = blend(col, (255, 255, 255), 0.4)
                cv.set(x, y, col)
            elif d <= 1.14:
                cv.set(x, y, (edge[0] // 3, edge[1] // 3, edge[2] // 3), 170)


def draw_round_rect(cv, x0, y0, x1, y1, rad, body, edge):
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            # 圆角距离场
            cx = min(max(x + 0.5, x0 + rad), x1 - rad)
            cy = min(max(y + 0.5, y0 + rad), y1 - rad)
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= rad:
                t = max(0.0, min(1.0, (d / rad - 0.4) / 0.6))
                cv.set(x, y, shade(edge, body, t * 0.9))
            elif d <= rad + 1.6:
                cv.set(x, y, (edge[0] // 3, edge[1] // 3, edge[2] // 3), 170)


def add_eyes(cv, cx, cy, gap, r, color=(20, 22, 30)):
    for ox in (-gap, gap):
        for y in range(cv.h):
            for x in range(cv.w):
                if math.hypot(x + 0.5 - (cx + ox), y + 0.5 - cy) <= r:
                    cv.set(x, y, color)


# ---------------------------------------------------------------- 具体素材

def make_player():
    cv = Canvas()
    draw_blob(cv, 32, 34, 15, (150, 245, 235), (20, 150, 165))
    # 兜帽/头顶
    for y in range(cv.h):
        for x in range(cv.w):
            dx, dy = x + 0.5 - 32, y + 0.5 - 34
            if dy < -4 and math.hypot(dx * 0.95, (dy + 4) * 1.25) <= 13:
                cv.set(x, y, (60, 200, 210))
    add_eyes(cv, 32, 32, 5, 1.6, (255, 255, 255))
    # 朝向指示：头顶的小三角（默认朝上）
    for i in range(4):
        for x in range(32 - i * 2, 32 + i * 2 + 1):
            cv.set(x, 8 + i, (255, 230, 120))
    return cv


def make_slime():
    cv = Canvas()
    draw_blob(cv, 32, 36, 14, (150, 235, 140), (40, 150, 90), wobble=0.12, seed=1.2)
    add_eyes(cv, 32, 34, 5, 1.8)
    return cv


def make_bat():
    cv = Canvas()
    draw_diamond(cv, 32, 34, 17, (205, 165, 245), (105, 55, 160))
    add_eyes(cv, 32, 32, 4, 1.5, (30, 20, 40))
    return cv


def make_brute():
    cv = Canvas()
    draw_round_rect(cv, 14, 14, 50, 52, 11, (245, 150, 130), (165, 55, 45))
    add_eyes(cv, 32, 30, 7, 2.2, (40, 20, 20))
    # 头顶两根角
    for i in range(8):
        cv.set(20 + i, 12 - i // 2, (120, 40, 35))
        cv.set(20 + i, 13 - i // 2, (120, 40, 35))
        cv.set(43 - i, 12 - i // 2, (120, 40, 35))
        cv.set(43 - i, 13 - i // 2, (120, 40, 35))
    return cv


def make_gem():
    cv = Canvas()
    draw_diamond(cv, 32, 32, 11, (140, 240, 255), (40, 150, 200))
    return cv


def make_projectile():
    cv = Canvas()
    # 外圈光晕
    for y in range(cv.h):
        for x in range(cv.w):
            d = math.hypot(x + 0.5 - 32, y + 0.5 - 32)
            if d <= 13:
                cv.set(x, y, (255, 245, 200), max(0, int(60 * (1 - d / 13))))
    draw_blob(cv, 32, 32, 6.5, (255, 255, 235), (255, 190, 90))
    return cv


def make_ground():
    """64x64 无缝平铺地面：深色底 + 1px 网格 + 少量噪点"""
    cv = Canvas()
    base = (26, 28, 38)
    line = (34, 37, 50)
    for y in range(cv.h):
        for x in range(cv.w):
            cv.set(x, y, base)
    for i in range(cv.w):
        cv.set(i, 0, line)
        cv.set(0, i, line)
    # 固定噪点（伪随机，保证可重复）
    n = 12345
    for _ in range(26):
        n = (n * 1103515245 + 12345) & 0x7FFFFFFF
        x = n % cv.w
        n = (n * 1103515245 + 12345) & 0x7FFFFFFF
        y = n % cv.h
        cv.set(x, y, (32, 35, 46))
    return cv


def make_shadow():
    cv = Canvas()
    for y in range(cv.h):
        for x in range(cv.w):
            d = math.hypot((x + 0.5 - 32) / 1.0, (y + 0.5 - 34) / 0.55)
            if d <= 15:
                cv.set(x, y, (0, 0, 0), int(90 * (1 - d / 15)))
    return cv


def main():
    arts = {
        "player": make_player(),
        "enemy_slime": make_slime(),
        "enemy_bat": make_bat(),
        "enemy_brute": make_brute(),
        "xp_gem": make_gem(),
        "projectile": make_projectile(),
        "ground": make_ground(),
        "shadow": make_shadow(),
    }
    for name, cv in arts.items():
        p = os.path.join(ART_DIR, name + ".png")
        cv.save(p)
        print("生成", os.path.relpath(p, os.path.join(os.path.dirname(__file__), "..")))


if __name__ == "__main__":
    main()
