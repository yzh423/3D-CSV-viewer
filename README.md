# 3D CSV Viewer

Open-source tools for inspecting robot TCP and controller trajectories stored in CSV episode files. The repository includes both a native animated desktop application and a fully offline browser viewer.

用于检查机器人 CSV episode 中 TCP 与手柄三维轨迹的开源工具。仓库同时提供原生桌面动画窗口和完全离线的浏览器查看器。

## Tools / 工具

### Native desktop animation / 原生桌面动画

- Animates left and right TCPs together using the recorded `t` timeline.
- Draws the moving TCP tool frame from `*_tcp_quat_w/x/y/z`: X red, Y green, Z blue.
- Includes play/pause, timeline scrubbing, `0.25×–4×` speed, looping, per-arm visibility, 3D rotation, pan, and zoom.

Windows users can double-click [`tools/episode-3d-desktop/run_viewer.bat`](tools/episode-3d-desktop/run_viewer.bat). Apple Silicon Mac users can double-click [`tools/episode-3d-desktop/run_viewer.command`](tools/episode-3d-desktop/run_viewer.command) after installing the dependencies below. Cross-platform launch:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/episode_3d_desktop.py examples/demo_episode.csv
```

### Apple Silicon macOS application

The release workflow builds a native ARM64 `3D-CSV-viewer.app` for M1, M2, M3, M4, and later Apple Silicon Macs. Download `3D-CSV-viewer-macOS-arm64.zip` from the latest release or the **Build macOS ARM64 app** workflow artifact.

The app is not notarized with an Apple Developer certificate. On first launch, extract the ZIP, Control-click `3D-CSV-viewer.app`, choose **Open**, then confirm **Open**. macOS remembers the approval for later launches.

### Offline browser viewer / 离线浏览器查看器

Open [`tools/episode-3d-viewer/index.html`](tools/episode-3d-viewer/index.html) directly. Drop one or more CSV files into the page to inspect left/right TCP and controller trajectories. Plotly and the CSV parser are vendored locally; no network or upload is used.

直接打开 `tools/episode-3d-viewer/index.html`，拖入一个或多个 CSV。所有解析均在本机完成，数据不会上传。

## Supported CSV schema / CSV 字段

The timeline column is `t`. The viewer detects any complete group below:

```text
right_tcp_pos_x/y/z          right_tcp_quat_w/x/y/z
left_tcp_pos_x/y/z           left_tcp_quat_w/x/y/z
right_controller_pos_x/y/z
left_controller_pos_x/y/z
```

`coordinate_frame` is optional. The desktop animation requires at least one complete TCP position and quaternion group. Quaternion order is `w,x,y,z`.

## Demo data / 示例数据

[`examples/demo_episode.csv`](examples/demo_episode.csv) is synthetic and contains no recorded user or factory data.

## Development

```bash
pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the tests on Windows, Ubuntu, and Apple Silicon macOS. Build workflows produce downloadable Windows x64 and macOS ARM64 PyInstaller application artifacts.

## Privacy

Both tools process CSV files locally. This repository contains no original factory recordings.

## License

[MIT](LICENSE)
