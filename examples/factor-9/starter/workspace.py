"""
Factor 9：Workspace & Artifacts Management（骨架代码）

目标：每个任务在隔离工作区中运行，产物（artifacts）作为运行的持久产出契约。
参考：nano-symphony 的 workspace 与统一 artifacts 管理
"""

# TODO 1: 实现 Workspace：
# - 每个任务创建独立目录（提示：tempfile.mkdtemp）
# - 初始化 git baseline（git init + 首次 commit），便于 diff 与回滚
# - 支持生命周期 hook：on_create / on_cleanup
# - 支持清理策略：keep / on_success / always
# TODO 2: 实现 ArtifactManager：
# - collect：按 glob 模式从工作区收集 artifacts，复制到 artifacts 目录
# - 写 manifest.json（名称、大小、相对路径、收集时间）作为产出契约
# - download：把 artifacts 拷贝到调用方指定目录
# - list：供 UI 呈现的结构化列表
# TODO 3: 演示：模拟一个任务在工作区里写文件，结束后收集 artifacts 并按策略清理


class Workspace:
    def __init__(self, task_id: str, cleanup_policy: str = "on_success"):
        raise NotImplementedError("TODO")


class ArtifactManager:
    def __init__(self, workspace, artifacts_dir: str):
        raise NotImplementedError("TODO")

    def collect(self, patterns: list) -> list:
        raise NotImplementedError("TODO")
