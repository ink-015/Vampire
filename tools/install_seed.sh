#!/usr/bin/env bash
# 把 seed/Assets 里的脚本与占位素材灌进 Unity 工程。
# 前提：已经用 Unity Hub 在 D:\work\Vampire 下新建了名为 game 的 2D 工程。
# 用法： bash tools/install_seed.sh

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SEED="$ROOT/seed/Assets"
TARGET="$ROOT/game/Assets"

if [ ! -d "$TARGET" ]; then
  echo "× 没找到 $TARGET"
  echo "  请先在 Unity Hub 里新建 2D 工程：位置选 D:\\work\\Vampire，项目名填 game"
  exit 1
fi

echo "→ 从 $SEED 复制到 $TARGET"
mkdir -p "$TARGET/Scripts" "$TARGET/Editor" "$TARGET/Resources"
cp -r "$SEED/Scripts/." "$TARGET/Scripts/"
cp -r "$SEED/Editor/." "$TARGET/Editor/"
cp -r "$SEED/Resources/." "$TARGET/Resources/"
echo "✓ 完成。回到 Unity 里等它编译，Console 没有红色报错就算通过。"
