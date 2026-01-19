  # 🎮 디스코드 팀짜기 봇 (Team Maker Bot)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-5865F2?logo=discord&logoColor=white)

> 친구들과 내전할 때, 팀 나누기 귀찮으셨나요?  
> 음성 채널에 있는 멤버들을 버튼 하나로 편하게 나눠주는 봇입니다!

## ✨ 주요 기능 (Features)

- **🕹️ 간편한 팀 구성**: `!팀짜기` 명령어 하나로 음성 채널 인원을 불러옵니다.
- **📋 멤버 직접 선택**: 드롭다운 메뉴(Select Menu)를 통해 게임에 참여할 인원만 쏙 골라낼 수 있습니다.
- **🤖 봇 자동 필터링**: 노래 봇이나 관리 봇은 팀원 목록에서 자동으로 제외됩니다.
- **🎲 무한 다시 섞기**: 결과가 마음에 안 드나요? `[다시 섞기]` 버튼만 누르면 즉시 새로운 팀 조합을 보여줍니다. (기록 유지됨)
- **🔒 안전한 보안**: 환경변수(.env)를 사용하여 토큰을 안전하게 관리합니다.

## 🚀 설치 및 실행 방법 (Installation)

이 프로젝트를 로컬(내 컴퓨터)이나 서버에서 실행하려면 다음 절차를 따르세요.

### 1. 저장소 복제 (Clone)
```bash
git clone https://github.com/jeongho30/Discord-team-maker-bot.git
```
### 2. 패키지 설치
```Bash
pip install -r requirements.txt
```
### 3. 환경 변수 설정 (.env)
프로젝트 폴더에 `.env` 파일을 생성하고 아래 내용을 입력하세요.
```코드 스니펫
DISCORD_TOKEN=여기에_당신의_봇_토큰을_입력하세요
```
### 4. 봇 실행
```Bash
python main.py
```
## 🎮 명령어 사용법 (Usage)
| 명령어 | 설명 |
| :---: | :---: |
| `!팀짜기` | 현재 음성 채널에 있는 멤버들을 불러와 팀 구성을 시작합니다. |
| `!초대` | 봇을 내 서버로 초대할 수 있는 링크 버튼을 띄웁니다. |
## 🛠️ 개발 환경
- Language: Python 3.13
- Library: `discord.py 2.6.4`
- Tools: `python-dotenv 1.2.1`
