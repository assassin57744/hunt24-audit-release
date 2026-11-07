"""pytest 公共配置：把项目根目录 (hunt24-audit/) 加入 sys.path，
使 tests/ 下的测试可以直接 import config / modules / utils。"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
