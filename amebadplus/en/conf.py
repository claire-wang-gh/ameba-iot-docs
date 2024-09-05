# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from pathlib import Path

# 导入公共配置
current_config_path = Path(__file__).resolve()
en_or_cn = current_config_path.parent.stem
repo_root = current_config_path.parent.parent.parent
sys.path.insert(0, str(repo_root))
from common_conf import *

# 项目设置
language = "en" if en_or_cn == "en" else "cn"
project = "ameba_docs"
copyright = "2024, Realsil"
author = "Realsil"

# 宏替换
CHIP_NAME = 'AmebaDPlus'
VERSION = '1.0.0'

rst_prolog = """
.. |CHIP_NAME| replace:: {0}
.. |VERSION| replace:: {1}
""".format(CHIP_NAME, VERSION)

# 确定NDA或非NDA入口
master_doc = get_master_doc(current_config_path, repo_root)
print(f"MASTER_DOC: {master_doc}")

# 更新需要排除的目录
if en_or_cn == "en":
    exclude_patterns.append("**/cn")
else:
    exclude_patterns.append("**/en")

exclude_rst = get_exclude_rst(repo_root / f"{master_doc}.rst", repo_root, exclude_patterns)
exclude_patterns.extend(exclude_rst)
print("Exclude:\n=============================================================")
for ign in exclude_patterns:
    print(ign)
