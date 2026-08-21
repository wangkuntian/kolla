import os
import subprocess


def test_copy_cacerts_accepts_openeuler_release(tmp_path):
    etc_dir = tmp_path / "etc"
    etc_dir.mkdir()
    (etc_dir / "openEuler-release").write_text(
        "openEuler release 24.03 (LTS-SP4)\n")

    env = os.environ.copy()
    env["KOLLA_OS_RELEASE_DIR"] = str(etc_dir)

    result = subprocess.run(
        ["bash", "docker/base/copy_cacerts.sh"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
