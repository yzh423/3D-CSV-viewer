# Public Repository Release Plan

## Scope

Publish both tools from the original project: the native PySide6 TCP animation window and the offline browser trajectory viewer. Include only source, vendored runtime assets, synthetic demo data, tests, documentation, CI, and MIT licensing. Exclude all recorded factory CSV files.

## Verification

1. Run all repository tests with the synthetic fixtures.
2. Load `examples/demo_episode.csv` through the desktop parser and confirm both arms.
3. Inspect the staged file list and search for recording filenames or factory paths.
4. Commit the intentional public files and push the initial `main` branch.

## Apple Silicon macOS Extension

- Add a double-clickable `.command` launcher that prefers the repository virtual environment.
- Add PingFang SC as the preferred Matplotlib CJK font.
- Test Python 3.11 and 3.12 on the standard ARM64 `macos-latest` runner.
- Build and archive an unsigned ARM64 `.app` with PyInstaller and document Gatekeeper's first-open flow.
