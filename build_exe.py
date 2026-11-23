# -*- coding: utf-8 -*-
"""Ddingdong.pyw -> dist/Ddingdong.exe (단일 파일) 빌드 스크립트.

사용:  py build_exe.py        (또는 build_exe.bat 더블클릭)
필요:  pip install pyinstaller   (빌드하는 PC에만 필요, 배포받는 PC는 불필요)
"""
import base64
import os
import subprocess
import sys
from importlib.machinery import SourceFileLoader

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Ddingdong.pyw")
NAME = "Ddingdong"


def main():
    # 내장 base64 아이콘 → exe 아이콘용 .ico 파일
    mod = SourceFileLoader("app_src", SRC).load_module()
    build_dir = os.path.join(HERE, "build")
    os.makedirs(build_dir, exist_ok=True)
    ico = os.path.join(build_dir, NAME + ".ico")
    with open(ico, "wb") as f:
        f.write(base64.b64decode(mod.ICON_ICO_B64))

    # exe 파일 속성(자세히 탭)에 들어갈 버전 정보 — APP_VERSION 하나만 고치면 된다
    ver = mod.APP_VERSION
    appname = getattr(mod, "APP_NAME_KO", mod.APP_NAME)    # 빌드 PC의 언어 설정과 무관하게 고정
    nums = ([int(x) for x in ver.split(".")] + [0, 0, 0, 0])[:4]
    tup = ", ".join(str(n) for n in nums)
    vfile = os.path.join(build_dir, "version_info.txt")
    with open(vfile, "w", encoding="utf-8") as f:
        f.write(f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers=({tup}), prodvers=({tup}), mask=0x3f, flags=0x0,
                    OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('041204b0', [
      StringStruct('FileDescription', '{appname}'),
      StringStruct('FileVersion', '{ver}'),
      StringStruct('InternalName', '{NAME}'),
      StringStruct('OriginalFilename', '{NAME}.exe'),
      StringStruct('ProductName', '{appname}'),
      StringStruct('ProductVersion', '{ver}')])]),
    VarFileInfo([VarStruct('Translation', [1042, 1200])])
  ])
""")

    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
           "--onefile", "--noconsole",
           "--name", NAME, "--icon", ico, "--version-file", vfile,
           "--distpath", os.path.join(HERE, "dist"),
           "--workpath", build_dir, "--specpath", build_dir,
           SRC]
    print(" ".join(cmd))
    rc = subprocess.call(cmd, cwd=HERE)
    if rc == 0:
        import hashlib
        out = os.path.join(HERE, "dist", NAME + ".exe")
        with open(out, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        print("\n완료: %s  (v%s)\nSHA-256: %s" % (out, ver, sha))
        print("GitHub Release(태그 v%s)에 %s.exe 를 올리면 자동 업데이트가 이를 내려받습니다." % (ver, NAME))
    else:
        print("\n빌드 실패 (pyinstaller 설치 여부: py -m pip install pyinstaller)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
