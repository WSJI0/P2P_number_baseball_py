# P2P_NumberBaseBall
Simple P2P(napster style) number baseball game  


## Environment
Windows
Python 3.6 ~

## requirements
pip install colorama (text color)


## File to run
server/regiServer.py (서버 실행파일)  
파일 안의 SERVER_IP 부분을 바꿔 사용하면 됩니다  
  
client/clientRUN.bat (클라이언트 실행파일)  
or  
python client.py [port]  
port는 9998(regiServer port)과 well-known port를 제외하고 사용 가능합니다  
파일 안의 SERVER_IP와 CLIENT_IP를 바꿔서 사용하면 됩니다


## User Commands
- help: client가 사용할 수 있는 command들의 목록과 간단한 설명을 출력합니다.

- list : 현재 online인 peer들의 목록을 출력합니다.

- list : 현재 같이 게임중인 peer들의 목록을 출력합니다.

- connect [peer] : 해당 peer와 게임을 시작합니다. 여기서 peer는 online peer list의 peer번호입니다.

- disconnect [peer] [peer] ... : 선택한 peer들과의 게임을 종료합니다. 여기서 peer는 connected peer list의 peer번호입니다.

- guess [peer] [your guessing number] : 해당 peer의 숫자를 추측합니다. 상대 peer는 이에 대한 답변을 돌려줍니다. 여기서 peer는 connected peer list의 peer번호입니다.

- logoff : 로그아웃

- block [peer] : 해당 peer와의 연결을 차단합니다. 여기서 peer는 online peer list의 peer번호입니다.
  
## How to play   
- 처음 client프로그램을 실행하면 자신의 숫자 3자리를 입력합니다. ex) 1 7 2  
- 이제 regiServer에 로그인되어 다른 peer들과 연결하여 게임을 할 수 있는 상태가 됩니다. 
- list명령어로 현재 online인 peer들의 목록을 가져온 후 connect 명령어로 선택한 peer와 게임을 시작합니다.
- connect명령어를 사용하지 않아도 다른 peer가 게임 연결 요청을 보내면 자동으로 수락됩니다. 이를 원치않으면 block명령어로 해당 peer를 차단하면 됩니다.
- conn명령어를 통해 현재 게임중인 peer들의 목록을 확인할 수 있습니다.
- guess명령어를 통해 현재 게임중인 peer들의 숫자를 맞출 수 있습니다.
- 해당 peer의 숫자를 추측하는 것이 끝났다면 disconnect명령어를 통해 연결을 끊을 수 있습니다. 이때 상대 peer가 플레이어의 숫자를 아직 추측하지 못했더라도 연결이 끊어지게 됩니다.
- 더 이상 게임을 하고 싶지않다면 logoff명령어를 통해 regiServer로 부터 로그아웃 할 수 있습니다.
  
## Protocols
- regiServer <-> peer
  - TCP  
  빠르게 응답을 처리할 필요가 없고, 속도보다는 데이터 무결성이 더 중요하다고 생각하였습니다.
  또한 server와 peer들간의 연결을 유지하여 만약 연결이 끊어진다면 해당 peer가 offline이 된것으로 간주하여 online peer list에서 해당 peer를 제외하게 됩니다.
  
- peer <-> peer
  - UDP
  delay에 크게 민감한 게임은 아니라고 생각하지만 TCP를 사용할 경우 각각의 연결마다 소켓을 유지해야하고,
  구현이 복잡해질것 같아서 UDP로 구현하였습니다. 다만 이 경우 게임중인 상대 peer가 갑자기 연결이 끊어져 버린다면 이를 바로 체크할 수는 없고 수동으로 disconnect 해줘야하는 문제점이 있습니다.


## Issues
- 갑자기 사라질 수 있는 peer
  - regiServer와는 연결 상태를 유지하기 때문에 갑자기 연결이 끊어지면 예외가 발생하여 server측에서는 해당 peer를 제외하게 됩니다. 하지만 peer와 peer간에는 일단 연결을 유지하지는 않기 때문에 갑자기 사라져도 알 수가 없습니다. 이는 regiServer가 peer가 사라질때마다 다른 peer들에게 알려주도록 구현하였습니다.

- Hack client
  - server측에서 게임을 돌리는 것이 아닌 client측에서 돌리는 것이기 때문에 나올 수 없는 숫자를 만들어내거나 일부로 계속해서 틀린 응답을 하도록 변조된 client프로그램을 사용하는 peer가 있을 수 있다고 생각하였습니다. 이 때 생각해낸 방법은 client에게 신고기능을 추가해 play log와 함께 server로 전송해 server에서 IP를 차단하는 방법, 그냥 단순히 사용자가 해당 peer를 차단하거나인데 server와의 소통을 줄이기 위해 후자를 선택하였습니다. 

- Console input
  - 입력과 출력이 서로 다른 쓰레드에서 동작하기 때문에 입력 도중에 출력이 발생하는등 꼬이는 경우가 생길 수 있습니다. 이 부분은 별도로 입력라인이 항상 최하단에 위치하도록 구현하였습니다.

- server와 peer간의 index 차이
  - 원래는 regiServer가 list가 아닌 dictionary로 peer들을 관리하고 이를 peer들에게 dictionary형태의 list를 제공하는 형태로 구현하였지만 peer입장에서 받은 list가 1, 2, 4, 7 과 같이 띄엄띄엄 있으면 보기 좋지 않을것 같아서 regiServer는 비어있는 index는 보내지않고 뒤에 peer들을 땡겨서 채워 넣어 보내도록 구현하였습니다. 이 때문에 regiServer와 peer간 유지하는 peer list의 index가 서로 다르기 때문에 다소 구현이 복잡해지고 모든 탐색 과정이 O(n)의 시간복잡도를 갖는등의 문제가 생겼지만 이 부분은 동접자수를 20으로 설정했기 때문에 크게 문제 되지않을거라고 생각하였습니다..