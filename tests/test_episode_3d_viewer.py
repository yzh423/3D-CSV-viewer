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
    assert not (ROOT / "docs").exists()
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
