# Configuration file for the Sphinx documentation builder.
# 
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# Author: terra_cai@realsil.com.cn

import re
import os
from pathlib import Path
from typing import List

# 初步获取需要排除的项
exclude_patterns = []
running_path = Path.cwd()
project_dir = running_path.parent
source_dir = project_dir.parent
for fpath in source_dir.iterdir():
    if fpath.name not in ["ameba", project_dir.name] and fpath.is_dir():
        exclude_patterns.append(fpath.name)


# 定义排除更多与toctree无关的rst的方法
def get_toctree_rst(root_rst: Path, toctree_rst_files: List) -> None:
    """
    get all used rst according to toctree
    Args:
        root_rst (Path): root rst to parser
        toctree_rst_files (List): list to store rst path

    Returns:
        None
    """
    root_rst = Path(root_rst).resolve()
    start_check = False
    if root_rst.exists():
        if root_rst not in toctree_rst_files:
            toctree_rst_files.append(root_rst)
        else:
            return  # 已经存在,则终止当前路径,防止陷入死循环
        if root_rst.stem not in ["index", "index_nda"]:
            return  # 只解析index,index_nda,提高效率
        for line in root_rst.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line.startswith(".. toctree::"):
                start_check = True
                continue
            if start_check and line and not line.startswith(":"):
                tag_mo = re.match(".+<(.+)>", line)
                if tag_mo:
                    sub_rst = tag_mo.group(1)
                    sub_rst = (root_rst.parent / sub_rst).resolve()
                else:
                    sub_rst = (root_rst.parent / line).resolve()
                sub_rst = sub_rst.with_suffix(".rst") if sub_rst.suffix == "" else sub_rst
                get_toctree_rst(sub_rst, toctree_rst_files)


def get_exclude_rst(root_rst: Path, repo_root: Path, exclude_patterns) -> List:
    """
    get exclude rst files
    Args:
        root_rst (Path): root rst path
        repo_root (Path): repo path
        exclude_patterns(List):

    Returns:
        List: list of exclude rst files
    """
    exclude_rst = []
    toctree_rst_files = []
    get_toctree_rst(root_rst, toctree_rst_files)
    for fpath in Path(repo_root).iterdir():
        if fpath.is_dir():
            if fpath.name in exclude_patterns:  # skip already in exclude dir
                continue
            for file in fpath.rglob("*.rst"):
                if file not in toctree_rst_files:
                    exclude_rst.append(os.path.relpath(file, repo_root).replace("\\", "/"))
        elif fpath.is_file() and fpath.suffix == ".rst":
            if fpath not in toctree_rst_files:
                exclude_rst.append(os.path.relpath(fpath, repo_root).replace("\\", "/"))

    return exclude_rst


def get_master_doc(config_file, repo_root):
    if os.environ.get("SET_NDA"):
        master_doc = os.path.relpath(f"{config_file.parent}/index_nda", repo_root).replace("\\", "/")
    else:
        master_doc = os.path.relpath(f"{config_file.parent}/index", repo_root).replace("\\", "/")
    return master_doc


# 公共设置
# 设置扩展
extensions = [
    "sphinx_rtd_theme",
    "sphinx_toggleprompt",
    "sphinx_tabs.tabs",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode"
]

toggleprompt_offset_right = 30  # 示例：设置提示符偏移量

source_suffix = {
    ".rst": "restructuredtext",
}

# 设置表格，图标标题格式
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Table %s',
    #    "section": "Section %s",
    #    "subsection": "Subsection %s",
    #    "subsubsection": "Subsubsection %s",
}

# 设置资源路径
templates_path = ["..\..\_templates"]
html_static_path = ["..\..\_static"]

# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_rtd_theme"
display_vcs_links = True

# Latex 相关的设置
latex_engine = 'xelatex'

inkscape_converter_bin = r'\\172.29.57.200\Dic\doc_tools\Inkscape\bin\inkscape.exe'
extensions.append("sphinxcontrib.inkscapeconverter")

latex_elements = {
    "papersize": "a4paper",
    'geometry': r' \usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}',
    'preamble': r'''
\usepackage{xeCJK}
'''
}
