# TCP 工具坐标系动画查看器

这是原生 PySide6 桌面窗口，不使用浏览器，也不需要网络。

## 启动

Windows 双击 `run_viewer.bat`；首次运行会自动创建 `.venv` 并安装所需依赖，不要求系统 Python 预装 PySide6。Apple Silicon Mac 双击 `run_viewer.command`。然后点击“打开 CSV”。也可以在项目根目录直接加载指定 episode：

```powershell
python scripts/episode_3d_desktop.py examples/demo_episode.csv
```

macOS 首次运行未公证的 `.app` 时，请按住 Control 点击应用，选择“打开”，再确认“打开”。

## 操作

- “播放/暂停”：按 CSV 的 `t` 时间推进左右 TCP。
- 时间滑块：拖动到任意时刻。
- 速度：选择 `0.25×` 至 `4×`。
- “循环”：到结尾后自动从头播放。
- “右 TCP/左 TCP”：分别隐藏或显示对应轨迹与工具轴。
- 图形工具栏：旋转、平移、缩放和保存当前画面。

橙色轨迹表示右 TCP，蓝色轨迹表示左 TCP。每个 TCP 原点处的红、绿、蓝短轴分别表示工具坐标系的 X、Y、Z 方向。工具轴由 CSV 中的 `*_tcp_quat_w/x/y/z` 四元数计算。

若某侧缺少完整 TCP 位置或四元数字段，该侧会被跳过；两侧都不可用时窗口会显示错误。
