using UnityEngine;

namespace Vampire
{
    /// <summary>
    /// 输入的唯一入口。项目有可能用「旧输入系统」也可能用「新输入系统」，
    /// 这里用编译宏同时兼容两套，换引擎版本或模板都不会编译报错。
    /// 以后要加手柄、触屏摇杆，只改这一个文件。
    /// </summary>
    public static class InputReader
    {
        public static Vector2 Move
        {
            get
            {
                Vector2 v = Vector2.zero;

#if ENABLE_LEGACY_INPUT_MANAGER
                if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow)) v.x -= 1f;
                if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow)) v.x += 1f;
                if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow)) v.y -= 1f;
                if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow)) v.y += 1f;
#elif ENABLE_INPUT_SYSTEM
                var kb = UnityEngine.InputSystem.Keyboard.current;
                if (kb != null)
                {
                    if (kb.aKey.isPressed || kb.leftArrowKey.isPressed) v.x -= 1f;
                    if (kb.dKey.isPressed || kb.rightArrowKey.isPressed) v.x += 1f;
                    if (kb.sKey.isPressed || kb.downArrowKey.isPressed) v.y -= 1f;
                    if (kb.wKey.isPressed || kb.upArrowKey.isPressed) v.y += 1f;
                }
#endif
                return v.sqrMagnitude > 1f ? v.normalized : v;
            }
        }

        /// <summary>重开一局 / 跳过结算，随便按一下空格。</summary>
        public static bool RestartPressed
        {
            get
            {
#if ENABLE_LEGACY_INPUT_MANAGER
                return Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.R);
#elif ENABLE_INPUT_SYSTEM
                var kb = UnityEngine.InputSystem.Keyboard.current;
                return kb != null && (kb.spaceKey.wasPressedThisFrame || kb.rKey.wasPressedThisFrame);
#else
                return false;
#endif
            }
        }
    }
}
