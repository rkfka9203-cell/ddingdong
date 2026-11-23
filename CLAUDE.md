# CLAUDE.md — 띵동 리마인더 (Ddingdong)

VS Code의 Claude Code가 이 프로젝트를 이어서 작업할 때 참고하는 지침입니다.

## 프로젝트 개요
- `Ddingdong.pyw` 단일 파일(약 2,800줄) tkinter 데스크톱 앱. 블로그·GitHub로 공개 배포하며 파일 하나로 배포하므로 **단일 파일 구조와 표준 라이브러리 전용**을 유지할 것.
- 대상 환경: Windows 10/11, Python 3.8+. Windows API는 `ctypes`로 호출하며 `IS_WIN` 체크 후 실패 시 조용히 넘어가는 패턴을 따른다.
- 구조·데이터 스키마·알려진 개선점은 `README.md` 참고.

## 작업 규칙
- 56–970줄의 base64 아이콘 문자열은 읽거나 수정하지 말 것(토큰 낭비). 아이콘 교체 요청 시에만 다룬다.
- UI 텍스트·주석은 한국어. 기존 색상 상수(`TEXT`, `BLUE` 등)와 `F(size, bold)` 폰트 헬퍼만 사용한다. Windows 기본 위젯(Spinbox, OptionMenu, Checkbutton) 대신 기존 커스텀 위젯을 쓴다.
- 새 위젯을 목록에 추가했다면 `ScrollArea.sync_wheel()`이 호출되는지 확인한다.
- `GROUPS` 순서와 `REPEAT_VALUES` 순서는 반드시 일치시켜야 한다(`_begin_edit`가 인덱스로 매핑).
- `reminder_data.json` 스키마를 바꾸면 `load_data()`의 `setdefault`로 이전 버전 파일과 호환되게 한다.
- 기능 추가 시 상단 docstring에 `vX.Y 변경점`을 추가하고 버전을 올린다.

## 검증
- 문법 확인: `python -c "import ast;ast.parse(open('Ddingdong.pyw',encoding='utf-8').read())"`
- 판정 로직(`base_match`, `should_fire`, `next_fire_date`)은 GUI 없이 import해서 테스트 가능:
  `python -c "from importlib.machinery import SourceFileLoader as L;m=L('r','Ddingdong.pyw').load_module();print(m.repeat_text({'repeat':'monthly','dom':32}))"`
  (import 시 GUI는 뜨지 않음 — `__main__` 가드)
- GUI 확인은 사용자가 Windows에서 직접 실행. "알림 미리보기" 버튼으로 알림 창 확인.

## exe 빌드
- `build_exe.bat` 또는 `py build_exe.py` → `dist/Ddingdong.exe` (PyInstaller `--onefile --noconsole`, 아이콘은 내장 base64에서 추출). `build/`·`dist/`는 git 제외.
- `BASE`가 `sys.argv[0]` 기준이라 exe 옆에 `reminder_data.json`이 생긴다. 이 경로 계산을 바꾸면 exe 배포가 깨질 수 있음.
- 앱 코드는 여전히 단일 파일·표준 라이브러리 전용. 빌드 스크립트만 PyInstaller에 의존.

## 공개 배포 규칙 (v2.9~)
- 예시 일정·기본값·placeholder에 특정 회사·부서·업무 용어(회의명, 시스템명 등)를 넣지 않는다. 범용 문구만 사용.
- 버전은 `APP_VERSION` 한 곳에서 관리(화면·exe 속성·업데이트 비교에 모두 사용). 기능 추가 시 docstring `vX.Y 변경점` + `APP_VERSION` 함께 올린다.
- 자동 업데이트: `GITHUB_REPO`("소유자/저장소")가 비어 있으면 기능이 꺼진다. 릴리스 태그는 `v<APP_VERSION>`, 자산 이름은 `UPDATE_ASSET`. 다운로드는 SHA-256 검증 필수(우회 금지), HTTPS·GitHub 도메인만 허용.
- 설정 창(⚙): 휴일·실행 기록·정보/업데이트는 메인 탭이 아니라 `_build_settings`의 페이지로 둔다.

## i18n · 테마 규칙 (v2.9~)
- UI에 보이는 문자열은 한국어 원문을 `T("...")`로 감싸고 `EN` 표에 영어를 추가한다. 로그 등 **저장되는 값**은 `T()`로 감싸지 않고(`# i18n:skip`) 표시할 때만 번역한다.
- 테마·언어는 시작 시 `_peek_prefs()`로 읽는다. 색상은 상수(`TEXT`, `CANVAS`, `BLUE` …)만 사용 — 하드코딩 색은 어두운 테마에서 깨진다. 파스텔 톤은 `tint()`를 쓴다.
- 이모지 대신 BMP 기호(`SYMBOL_CHOICES`)만 사용한다(Tk 이모지 렌더링 문제).
- 파일을 PowerShell `Set-Content -Encoding utf8`로 고치면 BOM이 붙어 문법 검사가 깨진다. 편집은 Edit 도구나 UTF-8(BOM 없음)로.

## 후원 · 의견 · 공개 저장소 규칙
- 저작권자는 `Ram's`(MIT). 커밋 작성자 이메일은 GitHub `noreply` 주소만 사용한다(저장소 로컬 git config).
- `FEEDBACK_EMAIL`(개인 메일/별칭)을 사용자 허락 없이 소스에 넣지 않는다. 공개 저장소·커밋 기록에 개인 메일이 남는다.
- 릴리스는 `v<APP_VERSION>` 태그 푸시 → GitHub Actions(`.github/workflows/release.yml`)가 exe를 빌드·첨부한다.
- 사용자용 문서는 `README.md`, 개발 문서는 `DEVELOPMENT.md`.
