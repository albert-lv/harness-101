"""
Factor 9：Workspace & Artifacts Management（参考实现）

每任务隔离工作区（git baseline、生命周期 hook、清理策略）+
artifacts 作为运行的持久产出契约（收集、manifest、下载、UI 列表）。
参考：nano-symphony 的 workspace 与统一 artifacts 管理
"""
import fnmatch
import json
import os
import shutil
import subprocess
import tempfile
import time


class Workspace:
    """每个任务一个独立目录，带 git baseline 与生命周期 hook。"""

    def __init__(self, task_id: str, cleanup_policy: str = "on_success",
                 on_create=None, on_cleanup=None):
        assert cleanup_policy in {"keep", "on_success", "always"}
        self.task_id = task_id
        self.cleanup_policy = cleanup_policy
        self.on_create = on_create or (lambda ws: None)
        self.on_cleanup = on_cleanup or (lambda ws: None)
        self.path = tempfile.mkdtemp(prefix=f"ws-{task_id}-")
        self._git_baseline()
        self.on_create(self)

    def _git_baseline(self):
        """git init + 空 baseline commit，之后所有改动可 diff / 回滚。"""
        def git(*args):
            subprocess.run(["git", *args], cwd=self.path, check=True,
                           capture_output=True, text=True)
        git("init", "-q")
        # 内联身份配置，避免依赖全局 git config
        git("-c", "user.name=harness", "-c", "user.email=harness@localhost",
            "commit", "-q", "--allow-empty", "-m", f"baseline: {self.task_id}")

    def diff_since_baseline(self) -> str:
        result = subprocess.run(["git", "status", "--short"], cwd=self.path,
                                capture_output=True, text=True)
        return result.stdout.strip()

    def cleanup(self, success: bool):
        self.on_cleanup(self)
        should_delete = (self.cleanup_policy == "always"
                         or (self.cleanup_policy == "on_success" and success))
        if should_delete:
            shutil.rmtree(self.path, ignore_errors=True)
            print(f"[workspace] 已清理 {self.path}")
        else:
            print(f"[workspace] 保留 {self.path}")


class ArtifactManager:
    """artifacts = 运行的持久产出契约：收集、manifest、下载、UI 列表。"""

    def __init__(self, workspace: Workspace, artifacts_dir: str):
        self.workspace = workspace
        self.artifacts_dir = artifacts_dir
        os.makedirs(artifacts_dir, exist_ok=True)

    def collect(self, patterns: list) -> list:
        collected = []
        for root, _, files in os.walk(self.workspace.path):
            for name in files:
                rel = os.path.relpath(os.path.join(root, name), self.workspace.path)
                if ".git" in rel.split(os.sep):
                    continue
                if any(fnmatch.fnmatch(rel, p) for p in patterns):
                    dst = os.path.join(self.artifacts_dir, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(os.path.join(root, name), dst)
                    collected.append({
                        "name": rel,
                        "size": os.path.getsize(dst),
                        "collected_at": time.time(),
                    })
        manifest_path = os.path.join(self.artifacts_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({"task_id": self.workspace.task_id, "artifacts": collected},
                      f, ensure_ascii=False, indent=2)
        return collected

    def list(self) -> list:
        """供 UI 呈现的结构化列表。"""
        with open(os.path.join(self.artifacts_dir, "manifest.json"), encoding="utf-8") as f:
            return json.load(f)["artifacts"]

    def download(self, dest_dir: str):
        """把 artifacts 整体拷贝给调用方（模拟下载）。"""
        shutil.copytree(self.artifacts_dir, dest_dir, dirs_exist_ok=True)


def simulate_task(ws: Workspace):
    with open(os.path.join(ws.path, "report.md"), "w", encoding="utf-8") as f:
        f.write("# 任务报告\n")
    with open(os.path.join(ws.path, "run.log"), "w", encoding="utf-8") as f:
        f.write("step1 ok\nstep2 ok\n")


if __name__ == "__main__":
    ws = Workspace("demo-1", cleanup_policy="on_success",
                   on_create=lambda w: print(f"[hook] on_create: {w.path}"))
    simulate_task(ws)
    print("[workspace] baseline 后的改动:\n" + ws.diff_since_baseline())
    artifacts = ArtifactManager(ws, os.path.join(tempfile.gettempdir(), "demo-artifacts"))
    artifacts.collect(["*.md", "*.log"])
    print("[artifacts] UI 列表:", json.dumps(artifacts.list(), ensure_ascii=False))
    ws.cleanup(success=True)
