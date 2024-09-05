#!/rtkoss/python/3.6.7/rhel7/x86_64/bin/python3
# coding=utf-8
"""
@Project : Python
@File    : trans_visio_files.py
@Time    : 2024/7/9 16:33
@Author  : terra_cai
@Email   : terra_cai@realsil.com.cn
@Software: PyCharm
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

my_real_path = Path(__file__).resolve()
libs = [
    str((my_real_path / '../../../../venv/Lib/site-packages').resolve())
]
for lib in libs:
    if lib not in sys.path:
        sys.path.insert(0, lib)

import re

import os
import win32com.client as win32


def clean_tmp():
    print("Clean temp...")
    tmp_dir = (Path(os.path.expanduser("~")) / "AppData\Local\Temp\gen_py").resolve()
    try:
        shutil.rmtree(tmp_dir)
        print(tmp_dir)
    except:
        pass


def visio_to_img(visio_file, img_path, retry=True):
    try:
        visio = win32.gencache.EnsureDispatch('Visio.Application')
        visio.Visible = True
        visio_file = str(Path(visio_file).resolve())
        print(f"Open {visio_file}")
        doc = visio.Documents.Open(visio_file)

        for page in doc.Pages:
            img_path = Path(img_path).resolve()
            img_path.parent.mkdir(parents=True, exist_ok=True)
            visio.ActiveWindow.Page = page
            visio.ActiveWindow.SelectAll()
            visio.ActiveWindow.Selection.Export(img_path)
            print(f"Exported {page.Name} to {img_path}")
            break
        doc.Close()
    except:
        if retry:
            clean_tmp()
            visio_to_img(visio_file, img_path, retry=False)
        else:
            import traceback
            traceback.print_exc()

    # 可选：退出Visio应用程序
    # visio.Quit()


def trans_visio_to_img(visio_dir, output_dir):
    visio_dir = Path(visio_dir).resolve()
    for visio in visio_dir.rglob("*.vs*"):
        rel_path = os.path.relpath(visio, visio_dir)
        img_path = (Path(output_dir) / rel_path).with_suffix(".svg")
        visio_to_img(visio, img_path)


def trans_all_visios_for_online_documents(root):
    has_visio = False
    for file in Path(root).rglob("*.vs*"):
        if file.parent.name == "vsd":
            img_path = file.parent.parent / "figures" / file.with_suffix(".svg").name
            if img_path.exists():
                if file.stat().st_mtime > img_path.stat().st_mtime:
                    visio_to_img(file, img_path)
                    has_visio = True
            else:
                has_visio = True
                visio_to_img(file, img_path)
    if has_visio:
        print("Trans over, you can close visio window.")
    else:
        print("No visio files need to trans.")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', help="Set visio dir.")
    arg_parser.add_argument('-o', help="Set output dir.")
    arg_parser.add_argument('-r', help="Set online document root dir.")
    args = arg_parser.parse_args()

    if sys.gettrace():
        args.v = r"."
        args.o = r"."
        # args.r = r"C:\Users\terra_cai\Desktop\hspec\rst"
    if args.v and args.o:
        trans_visio_to_img(args.v, args.o)
    if args.r:
        trans_all_visios_for_online_documents(args.r)
