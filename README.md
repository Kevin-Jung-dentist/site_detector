# 수서 빌라드지디 팝업 모니터링 (Site Detector)

이 프로젝트는 [수서 빌라드지디(suseovilladegd.com)](https://suseovilladegd.com/) 웹사이트의 팝업 카드가 업데이트되는 것을 감지하고, 변경 사항이 있을 때 GitHub 이슈를 통해 알림을 보내주는 GitHub Action 기반 모니터링 봇입니다.

## 🚀 어떻게 동작하나요?

1. **주기적 실행**: GitHub Action을 통해 6시간마다 자동으로 파이썬 스크립트(`monitor.py`)가 실행됩니다.
2. **팝업 데이터 수집**: BeautifulSoup을 이용해 메인 페이지에 떠 있는 팝업 이미지와 링크, 기간 등의 데이터를 수집합니다.
3. **변경점 비교**: 이전에 저장된 `popup_state.json` 파일의 데이터와 현재 데이터를 비교합니다.
4. **알림 전송 및 업데이트**: 변경이 감지되면 새로운 상태를 저장소에 커밋(`popup_state.json` 갱신)하고, **GitHub 이슈를 자동 생성**하여 이메일 등 알림을 받을 수 있게 해줍니다.

## ⚙️ 설정 방법 (사용자 가이드)

1. 이 프로젝트 파일들을 본인의 Github 저장소(Repository)에 **Push** 하거나 새 저장소를 만들어 업로드합니다.
2. 저장소의 **Settings(설정) -> Actions -> General** 로 이동합니다.
3. 스크롤을 내려 **Workflow permissions** 섹션에서 **Read and write permissions** 를 선택하고 저장합니다. (봇이 `popup_state.json` 파일을 커밋하고 이슈를 생성할 수 있도록 권한을 주는 과정입니다)
4. 완료되었습니다! 기본적으로 6시간마다 동작하며, 즉시 테스트해보고 싶다면 저장소의 **Actions** 탭에서 **Popup Monitor** 워크플로우를 선택하고 **Run workflow** 를 클릭하면 됩니다.

## 🔔 알림 방식 변경하기

기본적으로 GitHub 이슈가 생성되면 해당 저장소를 만든 사용자에게 GitHub에 등록된 이메일이나 앱으로 알림이 전송됩니다. 
만약 **텔레그램, 슬랙, 디스코드** 등으로 알림을 받고 싶다면 `.github/workflows/monitor.yml` 파일 하단에 Webhook 액션을 추가하고 파이썬 코드에서 해당 웹훅으로 메시지를 보내도록 수정할 수 있습니다.
