from pathlib import Path


VIEWER = Path(__file__).parents[1] / "tools" / "episode-3d-viewer" / "index.html"
ROOT = Path(__file__).parents[1]


def viewer_source() -> str:
    return VIEWER.read_text(encoding="utf-8")


def test_viewer_has_accessible_local_file_controls():
    source = viewer_source()
    assert '<link rel="icon" href="data:,">' in source
    assert '<script src="vendor/papaparse.min.js"></script>' in source
    assert '<script src="vendor/plotly.min.js"></script>' in source
    assert "cdn.jsdelivr.net" not in source
    assert 'type="file"' in source
    assert 'accept=".csv,text/csv"' in source
    assert 'multiple' in source
    assert 'id="drop-zone"' in source
    assert 'role="status"' in source
    assert 'role="alert"' in source


def test_offline_plotly_runtime_is_current_enough_for_stable_gl3d_camera_updates():
    plotly = (VIEWER.parent / "vendor" / "plotly.min.js").read_text(encoding="utf-8")
    assert "plotly.js v3.7.0" in plotly[:200]


def test_viewer_supports_expected_trajectory_groups():
    source = viewer_source()
    for prefix in ("right_controller", "right_tcp", "left_controller", "left_tcp"):
        assert prefix in source
        assert f"{prefix}_pos_x" in source


def test_viewer_uses_local_csv_parsing_and_interactive_3d():
    source = viewer_source()
    assert "Papa.parse" in source
    assert "Plotly.react" in source
    assert 'type: "scatter3d"' in source
    assert 'aspectmode: "data"' in source
    assert "plotly_click" in source
    assert "MAX_RENDER_POINTS" in source


def test_viewer_includes_camera_reset_and_empty_error_states():
    source = viewer_source()
    assert 'id="reset-camera"' in source
    assert 'id="empty-state"' in source
    assert 'id="error-list"' in source
    assert "No usable XYZ trajectories" in source


def test_viewer_has_desktop_equivalent_animation_controls():
    source = viewer_source()
    for control_id in (
        "episode-select", "play-button", "time-slider", "time-label",
        "speed-select", "loop-toggle", "right-toggle", "left-toggle",
    ):
        assert f'id="{control_id}"' in source
    for behavior in (
        "quaternionToMatrix", "nearestIndex", "requestAnimationFrame",
        "renderAnimationFrame", "AXIS_COLORS",
    ):
        assert behavior in source
    assert "_tcp_quat_w" in source


def test_public_repository_excludes_internal_docs_and_deploys_pages():
    docs = ROOT / "docs"
    assert not docs.exists() or not any(path.is_file() for path in docs.rglob("*"))
    workflow = ROOT / ".github" / "workflows" / "pages.yml"
    source = workflow.read_text(encoding="utf-8")
    assert "actions/deploy-pages" in source
    assert "tools/episode-3d-viewer" in source


def test_plot_is_initialized_before_plotly_event_binding():
    source = viewer_source()
    assert source.index("Plotly.newPlot") < source.index('plot.on("plotly_click"')


def test_repository_has_apple_silicon_launcher_and_build_workflow():
    launcher = ROOT / "tools" / "episode-3d-desktop" / "run_viewer.command"
    workflow = ROOT / ".github" / "workflows" / "build-macos-arm64.yml"
    assert launcher.is_file()
    assert "scripts/episode_3d_desktop.py" in launcher.read_text(encoding="utf-8")
    source = workflow.read_text(encoding="utf-8")
    assert "macos-latest" in source
    assert "--target-arch arm64" in source
    assert "3D-CSV-viewer.app" in source


def test_windows_launcher_bootstraps_an_isolated_environment():
    launcher = (ROOT / "tools" / "episode-3d-desktop" / "run_viewer.bat").read_text(encoding="utf-8")
    assert ".venv\\Scripts\\python.exe" in launcher
    assert "-m venv .venv" in launcher
    assert "-m pip install -r requirements.txt" in launcher


def test_animation_locks_ranges_and_yields_to_camera_interaction():
    source = viewer_source()
    assert "computeSceneRanges" in source
    assert "autorange: false" in source
    assert "userInteracting" in source
    assert 'plot.addEventListener("mousedown"' in source
    assert 'document.addEventListener("mouseup"' in source
    assert "if (userInteracting || now < cameraSettlingUntil)" in source


def test_tcp_tool_axes_have_shared_xyz_legend_entries():
    source = viewer_source()
    for axis in ("X", "Y", "Z"):
        assert f'工具轴 {axis}' in source
    assert 'legendgroup: `tool-axis-${axis}`' in source
    assert 'showlegend: !axisLegendAdded' in source
    assert 'groupclick: "togglegroup"' in source


def test_viewer_accepts_individual_files_and_folders():
    source = viewer_source()
    assert 'id="folder-input"' in source
    assert 'webkitdirectory' in source
    assert 'for="folder-input"' in source
    assert "file.webkitRelativePath" in source
    assert 'localeCompare' in source
    assert 'numeric: true' in source


def test_single_arm_episodes_do_not_report_the_absent_arm_as_invalid():
    source = viewer_source()
    assert "hasTcpPositionColumns" in source
    assert "tcpPositionSides" in source
    assert "result.tcpPositionSides.includes(side)" in source
    assert "toggle.disabled = !available" in source


def test_loaded_file_list_scrolls_without_horizontal_overflow():
    source = viewer_source()
    assert "#file-list" in source
    assert "max-height: clamp(" in source
    assert "overflow-y: auto" in source
    assert "overflow-x: hidden" in source
    assert "scrollbar-gutter: stable" in source
    assert "box-sizing: border-box" in source
    assert ".file-card { min-width: 0; width: 100%; box-sizing: border-box;" in source


def test_loaded_file_cards_select_and_highlight_the_active_episode():
    source = viewer_source()
    assert 'class="file-card"' in source
    assert 'data-episode-index="${index}"' in source
    assert 'aria-current="${activeEpisodeIndex === index}"' in source
    assert 'fileList.addEventListener("click"' in source
    assert "episodeSelect.value = String(index)" in source
    assert 'scrollIntoView({ block: "nearest", inline: "nearest" })' in source
    assert '.file-card[aria-current="true"]' in source


def test_camera_persists_until_the_explicit_reset_button_is_used():
    source = viewer_source()
    assert "let savedCamera = null" in source
    assert "rememberCurrentCamera" in source
    assert 'plot.on("plotly_relayout"' in source
    assert 'uirevision: "persistent-camera"' in source
    assert "sceneWithSavedCamera" in source
    assert "resetCameraView" in source
    assert "savedCamera = null" in source
    assert "`episode-${index}`" not in source


def test_camera_relayout_is_saved_synchronously_without_mouseup_redraw_race():
    source = viewer_source()
    assert "saveCameraFromRelayout" in source
    assert 'event["scene.camera"]' in source
    assert 'savedCamera = copyCamera(event["scene.camera"])' in source
    assert "requestAnimationFrame(rememberCurrentCamera)" not in source
    finish = source[source.index("function finishCameraInteraction"):source.index('document.addEventListener("mouseup"')]
    assert "renderAnimationFrame" not in finish


def test_new_file_batches_append_and_keep_every_loaded_episode():
    source = viewer_source()
    assert "episodeIdentity" in source
    assert "const previousEpisodes = loadedEpisodes" in source
    assert "loadedEpisodes = [...previousEpisodes" in source
    load = source[source.index("async function enhancedLoadFiles"):source.index("parseFile = enhancedParseFile")]
    assert "loadedEpisodes = []" not in load


def test_animation_waits_for_camera_to_settle_after_dragging():
    source = viewer_source()
    assert "cameraSettlingUntil" in source
    assert "CAMERA_SETTLE_MS" in source
    assert "extendCameraSettleWindow" in source
    assert "now < cameraSettlingUntil" in source
    assert "performance.now() + CAMERA_SETTLE_MS" in source


def test_animation_updates_never_write_an_old_camera_back_to_the_scene():
    source = viewer_source()
    assert 'uirevision: "persistent-camera"' in source
    assert "scheduleAnimationRestyle" in source
    assert "ANIMATION_FRAME_INTERVAL_MS" in source
    assert "animationRestylePending" in source
    assert 'Plotly.relayout(plot, { "scene.camera": camera })' not in source
    animation = source[source.index("function renderAnimationFrame"):source.index("function animationLoop")]
    assert "scheduleAnimationRestyle" in animation


def test_mouse_release_waits_for_plotlys_final_camera_event_before_resuming():
    source = viewer_source()
    assert "cameraReleaseTimer" in source
    assert "scheduleCameraInteractionFinish" in source
    assert "clearTimeout(cameraReleaseTimer)" in source
    assert "CAMERA_RELEASE_QUIET_MS" in source
    finish = source[source.index("function finishCameraInteraction"):source.index('document.addEventListener("mouseup"')]
    assert "userInteracting = false" not in finish
    relayout = source[source.index('plot.on("plotly_relayout"'):source.index('plot.on("plotly_click"')]
    assert "scheduleCameraInteractionFinish" in relayout
