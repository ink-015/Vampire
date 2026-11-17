# Git 与 GitHub 速查卡（这个项目专用的版本）

只写这个项目会用到的东西，不写完整 Git 手册。遇到表里没有的问题，先 `git status` 把原文读一遍再搜。

## 1. 一次性配置（新机器才需要）

```bash
git config --global user.name  "ink-015"
git config --global user.email "你的GitHub邮箱"
git config --global init.defaultBranch main
```

为什么必须配：每个提交都会记下「谁、什么时候」。邮箱要和 GitHub 账号对得上，提交才会挂到你头像下面。本项目已配好 `ink-015 / ink-015@users.noreply.github.com`，**如果你想用真实邮箱，在第一次推送前告诉我，我统一改一次**（未推送的提交改作者很干净，推送后再改就要重写历史）。

## 2. 第一次推送

```bash
cd D:/work/Vampire
git push -u origin main
```

- `-u` 的意思是「记住这个对应关系」，以后直接 `git push` 就行。
- 第一次会要求认证：正常弹 Windows 的 Git Credential Manager 窗口，选 **Sign in with your browser** → 浏览器里点授权即可，之后不再问。
- 如果弹的是命令行要密码：**GitHub 早就不接受账号密码了**，要填 Personal Access Token（GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens，权限勾 `Contents: Read and write`，有效期给 90 天）。Token 只显示一次，复制后当密码粘进去。

## 3. 每天的三板斧

```bash
git status                 # 我改了什么
git add -A                 # 全部加入本次提交
git commit -m "feat: 敌人追踪玩家"
git push                   # 推到 GitHub（有网就推，没网第二天一起推）
```

想只提交某几个文件：`git add Assets/Scripts/Enemy.cs`，别用 `-A`。

## 4. 提交信息怎么写

格式：`类型: 做了什么`。一句话说清结果，不写「修改了一些东西」。

| 类型 | 什么时候用 | 例子 |
|---|---|---|
| `feat` | 新功能 | `feat: 自动索敌与投射物` |
| `fix` | 修 bug | `fix: 升级面板不响应点击` |
| `perf` | 性能优化 | `perf: 子弹改用对象池` |
| `art` | 只动素材 | `art: 替换为统一风格素材` |
| `audio` | 只动声音 | `audio: 补充基础音效` |
| `docs` | 只动文档 | `docs: README 与演示视频` |
| `chore` | 杂活 | `chore: 升级到 Unity 6 LTS` |

## 5. 改坏了怎么救（按严重程度选）

| 情况 | 命令 | 结果 |
|---|---|---|
| 改坏了某个文件，还没提交 | `git restore Assets/Scripts/Enemy.cs` | 退回上次提交的版本，改动**丢失** |
| 改坏了，但想留着看看 | `git stash` / `git stash pop` | 收进抽屉，随时取回 |
| 已经提交但还没推送，想撤掉这次提交 | `git reset --soft HEAD~1` | 提交没了，改动还在工作区 |
| 已经推送上去了，想撤销 | `git revert <commit>` | 生成一个「反向提交」，历史保留，最安全 |
| 彻底搞乱了 | `git reflog` | 列出你每一步操作，找回任意一个旧状态 |

## 6. 常见报错对照

| 报错关键字 | 真实原因 | 处置 |
|---|---|---|
| `failed to push some refs` / `rejected` | 远端有你本地没有的提交（比如在网页上改过 README） | `git pull --rebase` 后再 `git push` |
| `Support for password authentication was removed` | 拿账号密码当密码了 | 改用 Token 或 Git Credential Manager |
| `src refspec main does not match any` | 本地分支不叫 main | `git branch -M main` |
| `CONNECT tunnel failed` / `502` | 网络或代理拦了 github.com | 换网络、关代理，或配 `git config --global http.proxy` |
| `file is 105 MB; exceeds GitHub's file size limit` | 提交了大文件（视频、素材包） | 从提交里移除 + 写进 `.gitignore` |
| `fatal: not a git repository` | 不在仓库目录里 | `cd D:/work/Vampire` |

## 7. 分支什么时候用

第一版（D1–D4）**直接在 main 上提交就行**，一天一次，简单可靠。

从 D5 开始练分支，只在两种时候用：

```bash
git switch -c feature/pool     # 开一条平行存档去试对象池
# 做完了、跑通了：
git switch main
git merge feature/pool
git branch -d feature/pool     # 删掉用完的分支
```

判断标准：**"这个改动如果做失败了，我要不要能一键回到现在？"** 要，就开分支；不要，就在 main 上直接做。

## 8. 这个项目必须遵守的两条

1. **`game/Library/` 绝对不能进仓库**。它有几个 G，每次打开工程都会重生成。`.gitignore` 已经写好，别用 `git add -f` 强行加。
2. **素材来源要留痕**。用了别人的 CC-BY 素材，必须在 `CREDITS.md` 写清作者与链接，否则将来公开仓库会有版权纠纷。
