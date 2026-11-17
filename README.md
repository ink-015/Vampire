# Vampire — 类吸血鬼幸存者小游戏

一个用来练手的作品集项目：跑位 + 自动攻击 + 刷怪 + 经验三选一，目标是一局 10 分钟、能完整玩完。
（玩法参考《吸血鬼幸存者》，代码与素材从头自己做，不使用任何原作资源。）

## 现在的状态

| 分支 | 状态 | 说明 |
|---|---|---|
| ① 素材 | 占位素材已完成，真素材待替换 | `tools/gen_art.py` 可一键重新生成 8 张 64×64 占位图；D10 换成统一风格素材 |
| ② 代码 | 地基片段已备好，玩法按天写 | `seed/Assets/Scripts/` 里是输入入口与素材取用两个基础类，其余每天手写 |
| ③ Git | 仓库已初始化 | 每天一个提交，D8 起打 tag，D14 推到 GitHub |

## 目录结构

```
Vampire/
├─ game/                  ← Unity 工程（用 Unity Hub 新建，不在本仓库里预置）
├─ seed/Assets/           ← 待灌入工程的脚本与占位素材
│   ├─ Scripts/Core/      ← InputReader（输入）、ArtLibrary（素材取用）
│   ├─ Editor/            ← 素材导入自动配置
│   └─ Resources/Art/     ← 8 张占位 PNG
├─ tools/
│   ├─ gen_art.py         ← 程序化占位素材生成器（纯 Python，无依赖）
│   └─ install_seed.sh    ← 把 seed/Assets 复制进 Unity 工程
└─ docs/
    └─ 01-每日作战计划.md  ← 14 天任务表 + git 学习曲线
```

## 怎么跑起来（第 1 天）

1. 装 Unity Hub → 装一个 **Unity 6 LTS** 或 **2022.3 LTS**（2D 用不到付费功能，个人版足够）。
2. Unity Hub → New project → 模板选 **2D (Built-in Render Pipeline)** → 位置 `D:\work\Vampire`，项目名 `game`。
3. 回到本目录执行：`bash tools/install_seed.sh`
4. 打开工程 → 任意空场景按 Play → Console 没有红字即通过。

> 为什么工程不直接放在仓库根目录：Unity Hub 不接受往非空文件夹里新建工程，`game/` 这一层是留给它自己生成的。

## 素材与版权

- 当前 8 张图由 `tools/gen_art.py` 程序化生成，**自己画的，无版权风险**，可直接公开。
- 替换真素材时遵守：CC0 可随意用；CC-BY 必须署名（写进 `CREDITS.md`）；标注「免费」≠ 可商用。
- 统一规格：**64×64 像素、透明背景、脚底对齐画面中心**，同名覆盖即可生效。

## 每日计划

见 [docs/01-每日作战计划.md](docs/01-每日作战计划.md)。
