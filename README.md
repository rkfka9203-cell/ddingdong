# 띵동 리마인더 (Ddingdong Reminder)

정해둔 시각이 되면 **화면 가득** 알려주는 가볍고 친근한 Windows 데스크톱 리마인더 + 메모장입니다.
설치 없이 exe 파일 하나로 실행되고, 창을 닫아도 트레이에서 계속 지켜봐요.

*A friendly Windows desktop reminder + notepad that alerts you full-screen at the time you choose. One portable exe, lives in the tray.*

## 다운로드

[**Releases**](https://github.com/rkfka9203-cell/ddingdong/releases/latest) 에서 `Ddingdong.exe` 를 받아 원하는 폴더에 두고 실행하세요. (Windows 10/11)

> 서명되지 않은 개인 개발 프로그램이라 처음 실행할 때 Windows SmartScreen이 경고할 수 있어요.
> **추가 정보 → 실행** 을 누르면 됩니다. 소스 코드는 이 저장소에 모두 공개되어 있습니다.

데이터(`reminder_data.json`)는 exe와 **같은 폴더**에 저장되니, 쓰기 권한이 있는 폴더(바탕화면·문서 등)에 두세요.

## 기능

- **일정**: 매일 / 평일 / 매주(요일 선택) / 매월(일자·말일) / 날짜 지정 1회, 공휴일·주말 다음 영업일 이월
- **빠른 알림**: "10분 / 30분 / 1시간 뒤" 버튼, 일정 복제, 일정별 색·기호 꾸미기
- **전체화면 알림**: 지정한 모니터에 크게 표시, "확인했어요" / "N분 뒤에 다시"(5·10·15·30분)
- **방해 금지 시간대**, 알림 소리 선택(비프 / 부드러운 알림음 / 끄기)
- **메모장**: 자동 저장, 체크박스 줄, 시각 삽입, .txt 내보내기
- **트레이 상주**, Windows 시작 시 자동 실행(선택)
- **밝은 / 어두운 테마**, **한국어 / English**
- **백업**: 일정·메모·휴일·설정을 .json 으로 내보내기 / 가져오기
- **자동 업데이트**: 새 버전이 나오면 알려주고, 설치하면 SHA-256 검증 후 교체·재시작

## 자동 업데이트와 개인정보

- 하루 한 번 이 저장소의 최신 Release 정보를 조회합니다(설정에서 끌 수 있어요). 요청에는 **사용자를 식별하는 정보가 포함되지 않습니다.**
- 내려받은 exe는 GitHub가 제공하는 SHA-256 값과 일치할 때만 설치합니다. 일정·메모 등 모든 데이터는 내 PC에만 저장돼요.

## 후원 · 의견

무료로 만들고 있어요. 도움이 되셨다면 **설정 ▸ 후원 · 의견** 에서 QR(카카오페이)로 커피 한 잔 부탁드려요 ☕
버그·아이디어는 같은 화면에서 보내 주시거나 [Issues](https://github.com/rkfka9203-cell/ddingdong/issues) 에 남겨 주세요.
(이슈는 누구나 볼 수 있으니 개인정보는 적지 마세요.)

## 소스에서 실행 / 빌드

Python 3.8+ 만 있으면 됩니다(외부 패키지 없음, 표준 라이브러리 `tkinter`·`ctypes`).

```powershell
pythonw Ddingdong.pyw          # 실행
pip install pyinstaller
python build_exe.py            # dist/Ddingdong.exe 생성 (build_exe.bat 더블클릭도 가능)
```

개발 구조·데이터 스키마·릴리스 절차는 [DEVELOPMENT.md](DEVELOPMENT.md) 를 보세요.

## 라이선스

[MIT](LICENSE) © 2026 Ram's
