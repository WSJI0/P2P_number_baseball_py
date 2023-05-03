# P2P_NumberBaseBall
Simple P2P(napster style) number baseball game  


## Environment
Windows
Python 3.6 ~


## File to run
server/regiServer.py (서버 실행파일)  
client/client.py (클라이언트 실행파일)


## User Commands
- help: client가 사용할 수 있는 command들의 목록과 간단한 설명을 출력합니다.

- online_users: 자신을 제외한 현재 online인 peer들의 목록을 출력합니다.

- 현재 online인 peer들과 게임을 시작합니다.

- disconnect [peer] : 선택한 peer와의 게임을 종료합니다.

- guess [peer] [your guessing number] : 해당 peer의 숫자를 추측합니다. 상대 peer는 이에 대한 답변을 돌려줍니다.

- logoff : send a message (notification) to regiServer for logging off 

## Protocols
- regiServer <-> peer
  - TCP  
  빠르게 응답을 처리할 필요가 없고, 속도보다는 데이터 무결성이 더 중요하다고 생각하였습니다.
  
- peer <-> peer
  - TCP
  마찬가지로 속도보다는 데이터 무결성이 더 중요하다고 생각해서 UDP가 아닌 TCP 프로토콜을 선택하였습니다.



## Issues
  
- Hack client
  - server측에서 게임을 돌리는 것이 아닌 client측에서 돌리는 것이기 때문에 나올 수 없는 숫자를 만들어내거나 일부로 계속해서 틀린 응답을 하도록 변조된 client프로그램을 사용하는 peer가 있을 수 있다고 생각하였습니다. 이 때 생각해낸 방법은 client에게 신고기능을 추가해 play log와 함께 server로 전송해 server에서 IP를 차단하는 방법, 그냥 단순히 client에게 차단 기능을 부여하는 방법이었는데 최대한 server와의 소통을 줄이자 생각해서 후자로 선택하였습니다.
