# 띵동 리마인더 — 개발 문서

단일 파일 Windows 데스크톱 리마인더 + 메모장. Python 표준 라이브러리(tkinter, ctypes)만 사용하며 외부 패키지가 없습니다.

## 실행

```powershell
pythonw Ddingdong.pyw      # 콘솔 없이 실행 (배포용)
python  Ddingdong.pyw      # 콘솔과 함께 실행 (디버깅용, 오류가 터미널에 보임)
```

VS Code에서는 `F5` 로 중단점을 걸고 실행할 수 있습니다.

- 데이터 파일: 실행 파일과 같은 폴더의 `reminder_data.json` (자동 생성). 이전 버전(SOE Reminder) 사용자는 이 파일을 새 exe 옆에 두면 그대로 이어서 씁니다.
- 오류 로그: 같은 폴더의 `reminder_error.log`
- Windows 전용 기능: 모니터 목록, 창 맨 앞으로 띄우기, IME 폰트 보정, 비프음 (다른 OS에서는 조용히 건너뜀)

## 기능 요약

| 화면 | 기능 |
|---|---|
| 일정 | 시각·일정명·메모, 반복 5종(매일/평일/매주 요일/매월 일자·말일/날짜 지정 1회), 날짜 필드 클릭 시 달력, 주말·공휴일 이월, 일정별 포인트 색·기호, 수정·**복제**·삭제, **빠른 알림(10분/30분/1시간 뒤)**, 다음 알림 예정일 표시 |
| 메모장 | 자동 저장(400ms 디바운스), 체크박스 줄·시각 삽입, .txt 내보내기 |
| 설정 ▸ 일반 | 테마(밝게/어둡게/시스템)·언어(자동/한국어/English), Windows 시작 시 자동 실행, 다시 알림 간격(5/10/15/30분), 알림 소리(비프/알림음/끄기), 방해 금지 시간대, 백업 내보내기·가져오기(.json) |
| 설정 ▸ 휴일 | 공휴일·개인 휴무일 텍스트 편집 (`YYYY-MM-DD  설명`, `#` 주석) |
| 설정 ▸ 실행 기록 | 알림 처리 결과 기록(매일 반복·미리보기 제외, 최대 300건), .csv 내보내기 |
| 설정 ▸ 정보 · 업데이트 | 버전 표시, 자동 업데이트 확인(켜기/끄기·지금 확인·설치), 데이터 폴더 열기 |

창을 최소화하거나 닫으면 트레이로 숨고, 종료는 트레이 아이콘 우클릭 → 종료입니다.

알림 시: 지정 모니터에 전체화면, 3초마다 비프, 처음 4회 맨 앞으로 강제 이동, "확인" 또는 "5분 후 다시".

## 코드 구조 (구역 순서 · 줄 번호는 자주 바뀌므로 이름으로 검색)

| 구역 | 내용 |
|---|---|
| 헤더 docstring | 버전별 변경 이력 |
| 상수 | `APP_NAME`, `APP_VERSION`, `GITHUB_REPO`, `UPDATE_ASSET` |
| 아이콘 | `ICON_ICO_B64`, `ICON_PNG_B64`(base64 내장), `ensure_icon_file`, `apply_app_icon` — **편집 시 이 구간은 접어두세요** |
| 팔레트·상수 | 색상, `GROUPS`, `REPEAT_*`, `WEEK_NAMES`, `LAST_DAY`, `CATCHUP_MIN` |
| 일정 판정 로직 | `DEFAULT_HOLIDAYS`, `parse_holidays`, `base_match`, `should_fire`, `next_fire_date`, `repeat_text` |
| 폰트·저장소·모니터·Win API·IME | `F()`, `load_data`/`save_data`, `pick_monitor`, `force_front`, `tune_ime` |
| 커스텀 위젯 | `RoundBox`, `Pill`, `TimeField`, `ToggleChip`, `DayField`, `CalendarPopup`, `DateField`, `Dropdown`, `ScrollArea` |
| `AlarmWindow` | 전체화면 알림 창 |
| 자동 업데이트 | `fetch_latest_release`, `download_release`(SHA-256 검증), `apply_update` |
| `TrayIcon` | `Shell_NotifyIconW`(ctypes) 트레이 아이콘 |
| `App` | 메인 창, 설정 창(`_build_settings`), 일정 CRUD, `_tick` 1초 루프, 업데이트 UI |
| 진입점 | `_fatal` 예외 훅, `App().mainloop()` |

### 데이터 스키마 (`reminder_data.json`)

```json
{
  "items": [{
    "id": "20261123091900123456", "time": "17:00", "title": "...", "memo": "...",
    "repeat": "daily|weekday|weekly|monthly|once",
    "weekdays": [0, 2],     // weekly: 0=월 ~ 6=일
    "dom": 15,              // monthly: 1~31, 32=말일
    "shift": true,          // weekly/monthly/once 에서만 의미 있음
    "day": "2026-11-23"     // once 알림 날짜(날짜 지정 1회)
  }],
  "memo": "...", "logs": [{"fired","time","title","repeat","result"}],
  "holidays": "텍스트 원문", "monitor": 0,
  "fired": ["2026-11-23|id", ...],   // 이미 울린 알림(어제 이전은 자동 정리)
  "auto_update": true, "update_checked": "2026-11-23 09:00"
}
```

### 알림 판정 흐름

`_tick()` (1초) → 스누즈 대기열(`pending`) 우선 → 아니면 `items` 중 `time == 현재 HH:MM` 이고 오늘 아직 안 울린(`fired`에 `날짜|id` 없음) 항목 → `should_fire()`:
- `daily`/`weekday` 또는 `shift=False` → `base_match()` 그대로
- 이월 켜짐 → 오늘이 영업일이고, 최근 15일 내 원래 예정일 중 `next_business_day()`가 오늘인 날이 있으면 발화

## 테마 · 언어 (i18n)

- 색상 상수(`TEXT`, `CANVAS` …)와 번역은 위젯이 만들어지기 전에 정해져야 하므로, 시작할 때 `reminder_data.json`의 `theme`/`lang`만 먼저 읽습니다(`_peek_prefs`). 설정에서 바꾸면 **다시 시작** 후 적용됩니다.
- UI 문구는 한국어 원문을 `T("...")`로 감싸고 `EN` 표에서 영어로 바꿉니다. 새 문구를 추가하면 `EN`에도 넣으세요(없으면 한국어가 그대로 보입니다).
- 로그에 저장되는 값(`"확인"`, `"스누즈"`, `"방해 금지로 건너뜀"`)은 한국어 코드 그대로 저장하고 **표시할 때만** `T()`로 번역합니다(코드 줄 끝 `# i18n:skip`).
- 기본 공휴일 표는 한국 기준이며, 설정 ▸ 휴일에서 자유롭게 고칠 수 있습니다.

## 릴리스 절차 (GitHub Actions)

1. 코드를 고치고 `APP_VERSION` 을 올립니다(docstring `vX.Y 변경점`도 함께).
2. 커밋·푸시 후 **태그 `v<APP_VERSION>`** 를 만들어 올립니다: `git tag v2.9.1 && git push origin v2.9.1`
3. `.github/workflows/release.yml` 이 Windows에서 `build_exe.py` 로 exe를 빌드해 Release에 `Ddingdong.exe` 를 첨부합니다(태그와 `APP_VERSION`이 다르면 실패).
4. 사용자 앱은 시작 후 하루 한 번 `releases/latest` 를 조회 → 더 높은 버전이면 헤더에 "새 버전" 표시 → 설치 시 exe를 받아 **GitHub가 계산한 SHA-256(digest)과 일치할 때만** `실행 중 exe → .old` 로 옮기고 교체한 뒤 재시작합니다.

- 상수: `GITHUB_REPO`(업데이트·이슈 링크), `UPDATE_ASSET`(자산 이름, 빌드 결과와 동일해야 함).
- 보안: HTTPS + `github.com`/`githubusercontent.com` 도메인만 허용, 해시가 없거나 불일치하면 설치하지 않고 릴리스 페이지를 엽니다. `.pyw` 로 실행 중이면 자동 설치 대신 릴리스 페이지를 엽니다.

## 후원 · 의견

- `DONATE_URL` / `DONATE_QR_B64` : 카카오페이 송금 링크와 QR(설정 ▸ 후원 · 의견, 트레이 메뉴).
- 의견: `FEEDBACK_EMAIL` 에 메일(또는 FormSubmit 별칭)이 있으면 FormSubmit(무료 폼→메일 중계)으로 개발자 메일에 직접 전달하고, 실패하면 공개 GitHub 이슈 작성 화면(제목·본문 미리 채움)으로 되돌아갑니다. 비어 있으면 처음부터 이슈 화면을 엽니다.
- v2.9.1부터 개발자 메일이 소스에 들어 있습니다(공개 저장소라 주소가 노출됨). 노출이 싫으면 FormSubmit이 활성화 후 발급하는 임의 별칭(alias)으로 교체하세요. 첫 전송 때 활성화 메일 승인이 필요합니다.
- 오류 기록 첨부는 기본 꺼짐(경로에 Windows 사용자 이름이 들어갈 수 있음).

## 분석 중 발견한 개선 포인트

**동작에 영향이 있을 수 있는 것**
1. `fired` 집합이 메모리에만 있음 → 알림 시각 같은 분에 앱을 재시작하면 같은 알림이 다시 울림. 프로그램을 며칠 켜두면 집합이 계속 커짐(실害는 작음).
2. ~~알림 창이 떠 있는 동안 다른 일정 시각이 지나가면 건너뜀~~ → v2.8에서 해결: `_tick`이 알림 창 유무와 무관하게 매 틱 검사해 `self.pending` 대기열에 넣고, 창이 닫히면 순서대로 표시.
3. `_tick`이 `after(1000)` 누적이라 시스템 부하·절전 복귀 시 특정 분을 통째로 건너뛸 수 있음 → "마지막 검사 시각 ~ 현재" 구간 검사로 바꾸면 견고해짐. 목록 갱신의 `now.second == 0` 조건도 같은 이유로 가끔 누락.
4. ~~`save_data()`가 예외를 무시함~~ → v2.8에서 해결: 임시파일 작성 후 `os.replace`로 교체, 실패 시 `App._save()`가 연속 실패 중 1회 알림.
5. ~~`load_data()`가 JSON 손상 시 조용히 샘플 데이터로 시작~~ → v2.8에서 해결: 손상 파일을 `.bak`(있으면 시각 접미사)으로 옮긴 뒤 시작.

**사소한 것**
6. `TimeField._key`: `if e.keysym in ("Up", "Right") and e.keysym == "Up"` — 사실상 `== "Up"`과 같음(정리만 필요).
7. `_end_edit()`가 반복 드롭다운·요일 칩·일자·이월 옵션은 초기화하지 않음 → 수정 취소 후 새 일정 추가 시 이전 값이 남음.
8. `ScrollArea._leave`의 `unbind_all`은 앱 전체 휠 바인딩을 제거 → 지금은 영향 없지만 다른 곳에서 `bind_all`을 쓰면 충돌.
9. ~~`once` 항목을 수정하면 `day`가 오늘로 바뀜~~ → v2.8에서 날짜 선택기 값으로 저장됨.
10. 2027년 공휴일은 잠정값 — 연말에 관보 확인 후 휴일 탭에서 갱신 필요.

## 다음 작업 아이디어
- ~~트레이 상주~~ → v2.8에서 구현: 최소화·창 닫기(X) 모두 트레이로 숨김, 종료는 트레이 우클릭 → 종료.
- Windows 시작 시 자동 실행 옵션
- ~~PyInstaller로 단일 exe 빌드~~ → `build_exe.bat`(또는 `py build_exe.py`) 실행 시 `dist/Ddingdong.exe` 생성. 빌드 PC에만 `pip install pyinstaller` 필요, 배포받는 PC는 Python 불필요. 데이터(`reminder_data.json`)는 exe와 같은 폴더에 생성됨.
- 일정 로직(1010–1158줄)을 별도 모듈로 분리해 단위 테스트 작성
