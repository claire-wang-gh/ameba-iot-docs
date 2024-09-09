# Configuration file for the Sphinx documentation builder.
# 
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# Author: terra_cai@realsil.com.cn

import re
import os
import shutil
from pathlib import Path
from typing import List

# 初步获取需要排除的项
exclude_patterns = []
running_path = Path.cwd()
project_dir = running_path.parent
repo_root = project_dir.parent

common_dirs_files = ["_static", "_templates", "ameba"]


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


def get_exclude_rst(root_rst: Path, src_root: Path, exclude_patterns) -> List:
    """
    get exclude rst files
    Args:
        root_rst (Path): root rst path
        src_root (Path): source path
        exclude_patterns(List):

    Returns:
        List: list of exclude rst files
    """
    exclude_rst = []
    toctree_rst_files = []
    get_toctree_rst(root_rst, toctree_rst_files)
    for fpath in Path(src_root).iterdir():
        if fpath.is_dir():
            if fpath.name in exclude_patterns:  # skip already in exclude dir
                continue
            for file in fpath.rglob("*.rst"):
                if file not in toctree_rst_files:
                    exclude_rst.append(os.path.relpath(file, src_root).replace("\\", "/"))
        elif fpath.is_file() and fpath.suffix == ".rst":
            if fpath not in toctree_rst_files:
                exclude_rst.append(os.path.relpath(fpath, src_root).replace("\\", "/"))

    return exclude_rst


def get_master_doc():
    if os.environ.get("SET_NDA"):
        master_doc = "index_nda"
    else:
        master_doc = "index"
    return master_doc


# -- 清理公共文件 -------------------------------------------------
def clean_common_files(source_dir):
    print("Clean common files...")
    for common_dirs_file in common_dirs_files:
        tgt_ = source_dir / common_dirs_file
        if tgt_.exists():
            try:
                if tgt_.is_file():
                    os.remove(tgt_)
                elif tgt_.is_dir():
                    shutil.rmtree(tgt_)
            except:
                print(f"[Warning]Fail to clean {tgt_}!")


# -- 复制公共文件 -------------------------------------------------
def copy_common_files(source_dir):
    for common_dirs_file in common_dirs_files:
        src_ = repo_root / common_dirs_file
        tgt_ = source_dir / common_dirs_file

        if src_.exists():
            try:
                if src_.is_file():
                    shutil.copy(src_, tgt_)
                elif src_.is_dir():
                    shutil.copytree(src_, tgt_)
                else:
                    pass
                print(f"Copy {src_}!")
            except:
                print(f"[Failed]Copy {src_}!")
        else:
            print(f"[Warning]Not exists {src_}!")


# -- 注册事件，用于清理公共文件 -------------------------------------------------
def run_after_build(app, exception):
    if exception is None:
        clean_common_files(app.srcdir)


def setup(app):
    app.connect('build-finished', run_after_build)


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
