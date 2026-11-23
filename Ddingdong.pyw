# -*- coding: utf-8 -*-
"""
띵동 리마인더(Ddingdong) - 단일 파일 데스크톱 리마인더 + 메모장  (v2.9.0)

v2.9.1 변경점
  - 의견 보내기가 개발자 메일로 바로 전달됨(FormSubmit), 실패하면 GitHub 이슈 화면으로 대체

v2.9 변경점
  - 프로그램 이름을 '띵동 리마인더(Ddingdong)'로 변경
  - 설정 ▸ 일반 추가: 테마(밝게/어둡게/시스템), 언어(자동/한국어/English), Windows 시작 시 자동 실행(트레이),
    다시 알림 간격(5/10/15/30분), 알림 소리(비프/알림음/끄기), 방해 금지 시간대, 일정 백업 내보내기·가져오기(.json)
  - 일정 복제, '10분/30분/1시간 뒤' 빠른 알림, 일정별 포인트 색·기호(목록·알림 화면에 표시)
  - 영어 UI 지원(UI 문구는 T()로 감싸고 EN 표에서 번역), 어두운 테마, 얇은 둥근 스크롤바
  - 설정 ▸ 후원 · 의견: 카카오페이 QR·링크, 의견 보내기(GitHub 이슈 또는 FormSubmit 메일), 트레이 메뉴에도 추가
  - 날짜 지정 필드를 클릭하면 달력 팝업으로 날짜 선택
  - 공개 배포용으로 예시 일정·문구를 범용 내용으로 교체
  - 디자인 개편: 새 색상 팔레트, 헤더(버전 표시·인사말·오늘 남은 알림 요약), 알약형 탭,
    둥근 카드형 일정 목록(그룹 색상 시각 칩), 더 큰 모서리 반경, 친근한 문구
  - '휴일'·'실행 기록'을 설정(⚙) 창으로 이동, 설정에 '정보·업데이트' 추가
  - 버전 정보(APP_VERSION) 표시 및 exe 파일 속성에 버전 기록
  - GitHub Releases 기반 자동 업데이트(exe 배포본: 다운로드 → SHA-256 검증 → 교체·재시작)

v2.8 변경점
  - 저장을 임시파일 작성 후 교체(os.replace)로 변경, JSON 손상 시 .bak으로 백업 후 시작
  - 저장 실패 시 사용자에게 알림(연속 실패 중 1회)
  - 알림 판정을 '마지막 검사 이후 지난 모든 분' 검사로 변경(절전 복귀 후 최대 30분 소급)
  - 이미 울린 기록(fired)을 파일에 저장 → 재시작해도 중복 알림 없음, 어제 이전 기록은 자동 정리
  - 최소화·창 닫기(X)하면 알림 영역(트레이) 아이콘으로 이동: 클릭 → 열기, 우클릭 → 열기/종료 (ctypes, 표준 라이브러리만)
    (트레이를 쓸 수 없는 환경에서는 X가 기존처럼 종료 확인)
  - 앱 아이콘 교체: 블루 그라데이션 라운드 사각형 + 흰 시계 + 오렌지 알림 배지(창·작업표시줄·트레이·exe 공용)
  - 반복에 '날짜 지정 1회' 추가: 연-월-일 선택기로 미래 날짜 지정(기존 '오늘 1회' 데이터와 호환)
  - 알림 창이 떠 있는 동안 시각이 된 일정(또는 같은 시각의 여러 일정)을 놓치지 않고 대기열에 넣어 순서대로 표시

v2.7 변경점
  - 반복 유형 확장: 매주(요일 지정, 복수 선택) · 매월(일자 지정, '말일' 포함)
  - 주말·공휴일에 걸린 일정을 다음 영업일로 자동 이월(항목별 옵션)
  - '휴일' 탭 추가: 공휴일·개인 휴무일 직접 관리(2026~2027 기본 표 내장)
  - 목록에 다음 알림 예정일 표시(이월 반영)

v2.6 변경점
  - 전체화면 알림 폰트 확대(비율 유지, 버튼은 기존 크기 유지)
  - 알림을 표시할 모니터 선택 기능 추가(주/보조 모니터, 설정 자동 저장)

v2.5 변경점
  - 목록 마우스 휠 스크롤 재수정: 그룹 헤더·행·칩 등 모든 하위 위젯에 재귀적으로 바인드
  - 입력 폼을 grid 가중치 배치로 교체 → 창 폭을 줄여도 반복·추가 버튼이 사라지지 않음
  - 등록된 일정 수정 기능 추가 (행의 '수정' 또는 더블클릭 → 수정 저장 / 취소)

v2.4 변경점
  - 반복 유형별 그룹(매일 루틴 / 평일 루틴 / 단건) 표시
  - 알람시계 앱 아이콘 내장(창·작업표시줄)

v2.1 변경점
  - 시각 입력기: Windows 기본 Spinbox 제거 → Canvas로 직접 그린 커스텀 TimeField
  - 반복 선택: tk.OptionMenu 제거 → 커스텀 둥근 드롭다운
  - 한글 입력 시 폰트가 굴림체로 틀어졌다 되돌아오는 현상 수정
    (실제 설치된 한글 폰트를 탐지해 단일 Font 객체로 전역 고정)

실행: 파일 더블클릭 (또는) pythonw Ddingdong.pyw
"""

import base64
import calendar
import csv
import hashlib
import json
import os
import queue
import re
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import ctypes
from datetime import datetime, timedelta

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, filedialog

APP_VERSION = "2.9.1"
# 자동 업데이트에 사용할 GitHub 저장소("소유자/저장소"). 비워 두면 업데이트 기능이 꺼진다.
GITHUB_REPO = "rkfka9203-cell/ddingdong"
# 후원(카카오페이 송금) — 링크와 QR 이미지
DONATE_URL = "https://qr.kakaopay.com/281006011102510980005626"
DONATE_QR_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAMYAAADGCAAAAACs8KCBAAACM0lEQVR42u3d22rEMAxFUan0/39ZfR0YEiS5Q6FZeeol48km4mAd"
    "y3JW/IfrK2DAgAEDBgwYMP7w+n79Jdsfq5f76+Kz7/e8f8v7jG76DIIKBoynKdWVesStznT06uov2bgnGmomqGDAeJpSRVtz4kKj"
    "OgoWDb3qP4OgggHjmUrVubKdFd5nguVtwIAB42NKFbceVLbzR28DBgwYO6Wq1fzqKtfr++27ZxBUMGA8Tanyl4buZ4L364OCCgaM"
    "x2NkfcCnmuoenwoGDBjTeqoaZnZ9HbtaK8yVG6aeCgYMPtW0TiCHVQc11LcUVDBgyP5WOnPiL+3GN6eCAcOcKm8rOa9+zkaOlsOK"
    "9xyOI6hgwHiOUvWrzesgZ7xXp467XoIKBowHZ395XG3emWtFY2Q7lGHAgNHxqaLtEcWBLnVUrlMvKqhgwOBT5Wqfcmctr257KfQd"
    "e0EFA8aTfarOnuLdWmE2ZmvFp4IBA8atTxWxqS7ouOideqoael+CCgYMu2n6ihQrjz0P9g8KKhgwKFWni1QeV3ie/1dQwYAR+qiv"
    "ZlY5rPDszMpKd2IYMDjqse+bFx/bX1OCCgYMSnWsKrXKFmuldfqow4BBqXZn0+xObehnkeqpYMCgVJ/rkjft29mvEeVTwYBBqeLg"
    "rIfz0xym/V4EFQwYlGo6F6phB9H+OPpTwYBBqU56m9eq3iCGczD9qWDACJWfq7W/PO6nV8MztmR/MGBQKm8DBgwYMGDAgAFjdf0A"
    "zUCxrOmCZ7YAAAAASUVORK5CYII="
)
# 의견 보내기: FEEDBACK_EMAIL 을 채우면 FormSubmit(무료 폼→메일 중계)으로 개발자 메일에 전달하고,
# 비워 두면 GitHub 이슈(공개) 작성 화면을 연다. 공개 저장소에 메일 주소가 노출되지 않도록
# FormSubmit 이 발급하는 임의 별칭(alias)을 넣는 것을 권장한다.
FEEDBACK_EMAIL = "rkfka9203@gmail.com"
FEEDBACK_ENDPOINT_BASE = "https://formsubmit.co/ajax/"
UPDATE_ASSET = "Ddingdong.exe"      # Release에 올리는 exe 파일명(빌드 결과와 동일해야 함)

IS_WIN = sys.platform.startswith("win")
if IS_WIN:
    import winsound

BASE = os.path.dirname(os.path.abspath(sys.argv[0]))
DATA_PATH = os.path.join(BASE, "reminder_data.json")


# ------------------------------------------------------------------ 테마 · 언어
#  색상 상수와 번역은 위젯이 만들어지기 전에 정해져야 하므로, 저장 파일에서
#  설정만 미리 읽는다. 값을 바꾸면 '다시 시작' 후 적용된다.
def _peek_prefs():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
        return str(d.get("theme", "system")), str(d.get("lang", "auto"))
    except Exception:
        return "system", "auto"


def _system_is_dark():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as k:
            return winreg.QueryValueEx(k, "AppsUseLightTheme")[0] == 0
    except Exception:
        return False


def _system_lang():
    try:
        lid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return "ko" if (lid & 0x3FF) == 0x12 else "en"
    except Exception:
        return "ko"


_PREF_THEME, _PREF_LANG = _peek_prefs()
DARK_MODE = _PREF_THEME == "dark" or (_PREF_THEME == "system" and _system_is_dark())
LANG = _PREF_LANG if _PREF_LANG in ("ko", "en") else _system_lang()


# ------------------------------------------------------------------ 번역(영어)
#  UI 문구는 한국어 원문을 T()로 감싸고, 아래 표에서 영어로 바꾼다.
EN = {'띵동 리마인더': 'Ddingdong Reminder',
 '매일 반복': 'Every day',
 '주말 포함 매일': 'Including weekends',
 '평일 반복': 'Weekdays',
 '월요일~금요일': 'Monday to Friday',
 '매주 반복': 'Every week',
 '지정한 요일마다': 'On the days you choose',
 '매월 반복': 'Every month',
 '지정한 일자마다': 'On the day you choose',
 '한 번만': 'Just once',
 '지정한 날짜에 1회': 'Once, on the date you pick',
 '매일': 'Daily',
 '평일': 'Weekdays',
 '매주': 'Weekly',
 '매월': 'Monthly',
 '1회': 'Once',
 '평일(월~금)': 'Weekdays (Mon-Fri)',
 '매주(요일 지정)': 'Weekly (pick days)',
 '매월(일자 지정)': 'Monthly (pick a day)',
 '날짜 지정 1회': 'Once (pick a date)',
 '월': 'Mon',
 '화': 'Tue',
 '수': 'Wed',
 '목': 'Thu',
 '금': 'Fri',
 '토': 'Sat',
 '일': 'Sun',
 '매주 ': 'Every ',
 '매월 말일': 'Monthly, last day',
 '매월 %d일': 'Monthly, day %d',
 '오늘 1회': 'Once, today',
 '%s(%s) 1회': '%s (%s), once',
 '올바른 데이터 파일이 아닙니다.': 'This is not a valid data file.',
 '하루 시작하기': 'Start your day',
 '오늘 할 일을 확인하세요': "Check today's to-dos",
 '주 모니터': 'Main monitor',
 '보조 모니터': 'Secondary monitor',
 '1일': 'Day 1',
 '말일': 'Last day',
 '%d일': 'Day %d',
 '%d년 %d월': '%d-%02d',
 '오늘': 'Today',
 '닫기': 'Close',
 '알림이 도착했어요': "Time's up!",
 '현재 ': 'Now ',
 '확인했어요': 'Got it',
 '%d분 뒤에 다시': 'Remind me in %d min',
 '확인': 'Confirmed',
 '스누즈': 'Snoozed',
 '5분 스누즈': 'Snoozed (5 min)',
 '검증 가능한 다운로드 정보가 없습니다.': 'No verifiable download information.',
 '신뢰할 수 없는 다운로드 주소입니다.': 'Untrusted download address.',
 '파일 무결성 검증에 실패했습니다(SHA-256 불일치).': 'File integrity check failed (SHA-256 mismatch).',
 '열기': 'Open',
 '종료': 'Quit',
 '일정 리마인더 · 감시 중': 'Ddingdong Reminder - running',
 '일정 리마인더': 'Reminder',
 '트레이에서 계속 감시합니다. 아이콘 클릭 → 열기, 우클릭 → 종료.': 'Still running in the tray. Click the icon to open, right-click '
                                           'to quit.',
 '저장에 실패했습니다. 변경 내용이 파일에 남지 않을 수 있습니다.\n(폴더 권한·OneDrive 동기화 잠금·디스크 공간을 확인하세요)\n\n': 'Saving failed. Your '
                                                                                    'changes may not be '
                                                                                    'written to disk.\n'
                                                                                    '(Check folder '
                                                                                    'permissions, OneDrive '
                                                                                    'sync locks and free '
                                                                                    'disk space.)\n'
                                                                                    '\n',
 '저장 실패': 'Save failed',
 'reminder_data.json 저장에 실패했습니다.': 'Could not save reminder_data.json.',
 '알림 표시 화면': 'Show alerts on',
 '일정': 'Schedule',
 '메모장': 'Notes',
 '설정': 'Settings',
 ' · 설정': ' - Settings',
 '일반': 'General',
 '휴일': 'Holidays',
 '실행 기록': 'History',
 '정보 · 업데이트': 'About & Updates',
 '시각': 'Time',
 '일정명': 'Title',
 '예) 약 먹기, 스트레칭': 'e.g. Take medicine, stretch',
 '메모 (선택)': 'Note (optional)',
 '예) 물 한 컵과 함께': 'e.g. With a glass of water',
 '반복': 'Repeat',
 '추가': 'Add',
 '수정 저장': 'Save changes',
 '취소': 'Cancel',
 '요일': 'Days',
 '일자': 'Day',
 "'말일' 선택 가능 · 31일로 두면 그 날짜가 없는 달은 말일로 자동 보정": "Choose 'Last day', or 31 to fall back to the last day in "
                                               'shorter months',
 '날짜': 'Date',
 '주말·공휴일이면 다음 영업일로 이월': 'If it falls on a weekend/holiday, move to the next business day',
 '꾸미기': 'Style',
 '알림 미리보기': 'Preview alert',
 '선택 삭제': 'Delete selected',
 '감시 중 · 알림 대기': 'Watching for alerts',
 '1시간 뒤': 'In 1 hour',
 '30분 뒤': 'In 30 min',
 '10분 뒤': 'In 10 min',
 '빠른 알림': 'Quick alert',
 '불러옴': 'Loaded',
 '비우기': 'Clear',
 '.txt 저장': 'Save .txt',
 '체크박스 줄': 'Checkbox line',
 '시각 삽입': 'Insert time',
 "한 줄에 날짜 하나(YYYY-MM-DD) · '#'으로 시작하는 줄은 메모로 무시됩니다": 'One date per line (YYYY-MM-DD). Lines starting with '
                                                     "'#' are ignored.",
 '기본 공휴일 다시 넣기': 'Restore default holidays',
 '오늘 날짜 추가': 'Add today',
 '휴일 %d일 등록됨': '%d holidays registered',
 '입력 중…': 'Typing…',
 '저장됨 · 휴일 %d일 등록': 'Saved - %d holidays',
 '기본 공휴일': 'Default holidays',
 '현재 내용을 기본 공휴일 표로 되돌릴까요?': 'Reset the list to the default holiday table?',
 '  휴무': '  Day off',
 '실행 기록 0건': '0 history entries',
 '기록 비우기': 'Clear history',
 '.csv 저장': 'Save .csv',
 '발생 일시': 'Fired at',
 '예정 시각': 'Scheduled',
 '처리': 'Result',
 '아직 등록된 일정이 없어요': 'No reminders yet',
 "위에서 시각과 이름을 넣고 '추가'를 눌러 보세요.\n정한 시간에 화면 가득 알려드릴게요.": "Enter a time and a title above, then press 'Add'.\n"
                                                       "We'll alert you full-screen at that time.",
 '휴일 → 다음 영업일': 'Holiday → next business day',
 '삭제': 'Delete',
 '수정': 'Edit',
 '복제': 'Duplicate',
 '늦은 시간이에요': "It's late",
 '좋은 아침이에요': 'Good morning',
 '좋은 오후예요': 'Good afternoon',
 '편안한 저녁이에요': 'Good evening',
 '오늘 남은 알림 %d개 · 다음은 %s %s': '%d alert(s) left today - next: %s %s',
 '오늘 남은 알림은 없어요': 'No more alerts today',
 '수정 중 · %s': 'Editing - %s',
 ' (복사)': ' (copy)',
 '삭제할 일정을 목록에서 클릭해 선택하세요.': 'Click a reminder in the list to select it first.',
 '입력 확인': 'Check input',
 '일정명을 입력하세요.': 'Please enter a title.',
 '반복할 요일을 하나 이상 선택하세요.': 'Choose at least one day.',
 '지난 날짜는 지정할 수 없습니다.\n오늘 또는 이후 날짜를 선택하세요.': "You can't pick a past date.\nChoose today or later.",
 '약 %d분 후': 'in about %d min',
 '약 %d시간 %d분 후': 'in about %dh %dm',
 '예정 없음': 'Nothing scheduled',
 '다음 알림 %s(%s) · %d일 후': 'Next: %s (%s) - in %d day(s)',
 '자동 저장됨 · %s · %d자': 'Autosaved - %s - %d chars',
 '메모 내용을 모두 지울까요?': 'Clear all notes?',
 '텍스트 파일': 'Text file',
 '실행 기록 %d건 (매일 반복 제외)': '%d history entries (daily repeats excluded)',
 "아직 기록이 없습니다. 반복이 '매일'이 아닌 일정이 실행되면 자동으로 기록됩니다.": "No history yet. Reminders that don't repeat daily are "
                                                   'logged here when they fire.',
 'CSV 파일': 'CSV file',
 '발생일시': 'Fired at',
 '예정시각': 'Scheduled',
 '실행 기록을 모두 삭제할까요?': 'Delete the whole history?',
 '이러한 형태로 전체화면 알림이 표시됩니다.': 'This is how the full-screen alert looks.',
 '방해 금지로 건너뜀': 'Skipped (Do not disturb)',
 '화면': 'Display',
 '시스템 설정 따르기': 'Follow system',
 '밝게': 'Light',
 '어둡게': 'Dark',
 '자동': 'Auto',
 '한국어': '한국어 (Korean)',
 '테마': 'Theme',
 '언어': 'Language',
 '변경 사항은 다시 시작하면 적용됩니다.': 'Changes apply after a restart.',
 '지금 다시 시작': 'Restart now',
 '시작': 'Startup',
 'Windows 시작 시 자동 실행 (트레이에서 조용히 시작)': 'Launch when Windows starts (quietly, in the tray)',
 '알림': 'Alerts',
 '%d분': '%d min',
 '다시 알림 간격': 'Snooze length',
 '기본 비프음': 'Classic beep',
 '부드러운 알림음': 'Soft chime',
 '소리 끄기': 'Sound off',
 '알림 소리': 'Alert sound',
 '들어보기': 'Preview',
 '방해 금지': 'Do not disturb',
 '사용': 'On',
 "방해 금지 시간에 울릴 알림은 화면에 띄우지 않고, 실행 기록에 '건너뜀'으로 남깁니다.": "Alerts due during these hours are not shown; they're "
                                                      "logged as 'Skipped' in History.",
 '백업': 'Backup',
 '내보내기 (.json)': 'Export (.json)',
 '가져오기 (.json)': 'Import (.json)',
 '일정·메모·휴일·실행 기록·설정이 한 파일에 담깁니다. PC를 바꿀 때 가져오기로 옮기세요.': 'Reminders, notes, holidays, history and settings go '
                                                        'into one file. Use Import to move to a new PC.',
 '시작 프로그램': 'Startup',
 '자동 실행 설정을 바꾸지 못했습니다.': "Couldn't change the startup setting.",
 '다시 시작': 'Restart',
 '다시 시작하지 못했습니다.\n\n%s': "Couldn't restart.\n\n%s",
 '내보내기': 'Export',
 '저장하지 못했습니다.\n\n%s': "Couldn't save.\n\n%s",
 '백업 파일을 저장했습니다.\n\n%s': 'Backup saved.\n\n%s',
 '가져오기': 'Import',
 '올바른 백업 파일이 아닙니다.': 'This is not a valid backup file.',
 "'예' : 현재 일정에 합치기 (같은 일정은 건너뜀)\n'아니오' : 파일 내용으로 덮어쓰기\n'취소' : 가져오지 않음": "'Yes': merge into current reminders "
                                                                        '(duplicates skipped)\n'
                                                                        "'No': overwrite with the file's "
                                                                        'contents\n'
                                                                        "'Cancel': don't import",
 '가져왔습니다. 테마·언어 같은 설정은 다시 시작하면 적용됩니다.': 'Imported. Settings such as theme and language apply after a '
                                        'restart.',
 '정해둔 시각에 전체화면으로 알려주는 데스크톱 리마인더 + 메모장': 'A desktop reminder + notepad that alerts you full-screen at the '
                                        'time you choose',
 '업데이트': 'Updates',
 '시작할 때 하루 한 번 새 버전 확인': 'Check for a new version once a day at startup',
 '업데이트 저장소가 설정되지 않아 확인할 수 없습니다.': 'No update repository is configured.',
 '마지막 확인: ': 'Last checked: ',
 '아직 확인하지 않았습니다.': 'Not checked yet.',
 '지금 확인': 'Check now',
 '새 버전 설치': 'Install update',
 '데이터': 'Data',
 '폴더 열기': 'Open folder',
 '업데이트 저장소(GITHUB_REPO)가 설정되지 않았습니다.': 'The update repository (GITHUB_REPO) is not configured.',
 '확인 중…': 'Checking…',
 '다운로드 중… %d%%': 'Downloading… %d%%',
 '설치 실패: %s': 'Install failed: %s',
 '업데이트에 실패했습니다.\n\n%s': 'The update failed.\n\n%s',
 '확인하지 못했습니다(네트워크 또는 저장소 설정 확인): %s': "Couldn't check (network or repository settings): %s",
 '새 버전 v%s 이(가) 있습니다. (현재 v%s)': 'Version v%s is available. (current v%s)',
 '새 버전 v%s': 'New v%s',
 '설정 → 정보 · 업데이트에서 설치할 수 있습니다.': 'Install it from Settings → About & Updates.',
 '새 버전 v%s 이(가) 있습니다.\n지금 설치할까요?': 'Version v%s is available.\nInstall it now?',
 '최신 버전입니다. (v%s · 확인 %s)': "You're up to date. (v%s - checked %s)",
 'v%s 을(를) 내려받아 설치합니다.\n설치가 끝나면 앱이 자동으로 다시 시작됩니다. 계속할까요?': 'Download and install v%s?\n'
                                                           "The app restarts automatically when it's done.",
 '다운로드 중… 0%': 'Downloading… 0%',
 '파일 교체에 실패했습니다.\n폴더 쓰기 권한을 확인해 주세요.\n\n%s': "Couldn't replace the file.\n"
                                             'Check write permission for the folder.\n'
                                             '\n'
                                             '%s',
 '리마인더를 종료할까요?\n종료하면 알림이 동작하지 않습니다.': "Quit the reminder?\nAlerts won't fire while it's closed.",
 '실행 오류': 'Startup error',
 '앱 실행 중 오류가 발생했습니다.\n같은 폴더의 reminder_error.log 파일을 확인하세요.\n\n': 'An error occurred.\n'
                                                                 'See reminder_error.log in the same '
                                                                 'folder.\n'
                                                                 '\n',
    '후원 · 의견': 'Support & Feedback',
    '무료로 만들고 있어요. 도움이 되셨다면 커피 한 잔 부탁드려요 ☕': 'Ddingdong is free. If it helps you, a coffee is appreciated ☕',
    '개발자 후원하기': 'Support the developer',
    '☕ 개발자 후원하기': '☕ Support the developer',
    '휴대폰 카메라로 QR을 찍거나, 버튼을 눌러 카카오페이 송금 페이지를 열어요.': 'Scan the QR code with your phone, or press the button to open the KakaoPay page.',
    '금액은 자유예요. 후원금은 기능 개선에 쓰여요.': 'Any amount is welcome. Donations go into improvements.',
    '개발자에게 의견 보내기': 'Send feedback to the developer',
    '버그, 원하는 기능, 불편한 점 무엇이든 좋아요.': 'Bugs, feature ideas, anything that bugs you - all welcome.',
    '개발자 메일로 바로 전달돼요.': "It goes straight to the developer's inbox.",
    'GitHub 이슈(공개)로 전달돼요.': "It's sent as a public GitHub issue.",
    '기능 제안': 'Feature idea',
    '버그 신고': 'Bug report',
    '기타': 'Other',
    '답장 받을 이메일 (선택)': 'Your email for a reply (optional)',
    '오류 기록(reminder_error.log)도 함께 보내기': 'Also send the error log (reminder_error.log)',
    '오류 기록에는 PC 경로(사용자 이름)가 들어 있을 수 있어요.': 'The log may contain file paths that include your Windows user name.',
    '보내기': 'Send',
    '내용을 입력해 주세요.': 'Please write something first.',
    '보내는 중…': 'Sending…',
    '✓ 보냈어요. 감사합니다!': '✓ Sent. Thank you!',
    '첫 전송: 개발자 메일함의 FormSubmit 활성화 메일을 승인해 주세요.': 'First send: the developer needs to approve the FormSubmit activation email.',
    '전송에 실패했어요. GitHub 이슈 작성 화면을 열게요.': 'Sending failed. Opening a GitHub issue draft instead.',
    'GitHub 이슈 작성 화면을 열었어요. 이슈는 누구나 볼 수 있는 공개 글이니 개인정보는 적지 마세요.': "Opened a GitHub issue draft. Issues are public, so don't include personal information.",
    '의견을 받을 곳이 아직 설정되지 않았어요.': 'No feedback channel is configured yet.',
    '후원하기': 'Support the developer',
    '의견 보내기': 'Send feedback',
}


def T(text):
    """현재 언어(LANG)로 번역한다. 번역이 없으면 원문(한국어)을 그대로 쓴다."""
    return EN.get(text, text) if LANG == "en" else text


APP_NAME_KO = "띵동 리마인더"  # i18n:skip
APP_NAME = T(APP_NAME_KO)

# ------------------------------------------------------------------ app icon
#  알람시계 아이콘을 파일에 직접 내장한다(별도 .ico 파일 불필요).
ICON_ICO_B64 = (
    "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"
)
ICON_PNG_B64 = (
    "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"
    "gg=="
)


def ensure_icon_file():
    """내장 .ico를 임시 폴더에 풀어 경로를 반환한다(실패 시 None)."""
    if not (IS_WIN and ICON_ICO_B64):
        return None
    try:
        raw = base64.b64decode(ICON_ICO_B64)
        path = os.path.join(tempfile.gettempdir(), "ddingdong.ico")
        if not os.path.exists(path) or os.path.getsize(path) != len(raw):
            with open(path, "wb") as f:
                f.write(raw)
        return path
    except Exception:
        return None


def apply_app_icon(win):
    """창 좌측 상단·작업표시줄 아이콘을 내장 이미지로 교체한다."""
    done = False
    if IS_WIN and ICON_ICO_B64:
        try:
            path = ensure_icon_file()
            win.iconbitmap(default=path)
            done = True
        except Exception:
            done = False
    if ICON_PNG_B64:
        try:
            win._icon_img = tk.PhotoImage(data=ICON_PNG_B64)
            win.iconphoto(True, win._icon_img)
            done = True
        except Exception:
            pass
    return done

# ------------------------------------------------------------------ palette
# ── 색상 팔레트(밝은 테마: 차가운 중성 톤 + 선명한 블루 포인트 / 어두운 테마)
if DARK_MODE:
    TEXT = "#E8ECF4"
    SUB = "#9AA3B5"
    CANVAS = "#14171F"
    SOFT = "#1C202B"
    SURFACE2 = "#272C39"
    BORDER = "#2B3140"
    BLUE = "#4C8DFF"
    BLUE_DEEP = "#3A78EA"
    BLUE_SOFT = "#23324F"
    GREEN = "#34C38F"
    GREEN_DEEP = "#2BA877"
    GREEN_SOFT = "#1B3A31"
    ORANGE = "#F29A3B"
    ORANGE_SOFT = "#3D2E1B"
    RED = "#F26B70"
    DARK = "#0B0D12"
    GREY = "#6B7385"
else:
    TEXT = "#1B2130"
    SUB = "#6B7385"
    CANVAS = "#FFFFFF"
    SOFT = "#F5F7FD"
    SURFACE2 = "#E9EDF5"
    BORDER = "#E8ECF5"
    BLUE = "#3478F6"
    BLUE_DEEP = "#2563DE"
    BLUE_SOFT = "#E8F0FE"
    GREEN = "#1FA971"
    GREEN_DEEP = "#178A5B"
    GREEN_SOFT = "#E3F6EE"
    ORANGE = "#F08A24"
    ORANGE_SOFT = "#FEF0DF"
    RED = "#E5484D"
    DARK = "#111827"
    GREY = "#A8B0C0"

# 일정별로 고를 수 있는 포인트 색과 기호(BMP 문자만 — Tk 이모지 문제 방지)
COLOR_CHOICES = ["", "#3478F6", "#1FA971", "#8B5CF6", "#EC5C95", "#F08A24", "#E5484D", "#14B8C4"]
SYMBOL_CHOICES = ["", "★", "♥", "☀", "☕", "✔", "♪", "✿", "☎", "⚑", "✈"]
SNOOZE_CHOICES = [5, 10, 15, 30]

# (repeat 키, 그룹명, 설명, 색상 바)  ※ GROUPS 순서와 REPEAT_VALUES 순서는 반드시 일치
GROUPS = [
    ("daily", T("매일 반복"), T("주말 포함 매일"), "#1FA971"),
    ("weekday", T("평일 반복"), T("월요일~금요일"), "#3478F6"),
    ("weekly", T("매주 반복"), T("지정한 요일마다"), "#8B5CF6"),
    ("monthly", T("매월 반복"), T("지정한 일자마다"), "#EC5C95"),
    ("once", T("한 번만"), T("지정한 날짜에 1회"), "#F08A24"),
]

REPEAT_LABEL = {"daily": T("매일"), "weekday": T("평일"), "weekly": T("매주"),
                "monthly": T("매월"), "once": T("1회")}
REPEAT_VALUES = [T("매일"), T("평일(월~금)"), T("매주(요일 지정)"), T("매월(일자 지정)"), T("날짜 지정 1회")]
REPEAT_KEY = {T("매일"): "daily", T("평일(월~금)"): "weekday", T("매주(요일 지정)"): "weekly",
              T("매월(일자 지정)"): "monthly", T("날짜 지정 1회"): "once"}

WEEK_NAMES = [T("월"), T("화"), T("수"), T("목"), T("금"), T("토"), T("일")]
CATCHUP_MIN = 30       # 절전·부하로 건너뛴 알림을 소급 검사하는 최대 범위(분)
LAST_DAY = 32         # 매월 반복에서 '말일'을 뜻하는 내부 값

# --------------------------------------------------------- 공휴일 / 영업일 계산
#  아래는 기본 표이며, 앱의 '휴일' 탭에서 자유롭게 편집·추가할 수 있다.
#  (하계휴가 등 개인 휴무일을 넣으면 이월 계산에 함께 반영된다)
DEFAULT_HOLIDAYS = """\
# ── 2026년 공휴일 (대체공휴일 포함)
2026-01-01  신정
2026-02-16  설 연휴
2026-02-17  설날
2026-02-18  설 연휴
2026-03-01  삼일절
2026-03-02  삼일절 대체공휴일
2026-05-05  어린이날
2026-05-24  부처님오신날
2026-05-25  부처님오신날 대체공휴일
2026-06-06  현충일
2026-08-15  광복절
2026-08-17  광복절 대체공휴일
2026-09-24  추석 연휴
2026-09-25  추석
2026-09-26  추석 연휴
2026-09-28  추석 대체공휴일
2026-10-03  개천절
2026-10-05  개천절 대체공휴일
2026-10-09  한글날
2026-12-25  성탄절

# ── 2027년 (잠정 · 관보 확정 시 수정)
2027-01-01  신정
2027-02-05  설 연휴
2027-02-06  설날
2027-02-07  설 연휴
2027-02-08  설 대체공휴일
2027-02-09  설 대체공휴일
2027-03-01  삼일절
2027-05-05  어린이날
2027-05-13  부처님오신날
2027-06-06  현충일
2027-08-15  광복절
2027-08-16  광복절 대체공휴일
2027-09-14  추석 연휴
2027-09-15  추석
2027-09-16  추석 연휴
2027-10-03  개천절
2027-10-04  개천절 대체공휴일
2027-10-09  한글날
2027-10-11  한글날 대체공휴일
2027-12-25  성탄절
2027-12-27  성탄절 대체공휴일

# ── 개인 휴무일·휴가는 아래에 같은 형식으로 추가하세요.
# 2026-07-27  하계휴가
"""


def parse_holidays(text):
    """휴일 탭 텍스트 → date 집합. '#' 주석과 날짜 뒤 설명은 무시한다."""
    out = set()
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        token = line.replace(".", "-").replace("/", "-").split()[0].strip()
        try:
            out.add(datetime.strptime(token, "%Y-%m-%d").date())
        except Exception:
            continue
    return out


def is_business_day(d, holidays):
    return d.weekday() < 5 and d not in holidays


def next_business_day(d, holidays, limit=30):
    """d가 영업일이면 그대로, 아니면 그 이후 첫 영업일."""
    cur = d
    for _ in range(limit):
        if is_business_day(cur, holidays):
            return cur
        cur += timedelta(days=1)
    return cur


def base_match(item, d):
    """휴일 이월을 적용하기 전, 해당 날짜가 원래 예정일인지 판정."""
    rep = item.get("repeat", "daily")
    if rep == "daily":
        return True
    if rep == "weekday":
        return d.weekday() < 5
    if rep == "weekly":
        try:
            days = [int(x) for x in item.get("weekdays", [])]
        except Exception:
            days = []
        return d.weekday() in days
    if rep == "monthly":
        try:
            dom = int(item.get("dom", 1) or 1)
        except Exception:
            dom = 1
        last = calendar.monthrange(d.year, d.month)[1]
        if dom >= LAST_DAY or dom > last:   # '말일' 또는 그 달에 없는 날짜(2/31 등)
            return d.day == last
        return d.day == dom
    if rep == "once":
        return item.get("day") == d.strftime("%Y-%m-%d")
    return False


def should_fire(item, d, holidays):
    """오늘(d) 알림을 띄워야 하는지. 주말·공휴일 이월 옵션을 반영한다."""
    rep = item.get("repeat", "daily")
    if rep in ("daily", "weekday") or not item.get("shift"):
        return base_match(item, d)
    if not is_business_day(d, holidays):
        return False
    # 최근 15일 안에 '오늘로 이월된' 예정일이 있는지 역방향으로 확인
    for back in range(0, 15):
        b = d - timedelta(days=back)
        if base_match(item, b) and next_business_day(b, holidays) == d:
            return True
    return False


def next_fire_date(item, start, holidays, span=400):
    """start 이후 가장 빠른 알림 예정일(이월 반영). 목록 표시용."""
    if item.get("repeat") == "once":      # 먼 미래 날짜도 찾을 수 있도록 지정일부터 탐색
        try:
            base = datetime.strptime(item.get("day", ""), "%Y-%m-%d").date()
            if base > start:
                start = base
        except Exception:
            pass
    for k in range(0, span):
        d = start + timedelta(days=k)
        if should_fire(item, d, holidays):
            return d
    return None


def repeat_text(it):
    """목록 칩에 표시할 반복 문구."""
    rep = it.get("repeat", "daily")
    if rep == "weekly":
        try:
            wd = sorted(int(x) for x in it.get("weekdays", []))
        except Exception:
            wd = []
        if wd:
            return T("매주 ") + "·".join(WEEK_NAMES[i] for i in wd)
        return T("매주")
    if rep == "monthly":
        try:
            dom = int(it.get("dom", 1) or 1)
        except Exception:
            dom = 1
        return T("매월 말일") if dom >= LAST_DAY else T("매월 %d일") % dom
    if rep == "once":
        try:
            d = datetime.strptime(it.get("day", ""), "%Y-%m-%d").date()
        except Exception:
            return T("1회")
        today = datetime.now().date()
        if d == today:
            return T("오늘 1회")
        fmt = "%m/%d" if d.year == today.year else "%Y/%m/%d"
        return T("%s(%s) 1회") % (d.strftime(fmt), WEEK_NAMES[d.weekday()])
    return REPEAT_LABEL.get(rep, T("매일"))

# ------------------------------------------------------------------ fonts
#  한글 입력 중 글자가 굴림체로 크게 떴다 줄어드는 현상은
#  지정한 폰트명이 실제로 없어 Tk가 기본 폰트로 대체하기 때문이다.
#  설치된 폰트 목록을 직접 조회해 존재하는 이름을 고르고,
#  모든 위젯이 동일한 Font 객체를 공유하도록 한다.
FAM = "TkDefaultFont"
_FONTS = {}


def init_fonts():
    global FAM
    try:
        installed = set(tkfont.families())
    except Exception:
        installed = set()
    for cand in ("맑은 고딕", "Malgun Gothic", "나눔고딕", "NanumGothic",
                 "Noto Sans KR", "돋움", "Dotum", "Segoe UI"):
        if cand in installed:
            FAM = cand
            break
    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
        try:
            tkfont.nametofont(name).configure(family=FAM, size=10)
        except Exception:
            pass


def F(size=10, bold=False):
    key = (size, bold)
    if key not in _FONTS:
        _FONTS[key] = tkfont.Font(family=FAM, size=size,
                                  weight="bold" if bold else "normal")
    return _FONTS[key]


# ------------------------------------------------------------------ storage
def normalize_data(d):
    """저장 파일/가져온 파일에 빠진 항목을 기본값으로 채운다(이전 버전과 호환)."""
    if not isinstance(d, dict) or not isinstance(d.get("items", []), list):
        raise ValueError(T("올바른 데이터 파일이 아닙니다."))
    d.setdefault("items", [])
    d.setdefault("memo", "")
    d.setdefault("logs", [])
    d.setdefault("holidays", DEFAULT_HOLIDAYS)
    d.setdefault("fired", [])
    d.setdefault("snooze_min", 5)
    d.setdefault("sound", "beep")
    d.setdefault("quiet", {"on": False, "start": "22:00", "end": "07:00"})
    d.setdefault("theme", "system")
    d.setdefault("lang", "auto")
    return d


def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return normalize_data(json.load(f))
        except Exception:
            # 손상된 파일은 덮어써지기 전에 .bak으로 보존(기존 .bak이 있으면 시각을 붙임)
            try:
                bak = DATA_PATH + ".bak"
                if os.path.exists(bak):
                    bak = DATA_PATH + datetime.now().strftime(".%Y%m%d_%H%M%S.bak")
                os.replace(DATA_PATH, bak)
            except Exception:
                pass
    return normalize_data({
        "items": [
            {"id": "sample1", "time": "09:00", "title": T("하루 시작하기"),
             "memo": T("오늘 할 일을 확인하세요"), "repeat": "weekday", "day": ""},
        ],
        "memo": "",
        "logs": [],
        "holidays": DEFAULT_HOLIDAYS,
    })


def save_data(data):
    """저장 성공 여부를 반환한다(실패 시 (False, 사유))."""
    # 임시파일에 먼저 쓴 뒤 교체 → 쓰기 도중 종료돼도 기존 파일이 손상되지 않음
    tmp = DATA_PATH + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, DATA_PATH)
        return True, ""
    except Exception as exc:
        try:
            os.remove(tmp)
        except Exception:
            pass
        return False, str(exc)


# ------------------------------------------------------------------ monitors
class _MONITORINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("rcMonitor", ctypes.c_long * 4),
                ("rcWork", ctypes.c_long * 4),
                ("dwFlags", ctypes.c_ulong)]


def list_monitors():
    """연결된 모니터 목록을 [{x, y, w, h, primary}] 형태로 반환한다."""
    out = []
    if not IS_WIN:
        return out
    try:
        u = ctypes.windll.user32
        proc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
                                  ctypes.c_void_p, ctypes.c_ssize_t)

        def _cb(hmon, hdc, lprc, data):
            mi = _MONITORINFO()
            mi.cbSize = ctypes.sizeof(_MONITORINFO)
            if u.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                l, t, r, b = mi.rcMonitor
                out.append({"x": int(l), "y": int(t),
                            "w": int(r - l), "h": int(b - t),
                            "primary": bool(mi.dwFlags & 1)})
            return 1

        u.EnumDisplayMonitors(0, 0, proc(_cb), 0)
    except Exception:
        return []
    out.sort(key=lambda m: (not m["primary"], m["x"], m["y"]))
    return out


def monitor_labels():
    """드롭다운에 표시할 모니터 이름 목록."""
    mons = list_monitors()
    if not mons:
        return [T("주 모니터")]
    labels = []
    for i, m in enumerate(mons):
        kind = T("주 모니터") if m["primary"] else T("보조 모니터")
        labels.append("%d. %s (%dx%d)" % (i + 1, kind, m["w"], m["h"]))
    return labels


def pick_monitor(index):
    """index번 모니터 정보. 없으면 주 모니터, 그리고 그것도 없으면 None."""
    mons = list_monitors()
    if not mons:
        return None
    try:
        index = int(index)
    except Exception:
        index = 0
    if 0 <= index < len(mons):
        return mons[index]
    return mons[0]


# ------------------------------------------------------------------ win api
def force_front(win):
    try:
        win.deiconify()
        win.lift()
        win.attributes("-topmost", True)
        win.focus_force()
    except Exception:
        pass
    if not IS_WIN:
        return
    try:
        u = ctypes.windll.user32
        k = ctypes.windll.kernel32
        hwnd = u.GetParent(win.winfo_id()) or win.winfo_id()
        u.ShowWindow(hwnd, 9)                            # SW_RESTORE
        fg = u.GetForegroundWindow()
        tid_fg = u.GetWindowThreadProcessId(fg, None)
        tid_me = k.GetCurrentThreadId()
        u.AttachThreadInput(tid_fg, tid_me, True)
        u.BringWindowToTop(hwnd)
        u.SetForegroundWindow(hwnd)
        u.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0003)     # HWND_TOPMOST
        u.AttachThreadInput(tid_fg, tid_me, False)
        u.FlashWindow(hwnd, True)
    except Exception:
        pass


SOUND_MODE = "beep"            # beep(기본 비프) / chime(부드러운 알림음) / off(소리 끄기)


def beep(mode=None):
    mode = mode or SOUND_MODE
    if mode == "off":
        return
    try:
        if IS_WIN:
            if mode == "chime":
                winsound.MessageBeep(0x40)          # MB_ICONASTERISK: 시스템 알림음
            else:
                winsound.Beep(880, 220)
                winsound.Beep(660, 220)
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
    except Exception:
        pass


def in_quiet_hours(cfg, hhmm):
    """방해 금지 시간대(자정을 넘는 구간 포함)에 hhmm 이 속하는지."""
    try:
        if not cfg.get("on"):
            return False
        s, e = cfg.get("start", "22:00"), cfg.get("end", "07:00")
        if s == e:
            return False
        return (s <= hhmm < e) if s < e else (hhmm >= s or hhmm < e)
    except Exception:
        return False


# ------------------------------------------------------------------ 시작 프로그램 · 재시작
_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
_RUN_NAME = "Ddingdong"


def _launch_command():
    if getattr(sys, "frozen", False):
        return [sys.executable]
    exe = sys.executable
    pyw = os.path.join(os.path.dirname(exe), "pythonw.exe")
    return [pyw if os.path.exists(pyw) else exe, os.path.abspath(sys.argv[0])]


def autostart_enabled():
    if not IS_WIN:
        return False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY) as k:
            winreg.QueryValueEx(k, _RUN_NAME)
        return True
    except Exception:
        return False


def set_autostart(on):
    """Windows 시작 시 트레이로 자동 실행(HKCU Run 키). 성공 여부를 반환한다."""
    if not IS_WIN:
        return False
    try:
        import winreg
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _RUN_KEY) as k:
            if on:
                cmd = " ".join('"%s"' % p for p in _launch_command()) + " --minimized"
                winreg.SetValueEx(k, _RUN_NAME, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(k, _RUN_NAME)
                except FileNotFoundError:
                    pass
        return True
    except Exception:
        return False


def set_dark_titlebar(win):
    """어두운 테마일 때 창 제목 표시줄도 어둡게(Windows 10 20H1+ / 11)."""
    if not (IS_WIN and DARK_MODE):
        return
    try:
        win.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(win.winfo_id()) or win.winfo_id()
        val = ctypes.c_int(1)
        for attr in (20, 19):                      # DWMWA_USE_IMMERSIVE_DARK_MODE
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attr, ctypes.byref(val), ctypes.sizeof(val))
    except Exception:
        pass


# ------------------------------------------------------------------ IME
#  Tk는 조합 중인 한글(미확정 문자)를 직접 그리지 않고 Windows IME에 위임한다.
#  IME는 아무 정보가 없으면 시스템 기본값(굴림체 · 큰 글씨)으로 그리기 때문에
#  입력 중에만 폰트가 틀어졌다가 확정 순간 원래 폰트로 바뀌는 현상이 생긴다.
#  IMM32 API로 조합창의 폰트와 위치를 직접 지정해 이를 없앨다.
CFS_POINT = 0x0002
HANGEUL_CHARSET = 129
CLEARTYPE_QUALITY = 5

if IS_WIN:

    class _LOGFONTW(ctypes.Structure):
        _fields_ = [("lfHeight", ctypes.c_long), ("lfWidth", ctypes.c_long),
                    ("lfEscapement", ctypes.c_long), ("lfOrientation", ctypes.c_long),
                    ("lfWeight", ctypes.c_long), ("lfItalic", ctypes.c_byte),
                    ("lfUnderline", ctypes.c_byte), ("lfStrikeOut", ctypes.c_byte),
                    ("lfCharSet", ctypes.c_byte), ("lfOutPrecision", ctypes.c_byte),
                    ("lfClipPrecision", ctypes.c_byte), ("lfQuality", ctypes.c_byte),
                    ("lfPitchAndFamily", ctypes.c_byte),
                    ("lfFaceName", ctypes.c_wchar * 32)]

    class _POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    class _RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                    ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    class _COMPOSITIONFORM(ctypes.Structure):
        _fields_ = [("dwStyle", ctypes.c_uint), ("ptCurrentPos", _POINT),
                    ("rcArea", _RECT)]


def tune_ime(widget, font, lx=2, ly=0):
    """조합 중인 한글이 위젯과 동일한 폰트·크기로, 커서 위치에 보이도록 IME에 알린다."""
    if not IS_WIN:
        return
    try:
        imm = ctypes.windll.imm32
        size = abs(int(font.actual("size")))
        px = int(round(size * float(widget.winfo_fpixels("1p"))))
        lf = _LOGFONTW()
        lf.lfHeight = -abs(px) or -14
        lf.lfWeight = 700 if font.actual("weight") == "bold" else 400
        lf.lfCharSet = HANGEUL_CHARSET
        lf.lfQuality = CLEARTYPE_QUALITY
        lf.lfFaceName = FAM[:31]

        own = widget.winfo_id()
        top_w = widget.winfo_toplevel()
        top = top_w.winfo_id()
        dx = widget.winfo_rootx() - top_w.winfo_rootx()
        dy = widget.winfo_rooty() - top_w.winfo_rooty()
        targets = [(own, lx, ly), (top, lx + dx, ly + dy)]
        try:
            parent = ctypes.windll.user32.GetParent(top)
            if parent:
                targets.append((parent, lx + dx, ly + dy))
        except Exception:
            pass

        for hwnd, cx, cy in targets:
            if not hwnd:
                continue
            himc = imm.ImmGetContext(hwnd)
            if not himc:
                continue
            cf = _COMPOSITIONFORM()
            cf.dwStyle = CFS_POINT
            cf.ptCurrentPos.x = int(cx)
            cf.ptCurrentPos.y = int(cy)
            imm.ImmSetCompositionFontW(himc, ctypes.byref(lf))
            imm.ImmSetCompositionWindow(himc, ctypes.byref(cf))
            imm.ImmReleaseContext(hwnd, himc)
    except Exception:
        pass


# ------------------------------------------------------------------ widgets
def round_points(x1, y1, x2, y2, r):
    return [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]


class RoundBox(tk.Canvas):
    """둥근 모서리 카드 배경. 내부 위젯은 self.body 에 배치한다."""

    def __init__(self, parent, bg=CANVAS, border=BORDER, radius=20,
                 page_bg=CANVAS, pad=1, **kw):
        super().__init__(parent, bg=page_bg, highlightthickness=0, bd=0, **kw)
        self.bg, self.border, self.radius, self.pad = bg, border, radius, pad
        self._shape = None
        self.body = tk.Frame(self, bg=bg)
        self.bind("<Configure>", self._draw)

    def _draw(self, _e=None):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4 or h < 4:
            return
        if self._shape:
            self.delete(self._shape)
        self._shape = self.create_polygon(
            round_points(1, 1, w - 2, h - 2, self.radius),
            smooth=True, splinesteps=24, fill=self.bg,
            outline=self.border if self.border else self.bg)
        self.tag_lower(self._shape)
        self.body.place(x=self.pad + 1, y=self.pad + 1,
                        width=w - 2 * self.pad - 3, height=h - 2 * self.pad - 3)


class Pill(tk.Canvas):
    """둥근 버튼 / 태그 칩."""

    def __init__(self, parent, text, command=None, fg=TEXT, bg=CANVAS,
                 border=BORDER, hover=SOFT, page_bg=CANVAS, size=10,
                 bold=False, padx=16, height=38, radius=None, min_width=0):
        f = F(size, bold)
        w = max(min_width, f.measure(text) + padx * 2)
        if radius is None:                    # 기본은 완전히 둥근 알약 모양
            radius = height // 2
        super().__init__(parent, width=w, height=height, bg=page_bg,
                         highlightthickness=0, bd=0)
        self.command, self.bg, self.hover, self.border = command, bg, hover, border
        self._shape = self.create_polygon(
            round_points(1, 1, w - 1, height - 1, radius), smooth=True,
            splinesteps=24, fill=bg, outline=border if border else bg)
        self._text = self.create_text(w / 2, height / 2 + 1, text=text, fill=fg, font=f)
        if command:
            self.configure(cursor="hand2")
            self.bind("<Button-1>", lambda e: command())
            self.bind("<Enter>", lambda e: self.itemconfig(self._shape, fill=self.hover))
            self.bind("<Leave>", lambda e: self.itemconfig(self._shape, fill=self.bg))

    def restyle(self, fg, bg, hover=None):
        """탭처럼 선택 상태에 따라 색을 바꾸는 용도."""
        self.bg = bg
        if hover:
            self.hover = hover
        self.itemconfig(self._shape, fill=bg, outline=bg)
        self.itemconfig(self._text, fill=fg)


def tint(color, amount=0.86):
    """색을 흰색 쪽으로 섞어 부드러운 파스텔 톤을 만든다."""
    c = color.lstrip("#")
    rgb = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    b = CANVAS.lstrip("#")                    # 밝은 테마는 흰색, 어두운 테마는 배경색 쪽으로 섞는다
    base = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(int(v + (t - v) * amount) for v, t in zip(rgb, base))


class Card(tk.Canvas):
    """내용 높이에 맞춰 자라는 둥근 카드(목록 행용). 내용은 self.body 에 배치한다."""

    def __init__(self, parent, bg=SOFT, page_bg=CANVAS, radius=18, border=None):
        super().__init__(parent, bg=page_bg, highlightthickness=0, bd=0, height=10)
        self.fill, self.edge, self.r = bg, border, radius
        self.inset = int(radius * 0.3) + 2        # 모서리 바깥으로 내용이 삐져나오지 않게
        self.body = tk.Frame(self, bg=bg)
        self._win = self.create_window(self.inset, self.inset, window=self.body,
                                       anchor="nw")
        self._shape = None
        self.bind("<Configure>", self._draw)
        self.body.bind("<Configure>", self._fit)

    def _fit(self, e):
        self.configure(height=e.height + self.inset * 2)

    def _draw(self, e):
        w, h = e.width, e.height
        if w < 4 or h < 4:
            return
        if self._shape:
            self.delete(self._shape)
        self._shape = self.create_polygon(
            round_points(1, 1, w - 2, h - 2, self.r), smooth=True, splinesteps=24,
            fill=self.fill, outline=self.edge or self.fill)
        self.tag_lower(self._shape)
        self.itemconfig(self._win, width=max(1, w - self.inset * 2))


class TimeField(tk.Canvas):
    """Canvas로 직접 그린 시각 입력기. Windows 기본 Spinbox를 쓰지 않는다.

    - 시 / 분 세그먼트 클릭 선택, 마우스 휠로 증감
    - 오른쪽 쉐브론 ▲ / ▼ 로 증감, 숫자 타이핑 지원
    """

    W, H = 168, 46

    def __init__(self, parent, page_bg=SOFT, hh=17, mm=0):
        super().__init__(parent, width=self.W, height=self.H, bg=page_bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.hh, self.mm, self.sel, self.buf = hh, mm, "h", ""
        self.create_polygon(round_points(1, 1, self.W - 1, self.H - 1, 16),
                            smooth=True, splinesteps=24, fill=CANVAS, outline=BORDER)

        self.hx = (10, 7, 62, self.H - 7)
        self.mx = (74, 7, 126, self.H - 7)
        self.box_h = self.create_polygon(round_points(*self.hx, r=11), smooth=True,
                                         splinesteps=18, fill=CANVAS, outline="")
        self.box_m = self.create_polygon(round_points(*self.mx, r=11), smooth=True,
                                         splinesteps=18, fill=CANVAS, outline="")
        self.t_h = self.create_text(36, self.H / 2, text="00", font=F(16, True), fill=TEXT)
        self.create_text(68, self.H / 2 - 1, text=":", font=F(14, True), fill=GREY)
        self.t_m = self.create_text(100, self.H / 2, text="00", font=F(16, True), fill=TEXT)

        self.create_line(133, 6, 133, self.H - 6, fill=BORDER)
        self.up = self.create_line(143, 19, 149, 13, 155, 19, fill=SUB, width=2,
                                   capstyle="round", joinstyle="round")
        self.dn = self.create_line(143, 27, 149, 33, 155, 27, fill=SUB, width=2,
                                   capstyle="round", joinstyle="round")

        self.on_change = None
        self.bind("<Button-1>", self._click)
        self.bind("<MouseWheel>", lambda e: self._step(1 if e.delta > 0 else -1))
        self.bind("<Key>", self._key)
        self.bind("<FocusOut>", lambda e: self._render())
        for item in (self.up, self.dn):
            self.tag_bind(item, "<Enter>", lambda e, i=item: self.itemconfig(i, fill=BLUE))
            self.tag_bind(item, "<Leave>", lambda e, i=item: self.itemconfig(i, fill=SUB))
        self._render()

    def _render(self):
        self.itemconfig(self.t_h, text="%02d" % self.hh)
        self.itemconfig(self.t_m, text="%02d" % self.mm)
        on_h = self.sel == "h"
        self.itemconfig(self.box_h, fill=BLUE_SOFT if on_h else CANVAS)
        self.itemconfig(self.box_m, fill=CANVAS if on_h else BLUE_SOFT)
        self.itemconfig(self.t_h, fill=BLUE if on_h else TEXT)
        self.itemconfig(self.t_m, fill=TEXT if on_h else BLUE)

    def _click(self, e):
        self.focus_set()
        self.buf = ""
        if e.x >= 136:
            self._step(1 if e.y < self.H / 2 else -1)
            return
        self.sel = "h" if e.x < 68 else "m"
        self._render()

    def _step(self, d):
        if self.sel == "h":
            self.hh = (self.hh + d) % 24
        else:
            self.mm = (self.mm + d) % 60
        self.buf = ""
        self._render()
        self._notify()

    def _notify(self):
        if self.on_change:
            try:
                self.on_change()
            except Exception:
                pass

    def _key(self, e):
        if e.keysym in ("Up", "Right") and e.keysym == "Up":
            return self._step(1)
        if e.keysym == "Down":
            return self._step(-1)
        if e.keysym in ("Left", "Right", "Tab"):
            self.sel = "h" if e.keysym == "Left" else "m"
            self.buf = ""
            return self._render()
        if not e.char.isdigit():
            return
        self.buf = (self.buf + e.char)[-2:]
        v = int(self.buf)
        if self.sel == "h":
            self.hh = v if v <= 23 else int(e.char)
            if len(self.buf) == 2 or self.hh > 2:
                self.sel, self.buf = "m", ""
        else:
            self.mm = v if v <= 59 else int(e.char)
            if len(self.buf) == 2:
                self.buf = ""
        self._render()
        self._notify()

    def get(self):
        return "%02d:%02d" % (self.hh, self.mm)

    def set(self, hh, mm):
        self.hh, self.mm, self.buf = int(hh) % 24, int(mm) % 60, ""
        self._render()


class ToggleChip(tk.Canvas):
    """켜짐/꺼짐 상태를 가지는 둥근 칩. Windows 기본 Checkbutton을 대체한다."""

    def __init__(self, parent, text, page_bg=SOFT, on=False, padx=12,
                 height=34, radius=17, command=None, min_width=0):
        f = F(9, True)
        w = max(min_width, f.measure(text) + padx * 2)
        super().__init__(parent, width=w, height=height, bg=page_bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.on, self.command = bool(on), command
        self._shape = self.create_polygon(
            round_points(1, 1, w - 1, height - 1, radius), smooth=True,
            splinesteps=24, fill=CANVAS, outline=BORDER)
        self._text = self.create_text(w / 2, height / 2 + 1, text=text,
                                      fill=SUB, font=f)
        self.bind("<Button-1>", lambda e: self.toggle())
        self._render()

    def _render(self):
        self.itemconfig(self._shape, fill=BLUE_SOFT if self.on else CANVAS,
                        outline=BLUE if self.on else BORDER)
        self.itemconfig(self._text, fill=BLUE if self.on else SUB)

    def toggle(self):
        self.set(not self.on)
        if self.command:
            self.command(self.on)

    def set(self, on):
        self.on = bool(on)
        self._render()

    def get(self):
        return self.on


class DayField(tk.Canvas):
    """1~31일 + '말일' 선택기. TimeField와 동일한 조작감을 유지한다."""

    W, H = 128, 46

    def __init__(self, parent, page_bg=SOFT, value=1):
        super().__init__(parent, width=self.W, height=self.H, bg=page_bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.value, self.buf = int(value), ""
        self.create_polygon(round_points(1, 1, self.W - 1, self.H - 1, 16),
                            smooth=True, splinesteps=24, fill=CANVAS, outline=BORDER)
        self.box = self.create_polygon(round_points(10, 7, 92, self.H - 7, r=11),
                                       smooth=True, splinesteps=18,
                                       fill=BLUE_SOFT, outline="")
        self.t = self.create_text(51, self.H / 2, text=T("1일"), font=F(14, True),
                                  fill=BLUE)
        self.create_line(99, 6, 99, self.H - 6, fill=BORDER)
        self.up = self.create_line(107, 19, 113, 13, 119, 19, fill=SUB, width=2,
                                   capstyle="round", joinstyle="round")
        self.dn = self.create_line(107, 27, 113, 33, 119, 27, fill=SUB, width=2,
                                   capstyle="round", joinstyle="round")
        self.bind("<Button-1>", self._click)
        self.bind("<MouseWheel>", lambda e: self._step(1 if e.delta > 0 else -1))
        self.bind("<Key>", self._key)
        for item in (self.up, self.dn):
            self.tag_bind(item, "<Enter>", lambda e, i=item: self.itemconfig(i, fill=BLUE))
            self.tag_bind(item, "<Leave>", lambda e, i=item: self.itemconfig(i, fill=SUB))
        self._render()

    def _render(self):
        self.itemconfig(self.t, text=T("말일") if self.value >= LAST_DAY
                        else T("%d일") % self.value)

    def _click(self, e):
        self.focus_set()
        self.buf = ""
        if e.x >= 100:
            self._step(1 if e.y < self.H / 2 else -1)

    def _step(self, d):
        self.value = (self.value - 1 + d) % LAST_DAY + 1
        self.buf = ""
        self._render()

    def _key(self, e):
        if e.keysym in ("Up", "Right"):
            return self._step(1)
        if e.keysym in ("Down", "Left"):
            return self._step(-1)
        if not e.char.isdigit():
            return
        self.buf = (self.buf + e.char)[-2:]
        v = int(self.buf)
        if 1 <= v <= 31:
            self.value = v
        else:
            self.value = max(1, int(e.char))
            self.buf = e.char
        self._render()

    def get(self):
        return self.value

    def set(self, v):
        try:
            v = int(v)
        except Exception:
            v = 1
        self.value = min(max(v, 1), LAST_DAY)
        self.buf = ""
        self._render()


class CalendarPopup(tk.Toplevel):
    """날짜 선택 달력. 앵커 위젯 아래에 뜨며 날짜를 고르면 on_pick(date) 호출 후 닫힌다."""

    def __init__(self, anchor, current, on_pick, on_close):
        super().__init__(anchor)
        self.sel, self.on_pick, self.on_close = current, on_pick, on_close
        self.view = current.replace(day=1)
        self.overrideredirect(True)
        self.configure(bg=BORDER)
        self.attributes("-topmost", True)
        self.wrap = tk.Frame(self, bg=CANVAS)
        self.wrap.pack(padx=1, pady=1)
        self._draw()
        self.update_idletasks()
        x, y = anchor.winfo_rootx(), anchor.winfo_rooty() + anchor.winfo_height() + 4
        if y + self.winfo_reqheight() > self.winfo_screenheight():     # 아래 공간이 없으면 위로
            y = anchor.winfo_rooty() - self.winfo_reqheight() - 4
        self.geometry("+%d+%d" % (x, max(0, y)))
        self.bind("<Button-1>", self._outside)
        self.bind("<Escape>", lambda e: self.on_close())
        self.grab_set()
        self.focus_set()

    def _outside(self, e):
        if e.widget is self:                  # 달력 밖 클릭은 grab 창으로 전달된다
            self.on_close()

    def dispose(self):
        try:
            self.grab_release()
            self.destroy()
        except Exception:
            pass

    def _shift_month(self, delta):
        m = self.view.year * 12 + self.view.month - 1 + delta
        self.view = self.view.replace(year=m // 12, month=m % 12 + 1)
        self._draw()

    def _btn(self, parent, text, cmd, **kw):
        lb = tk.Label(parent, text=text, bg=kw.pop("bg", CANVAS), fg=kw.pop("fg", TEXT),
                      cursor="hand2", **kw)
        lb.bind("<Button-1>", lambda e: cmd())
        return lb

    def _draw(self):
        for w in self.wrap.winfo_children():
            w.destroy()
        today = datetime.now().date()
        head = tk.Frame(self.wrap, bg=CANVAS)
        head.pack(fill="x", padx=10, pady=(10, 4))
        self._btn(head, "‹", lambda: self._shift_month(-1), font=F(14, True),
                  padx=10).pack(side="left")
        self._btn(head, "›", lambda: self._shift_month(1), font=F(14, True),
                  padx=10).pack(side="right")
        tk.Label(head, text=T("%d년 %d월") % (self.view.year, self.view.month), bg=CANVAS,
                 fg=TEXT, font=F(11, True)).pack(expand=True)

        grid = tk.Frame(self.wrap, bg=CANVAS)
        grid.pack(padx=10)
        for c, nm in enumerate(WEEK_NAMES):
            tk.Label(grid, text=nm, width=4, bg=CANVAS, font=F(9, True), pady=4,
                     fg=BLUE if c == 5 else RED if c == 6 else SUB).grid(row=0, column=c)
        weeks = calendar.Calendar(0).monthdatescalendar(self.view.year, self.view.month)
        for r, week in enumerate(weeks, start=1):
            for c, d in enumerate(week):
                is_sel, is_today = d == self.sel, d == today
                other = d.month != self.view.month
                bg = BLUE if is_sel else CANVAS
                fg = ("white" if is_sel else GREY if other or d < today
                      else BLUE if is_today else TEXT)
                cell = tk.Label(grid, text=str(d.day), width=4, pady=5, bg=bg, fg=fg,
                                font=F(10, is_sel or is_today), cursor="hand2")
                cell.grid(row=r, column=c, pady=1)
                cell.bind("<Button-1>", lambda e, dd=d: self.on_pick(dd))
                if not is_sel:
                    cell.bind("<Enter>", lambda e, w=cell: w.config(bg=BLUE_SOFT))
                    cell.bind("<Leave>", lambda e, w=cell: w.config(bg=CANVAS))

        foot = tk.Frame(self.wrap, bg=CANVAS)
        foot.pack(fill="x", padx=10, pady=(6, 10))
        self._btn(foot, T("오늘"), lambda: self.on_pick(today), font=F(9, True),
                  fg=BLUE, padx=12, pady=5).pack(side="left")
        self._btn(foot, T("닫기"), self.on_close, font=F(9), fg=SUB, padx=12,
                  pady=5).pack(side="right")


class DateField(tk.Canvas):
    """연-월-일 선택기. 구간을 클릭해 고른 뒤 ▲▼·휠·방향키로 바꾼다."""

    W, H = 240, 46
    SEGS = ((12, 64), (76, 108), (120, 152))      # 연, 월, 일 클릭 영역

    def __init__(self, parent, page_bg=SOFT, value=None):
        super().__init__(parent, width=self.W, height=self.H, bg=page_bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.date = datetime.now().date()
        self.seg = 2
        self.create_polygon(round_points(1, 1, self.W - 1, self.H - 1, 16),
                            smooth=True, splinesteps=24, fill=CANVAS, outline=BORDER)
        self.box = self.create_polygon(round_points(120, 7, 152, self.H - 7, r=11),
                                       smooth=True, splinesteps=18,
                                       fill=BLUE_SOFT, outline="")
        mid = self.H / 2
        self.t = [self.create_text(38, mid, font=F(14, True), fill=BLUE),
                  self.create_text(92, mid, font=F(14, True), fill=BLUE),
                  self.create_text(136, mid, font=F(14, True), fill=BLUE)]
        self.create_text(70, mid, text="-", font=F(14, True), fill=SUB)
        self.create_text(114, mid, text="-", font=F(14, True), fill=SUB)
        self.t_wk = self.create_text(180, mid, font=F(10), fill=SUB)
        self.create_line(205, 6, 205, self.H - 6, fill=BORDER)
        self.up = self.create_line(215, 19, 221, 13, 227, 19, fill=SUB, width=2,
                                   capstyle="round", joinstyle="round")
        self.dn = self.create_line(215, 27, 221, 33, 227, 27, fill=SUB, width=2,
                                   capstyle="round", joinstyle="round")
        self.pop = None
        self.bind("<Button-1>", self._click)
        self.bind("<MouseWheel>", self._wheel)
        self.bind("<Key>", self._key)
        for item in (self.up, self.dn):
            self.tag_bind(item, "<Enter>", lambda e, i=item: self.itemconfig(i, fill=BLUE))
            self.tag_bind(item, "<Leave>", lambda e, i=item: self.itemconfig(i, fill=SUB))
        if value:
            self.set(value)
        else:
            self._render()

    def _render(self):
        d = self.date
        self.itemconfig(self.t[0], text="%04d" % d.year)
        self.itemconfig(self.t[1], text="%02d" % d.month)
        self.itemconfig(self.t[2], text="%02d" % d.day)
        self.itemconfig(self.t_wk, text="(%s)" % WEEK_NAMES[d.weekday()])
        x0, x1 = self.SEGS[self.seg]
        self.coords(self.box, *round_points(x0, 7, x1, self.H - 7, r=11))

    def _seg_at(self, x):
        for i, (a, b) in enumerate(self.SEGS):
            if a - 6 <= x <= b + 4:
                return i
        return None

    def _click(self, e):
        self.focus_set()
        if e.x >= 206:                        # ▲▼ 로 현재 구간 증감
            return self._step(1 if e.y < self.H / 2 else -1)
        i = self._seg_at(e.x)
        if i is not None:
            self.seg = i
        self._render()
        self._toggle_calendar()               # 날짜 영역 클릭 → 달력 팝업

    def _wheel(self, e):
        i = self._seg_at(e.x)                 # 휠은 마우스가 올려진 구간(연/월/일)을 증감
        if i is not None:
            self.seg = i
        self._step(1 if e.delta > 0 else -1)

    def _toggle_calendar(self):
        if self.pop is not None:
            return self._close_calendar()
        self.pop = CalendarPopup(self, self.date, self._cal_pick, self._close_calendar)

    def _close_calendar(self):
        if self.pop is not None:
            pop, self.pop = self.pop, None
            pop.dispose()

    def _cal_pick(self, d):
        self.date = d
        self._close_calendar()
        self._render()

    def _step(self, delta):
        d = self.date
        try:
            if self.seg == 2:
                d = d + timedelta(days=delta)
            else:
                months = d.year * 12 + d.month - 1 + delta * (12 if self.seg == 0 else 1)
                y, m = months // 12, months % 12 + 1
                d = d.replace(year=y, month=m,
                              day=min(d.day, calendar.monthrange(y, m)[1]))
        except Exception:
            return
        self.date = d
        self._render()

    def _key(self, e):
        if e.keysym == "Up":
            return self._step(1)
        if e.keysym == "Down":
            return self._step(-1)
        if e.keysym in ("Left", "Right"):
            self.seg = (self.seg + (1 if e.keysym == "Right" else -1)) % 3
            self._render()

    def get(self):
        return self.date.strftime("%Y-%m-%d")

    def set(self, v):
        try:
            self.date = (v if hasattr(v, "year")
                         else datetime.strptime(str(v), "%Y-%m-%d").date())
        except Exception:
            self.date = datetime.now().date()
        self._render()


class ChoiceStrip(tk.Canvas):
    """색 점(kind='color') 또는 기호(kind='symbol') 중 하나를 고르는 가로 선택기.
    values 의 '' 는 '없음'을 뜻한다."""

    def __init__(self, parent, values, kind, page_bg=SOFT, size=32, gap=6, on_change=None):
        self.values, self.kind, self.size, self.gap = list(values), kind, size, gap
        self.value, self.on_change = self.values[0], on_change
        w = len(self.values) * (size + gap) - gap + 4
        super().__init__(parent, width=w, height=size + 4, bg=page_bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.bind("<Button-1>", self._click)
        self._draw()

    def _draw(self):
        self.delete("all")
        for i, v in enumerate(self.values):
            x0 = 2 + i * (self.size + self.gap)
            x1, y0, y1 = x0 + self.size, 2, 2 + self.size
            on = (v == self.value)
            if self.kind == "color":
                if v:
                    self.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=v, outline=v)
                else:
                    self.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, outline=GREY, width=2)
                    self.create_line(x0 + 10, y1 - 10, x1 - 10, y0 + 10, fill=GREY, width=2)
            else:
                self.create_text((x0 + x1) / 2, (y0 + y1) / 2 + 1, text=v or "–",
                                 font=F(13), fill=TEXT if v else GREY)
            if on:
                self.create_oval(x0, y0, x1, y1, outline=BLUE, width=2)

    def _click(self, e):
        i = (e.x - 2) // (self.size + self.gap)
        if 0 <= i < len(self.values):
            self.set(self.values[i])
            if self.on_change:
                self.on_change(self.value)

    def get(self):
        return self.value

    def set(self, v):
        self.value = v if v in self.values else self.values[0]
        self._draw()


class Dropdown(tk.Canvas):
    """커스텀 둥근 드롭다운. tk.OptionMenu의 사각 버튼을 대체한다."""

    def __init__(self, parent, values, value=None, page_bg=SOFT, width=150,
                 height=46, on_change=None):
        super().__init__(parent, width=width, height=height, bg=page_bg,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.values = list(values)
        self.on_change = on_change
        self.value = value or self.values[0]
        self.w, self.h, self.top = width, height, None
        self._shape = self.create_polygon(
            round_points(1, 1, width - 1, height - 1, 16), smooth=True,
            splinesteps=24, fill=CANVAS, outline=BORDER)
        self.t = self.create_text(15, height / 2, text=self.value, anchor="w",
                                  font=F(10), fill=TEXT)
        cx, cy = width - 20, height / 2 - 1
        self.chev = self.create_line(cx - 5, cy - 2, cx, cy + 3, cx + 5, cy - 2,
                                     fill=SUB, width=2, capstyle="round",
                                     joinstyle="round")
        self.bind("<Button-1>", lambda e: self._toggle())
        self.bind("<Enter>", lambda e: self.itemconfig(self._shape, fill=SOFT))
        self.bind("<Leave>", lambda e: self.itemconfig(self._shape, fill=CANVAS))

    def get(self):
        return self.value

    def set(self, val):
        if val in self.values:
            self.value = val
            self.itemconfig(self.t, text=val)

    def _toggle(self):
        if self.top is not None:
            return self._close()
        self.itemconfig(self.chev, fill=BLUE)
        t = tk.Toplevel(self)
        self.top = t
        t.overrideredirect(True)
        t.configure(bg=BORDER)
        t.attributes("-topmost", True)
        wrap = tk.Frame(t, bg=CANVAS)
        wrap.pack(padx=1, pady=1)
        for v in self.values:
            row = tk.Label(wrap, text=v, font=F(10), bg=CANVAS,
                           fg=BLUE if v == self.value else TEXT, anchor="w",
                           padx=14, pady=9, width=max(10, self.w // 9),
                           cursor="hand2")
            row.pack(fill="x")
            row.bind("<Enter>", lambda e, r=row: r.config(bg=BLUE_SOFT))
            row.bind("<Leave>", lambda e, r=row: r.config(bg=CANVAS))
            row.bind("<Button-1>", lambda e, val=v: self._pick(val))
        t.update_idletasks()
        t.geometry("+%d+%d" % (self.winfo_rootx(), self.winfo_rooty() + self.h + 4))
        t.bind("<Button-1>", self._maybe_close)
        t.bind("<Escape>", lambda e: self._close())
        t.grab_set()

    def _maybe_close(self, e):
        if e.widget is self.top:
            self._close()

    def _pick(self, val):
        self.value = val
        self.itemconfig(self.t, text=val)
        self._close()
        if self.on_change:
            try:
                self.on_change(val)
            except Exception:
                pass

    def _close(self):
        if self.top is not None:
            try:
                self.top.grab_release()
                self.top.destroy()
            except Exception:
                pass
            self.top = None
        self.itemconfig(self.chev, fill=SUB)


class SlimScrollbar(tk.Canvas):
    """얇은 둥근 스크롤바. Windows 기본 Scrollbar는 색을 바꿀 수 없어(어두운 테마에서 튐) 직접 그린다."""

    def __init__(self, parent, command, bg=CANVAS):
        super().__init__(parent, width=10, bg=bg, highlightthickness=0, bd=0)
        self.command, self.lo, self.hi, self.grab = command, 0.0, 1.0, None
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Button-1>", self._press)
        self.bind("<B1-Motion>", self._move)
        self.bind("<ButtonRelease-1>", lambda e: setattr(self, "grab", None))

    def set(self, lo, hi):                     # yscrollcommand 규약
        self.lo, self.hi = float(lo), float(hi)
        self._draw()

    def _draw(self):
        self.delete("all")
        h = self.winfo_height()
        if h < 8 or self.hi - self.lo >= 0.999:
            return
        y0, y1 = self.lo * h + 2, max(self.hi * h - 2, self.lo * h + 24)
        self.create_polygon(round_points(2, y0, 8, y1, 3), smooth=True, splinesteps=12,
                            fill=GREY, outline=GREY)

    def _press(self, e):
        h = max(1, self.winfo_height())
        if self.lo * h <= e.y <= self.hi * h:
            self.grab = e.y - self.lo * h      # 썸 안쪽을 잡은 위치
        else:                                  # 빈 곳 클릭: 한 페이지씩 이동
            self.command("scroll", -1 if e.y < self.lo * h else 1, "pages")

    def _move(self, e):
        if self.grab is not None:
            h = max(1, self.winfo_height())
            self.command("moveto", min(max((e.y - self.grab) / h, 0.0), 1.0))


class ScrollArea(tk.Frame):
    """세로 스크롤 영역. 내부 위젯은 self.inner 에 pack 한다."""

    def __init__(self, parent, bg=CANVAS):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.sb = SlimScrollbar(self, self.canvas.yview, bg=bg)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.sb.pack(side="right", fill="y")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self._win, width=e.width))
        for w in (self, self.canvas, self.inner, self.sb):
            self._bind_wheel(w)
        self.bind("<Enter>", self._enter, add="+")
        self.bind("<Leave>", self._leave, add="+")

    # -------------------------------------------------- 마우스 휠 스크롤
    def _bind_wheel(self, w):
        w.bind("<MouseWheel>", self._wheel, add="+")
        w.bind("<Button-4>", self._wheel_x11, add="+")
        w.bind("<Button-5>", self._wheel_x11, add="+")
        w._wheel_bound = True

    def sync_wheel(self):
        """목록을 다시 그린 뒤 호출. 새로 생긴 모든 하위 위젯(행·라벨·칩)에
        휠 이벤트를 연결한다. Tk는 커서 바로 아래 위젯에만 휠을 전달하므로
        그룹 헤더나 행 위에서도 스크롤되려면 모두 바인드해야 한다."""
        stack = [self.inner]
        while stack:
            w = stack.pop()
            if not getattr(w, "_wheel_bound", False):
                self._bind_wheel(w)
            stack.extend(w.winfo_children())

    def _enter(self, _e=None):
        for seq, fn in (("<MouseWheel>", self._wheel),
                        ("<Button-4>", self._wheel_x11),
                        ("<Button-5>", self._wheel_x11)):
            self.bind_all(seq, fn, add="+")

    def _leave(self, _e=None):
        try:
            w = self.winfo_containing(*self.winfo_pointerxy())
        except Exception:
            w = None
        while w is not None:                      # 내부 자식으로 이동한 경우는 유지
            if w is self:
                return
            w = getattr(w, "master", None)
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            try:
                self.unbind_all(seq)
            except Exception:
                pass

    def _scroll(self, units):
        try:
            first, last = self.canvas.yview()
        except Exception:
            return
        if first <= 0.0 and last >= 1.0:          # 스크롤할 내용이 없음
            return
        self.canvas.yview_scroll(units, "units")

    def _wheel(self, e):
        delta = int(-1 * (e.delta / 120)) or (-1 if e.delta > 0 else 1)
        self._scroll(delta * 3)
        return "break"

    def _wheel_x11(self, e):
        self._scroll(-3 if getattr(e, "num", 5) == 4 else 3)
        return "break"


# ------------------------------------------------------------------ alarm
class AlarmWindow(tk.Toplevel):
    def __init__(self, master, item, on_close):
        super().__init__(master)
        self.item, self.on_close = item, on_close
        self.beeping, self.raise_count = True, 0

        self.title("REMINDER")
        self.configure(bg=DARK)
        self.attributes("-topmost", True)

        # ── 표시할 모니터 결정 (주/보조)
        idx = 0
        try:
            idx = master.alarm_monitor_index()
        except Exception:
            idx = 0
        try:
            snooze_min = master.snooze_minutes()
        except Exception:
            snooze_min = 5
        mon = pick_monitor(idx)
        if mon:
            self.geometry("%dx%d+%d+%d" % (mon["w"], mon["h"], mon["x"], mon["y"]))
            self.update_idletasks()
        try:
            self.attributes("-fullscreen", True)
        except Exception:
            self.state("zoomed")
        if mon:
            self.after(80, lambda m=mon: self._ensure_monitor(m))
        self.protocol("WM_DELETE_WINDOW", self.finish_ok)
        self.bind("<Escape>", lambda e: self.finish_ok())

        box = tk.Frame(self, bg=DARK)
        box.place(relx=0.5, rely=0.5, anchor="center")

        wrap_w = int(mon["w"] * 0.78) if mon else 1400

        tk.Label(box, text=T("알림이 도착했어요"), bg=DARK, fg=item.get("color") or "#F5A458",
                 font=F(17)).pack(pady=(0, 22))
        tk.Label(box, text=item.get("time", ""), bg=DARK, fg="white",
                 font=F(128, True)).pack()
        tk.Label(box, text=(item["icon"] + " " if item.get("icon") else "") + item.get("title", ""),
                 bg=DARK, fg="white",
                 font=F(44, True), wraplength=wrap_w,
                 justify="center").pack(pady=(24, 0))
        if item.get("memo"):
            tk.Label(box, text=item["memo"], bg=DARK, fg=GREY, font=F(20),
                     wraplength=int(wrap_w * 0.82),
                     justify="center").pack(pady=(20, 0))
        tk.Label(box, text=T("현재 ") + datetime.now().strftime("%Y-%m-%d %H:%M"),
                 bg=DARK, fg=GREY, font=F(14)).pack(pady=(24, 0))

        btns = tk.Frame(box, bg=DARK)
        btns.pack(pady=(48, 0))
        Pill(btns, T("확인했어요"), self.finish_ok, fg=DARK, bg="white", border="",
             hover="#EDEDED", page_bg=DARK, size=12, bold=True, height=52,
             radius=None, min_width=200).pack(side="left", padx=8)
        Pill(btns, T("%d분 뒤에 다시") % snooze_min, self.finish_snooze, fg="white", bg=DARK,
             border="#5A5A5A", hover="#2B2B2B", page_bg=DARK, size=12,
             height=56, radius=None, min_width=200).pack(side="left", padx=8)

        self.after(50, lambda: force_front(self))
        self._loop()

    def _ensure_monitor(self, mon):
        """전체화면 전환 후에도 지정 모니터에 있지 않으면 강제로 이동한다."""
        try:
            if abs(self.winfo_rootx() - mon["x"]) <= 4 and \
               abs(self.winfo_rooty() - mon["y"]) <= 4:
                return
            self.attributes("-fullscreen", False)
            self.overrideredirect(True)
            self.geometry("%dx%d+%d+%d" % (mon["w"], mon["h"], mon["x"], mon["y"]))
            self.lift()
            self.attributes("-topmost", True)
            force_front(self)
        except Exception:
            pass

    def _loop(self):
        if not self.beeping:
            return
        beep()
        self.raise_count += 1
        if self.raise_count <= 4:
            force_front(self)
        self.after(3000, self._loop)

    def _close(self, result):
        self.beeping = False
        try:
            self.destroy()
        except Exception:
            pass
        self.on_close(self.item, result)

    def finish_ok(self):
        self._close("확인")  # i18n:skip

    def finish_snooze(self):
        self._close("스누즈")  # i18n:skip


# ------------------------------------------------------------------ auto update
#  GitHub Releases(최신 릴리스)를 조회해 새 버전이 있으면 exe를 내려받아 교체한다.
#  - 전송 정보: 요청 URL과 일반적인 User-Agent뿐(사용자 식별 정보 없음)
#  - 무결성: 릴리스 자산의 SHA-256(digest)과 일치할 때만 설치한다.
#  - 설치(교체)는 PyInstaller exe 배포본에서만 동작하고, 그 외에는 릴리스 페이지를 연다.
FROZEN = bool(getattr(sys, "frozen", False))
_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_TRUSTED_HOSTS = ("github.com", "githubusercontent.com")


def parse_version(text):
    nums = [int(x) for x in re.findall(r"\d+", str(text).split("-")[0])][:3]
    return tuple(nums + [0] * (3 - len(nums)))


def update_enabled():
    return bool(_REPO_RE.match(GITHUB_REPO or ""))


def _trusted(url):
    m = re.match(r"^https://([^/]+)/", url or "")
    host = m.group(1).lower() if m else ""
    return any(host == h or host.endswith("." + h) for h in _TRUSTED_HOSTS)


def fetch_latest_release(timeout=8):
    """최신 릴리스 정보 dict(version, page, asset_url, sha256, notes)를 반환한다."""
    url = "https://api.github.com/repos/%s/releases/latest" % GITHUB_REPO
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "DesktopReminder-Updater"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        j = json.loads(r.read().decode("utf-8"))
    asset = next((a for a in j.get("assets", []) if a.get("name") == UPDATE_ASSET), None)
    digest = (asset or {}).get("digest") or ""
    return {
        "version": str(j.get("tag_name", "")).lstrip("vV"),
        "page": j.get("html_url", ""),
        "asset_url": (asset or {}).get("browser_download_url", ""),
        "sha256": digest[7:].lower() if digest.startswith("sha256:") else "",
        "notes": (j.get("body") or "").strip(),
    }


def download_release(info, dest, progress=None, timeout=20):
    """exe를 dest.part로 받아 SHA-256 검증 후 dest로 옮긴다. 실패하면 예외."""
    if not (_trusted(info.get("asset_url")) and info.get("sha256")):
        raise ValueError(T("검증 가능한 다운로드 정보가 없습니다."))
    part = dest + ".part"
    h = hashlib.sha256()
    req = urllib.request.Request(info["asset_url"],
                                 headers={"User-Agent": "DesktopReminder-Updater"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r, open(part, "wb") as f:
            if not _trusted(r.geturl()):
                raise ValueError(T("신뢰할 수 없는 다운로드 주소입니다."))
            total = int(r.headers.get("Content-Length") or 0)
            got = 0
            while True:
                chunk = r.read(256 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                h.update(chunk)
                got += len(chunk)
                if progress and total:
                    progress(int(got * 100 / total))
        if h.hexdigest().lower() != info["sha256"]:
            raise ValueError(T("파일 무결성 검증에 실패했습니다(SHA-256 불일치)."))
        os.replace(part, dest)
    except Exception:
        try:
            os.remove(part)
        except Exception:
            pass
        raise


def apply_update(new_path):
    """실행 중인 exe를 새 파일로 교체하고 새 프로세스를 띄운다(exe 배포본 전용).
    실행 중인 exe도 이름 변경은 가능하므로 .old로 옮긴 뒤 새 파일을 제자리에 둔다."""
    exe = sys.executable
    old = exe + ".old"
    try:
        if os.path.exists(old):
            os.remove(old)
    except Exception:
        pass
    os.replace(exe, old)
    try:
        os.replace(new_path, exe)
    except Exception:
        os.replace(old, exe)               # 실패하면 원상 복구
        raise
    env = dict(os.environ)
    env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"   # 새 프로세스가 임시 폴더를 새로 풀도록
    subprocess.Popen([exe], env=env, close_fds=True,
                     creationflags=0x00000008 | 0x00000200)   # DETACHED | NEW_PROCESS_GROUP


def cleanup_old_exe():
    if FROZEN:
        try:
            old = sys.executable + ".old"
            if os.path.exists(old):
                os.remove(old)
        except Exception:
            pass


# ------------------------------------------------------------------ 후원 · 의견
def open_donate(*_):
    webbrowser.open(DONATE_URL)


def _error_log_tail(n=40):
    try:
        with open(os.path.join(BASE, "reminder_error.log"), "r", encoding="utf-8",
                  errors="ignore") as f:
            return "".join(f.readlines()[-n:])
    except Exception:
        return ""


def _feedback_meta():
    import platform
    return "%s %s / %s" % (APP_NAME_KO, APP_VERSION, platform.platform())


def feedback_issue_url(category, message):
    """공개 GitHub 이슈 작성 화면(제목·본문 미리 채움)."""
    body = message[:1500] + "\n\n---\n" + _feedback_meta()
    q = urllib.parse.urlencode({"title": "[%s] " % category, "body": body},
                               quote_via=urllib.parse.quote)
    return "https://github.com/%s/issues/new?%s" % (GITHUB_REPO, q)


def send_feedback_mail(category, message, reply_to="", include_log=False):
    """FormSubmit 중계로 개발자 메일에 전송. 성공 True / 최초 활성화 필요 'activate' / 실패 False."""
    if not FEEDBACK_EMAIL:
        return False
    data = {"_subject": "[%s %s] %s" % (APP_NAME_KO, APP_VERSION, category),
            "_template": "box", "_captcha": "false",
            "분류": category, "내용": message, "버전": APP_VERSION,
            "환경": _feedback_meta()}
    if reply_to:
        data["_replyto"] = reply_to
        data["답장 메일"] = reply_to
    if include_log:
        data["오류 기록"] = _error_log_tail() or "(없음)"
    try:
        req = urllib.request.Request(
            FEEDBACK_ENDPOINT_BASE + FEEDBACK_EMAIL,
            data=json.dumps(data).encode("utf-8"), method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json",
                     "User-Agent": "Mozilla/5.0 (Ddingdong/%s)" % APP_VERSION,
                     "Referer": "https://github.com/%s" % GITHUB_REPO,
                     "Origin": "https://github.com"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                raw = r.read().decode("utf-8")
        except urllib.error.HTTPError as he:
            raw = he.read().decode("utf-8", "ignore")
        try:
            res = json.loads(raw or "{}")
        except Exception:
            res = {"message": raw[:300]}
        ok = str(res.get("success", "")).lower() == "true"
        if not ok and "activat" in str(res.get("message", "")).lower():
            return "activate"
        return ok
    except Exception:
        return False


# ------------------------------------------------------------------ tray icon
class TrayIcon:
    """Shell_NotifyIconW(ctypes) 기반 알림 영역 아이콘. 표준 라이브러리만 사용한다.
    보이지 않는 메시지 전용 창이 아이콘 클릭 메시지를 받는다(Tk 메인루프가 디스패치)."""

    WM_TRAY = 0x0400 + 20            # WM_USER + 20
    CMD_OPEN, CMD_QUIT = 1, 2

    def __init__(self, app, tip, on_open, on_quit, extra=()):
        from ctypes import wintypes
        self.app, self.on_open, self.on_quit = app, on_open, on_quit
        self.extra = list(extra)            # [(메뉴 id, 라벨, 콜백)]
        self.added = False
        self.u = ctypes.WinDLL("user32", use_last_error=True)
        self.s = ctypes.WinDLL("shell32", use_last_error=True)
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        LRESULT = ctypes.c_ssize_t
        WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT,
                                     wintypes.WPARAM, wintypes.LPARAM)

        class WNDCLASSW(ctypes.Structure):
            _fields_ = [("style", wintypes.UINT), ("lpfnWndProc", WNDPROC),
                        ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int),
                        ("hInstance", wintypes.HANDLE), ("hIcon", wintypes.HANDLE),
                        ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HANDLE),
                        ("lpszMenuName", wintypes.LPCWSTR),
                        ("lpszClassName", wintypes.LPCWSTR)]

        class GUID(ctypes.Structure):
            _fields_ = [("a", wintypes.DWORD), ("b", wintypes.WORD),
                        ("c", wintypes.WORD), ("d", ctypes.c_ubyte * 8)]

        class NID(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.DWORD), ("hWnd", wintypes.HWND),
                        ("uID", wintypes.UINT), ("uFlags", wintypes.UINT),
                        ("uCallbackMessage", wintypes.UINT), ("hIcon", wintypes.HANDLE),
                        ("szTip", ctypes.c_wchar * 128), ("dwState", wintypes.DWORD),
                        ("dwStateMask", wintypes.DWORD), ("szInfo", ctypes.c_wchar * 256),
                        ("uVersion", wintypes.UINT), ("szInfoTitle", ctypes.c_wchar * 64),
                        ("dwInfoFlags", wintypes.DWORD), ("guid", GUID),
                        ("hBalloonIcon", wintypes.HANDLE)]

        self._NID = NID
        u, s = self.u, self.s
        u.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT,
                                     wintypes.WPARAM, wintypes.LPARAM]
        u.DefWindowProcW.restype = LRESULT
        u.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
        u.CreateWindowExW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
                                      wintypes.DWORD, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_int, wintypes.HWND,
                                      wintypes.HANDLE, wintypes.HANDLE, wintypes.LPVOID]
        u.CreateWindowExW.restype = wintypes.HWND
        u.LoadImageW.argtypes = [wintypes.HANDLE, wintypes.LPCWSTR, wintypes.UINT,
                                 ctypes.c_int, ctypes.c_int, wintypes.UINT]
        u.LoadImageW.restype = wintypes.HANDLE
        u.LoadIconW.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
        u.LoadIconW.restype = wintypes.HANDLE
        u.CreatePopupMenu.restype = wintypes.HANDLE
        u.AppendMenuW.argtypes = [wintypes.HANDLE, wintypes.UINT,
                                  ctypes.c_size_t, wintypes.LPCWSTR]
        u.TrackPopupMenu.argtypes = [wintypes.HANDLE, wintypes.UINT, ctypes.c_int,
                                     ctypes.c_int, ctypes.c_int, wintypes.HWND,
                                     ctypes.c_void_p]
        u.DestroyMenu.argtypes = [wintypes.HANDLE]
        u.DestroyWindow.argtypes = [wintypes.HWND]
        u.SetForegroundWindow.argtypes = [wintypes.HWND]
        u.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT,
                                   wintypes.WPARAM, wintypes.LPARAM]
        s.Shell_NotifyIconW.argtypes = [wintypes.DWORD, ctypes.POINTER(NID)]
        k.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        k.GetModuleHandleW.restype = wintypes.HANDLE

        self._proc_ref = WNDPROC(self._wndproc)       # GC 방지용 참조 유지
        hinst = k.GetModuleHandleW(None)
        cls = "SimpleReminderTray"
        wc = WNDCLASSW()
        wc.lpfnWndProc = self._proc_ref
        wc.hInstance = hinst
        wc.lpszClassName = cls
        u.RegisterClassW(ctypes.byref(wc))            # 이미 등록돼 있어도 무방
        self.hwnd = u.CreateWindowExW(0, cls, "Reminder Tray", 0, 0, 0, 0, 0,
                                      wintypes.HWND(-3), None, hinst, None)  # HWND_MESSAGE
        if not self.hwnd:
            raise OSError("tray window")
        self._taskbar_msg = u.RegisterWindowMessageW("TaskbarCreated")

        self.hicon = None
        path = ensure_icon_file()
        if path:
            cx = u.GetSystemMetrics(49)               # SM_CXSMICON
            self.hicon = u.LoadImageW(None, path, 1, cx, cx, 0x10)  # IMAGE_ICON, LR_LOADFROMFILE
        if not self.hicon:
            self.hicon = u.LoadIconW(None, ctypes.c_void_p(32512))  # IDI_APPLICATION
        self.tip = tip

    # NOTIFYICONDATAW 공통 필드
    def _nid(self, flags):
        n = self._NID()
        n.cbSize = ctypes.sizeof(self._NID)
        n.hWnd, n.uID, n.uFlags = self.hwnd, 1, flags
        n.uCallbackMessage = self.WM_TRAY
        n.hIcon = self.hicon
        n.szTip = self.tip
        return n

    def show(self):
        if self.added:
            return
        n = self._nid(0x1 | 0x2 | 0x4)                # NIF_MESSAGE | ICON | TIP
        self.added = bool(self.s.Shell_NotifyIconW(0, ctypes.byref(n)))   # NIM_ADD

    def hide(self):
        if not self.added:
            return
        n = self._nid(0)
        self.s.Shell_NotifyIconW(2, ctypes.byref(n))  # NIM_DELETE
        self.added = False

    def balloon(self, title, text):
        if not self.added:
            return
        n = self._nid(0x10)                           # NIF_INFO
        n.szInfoTitle, n.szInfo, n.dwInfoFlags = title, text, 1   # NIIF_INFO
        self.s.Shell_NotifyIconW(1, ctypes.byref(n))  # NIM_MODIFY

    def destroy(self):
        self.hide()
        try:
            self.u.DestroyWindow(self.hwnd)
        except Exception:
            pass

    def _menu(self):
        from ctypes import wintypes
        u = self.u
        pt = wintypes.POINT()
        u.GetCursorPos(ctypes.byref(pt))
        m = u.CreatePopupMenu()
        u.AppendMenuW(m, 0x0, self.CMD_OPEN, T("열기"))
        for cid, label, _cb in self.extra:
            u.AppendMenuW(m, 0x0, cid, label)
        u.AppendMenuW(m, 0x800, 0, None)              # MF_SEPARATOR
        u.AppendMenuW(m, 0x0, self.CMD_QUIT, T("종료"))
        u.SetForegroundWindow(self.hwnd)              # 메뉴 바깥 클릭 시 닫히도록
        cmd = u.TrackPopupMenu(m, 0x0100 | 0x0002, pt.x, pt.y, 0, self.hwnd, None)
        u.PostMessageW(self.hwnd, 0, 0, 0)            # WM_NULL
        u.DestroyMenu(m)
        if cmd == self.CMD_OPEN:
            self.app.after(0, self.on_open)
        elif cmd == self.CMD_QUIT:
            self.app.after(0, self.on_quit)
        else:
            for cid, _label, cb in self.extra:
                if cmd == cid:
                    self.app.after(0, cb)

    def _wndproc(self, hwnd, msg, wp, lp):
        try:
            if msg == self.WM_TRAY:
                ev = lp & 0xFFFF
                if ev in (0x0202, 0x0203):            # WM_LBUTTONUP / DBLCLK
                    self.app.after(0, self.on_open)
                elif ev in (0x0205, 0x007B):          # WM_RBUTTONUP / CONTEXTMENU
                    self._menu()
                return 0
            if msg == self._taskbar_msg and self.added:   # 탐색기 재시작 시 아이콘 복구
                self.added = False
                self.show()
                return 0
        except Exception:
            pass
        return self.u.DefWindowProcW(hwnd, msg, wp, lp)


# ------------------------------------------------------------------ main app
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        init_fonts()
        self.data = load_data()
        self._apply_sound()
        # 이미 울린 알림 기록(날짜|id). 파일에 저장해 재시작해도 같은 알림이 다시 울리지 않는다.
        self.fired = {k for k in self.data.get("fired", []) if isinstance(k, str)}
        # 시작한 그 분도 검사 대상(이미 울린 기록은 fired로 걸러짐)
        self._last_min = (datetime.now().replace(second=0, microsecond=0)
                          - timedelta(minutes=1))
        self._shown_min = None
        self.pending = []
        self.alarm = None
        self.memo_job = None
        self.hol_job = None
        self._hol_text = None
        self._hol_set = set()
        self.selected_id = None
        self.edit_id = None
        self.tab = "schedule"
        self._upd_q, self._upd_busy, self._upd_manual = queue.Queue(), False, False
        self.update_info, self.upd_chip = None, None
        cleanup_old_exe()                  # 이전 업데이트에서 남은 .old 파일 정리

        self.title(APP_NAME)
        apply_app_icon(self)
        self.geometry("1080x700")
        self.minsize(880, 610)
        self.configure(bg=CANVAS)

        self._build_header()
        self._build_tabs()
        self._build_pages()
        self._select_tab("schedule")
        self._refresh_items()
        self._refresh_logs()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # 최소화하면 작업표시줄 대신 알림 영역(트레이)으로 보낸다
        self.tray, self._in_tray, self._tray_tip_shown = None, False, False
        if IS_WIN:
            try:
                self.tray = TrayIcon(self, T("일정 리마인더 · 감시 중"),
                                     self.from_tray, self._quit_from_tray,
                                     extra=[(3, T("후원하기"), open_donate),
                                            (4, T("의견 보내기"), self.open_feedback)])
                self.bind("<Unmap>", self._on_unmap)
            except Exception:
                self.tray = None
        self._tick()

        set_dark_titlebar(self)
        if "--minimized" in sys.argv:                # 자동 실행: 트레이에서 조용히 시작
            self.after(500, self._start_hidden)

        # 하루 한 번(설정에서 끌 수 있음) 시작 직후 새 버전을 조용히 확인한다
        today = datetime.now().strftime("%Y-%m-%d")
        if (update_enabled() and self.data.get("auto_update", True)
                and self.data.get("update_checked", "")[:10] != today):
            self.after(4000, self.check_update)

    # ---------------------------------------------------------- tray / save
    def _on_unmap(self, e):
        if e.widget is self and not self._in_tray:
            self.after(60, self._maybe_to_tray)

    def _maybe_to_tray(self):
        try:
            if self.tray and not self._in_tray and self.state() == "iconic":
                self.to_tray()
        except Exception:
            pass

    def _start_hidden(self):
        if self.tray:
            self.to_tray(balloon=False)
        else:
            self.iconify()

    def _on_close(self):
        """창 닫기(X): 트레이를 쓸 수 있으면 숨기기만 하고, 아니면 종료 확인."""
        if self.tray and not self._in_tray:
            self.to_tray()
            if self._in_tray:
                return
        self._on_quit()

    def to_tray(self, balloon=True):
        self.tray.show()
        if not self.tray.added:          # 아이콘 등록 실패 시 일반 최소화 유지
            return
        self._in_tray = True
        self.withdraw()
        if balloon and not self._tray_tip_shown:
            self._tray_tip_shown = True
            self.tray.balloon(T("일정 리마인더"), T("트레이에서 계속 감시합니다. 아이콘 클릭 → 열기, 우클릭 → 종료."))

    def from_tray(self):
        self._in_tray = False
        self.deiconify()
        self.state("normal")
        try:
            force_front(self)
        except Exception:
            pass
        if self.tray:
            self.tray.hide()

    def _quit_from_tray(self):
        self.from_tray()
        self._on_quit()

    def _save(self):
        """일정 데이터 저장. 실패하면 연속 실패 중 한 번만 사용자에게 알린다."""
        # fired는 어제 이후 기록만 유지해 집합이 계속 커지지 않게 한다
        cutoff = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.fired = {k for k in self.fired if k[:10] >= cutoff}
        self.data["fired"] = sorted(self.fired)
        ok, err = save_data(self.data)
        if ok:
            self._save_failed = False
        elif not getattr(self, "_save_failed", False):
            self._save_failed = True
            msg = (T("저장에 실패했습니다. 변경 내용이 파일에 남지 않을 수 있습니다.\n"
                   "(폴더 권한·OneDrive 동기화 잠금·디스크 공간을 확인하세요)\n\n")
                   + DATA_PATH + "\n" + err)
            if self._in_tray and self.tray:
                self.tray.balloon(T("저장 실패"), T("reminder_data.json 저장에 실패했습니다."))
            else:
                messagebox.showerror(T("저장 실패"), msg)
        return ok

    # ---------------------------------------------------------- header
    def _build_header(self):
        head = tk.Frame(self, bg=CANVAS)
        head.pack(fill="x", padx=28, pady=(20, 4))
        left = tk.Frame(head, bg=CANVAS)
        left.pack(side="left", anchor="w")
        trow = tk.Frame(left, bg=CANVAS)
        trow.pack(anchor="w")
        self.hdr_trow = trow
        tk.Label(trow, text=APP_NAME, bg=CANVAS, fg=TEXT,
                 font=F(18, True)).pack(side="left")
        Pill(trow, "v" + APP_VERSION, None, fg=BLUE, bg=BLUE_SOFT, border="",
             page_bg=CANVAS, size=8, bold=True, height=22, radius=11,
             padx=9).pack(side="left", padx=(10, 0), pady=(4, 0))
        self.lbl_hello = tk.Label(left, text="", bg=CANVAS, fg=SUB, font=F(10))
        self.lbl_hello.pack(anchor="w", pady=(5, 0))

        right = tk.Frame(head, bg=CANVAS)
        right.pack(side="right", anchor="e")
        self.lbl_clock = tk.Label(right, text="--:--:--", bg=CANVAS, fg=TEXT,
                                  font=F(24, True))
        self.lbl_clock.pack(anchor="e")
        self.lbl_date = tk.Label(right, text="", bg=CANVAS, fg=SUB, font=F(9))
        self.lbl_date.pack(anchor="e")

        # ── 알림을 띄울 모니터 선택
        mon_box = tk.Frame(head, bg=CANVAS)
        mon_box.pack(side="right", anchor="e", padx=(0, 26))
        tk.Label(mon_box, text=T("알림 표시 화면"), bg=CANVAS, fg=SUB,
                 font=F(9)).pack(anchor="w", pady=(0, 4))
        self.mon_values = monitor_labels()
        saved = self.data.get("monitor", 0)
        try:
            saved = int(saved)
        except Exception:
            saved = 0
        if not (0 <= saved < len(self.mon_values)):
            saved = 0
        self.dd_monitor = Dropdown(mon_box, self.mon_values,
                                   value=self.mon_values[saved],
                                   page_bg=CANVAS, width=236, height=38)
        self.dd_monitor.pack(anchor="w")

    # ---------------------------------------------------------- tabs
    def _build_tabs(self):
        wrap = tk.Frame(self, bg=CANVAS)
        wrap.pack(fill="x", padx=28, pady=(14, 0))
        self.tab_btn = {}                             # 둥근 알약형 탭
        for key, text in (("schedule", T("일정")), ("memo", T("메모장"))):
            p = Pill(wrap, text, lambda k=key: self._select_tab(k), fg=SUB, bg=SOFT,
                     border="", hover=SURFACE2, page_bg=CANVAS, size=10, bold=True,
                     height=40, padx=26)
            p.pack(side="left", padx=(0, 8))
            self.tab_btn[key] = p
        Pill(wrap, T("설정"), self.open_settings, bg=SOFT, border="", hover=SURFACE2,
             page_bg=CANVAS, size=10, bold=True, height=40,
             padx=24).pack(side="right")

    @staticmethod
    def _style_tabs(buttons, active):
        for k, p in buttons.items():
            on = (k == active)
            p.restyle("white" if on else SUB, BLUE if on else SOFT,
                      BLUE_DEEP if on else SURFACE2)

    def _select_tab(self, key):
        self.tab = key
        self._style_tabs(self.tab_btn, key)
        for k in self.tab_btn:
            self.pages[k].pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        if key == "memo":
            self.txt_memo.focus_set()
        else:
            self._refresh_items()

    # ---------------------------------------------------------- pages
    def _build_pages(self):
        holder = tk.Frame(self, bg=CANVAS)
        holder.pack(fill="both", expand=True, padx=28, pady=(16, 22))
        self.pages = {
            "schedule": tk.Frame(holder, bg=CANVAS),
            "memo": tk.Frame(holder, bg=CANVAS),
        }
        self._build_schedule(self.pages["schedule"])
        self._build_memo(self.pages["memo"])
        self._build_settings()

    # ---------------------------------------------------------- settings window
    def _build_settings(self):
        """휴일·실행 기록·정보/업데이트는 별도 설정 창에 둔다(닫으면 숨기기만 한다)."""
        w = tk.Toplevel(self)
        w.withdraw()
        w.title(APP_NAME + T(" · 설정"))
        w.configure(bg=CANVAS)
        w.geometry("840x700")
        w.minsize(680, 480)
        w.protocol("WM_DELETE_WINDOW", self.close_settings)
        w.bind("<Escape>", lambda e: self.close_settings())
        self.settings = w

        top = tk.Frame(w, bg=CANVAS)
        top.pack(fill="x", padx=26, pady=(20, 0))
        self.stab_btn = {}
        for key, text in (("general", T("일반")), ("holiday", T("휴일")), ("log", T("실행 기록")),
                          ("support", T("후원 · 의견")), ("about", T("정보 · 업데이트"))):
            p = Pill(top, text, lambda k=key: self._select_stab(k), fg=SUB, bg=SOFT,
                     border="", hover=SURFACE2, page_bg=CANVAS, size=10, bold=True,
                     height=38, padx=22)
            p.pack(side="left", padx=(0, 8))
            self.stab_btn[key] = p

        holder = tk.Frame(w, bg=CANVAS)
        holder.pack(fill="both", expand=True, padx=26, pady=(16, 22))
        self.spages = {k: tk.Frame(holder, bg=CANVAS)
                       for k in ("general", "holiday", "log", "support", "about")}
        self._build_general(self.spages["general"])
        self._build_support(self.spages["support"])
        self._build_holiday(self.spages["holiday"])
        self._build_log(self.spages["log"])
        self._build_about(self.spages["about"])
        self._select_stab("general")
        set_dark_titlebar(w)

    def _select_stab(self, key):
        self._style_tabs(self.stab_btn, key)
        for k in self.stab_btn:
            self.spages[k].pack_forget()
        self.spages[key].pack(fill="both", expand=True)

    def open_settings(self, tab=None):
        if tab:
            self._select_stab(tab)
        w = self.settings
        if not w.winfo_viewable():
            self.update_idletasks()
            x = self.winfo_rootx() + max(0, (self.winfo_width() - 840) // 2)
            y = self.winfo_rooty() + 40
            w.geometry("840x700+%d+%d" % (x, y))
        w.deiconify()
        set_dark_titlebar(w)
        w.lift()
        w.focus_force()

    def close_settings(self):
        self.settings.withdraw()

    # ---------------------------------------------------------- schedule
    def _build_schedule(self, parent):
        card = RoundBox(parent, bg=SOFT, page_bg=CANVAS, height=176)
        self.form_card = card
        card.pack(fill="x")
        card.pack_propagate(False)
        inner = tk.Frame(card.body, bg=SOFT)
        inner.place(relx=0, rely=0.5, anchor="w", x=18, relwidth=0.985)

        def cap(parent_, text):
            tk.Label(parent_, text=text, bg=SOFT, fg=SUB,
                     font=F(9)).pack(anchor="w", pady=(0, 6))

        # 창 폭이 줄어들어도 '반복·추가'가 잘리지 않도록 grid 가중치로 배치한다.
        # 가변 폭은 일정명/메모 컬럼만 흡수하고 나머지는 고정 폭을 지킨다.
        inner.grid_columnconfigure(0, weight=0, minsize=TimeField.W)
        inner.grid_columnconfigure(1, weight=3, minsize=140)
        inner.grid_columnconfigure(2, weight=2, minsize=110)
        inner.grid_columnconfigure(3, weight=0, minsize=196)
        inner.grid_columnconfigure(4, weight=0, minsize=88)
        inner.grid_columnconfigure(5, weight=0)

        now = datetime.now()
        c0 = tk.Frame(inner, bg=SOFT)
        c0.grid(row=0, column=0, sticky="w", padx=(0, 14))
        cap(c0, T("시각"))
        self.time_field = TimeField(c0, page_bg=SOFT, hh=now.hour, mm=0)
        self.time_field.pack()

        c1 = tk.Frame(inner, bg=SOFT)
        c1.grid(row=0, column=1, sticky="ew", padx=(0, 14))
        cap(c1, T("일정명"))
        self.e_title = self._entry(c1, T("예) 약 먹기, 스트레칭"))

        c2 = tk.Frame(inner, bg=SOFT)
        c2.grid(row=0, column=2, sticky="ew", padx=(0, 14))
        cap(c2, T("메모 (선택)"))
        self.e_memo = self._entry(c2, T("예) 물 한 컵과 함께"))

        c3 = tk.Frame(inner, bg=SOFT)
        c3.grid(row=0, column=3, sticky="w", padx=(0, 14))
        cap(c3, T("반복"))
        self.dd_repeat = Dropdown(c3, REPEAT_VALUES, REPEAT_VALUES[1], page_bg=SOFT,
                                  width=196, on_change=self._sync_repeat_ui)
        self.dd_repeat.pack()

        c4 = tk.Frame(inner, bg=SOFT)
        c4.grid(row=0, column=4, sticky="w")
        cap(c4, " ")
        self.btn_add = Pill(c4, T("추가"), self.add_item, fg="white", bg=BLUE,
                            border="", hover=BLUE_DEEP, page_bg=SOFT, size=10,
                            bold=True, height=46, radius=None, min_width=84)
        self.btn_add.pack()
        self.btn_save = Pill(c4, T("수정 저장"), self.add_item, fg="white", bg=GREEN,
                             border="", hover=GREEN_DEEP, page_bg=SOFT, size=10,
                             bold=True, height=46, radius=None, min_width=88)

        c5 = tk.Frame(inner, bg=SOFT)
        c5.grid(row=0, column=5, sticky="w", padx=(8, 0))
        cap(c5, " ")
        self.btn_cancel = Pill(c5, T("취소"), self._end_edit, page_bg=SOFT, size=10,
                               height=46, radius=None, min_width=64)

        # ── 반복 유형별 상세 옵션 (매주: 요일 / 매월: 일자 / 휴일 이월)
        self.opt_row = tk.Frame(inner, bg=SOFT)
        self.opt_row.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(14, 0))

        self.wk_box = tk.Frame(self.opt_row, bg=SOFT)
        tk.Label(self.wk_box, text=T("요일"), bg=SOFT, fg=SUB,
                 font=F(9)).pack(side="left", padx=(0, 10))
        self.wk_chips = []
        for nm in WEEK_NAMES:
            chip = ToggleChip(self.wk_box, nm, page_bg=SOFT, min_width=40, padx=10)
            chip.pack(side="left", padx=(0, 6))
            self.wk_chips.append(chip)
        self.wk_chips[0].set(True)

        self.dom_box = tk.Frame(self.opt_row, bg=SOFT)
        tk.Label(self.dom_box, text=T("일자"), bg=SOFT, fg=SUB,
                 font=F(9)).pack(side="left", padx=(0, 10))
        self.day_field = DayField(self.dom_box, page_bg=SOFT, value=1)
        self.day_field.pack(side="left")
        tk.Label(self.dom_box,
                 text=T("'말일' 선택 가능 · 31일로 두면 그 날짜가 없는 달은 말일로 자동 보정"),
                 bg=SOFT, fg=SUB, font=F(9)).pack(side="left", padx=(12, 0))

        self.date_box = tk.Frame(self.opt_row, bg=SOFT)
        tk.Label(self.date_box, text=T("날짜"), bg=SOFT, fg=SUB,
                 font=F(9)).pack(side="left", padx=(0, 10))
        self.date_field = DateField(self.date_box, page_bg=SOFT)
        self.date_field.pack(side="left")

        self.shift_box = tk.Frame(self.opt_row, bg=SOFT)
        self.chk_shift = ToggleChip(self.shift_box, T("주말·공휴일이면 다음 영업일로 이월"),
                                    page_bg=SOFT, padx=14)
        self.chk_shift.set(True)
        self.chk_shift.pack(side="left")

        # ── 꾸미기: 일정별 포인트 색·기호(목록과 알림 화면에 표시)
        deco = tk.Frame(inner, bg=SOFT)
        deco.grid(row=2, column=0, columnspan=6, sticky="w", pady=(14, 0))
        tk.Label(deco, text=T("꾸미기"), bg=SOFT, fg=SUB, font=F(9)).pack(side="left", padx=(0, 12))
        self.strip_color = ChoiceStrip(deco, COLOR_CHOICES, "color", page_bg=SOFT, size=30, gap=4)
        self.strip_color.pack(side="left")
        tk.Frame(deco, bg=BORDER, width=1, height=24).pack(side="left", padx=14)
        self.strip_symbol = ChoiceStrip(deco, SYMBOL_CHOICES, "symbol", page_bg=SOFT, size=30, gap=4)
        self.strip_symbol.pack(side="left")

        bar = tk.Frame(parent, bg=CANVAS)
        bar.pack(fill="x", pady=(16, 10))
        Pill(bar, T("알림 미리보기"), self.preview, page_bg=CANVAS).pack(side="left")
        Pill(bar, T("선택 삭제"), self.delete_item, page_bg=CANVAS).pack(side="left", padx=8)
        Pill(bar, T("감시 중 · 알림 대기"), None, fg=GREEN, bg=GREEN_SOFT,
             border="", page_bg=CANVAS, size=9, height=34,
             radius=17).pack(side="left", padx=6)
        self.lbl_edit = tk.Label(bar, text="", bg=CANVAS, fg=ORANGE, font=F(9, True))
        for minutes, text in ((60, T("1시간 뒤")), (30, T("30분 뒤")), (10, T("10분 뒤"))):
            Pill(bar, text, lambda m=minutes: self.quick_add(m), page_bg=CANVAS, size=9,
                 height=34, padx=14).pack(side="right", padx=(6, 0))
        tk.Label(bar, text=T("빠른 알림"), bg=CANVAS, fg=SUB, font=F(9)).pack(side="right", padx=(0, 8))

        listcard = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        listcard.pack(fill="both", expand=True)
        self.list_area = ScrollArea(listcard.body, bg=CANVAS)
        self.list_area.pack(fill="both", expand=True, padx=1, pady=1)

        self._sync_repeat_ui()

    def _sync_repeat_ui(self, _v=None):
        """선택한 반복 유형에 맞는 상세 옵션만 노출하고 카드 높이를 조정한다."""
        rep = REPEAT_KEY.get(self.dd_repeat.get(), "daily")
        for f in (self.wk_box, self.dom_box, self.date_box, self.shift_box):
            f.pack_forget()
        if rep == "weekly":
            self.wk_box.pack(side="left")
        elif rep == "monthly":
            self.dom_box.pack(side="left")
        elif rep == "once":
            self.date_box.pack(side="left")
        if rep in ("weekly", "monthly", "once"):
            self.shift_box.pack(side="left", padx=(18, 0))
            self.opt_row.grid()
            self.form_card.configure(height=240)
        else:
            self.opt_row.grid_remove()
            self.form_card.configure(height=176)

    def _entry(self, parent, placeholder, page_bg=SOFT, on_return=None):
        """둥근 테두리 입력창. 폰트는 전역 Font 객체를 공유해
        한글 입력 중 다른 폰트로 틀어지는 현상을 막는다."""
        box = RoundBox(parent, bg=CANVAS, page_bg=page_bg, radius=16, height=46)
        box.pack(fill="x")
        box.pack_propagate(False)
        fnt = F(11)
        e = tk.Entry(box.body, font=fnt, relief="flat", bd=0, bg=CANVAS, fg=GREY,
                     highlightthickness=0, insertbackground=TEXT,
                     selectbackground=BLUE_SOFT, selectforeground=TEXT)
        e.place(relx=0, rely=0.5, anchor="w", x=13, relwidth=0.94)
        e.insert(0, placeholder)
        e._ph = placeholder

        def sync_ime(_=None):
            try:
                lx = fnt.measure(e.get()[:e.index("insert")])
            except Exception:
                lx = 0
            tune_ime(e, fnt, lx, 0)

        def focus_in(_):
            if e.get() == placeholder:
                e.delete(0, "end")
            e.config(fg=TEXT)
            box._shape and box.itemconfig(box._shape, outline=BLUE)
            e.after(10, sync_ime)

        def focus_out(_):
            if not e.get().strip():
                e.delete(0, "end")
                e.insert(0, placeholder)
                e.config(fg=GREY)
            box._shape and box.itemconfig(box._shape, outline=BORDER)

        e.bind("<FocusIn>", focus_in)
        e.bind("<FocusOut>", focus_out)
        e.bind("<KeyRelease>", sync_ime, add="+")
        e.bind("<Button-1>", sync_ime, add="+")
        e.bind("<Return>", lambda _e: (on_return or self.add_item)())
        return e

    def _value(self, entry):
        v = entry.get().strip()
        return "" if v == getattr(entry, "_ph", None) else v

    # ---------------------------------------------------------- memo
    def _build_memo(self, parent):
        card = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        card.pack(fill="both", expand=True)
        body = card.body

        bar = tk.Frame(body, bg=SOFT, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        self.lbl_memo_status = tk.Label(bar, text=T("불러옴"), bg=SOFT, fg=SUB, font=F(9))
        self.lbl_memo_status.pack(side="left", padx=18)
        for text, cmd in ((T("비우기"), self.memo_clear),
                          (T(".txt 저장"), self.memo_export),
                          (T("체크박스 줄"), lambda: self.memo_insert("\n□ ")),
                          (T("시각 삽입"), self.memo_stamp)):
            Pill(bar, text, cmd, page_bg=SOFT, size=9, height=34,
                 padx=13).pack(side="right", padx=(0, 8))
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x")

        holder = tk.Frame(body, bg=CANVAS)
        holder.pack(fill="both", expand=True)
        memo_font = F(11)
        self.txt_memo = tk.Text(holder, font=memo_font, relief="flat", wrap="word",
                                padx=22, pady=18, spacing3=6, undo=True,
                                bg=CANVAS, fg=TEXT, insertbackground=TEXT,
                                selectbackground=BLUE_SOFT, selectforeground=TEXT,
                                highlightthickness=0, bd=0)
        sb = SlimScrollbar(holder, self.txt_memo.yview, bg=CANVAS)
        self.txt_memo.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.txt_memo.pack(side="left", fill="both", expand=True)
        self.txt_memo.insert("1.0", self.data.get("memo", ""))

        def memo_ime(_=None):
            try:
                bb = self.txt_memo.bbox("insert")
            except Exception:
                bb = None
            if bb:
                tune_ime(self.txt_memo, memo_font, bb[0], bb[1])
            else:
                tune_ime(self.txt_memo, memo_font, 22, 18)

        self.txt_memo.bind("<KeyRelease>", self._memo_changed)
        self.txt_memo.bind("<KeyRelease>", memo_ime, add="+")
        self.txt_memo.bind("<FocusIn>", memo_ime, add="+")
        self.txt_memo.bind("<Button-1>", lambda e: self.txt_memo.after(10, memo_ime),
                           add="+")

    # ---------------------------------------------------------- holiday
    def _build_holiday(self, parent):
        card = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        card.pack(fill="both", expand=True)
        body = card.body

        bar = tk.Frame(body, bg=SOFT, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        self.lbl_hol_status = tk.Label(bar, text=T("불러옴"), bg=SOFT, fg=SUB, font=F(9))
        self.lbl_hol_status.pack(side="left", padx=18)
        tk.Label(bar, text=T("한 줄에 날짜 하나(YYYY-MM-DD) · '#'으로 시작하는 줄은 메모로 무시됩니다"),
                 bg=SOFT, fg=SUB, font=F(9)).pack(side="left")
        Pill(bar, T("기본 공휴일 다시 넣기"), self.holiday_reset, page_bg=SOFT,
             size=9, height=34, padx=13).pack(side="right", padx=(0, 8))
        Pill(bar, T("오늘 날짜 추가"), self.holiday_today, page_bg=SOFT,
             size=9, height=34, padx=13).pack(side="right", padx=(0, 8))
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x")

        holder = tk.Frame(body, bg=CANVAS)
        holder.pack(fill="both", expand=True)
        hol_font = F(11)
        self.txt_hol = tk.Text(holder, font=hol_font, relief="flat", wrap="word",
                               padx=22, pady=18, spacing3=4, undo=True,
                               bg=CANVAS, fg=TEXT, insertbackground=TEXT,
                               selectbackground=BLUE_SOFT, selectforeground=TEXT,
                               highlightthickness=0, bd=0)
        sb = SlimScrollbar(holder, self.txt_hol.yview, bg=CANVAS)
        self.txt_hol.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.txt_hol.pack(side="left", fill="both", expand=True)
        self.txt_hol.insert("1.0", self.data.get("holidays", DEFAULT_HOLIDAYS))
        self.txt_hol.bind("<KeyRelease>", self._hol_changed)
        self.lbl_hol_status.config(text=T("휴일 %d일 등록됨") % len(self.holidays()))

    def _hol_changed(self, _e=None):
        self.lbl_hol_status.config(text=T("입력 중…"))
        if self.hol_job:
            self.after_cancel(self.hol_job)
        self.hol_job = self.after(400, self._hol_save)

    def _hol_save(self):
        self.hol_job = None
        self.data["holidays"] = self.txt_hol.get("1.0", "end-1c")
        self._save()
        self.lbl_hol_status.config(text=T("저장됨 · 휴일 %d일 등록") % len(self.holidays()))
        if self.tab == "schedule":
            self._refresh_items()

    def holiday_reset(self):
        if not messagebox.askyesno(T("기본 공휴일"), T("현재 내용을 기본 공휴일 표로 되돌릴까요?")):
            return
        self.txt_hol.delete("1.0", "end")
        self.txt_hol.insert("1.0", DEFAULT_HOLIDAYS)
        self._hol_save()

    def holiday_today(self):
        self.txt_hol.insert("end", "\n" + datetime.now().strftime("%Y-%m-%d")
                            + T("  휴무"))
        self._hol_save()

    # ---------------------------------------------------------- log
    def _build_log(self, parent):
        card = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        card.pack(fill="both", expand=True)
        body = card.body

        bar = tk.Frame(body, bg=SOFT, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        self.lbl_log_status = tk.Label(bar, text=T("실행 기록 0건"), bg=SOFT, fg=SUB,
                                       font=F(9))
        self.lbl_log_status.pack(side="left", padx=18)
        Pill(bar, T("기록 비우기"), self.log_clear, page_bg=SOFT, size=9,
             height=34, padx=13).pack(side="right", padx=(0, 8))
        Pill(bar, T(".csv 저장"), self.log_export, page_bg=SOFT, size=9,
             height=34, padx=13).pack(side="right", padx=(0, 8))
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x")

        head = tk.Frame(body, bg=CANVAS)
        head.pack(fill="x")
        for text, w, a in ((T("발생 일시"), 20, "w"), (T("예정 시각"), 10, "center"),
                           (T("일정명"), 34, "w"), (T("반복"), 10, "center"),
                           (T("처리"), 12, "center")):
            tk.Label(head, text=text, width=w, anchor=a, bg=CANVAS, fg=SUB,
                     font=F(9, True), pady=11).pack(side="left", padx=(14, 0))
        tk.Frame(body, bg=BORDER, height=1).pack(fill="x")
        self.log_area = ScrollArea(body, bg=CANVAS)
        self.log_area.pack(fill="both", expand=True)

    # ---------------------------------------------------------- rows
    def _clear(self, frame):
        for w in frame.winfo_children():
            w.destroy()

    def _refresh_items(self):
        holder = self.list_area.inner
        self._clear(holder)
        items = sorted(self.data["items"], key=lambda x: x["time"])
        if not items:
            tk.Label(holder, text=T("아직 등록된 일정이 없어요"), bg=CANVAS, fg=TEXT,
                     font=F(13, True)).pack(pady=(64, 6))
            tk.Label(holder, text=T("위에서 시각과 이름을 넣고 '추가'를 눌러 보세요.\n"
                                  "정한 시간에 화면 가득 알려드릴게요."),
                     bg=CANVAS, fg=SUB, font=F(10), justify="center").pack()
        else:
            # 반복 유형별로 그룹을 나눠 표시한다.
            for key, title, desc, tone in GROUPS:
                sub = [i for i in items if i.get("repeat", "daily") == key]
                if not sub:
                    continue
                self._group_header(holder, title, desc, len(sub), tone,
                                   first=not holder.winfo_children())
                for idx, it in enumerate(sub):
                    self._row(holder, it, idx)
        self._update_hello()
        # 새로 그린 행·그룹 헤더에도 마우스 휠을 연결한다.
        self.list_area.sync_wheel()

    def _group_header(self, holder, title, desc, count, tone, first=False):
        bar = tk.Frame(holder, bg=CANVAS)
        bar.pack(fill="x", padx=6, pady=(4 if first else 20, 8))
        dot = tk.Canvas(bar, width=12, height=12, bg=CANVAS, highlightthickness=0)
        dot.create_oval(1, 1, 11, 11, fill=tone, outline=tone)
        dot.pack(side="left", pady=(2, 0))
        tk.Label(bar, text=title, bg=CANVAS, fg=TEXT, font=F(11, True),
                 padx=8).pack(side="left")
        Pill(bar, "%d" % count, None, fg=tone, bg=tint(tone), border="",
             page_bg=CANVAS, size=8, bold=True, height=20, padx=9).pack(side="left")
        tk.Label(bar, text=desc, bg=CANVAS, fg=SUB, font=F(9),
                 padx=10).pack(side="left")

    def _row(self, holder, it, idx):
        selected = (self.selected_id == it["id"])
        base = BLUE_SOFT if selected else SOFT
        tone = it.get("color") or next((g[3] for g in GROUPS if g[0] == it.get("repeat", "daily")), BLUE)
        card = Card(holder, bg=base, page_bg=CANVAS, radius=20)
        card.pack(fill="x", padx=6, pady=(0, 8))
        row = tk.Frame(card.body, bg=base)
        row.pack(fill="x")

        time_lbl = Pill(row, it["time"], None, fg=tone, bg=tint(tone, 0.82),
                        border="", page_bg=base, size=14, bold=True, height=44,
                        padx=18, min_width=92)
        time_lbl.pack(side="left", padx=(12, 6), pady=12)

        mid = tk.Frame(row, bg=base)
        mid.pack(side="left", fill="x", expand=True, pady=10, padx=(6, 0))
        t1 = tk.Label(mid, text=(it["icon"] + " " if it.get("icon") else "") + it["title"],
                      bg=base, fg=TEXT, font=F(10, True),
                      anchor="w")
        t1.pack(anchor="w")
        subs = [t1]
        if it.get("memo"):
            t2 = tk.Label(mid, text=it["memo"], bg=base, fg=SUB, font=F(9), anchor="w")
            t2.pack(anchor="w", pady=(1, 0))
            subs.append(t2)

        metarow = tk.Frame(mid, bg=base)
        metarow.pack(anchor="w", pady=(4, 0))
        rep = it.get("repeat", "daily")
        Pill(metarow, repeat_text(it), None,
             fg=SUB if rep == "once" else BLUE,
             bg=SURFACE2 if rep == "once" else BLUE_SOFT,
             border="", page_bg=base, size=8, height=22, radius=11,
             padx=9).pack(side="left")
        if it.get("shift"):
            Pill(metarow, T("휴일 → 다음 영업일"), None, fg=GREEN, bg=GREEN_SOFT,
                 border="", page_bg=base, size=8, height=22, radius=11,
                 padx=9).pack(side="left", padx=(6, 0))
        t3 = tk.Label(metarow, text="  " + self._left_text(it), bg=base, fg=SUB,
                      font=F(9))
        t3.pack(side="left")
        subs.append(t3)

        dele = tk.Label(row, text=T("삭제"), bg=base, fg=SUB, font=F(9),
                        padx=16, cursor="hand2")
        dele.pack(side="right")
        dele.bind("<Button-1>", lambda e, i=it: self._delete_id(i["id"]))
        dele.bind("<Enter>", lambda e: dele.config(fg=RED))
        dele.bind("<Leave>", lambda e: dele.config(fg=SUB))

        edit = tk.Label(row, text=T("수정"), bg=base, fg=SUB, font=F(9),
                        padx=8, cursor="hand2")
        edit.pack(side="right")
        edit.bind("<Button-1>", lambda e, i=it: self._begin_edit(i))
        edit.bind("<Enter>", lambda e: edit.config(fg=BLUE))
        edit.bind("<Leave>", lambda e: edit.config(fg=SUB))

        dup = tk.Label(row, text=T("복제"), bg=base, fg=SUB, font=F(9), padx=8, cursor="hand2")
        dup.pack(side="right")
        dup.bind("<Button-1>", lambda e, i=it: self._duplicate(i))
        dup.bind("<Enter>", lambda e: dup.config(fg=BLUE))
        dup.bind("<Leave>", lambda e: dup.config(fg=SUB))

        for w in [card, card.body, row, time_lbl, mid, metarow] + subs:
            w.bind("<Button-1>", lambda e, i=it: self._select_row(i["id"]))
            w.bind("<Double-Button-1>", lambda e, i=it: self._begin_edit(i))

    def _update_hello(self):
        """헤더 인사말 + 오늘 남은 알림 요약."""
        try:
            now = datetime.now()
            h = now.hour
            greet = (T("늦은 시간이에요") if h < 5 else T("좋은 아침이에요") if h < 12
                     else T("좋은 오후예요") if h < 18 else T("편안한 저녁이에요"))
            hol, hhmm = self.holidays(), now.strftime("%H:%M")
            left = sorted((it["time"], it["title"]) for it in self.data["items"]
                          if it["time"] > hhmm and should_fire(it, now.date(), hol))
            if left:
                tail = T("오늘 남은 알림 %d개 · 다음은 %s %s") % (len(left), left[0][0], left[0][1])
            else:
                tail = T("오늘 남은 알림은 없어요")
            self.lbl_hello.config(text="%s. %s" % (greet, tail))
        except Exception:
            pass

    def _select_row(self, item_id):
        self.selected_id = None if self.selected_id == item_id else item_id
        self._refresh_items()

    def _delete_id(self, item_id):
        self.data["items"] = [i for i in self.data["items"] if i["id"] != item_id]
        if self.selected_id == item_id:
            self.selected_id = None
        self._save()
        if self.edit_id == item_id:
            self._end_edit()
        else:
            self._refresh_items()

    # ---------------------------------------------------------- 수정 모드
    def _fill(self, entry, text):
        entry.delete(0, "end")
        if text:
            entry.insert(0, text)
            entry.config(fg=TEXT)
        else:
            entry.insert(0, getattr(entry, "_ph", ""))
            entry.config(fg=GREY)

    def _load_form(self, it):
        """일정 값을 입력 폼에 채운다(수정·복제 공용)."""
        try:
            hh, mm = it["time"].split(":")
            self.time_field.set(hh, mm)
        except Exception:
            pass
        self._fill(self.e_title, it.get("title", ""))
        self._fill(self.e_memo, it.get("memo", ""))
        rep = it.get("repeat", "daily")
        keys = [g[0] for g in GROUPS]
        if rep in keys:
            self.dd_repeat.set(REPEAT_VALUES[keys.index(rep)])
        try:
            wd = [int(x) for x in it.get("weekdays", [])]
        except Exception:
            wd = []
        for i, chip in enumerate(self.wk_chips):
            chip.set(i in wd)
        self.day_field.set(it.get("dom", 1) or 1)
        self.chk_shift.set(bool(it.get("shift")))
        self.date_field.set(it.get("day", ""))
        self.strip_color.set(it.get("color", ""))
        self.strip_symbol.set(it.get("icon", ""))
        self._sync_repeat_ui()

    def _begin_edit(self, it):
        """기존 일정을 상단 입력 폼으로 불러와 수정 모드로 전환한다."""
        self.edit_id = it["id"]
        self.selected_id = it["id"]
        self._load_form(it)
        self.btn_add.pack_forget()
        self.btn_save.pack()
        self.btn_cancel.pack()
        self.lbl_edit.config(text=T("수정 중 · %s") % it.get("title", ""))
        self.lbl_edit.pack(side="left", padx=(10, 0))
        self._refresh_items()
        self.e_title.focus_set()
        self.e_title.icursor("end")

    def _duplicate(self, it):
        """선택한 일정을 새 일정의 초안으로 복제한다(저장은 '추가'를 눌러야 함)."""
        if self.edit_id:
            self._end_edit()
        self._load_form(it)
        self._fill(self.e_title, it.get("title", "") + T(" (복사)"))
        if it.get("repeat") == "once":
            self.date_field.set(datetime.now().date())
        self.e_title.focus_set()
        self.e_title.icursor("end")

    def quick_add(self, minutes):
        """지금부터 N분 뒤에 한 번 울리는 일정을 바로 추가한다."""
        due = datetime.now() + timedelta(minutes=minutes)
        title = self._value(self.e_title) or T("빠른 알림")
        self.data["items"].append({
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "time": due.strftime("%H:%M"), "title": title, "memo": "",
            "repeat": "once", "weekdays": [], "dom": 1, "shift": False,
            "day": due.strftime("%Y-%m-%d"),
            "color": self.strip_color.get(), "icon": self.strip_symbol.get(),
        })
        self._save()
        self._fill(self.e_title, "")
        self._refresh_items()

    def _end_edit(self):
        """수정 모드 해제 및 입력 폼 초기화."""
        self.edit_id = None
        self.strip_color.set("")
        self.strip_symbol.set("")
        self.btn_save.pack_forget()
        self.btn_cancel.pack_forget()
        self.btn_add.pack()
        self.lbl_edit.pack_forget()
        self._fill(self.e_title, "")
        self._fill(self.e_memo, "")
        self.date_field.set(datetime.now().date())
        self.focus_set()
        self._refresh_items()

    def delete_item(self):
        if not self.selected_id:
            messagebox.showinfo(T("삭제"), T("삭제할 일정을 목록에서 클릭해 선택하세요."))
            return
        self._delete_id(self.selected_id)

    # ---------------------------------------------------------- schedule ops
    def add_item(self):
        title = self._value(self.e_title)
        if not title:
            messagebox.showwarning(T("입력 확인"), T("일정명을 입력하세요."))
            return
        repeat = REPEAT_KEY.get(self.dd_repeat.get(), "daily")
        weekdays = [i for i, c in enumerate(self.wk_chips) if c.get()]
        if repeat == "weekly" and not weekdays:
            messagebox.showwarning(T("입력 확인"), T("반복할 요일을 하나 이상 선택하세요."))
            return
        dom = self.day_field.get()
        shift = bool(self.chk_shift.get()) and repeat in ("weekly", "monthly", "once")
        today = datetime.now().strftime("%Y-%m-%d")
        day = self.date_field.get() if repeat == "once" else today
        if repeat == "once" and day < today:
            old = None
            if self.edit_id:
                old = next((i for i in self.data["items"] if i["id"] == self.edit_id), None)
            if old is None or old.get("day") != day:     # 기존 지난 일정의 다른 항목만 수정하는 경우는 허용
                messagebox.showwarning(T("입력 확인"), T("지난 날짜는 지정할 수 없습니다.\n오늘 또는 이후 날짜를 선택하세요."))
                return

        if self.edit_id:                       # 기존 일정 수정 저장
            for it in self.data["items"]:
                if it["id"] == self.edit_id:
                    it["time"] = self.time_field.get()
                    it["title"] = title
                    it["memo"] = self._value(self.e_memo)
                    it["repeat"] = repeat
                    it["weekdays"] = weekdays
                    it["dom"] = dom
                    it["shift"] = shift
                    it["color"] = self.strip_color.get()
                    it["icon"] = self.strip_symbol.get()
                    if repeat == "once":
                        it["day"] = day
                    break
            # 시각을 바꿨으면 오늘 다시 울릴 수 있도록 발생 기록 초기화
            self.fired = {k for k in self.fired
                          if not k.endswith("|" + self.edit_id)}
            self._save()
            self._end_edit()
            return

        self.data["items"].append({
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "time": self.time_field.get(),
            "title": title,
            "memo": self._value(self.e_memo),
            "repeat": repeat,
            "weekdays": weekdays,
            "dom": dom,
            "shift": shift,
            "day": day,
            "color": self.strip_color.get(),
            "icon": self.strip_symbol.get(),
        })
        self._save()
        self.strip_color.set("")
        self.strip_symbol.set("")
        for e in (self.e_title, self.e_memo):
            e.delete(0, "end")
            e.insert(0, getattr(e, "_ph", ""))
            e.config(fg=GREY)
        self.focus_set()
        self._refresh_items()

    def _left_text(self, it):
        """다음 알림까지 남은 시간 / 예정일. 휴일 이월을 반영해 계산한다."""
        now = datetime.now()
        try:
            hh, mm = it["time"].split(":")
        except Exception:
            return ""
        hol = self.holidays()
        nd = next_fire_date(it, now.date(), hol)
        if nd == now.date():
            target = now.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
            if target < now:
                nd = next_fire_date(it, now.date() + timedelta(days=1), hol)
            else:
                mins = int((target - now).total_seconds() // 60)
                if mins < 60:
                    return T("약 %d분 후") % mins
                return T("약 %d시간 %d분 후") % (mins // 60, mins % 60)
        if nd is None:
            return T("예정 없음")
        days = (nd - now.date()).days
        return T("다음 알림 %s(%s) · %d일 후") % (
            nd.strftime("%m/%d"), WEEK_NAMES[nd.weekday()], days)

    # ---------------------------------------------------------- memo ops
    def _memo_changed(self, _e=None):
        self.lbl_memo_status.config(text=T("입력 중…"))
        if self.memo_job:
            self.after_cancel(self.memo_job)
        self.memo_job = self.after(400, self._memo_save)

    def _memo_save(self):
        self.data["memo"] = self.txt_memo.get("1.0", "end-1c")
        self._save()
        self.lbl_memo_status.config(
            text=T("자동 저장됨 · %s · %d자")
                 % (datetime.now().strftime("%H:%M"), len(self.data["memo"])))

    def memo_insert(self, text):
        self.txt_memo.insert("insert", text)
        self.txt_memo.focus_set()
        self._memo_save()

    def memo_stamp(self):
        self.memo_insert("\n[" + datetime.now().strftime("%m/%d %H:%M") + "] ")

    def memo_clear(self):
        if messagebox.askyesno(T("비우기"), T("메모 내용을 모두 지울까요?")):
            self.txt_memo.delete("1.0", "end")
            self._memo_save()

    def memo_export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[(T("텍스트 파일"), "*.txt")],
            initialfile="memo_%s.txt" % datetime.now().strftime("%Y-%m-%d"))
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.txt_memo.get("1.0", "end-1c"))

    # ---------------------------------------------------------- log ops
    def _add_log(self, item, result):
        if item.get("repeat") == "daily" or item.get("preview"):
            return
        self.data["logs"].insert(0, {
            "fired": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time": item.get("time", ""),
            "title": item.get("title", ""),
            "repeat": repeat_text(item) if item.get("repeat") else "-",
            "result": result,
        })
        self.data["logs"] = self.data["logs"][:300]
        self._save()
        self._refresh_logs()

    def _refresh_logs(self):
        holder = self.log_area.inner
        self._clear(holder)
        logs = self.data["logs"]
        self.lbl_log_status.config(text=T("실행 기록 %d건 (매일 반복 제외)") % len(logs))
        if not logs:
            tk.Label(holder, text=T("아직 기록이 없습니다. 반복이 '매일'이 아닌 일정이 실행되면 자동으로 기록됩니다."),
                     bg=CANVAS, fg=SUB, font=F(10), pady=48).pack()
            self.log_area.sync_wheel()
            return
        for i, l in enumerate(logs):
            if i:
                tk.Frame(holder, bg=BORDER, height=1).pack(fill="x")
            row = tk.Frame(holder, bg=CANVAS)
            row.pack(fill="x")
            cells = ((l["fired"], 20, "w", SUB, False),
                     (l["time"], 10, "center", TEXT, True),
                     (l["title"], 34, "w", TEXT, False),
                     (l["repeat"], 10, "center", SUB, False),
                     (T(l["result"]), 12, "center", SUB, False))
            for text, w, a, fg, bold in cells:
                tk.Label(row, text=text, width=w, anchor=a, bg=CANVAS, fg=fg,
                         font=F(9, bold), pady=11).pack(side="left", padx=(14, 0))
        self.log_area.sync_wheel()

    def log_export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[(T("CSV 파일"), "*.csv")],
            initialfile="reminder_log_%s.csv" % datetime.now().strftime("%Y-%m-%d"))
        if not path:
            return
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow([T("발생일시"), T("예정시각"), T("일정명"), T("반복"), T("처리")])
            for l in self.data["logs"]:
                w.writerow([l["fired"], l["time"], l["title"], l["repeat"], T(l["result"])])

    def log_clear(self):
        if messagebox.askyesno(T("기록 비우기"), T("실행 기록을 모두 삭제할까요?")):
            self.data["logs"] = []
            self._save()
            self._refresh_logs()

    # ---------------------------------------------------------- alarm flow
    def preview(self):
        self._show_alarm({"time": datetime.now().strftime("%H:%M"),
                          "title": T("알림 미리보기"),
                          "memo": T("이러한 형태로 전체화면 알림이 표시됩니다."),
                          "repeat": "daily", "preview": True})

    def alarm_monitor_index(self):
        """현재 선택된 알림 모니터 인덱스(0 = 주 모니터)."""
        try:
            return self.mon_values.index(self.dd_monitor.get())
        except Exception:
            return 0

    def _show_alarm(self, item):
        if self.alarm is not None:
            return
        self.alarm = AlarmWindow(self, item, self._alarm_closed)

    def _alarm_closed(self, item, result):
        self.alarm = None
        self._add_log(item, result)
        if result == "스누즈":  # i18n:skip
            self.pending.append((datetime.now() + timedelta(minutes=self.snooze_minutes()), item))

    def snooze_minutes(self):
        try:
            return max(1, min(120, int(self.data.get("snooze_min", 5))))
        except Exception:
            return 5

    def holidays(self):
        """'휴일' 탭 텍스트를 파싱한 날짜 집합(내용이 바뀔 때만 재계산)."""
        text = self.data.get("holidays", "")
        if text != self._hol_text:
            self._hol_text = text
            self._hol_set = parse_holidays(text)
        return self._hol_set

    def _active_today(self, item):
        return should_fire(item, datetime.now().date(), self.holidays())

    # ---------------------------------------------------------- loop
    def _tick(self):
        now = datetime.now()
        self.lbl_clock.config(text=now.strftime("%H:%M:%S"))
        week = WEEK_NAMES[now.weekday()]
        self.lbl_date.config(text=now.strftime("%Y. %m. %d") + " (" + week + ")")

        # 마지막 검사 이후 지나간 모든 분을 검사한다(절전 복귀·부하로 틱이 늦어도 놓치지 않음).
        # 알림 창이 떠 있어도 시각이 된 일정은 항상 대기열에 넣는다.
        cur_min = now.replace(second=0, microsecond=0)
        start = self._last_min + timedelta(minutes=1)
        if start < cur_min - timedelta(minutes=CATCHUP_MIN):
            start = cur_min - timedelta(minutes=CATCHUP_MIN)
        hol = self.holidays()
        added = False
        m = start
        while m <= cur_min:
            hhmm, day, d = m.strftime("%H:%M"), m.strftime("%Y-%m-%d"), m.date()
            for it in self.data["items"]:
                key = day + "|" + it["id"]
                if it["time"] == hhmm and key not in self.fired and should_fire(it, d, hol):
                    self.fired.add(key)
                    added = True
                    if in_quiet_hours(self.data.get("quiet", {}), hhmm):
                        self._add_log(it, "방해 금지로 건너뜀")  # i18n:skip
                        continue
                    self.pending.append((now, it))
            m += timedelta(minutes=1)
        self._last_min = max(self._last_min, cur_min)
        if added:
            self._save()          # fired 기록을 함께 저장(재시작 시 중복 알림 방지)

        if self.alarm is None:
            due = [p for p in self.pending if p[0] <= now]
            if due and in_quiet_hours(self.data.get("quiet", {}), now.strftime("%H:%M")):
                for p in due:                          # 방해 금지 중에는 다시 알림도 건너뜀
                    self.pending.remove(p)
                    self._add_log(p[1], "방해 금지로 건너뜀")  # i18n:skip
            elif due:
                first = min(due, key=lambda p: p[0])
                self.pending.remove(first)
                self._show_alarm(first[1])

        # 모니터 선택이 바뀌면 저장
        try:
            idx = self.alarm_monitor_index()
            if self.data.get("monitor", 0) != idx:
                self.data["monitor"] = idx
                self._save()
        except Exception:
            pass

        if cur_min != self._shown_min:
            self._shown_min = cur_min
            if self.tab == "schedule":
                self._refresh_items()          # (인사말도 함께 갱신)
            else:
                self._update_hello()
        self.after(1000, self._tick)

    # ---------------------------------------------------------- support / feedback
    def _build_support(self, parent):
        card = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        card.pack(fill="both", expand=True)
        area = ScrollArea(card.body, bg=CANVAS)
        area.pack(fill="both", expand=True, padx=1, pady=1)
        pad = tk.Frame(area.inner, bg=CANVAS)
        pad.pack(fill="both", expand=True, padx=30, pady=24)
        self._fb_q = queue.Queue()

        tk.Label(pad, text=T("무료로 만들고 있어요. 도움이 되셨다면 커피 한 잔 부탁드려요 ☕"),
                 bg=CANVAS, fg=SUB, font=F(10)).pack(anchor="w")

        # ── 후원
        tk.Label(pad, text=T("개발자 후원하기"), bg=CANVAS, fg=TEXT,
                 font=F(11, True)).pack(anchor="w", pady=(22, 4))
        tk.Label(pad, text=T("휴대폰 카메라로 QR을 찍거나, 버튼을 눌러 카카오페이 송금 페이지를 열어요."),
                 bg=CANVAS, fg=SUB, font=F(9), wraplength=620, justify="left").pack(anchor="w")
        row = tk.Frame(pad, bg=CANVAS)
        row.pack(fill="x", pady=(12, 0))
        try:
            self._qr_img = tk.PhotoImage(data=DONATE_QR_B64)
            tk.Label(row, image=self._qr_img, bg="white", bd=0,
                     padx=6, pady=6).pack(side="left")
        except Exception:
            pass
        right = tk.Frame(row, bg=CANVAS)
        right.pack(side="left", padx=20)
        tk.Label(right, text=T("금액은 자유예요. 후원금은 기능 개선에 쓰여요."), bg=CANVAS,
                 fg=TEXT, font=F(10), wraplength=360, justify="left").pack(anchor="w", pady=(0, 12))
        Pill(right, T("☕ 개발자 후원하기"), open_donate, fg="#191919", bg="#FEE500",
             border="", hover="#F5DC00", page_bg=CANVAS, size=10, bold=True, height=44,
             padx=24).pack(anchor="w")

        # ── 의견
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(24, 18))
        tk.Label(pad, text=T("개발자에게 의견 보내기"), bg=CANVAS, fg=TEXT,
                 font=F(11, True)).pack(anchor="w", pady=(0, 4))
        direct = bool(FEEDBACK_EMAIL)
        tk.Label(pad, text=T("버그, 원하는 기능, 불편한 점 무엇이든 좋아요.") + " " +
                 (T("개발자 메일로 바로 전달돼요.") if direct
                  else T("GitHub 이슈(공개)로 전달돼요.")),
                 bg=CANVAS, fg=SUB, font=F(9), wraplength=620, justify="left").pack(anchor="w")

        cats = tk.Frame(pad, bg=CANVAS)
        cats.pack(anchor="w", pady=(12, 8))
        self._fb_cat = "기능 제안"  # i18n:skip
        self._fb_chips = {}

        def pick(key):
            self._fb_cat = key
            for k, c in self._fb_chips.items():
                c.set(k == key)
        for key, label in (("기능 제안", T("기능 제안")), ("버그 신고", T("버그 신고")),  # i18n:skip
                           ("기타", T("기타"))):  # i18n:skip
            chip = ToggleChip(cats, label, page_bg=CANVAS, padx=18, on=(key == self._fb_cat),
                              command=lambda on, k=key: pick(k))
            chip.pack(side="left", padx=(0, 8))
            self._fb_chips[key] = chip

        box = RoundBox(pad, bg=CANVAS, page_bg=CANVAS, radius=16, height=130)
        box.pack(fill="x")
        box.pack_propagate(False)
        fb_font = F(11)
        self.txt_fb = tk.Text(box.body, font=fb_font, relief="flat", wrap="word", padx=14,
                              pady=10, bg=CANVAS, fg=TEXT, insertbackground=TEXT,
                              selectbackground=BLUE_SOFT, selectforeground=TEXT,
                              highlightthickness=0, bd=0, undo=True)
        self.txt_fb.pack(fill="both", expand=True)

        def fb_ime(_=None):
            try:
                bb = self.txt_fb.bbox("insert")
            except Exception:
                bb = None
            tune_ime(self.txt_fb, fb_font, bb[0] if bb else 14, bb[1] if bb else 10)
        self.txt_fb.bind("<KeyRelease>", fb_ime, add="+")
        self.txt_fb.bind("<FocusIn>", fb_ime, add="+")

        tk.Frame(pad, bg=CANVAS, height=8).pack()
        self.e_fb_reply = self._entry(pad, T("답장 받을 이메일 (선택)"), page_bg=CANVAS,
                                      on_return=lambda: None)
        self.chk_fb_log = None
        if direct:
            self.chk_fb_log = ToggleChip(pad, T("오류 기록(reminder_error.log)도 함께 보내기"),
                                         page_bg=CANVAS, padx=16, on=False)
            self.chk_fb_log.pack(anchor="w", pady=(10, 0))
            tk.Label(pad, text=T("오류 기록에는 PC 경로(사용자 이름)가 들어 있을 수 있어요."),
                     bg=CANVAS, fg=SUB, font=F(9)).pack(anchor="w", pady=(4, 0))

        bar = tk.Frame(pad, bg=CANVAS)
        bar.pack(fill="x", pady=(14, 0))
        self.lbl_fb = tk.Label(bar, text="", bg=CANVAS, fg=SUB, font=F(9), wraplength=420,
                               justify="left")
        self.lbl_fb.pack(side="left")
        self.btn_fb = Pill(bar, T("보내기"), self.send_feedback, fg="white", bg=BLUE,
                           border="", hover=BLUE_DEEP, page_bg=CANVAS, size=10, bold=True,
                           height=42, padx=28)
        self.btn_fb.pack(side="right")
        area.sync_wheel()

    def open_feedback(self):
        self.open_settings("support")

    def _fb_status(self, text, color=SUB):
        self.lbl_fb.config(text=text, fg=color)

    def send_feedback(self):
        msg = self.txt_fb.get("1.0", "end").strip()
        if len(msg) < 3:
            self._fb_status(T("내용을 입력해 주세요."), RED)
            return
        reply = self._value(self.e_fb_reply)
        cat = self._fb_cat
        if not FEEDBACK_EMAIL:                         # 공개 GitHub 이슈로 전달
            if not update_enabled():
                self._fb_status(T("의견을 받을 곳이 아직 설정되지 않았어요."), ORANGE)
                return
            webbrowser.open(feedback_issue_url(cat, msg))
            self._fb_status(T("GitHub 이슈 작성 화면을 열었어요. 이슈는 누구나 볼 수 있는 공개 글이니 개인정보는 적지 마세요."), GREEN_DEEP)
            return
        self._fb_status(T("보내는 중…"))
        with_log = bool(self.chk_fb_log and self.chk_fb_log.get())

        def work():
            self._fb_q.put((msg, cat, send_feedback_mail(cat, msg, reply, with_log)))
        threading.Thread(target=work, daemon=True).start()
        self.after(300, self._poll_feedback)

    def _poll_feedback(self):
        try:
            msg, cat, res = self._fb_q.get_nowait()
        except queue.Empty:
            self.after(300, self._poll_feedback)
            return
        if res == "activate":
            self._fb_status(T("첫 전송: 개발자 메일함의 FormSubmit 활성화 메일을 승인해 주세요."), ORANGE)
        elif res:
            self.txt_fb.delete("1.0", "end")
            self._fb_status(T("✓ 보냈어요. 감사합니다!"), GREEN_DEEP)
        else:
            self._fb_status(T("전송에 실패했어요. GitHub 이슈 작성 화면을 열게요."), RED)
            if update_enabled():
                webbrowser.open(feedback_issue_url(cat, msg))

    # ---------------------------------------------------------- general settings
    def _build_general(self, parent):
        card = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        card.pack(fill="both", expand=True)
        area = ScrollArea(card.body, bg=CANVAS)
        area.pack(fill="both", expand=True, padx=1, pady=1)
        pad = tk.Frame(area.inner, bg=CANVAS)
        pad.pack(fill="both", expand=True, padx=30, pady=24)

        def section(title, first=False):
            if not first:
                tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(20, 16))
            tk.Label(pad, text=title, bg=CANVAS, fg=TEXT,
                     font=F(11, True)).pack(anchor="w", pady=(0, 8))

        def line(label):
            r = tk.Frame(pad, bg=CANVAS)
            r.pack(fill="x", pady=4)
            tk.Label(r, text=label, bg=CANVAS, fg=TEXT, font=F(10), width=14,
                     anchor="w").pack(side="left")
            return r

        def hint(text):
            tk.Label(pad, text=text, bg=CANVAS, fg=SUB, font=F(9), wraplength=620,
                     justify="left").pack(anchor="w", pady=(4, 0))

        # ── 화면
        section(T("화면"), first=True)
        theme_opts = [("system", T("시스템 설정 따르기")), ("light", T("밝게")), ("dark", T("어둡게"))]
        lang_opts = [("auto", T("자동")), ("ko", T("한국어")), ("en", "English")]

        def pick_dropdown(row, opts, cur, key):
            labels = [t for _k, t in opts]
            by_label = {t: k for k, t in opts}
            cur_label = next((t for k, t in opts if k == cur), labels[0])
            dd = Dropdown(row, labels, cur_label, page_bg=CANVAS, width=200, height=40,
                          on_change=lambda v: self._set_pref(key, by_label.get(v)))
            dd.pack(side="left")
        pick_dropdown(line(T("테마")), theme_opts, self.data.get("theme", "system"), "theme")
        pick_dropdown(line(T("언어")), lang_opts, self.data.get("lang", "auto"), "lang")
        self.restart_box = tk.Frame(pad, bg=CANVAS)
        tk.Label(self.restart_box, text=T("변경 사항은 다시 시작하면 적용됩니다."), bg=CANVAS,
                 fg=ORANGE, font=F(9, True)).pack(side="left", padx=(0, 12))
        Pill(self.restart_box, T("지금 다시 시작"), self.restart_app, fg="white", bg=BLUE,
             border="", hover=BLUE_DEEP, page_bg=CANVAS, size=9, bold=True, height=34,
             padx=16).pack(side="left")

        # ── 시작
        if IS_WIN:
            section(T("시작"))
            self.chk_auto = ToggleChip(pad, T("Windows 시작 시 자동 실행 (트레이에서 조용히 시작)"),
                                       page_bg=CANVAS, on=autostart_enabled(), padx=16,
                                       command=self._toggle_autostart)
            self.chk_auto.pack(anchor="w")

        # ── 알림
        section(T("알림"))
        sn_labels = [T("%d분") % m for m in SNOOZE_CHOICES]
        cur_sn = self.snooze_minutes()
        Dropdown(line(T("다시 알림 간격")), sn_labels,
                 T("%d분") % cur_sn if cur_sn in SNOOZE_CHOICES else sn_labels[0],
                 page_bg=CANVAS, width=200, height=40,
                 on_change=lambda v: self._set_pref("snooze_min", int(re.sub(r"\D", "", v)))
                 ).pack(side="left")

        sound_opts = [("beep", T("기본 비프음")), ("chime", T("부드러운 알림음")), ("off", T("소리 끄기"))]
        srow = line(T("알림 소리"))
        by_label = {t: k for k, t in sound_opts}
        cur_sound = self.data.get("sound", "beep")
        Dropdown(srow, [t for _k, t in sound_opts],
                 next((t for k, t in sound_opts if k == cur_sound), sound_opts[0][1]),
                 page_bg=CANVAS, width=200, height=40,
                 on_change=lambda v: self._sound_changed(by_label.get(v, "beep"))
                 ).pack(side="left")
        Pill(srow, T("들어보기"), lambda: beep(SOUND_MODE), page_bg=CANVAS, size=9, height=36,
             padx=16).pack(side="left", padx=(10, 0))

        q = self.data.get("quiet", {})
        qrow = line(T("방해 금지"))
        self.chk_quiet = ToggleChip(qrow, T("사용"), page_bg=CANVAS, on=bool(q.get("on")),
                                    padx=16, command=lambda on: self._quiet_changed())
        self.chk_quiet.pack(side="left", padx=(0, 12))

        def hm(v, default):
            for cand in (v, default):
                try:
                    a, b = str(cand).split(":")
                    return int(a), int(b)
                except Exception:
                    continue
            return 0, 0
        sh, sm = hm(q.get("start"), "22:00")
        eh, em = hm(q.get("end"), "07:00")
        self.tf_q_start = TimeField(qrow, page_bg=CANVAS, hh=sh, mm=sm)
        self.tf_q_start.pack(side="left")
        tk.Label(qrow, text="~", bg=CANVAS, fg=SUB, font=F(12)).pack(side="left", padx=8)
        self.tf_q_end = TimeField(qrow, page_bg=CANVAS, hh=eh, mm=em)
        self.tf_q_end.pack(side="left")
        self.tf_q_start.on_change = self.tf_q_end.on_change = self._quiet_changed
        hint(T("방해 금지 시간에 울릴 알림은 화면에 띄우지 않고, 실행 기록에 '건너뜀'으로 남깁니다."))

        # ── 백업
        section(T("백업"))
        brow = tk.Frame(pad, bg=CANVAS)
        brow.pack(anchor="w")
        Pill(brow, T("내보내기 (.json)"), self.data_export, page_bg=CANVAS, size=10, height=40,
             padx=20).pack(side="left")
        Pill(brow, T("가져오기 (.json)"), self.data_import, page_bg=CANVAS, size=10, height=40,
             padx=20).pack(side="left", padx=(8, 0))
        hint(T("일정·메모·휴일·실행 기록·설정이 한 파일에 담깁니다. PC를 바꿀 때 가져오기로 옮기세요."))
        area.sync_wheel()

    def _set_pref(self, key, value):
        if value is None:
            return
        self.data[key] = value
        self._save()
        if key in ("theme", "lang"):
            self.restart_box.pack(anchor="w", pady=(10, 0))

    def _sound_changed(self, mode):
        self._set_pref("sound", mode)
        self._apply_sound()
        beep(mode)

    def _apply_sound(self):
        global SOUND_MODE
        SOUND_MODE = self.data.get("sound", "beep")

    def _quiet_changed(self):
        cfg = {"on": bool(self.chk_quiet.get()), "start": self.tf_q_start.get(),
               "end": self.tf_q_end.get()}
        if cfg != self.data.get("quiet"):
            self.data["quiet"] = cfg
            self._save()

    def _toggle_autostart(self, on):
        if not set_autostart(on):
            messagebox.showerror(T("시작 프로그램"), T("자동 실행 설정을 바꾸지 못했습니다."),
                                 parent=self.settings)
        self.chk_auto.set(autostart_enabled())

    def restart_app(self):
        """저장 후 새 프로세스로 다시 시작(테마·언어 적용용)."""
        try:
            self._memo_save()
            if self.hol_job:
                self._hol_save()
            env = dict(os.environ)
            env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"
            subprocess.Popen(_launch_command(), env=env, close_fds=True,
                             creationflags=0x00000008 | 0x00000200)
        except Exception as exc:
            messagebox.showerror(T("다시 시작"), T("다시 시작하지 못했습니다.\n\n%s") % exc,
                                 parent=self.settings)
            return
        if self.tray:
            self.tray.destroy()
        self.destroy()

    def data_export(self):
        path = filedialog.asksaveasfilename(
            parent=self.settings, defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="ddingdong_backup_%s.json" % datetime.now().strftime("%Y-%m-%d"))
        if not path:
            return
        self.data["memo"] = self.txt_memo.get("1.0", "end-1c")
        d = {k: v for k, v in self.data.items() if k not in ("fired", "update_checked")}
        d["_app"], d["_version"] = APP_NAME, APP_VERSION
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            messagebox.showerror(T("내보내기"), T("저장하지 못했습니다.\n\n%s") % exc, parent=self.settings)
            return
        messagebox.showinfo(T("내보내기"), T("백업 파일을 저장했습니다.\n\n%s") % path, parent=self.settings)

    def data_import(self):
        path = filedialog.askopenfilename(parent=self.settings,
                                          filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                new = normalize_data(json.load(f))
        except Exception:
            messagebox.showerror(T("가져오기"), T("올바른 백업 파일이 아닙니다."), parent=self.settings)
            return
        ans = messagebox.askyesnocancel(
            T("가져오기"),
            T("'예' : 현재 일정에 합치기 (같은 일정은 건너뜀)\n"
            "'아니오' : 파일 내용으로 덮어쓰기\n"
            "'취소' : 가져오지 않음"), parent=self.settings)
        if ans is None:
            return
        try:                                   # 되돌릴 수 있도록 현재 데이터를 따로 보관
            with open(DATA_PATH + ".before_import.json", "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        if ans:
            have = {i.get("id") for i in self.data["items"]}
            self.data["items"] += [i for i in new["items"] if i.get("id") not in have]
        else:
            keep = {k: self.data.get(k) for k in ("update_checked",) if k in self.data}
            self.data = new
            self.data.update(keep)
            self.data["fired"] = sorted(self.fired)
        self._apply_sound()
        self.txt_memo.delete("1.0", "end")
        self.txt_memo.insert("1.0", self.data.get("memo", ""))
        self.txt_hol.delete("1.0", "end")
        self.txt_hol.insert("1.0", self.data.get("holidays", DEFAULT_HOLIDAYS))
        self._save()
        self._refresh_items()
        self._refresh_logs()
        messagebox.showinfo(T("가져오기"), T("가져왔습니다. 테마·언어 같은 설정은 다시 시작하면 적용됩니다."),
                            parent=self.settings)

    # ---------------------------------------------------------- about / update
    def _build_about(self, parent):
        card = RoundBox(parent, bg=CANVAS, page_bg=CANVAS)
        card.pack(fill="both", expand=True)
        pad = tk.Frame(card.body, bg=CANVAS)
        pad.pack(fill="both", expand=True, padx=30, pady=26)

        row = tk.Frame(pad, bg=CANVAS)
        row.pack(fill="x")
        tk.Label(row, text=APP_NAME, bg=CANVAS, fg=TEXT, font=F(17, True)).pack(side="left")
        Pill(row, "v" + APP_VERSION, None, fg=BLUE, bg=BLUE_SOFT, border="",
             page_bg=CANVAS, size=9, bold=True, height=26, radius=13,
             padx=11).pack(side="left", padx=(10, 0))
        tk.Label(pad, text=T("정해둔 시각에 전체화면으로 알려주는 데스크톱 리마인더 + 메모장"),
                 bg=CANVAS, fg=SUB, font=F(10)).pack(anchor="w", pady=(6, 0))

        def section(title):
            tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(22, 14))
            tk.Label(pad, text=title, bg=CANVAS, fg=TEXT,
                     font=F(11, True)).pack(anchor="w", pady=(0, 10))

        section(T("업데이트"))
        self.chk_autoupd = ToggleChip(pad, T("시작할 때 하루 한 번 새 버전 확인"), page_bg=CANVAS,
                                      on=bool(self.data.get("auto_update", True)),
                                      padx=16, command=self._set_auto_update)
        self.chk_autoupd.pack(anchor="w")
        last = self.data.get("update_checked", "")
        if not update_enabled():
            msg = T("업데이트 저장소가 설정되지 않아 확인할 수 없습니다.")
        else:
            msg = (T("마지막 확인: ") + last) if last else T("아직 확인하지 않았습니다.")
        self.lbl_upd = tk.Label(pad, text=msg, bg=CANVAS, fg=SUB, font=F(10),
                                wraplength=640, justify="left")
        self.lbl_upd.pack(anchor="w", pady=(12, 0))
        btns = tk.Frame(pad, bg=CANVAS)
        btns.pack(anchor="w", pady=(12, 0))
        Pill(btns, T("지금 확인"), lambda: self.check_update(True), page_bg=CANVAS,
             size=10, bold=True, height=40, radius=None, padx=20).pack(side="left")
        self.btn_inst = Pill(btns, T("새 버전 설치"), self.install_update, fg="white",
                             bg=BLUE, border="", hover=BLUE_DEEP, page_bg=CANVAS,
                             size=10, bold=True, height=40, radius=None, padx=20)

        section(T("데이터"))
        tk.Label(pad, text=DATA_PATH, bg=CANVAS, fg=SUB, font=F(9), wraplength=640,
                 justify="left").pack(anchor="w")
        Pill(pad, T("폴더 열기"), self.open_data_folder, page_bg=CANVAS, size=10,
             height=38, radius=None, padx=18).pack(anchor="w", pady=(10, 0))

    def open_data_folder(self):
        try:
            os.startfile(BASE)
        except Exception:
            pass

    def _set_auto_update(self, on):
        self.data["auto_update"] = bool(on)
        self._save()

    def _upd_status(self, text, color=SUB):
        self.lbl_upd.config(text=text, fg=color)

    def check_update(self, manual=False):
        """새 버전 조회(백그라운드 스레드). 결과는 큐로 받아 메인 스레드에서 처리한다."""
        if not update_enabled():
            if manual:
                self._upd_status(T("업데이트 저장소(GITHUB_REPO)가 설정되지 않았습니다."), ORANGE)
            return
        if self._upd_busy:
            return
        self._upd_busy, self._upd_manual = True, manual
        if manual:
            self._upd_status(T("확인 중…"))

        def work():
            try:
                self._upd_q.put(("check", fetch_latest_release(), None))
            except Exception as exc:
                self._upd_q.put(("check", None, exc))
        threading.Thread(target=work, daemon=True).start()
        self.after(300, self._poll_update)

    def _poll_update(self):
        try:
            while True:
                self._on_update_msg(*self._upd_q.get_nowait())
        except queue.Empty:
            pass
        if self._upd_busy:
            self.after(300, self._poll_update)

    def _on_update_msg(self, kind, payload, err):
        if kind == "progress":
            self._upd_status(T("다운로드 중… %d%%") % payload, BLUE)
            return
        self._upd_busy = False
        if kind == "done":
            if err:
                self.btn_inst.pack(side="left", padx=(8, 0))
                self._upd_status(T("설치 실패: %s") % err, RED)
                messagebox.showerror(T("업데이트"), T("업데이트에 실패했습니다.\n\n%s") % err)
            else:
                self._finish_update(payload)
            return
        # kind == "check"
        if err:
            if self._upd_manual:
                self._upd_status(T("확인하지 못했습니다(네트워크 또는 저장소 설정 확인): %s") % err, RED)
            return
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["update_checked"] = stamp
        self._save()
        info = payload
        if parse_version(info["version"]) > parse_version(APP_VERSION):
            self.update_info = info
            self._upd_status(T("새 버전 v%s 이(가) 있습니다. (현재 v%s)") % (info["version"], APP_VERSION),
                             GREEN_DEEP)
            self.btn_inst.pack(side="left", padx=(8, 0))
            self._show_update_chip(info["version"])
            if self._in_tray and self.tray:
                self.tray.balloon(T("새 버전 v%s") % info["version"],
                                  T("설정 → 정보 · 업데이트에서 설치할 수 있습니다."))
            if self._upd_manual:
                self.open_settings("about")
                if messagebox.askyesno(T("업데이트"), T("새 버전 v%s 이(가) 있습니다.\n지금 설치할까요?")
                                       % info["version"], parent=self.settings):
                    self.install_update()
        else:
            self._upd_status(T("최신 버전입니다. (v%s · 확인 %s)") % (APP_VERSION, stamp))

    def _show_update_chip(self, ver):
        if self.upd_chip is not None:
            self.upd_chip.destroy()
        self.upd_chip = Pill(self.hdr_trow, T("새 버전 v%s") % ver, lambda: self.open_settings("about"),
                             fg="white", bg=ORANGE, border="", hover="#D9771A",
                             page_bg=CANVAS, size=8, bold=True, height=22, radius=11, padx=10)
        self.upd_chip.pack(side="left", padx=(8, 0), pady=(4, 0))

    def install_update(self):
        info = self.update_info
        if not info:
            return
        if not (FROZEN and info.get("asset_url") and info.get("sha256")):
            # 파이썬 스크립트로 실행 중이거나 검증 정보가 없으면 자동 설치 대신 릴리스 페이지를 연다
            page = info.get("page") if _trusted(info.get("page")) \
                else "https://github.com/%s/releases" % GITHUB_REPO
            webbrowser.open(page)
            return
        if self._upd_busy:
            return
        if not messagebox.askyesno(T("업데이트"), T("v%s 을(를) 내려받아 설치합니다.\n"
                                   "설치가 끝나면 앱이 자동으로 다시 시작됩니다. 계속할까요?")
                                   % info["version"], parent=self.settings):
            return
        self._upd_busy = True
        self.btn_inst.pack_forget()
        dest = sys.executable + ".new"

        def work():
            try:
                download_release(info, dest, lambda p: self._upd_q.put(("progress", p, None)))
                self._upd_q.put(("done", dest, None))
            except Exception as exc:
                self._upd_q.put(("done", None, exc))
        threading.Thread(target=work, daemon=True).start()
        self._upd_status(T("다운로드 중… 0%"), BLUE)
        self.after(300, self._poll_update)

    def _finish_update(self, new_path):
        try:
            self._memo_save()
            if self.hol_job:
                self._hol_save()
            apply_update(new_path)
        except Exception as exc:
            self._upd_status(T("설치 실패: %s") % exc, RED)
            messagebox.showerror(T("업데이트"), T("파일 교체에 실패했습니다.\n"
                                 "폴더 쓰기 권한을 확인해 주세요.\n\n%s") % exc)
            return
        if self.tray:
            self.tray.destroy()
        self.destroy()

    def _on_quit(self):
        if messagebox.askyesno(T("종료"), T("리마인더를 종료할까요?\n종료하면 알림이 동작하지 않습니다.")):
            self._memo_save()
            if self.hol_job:
                self._hol_save()
            if self.tray:
                self.tray.destroy()
            self.destroy()


def _fatal(exc_type, exc, tb):
    """.pyw 로 실행하면 오류가 보이지 않고 그냥 꺼진다.
    예외를 로그 파일로 남기고 메시지로 알려준다."""
    import traceback
    text = "".join(traceback.format_exception(exc_type, exc, tb))
    try:
        with open(os.path.join(BASE, "reminder_error.log"), "w",
                  encoding="utf-8") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + text)
    except Exception:
        pass
    try:
        messagebox.showerror(T("실행 오류"),
                             T("앱 실행 중 오류가 발생했습니다.\n"
                             "같은 폴더의 reminder_error.log 파일을 확인하세요.\n\n")
                             + text[-800:])
    except Exception:
        pass


if __name__ == "__main__":
    sys.excepthook = _fatal
    try:
        App().mainloop()
    except Exception:
        _fatal(*sys.exc_info())
