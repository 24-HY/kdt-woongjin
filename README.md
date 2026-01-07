# kdt-woongjin

지하철 실시간 열차위치정보 API ENDPOINT
http://swopenapi.seoul.go.kr/api/subway/sample/xml/realtimePosition/0/5/1호선


요청인자
변수명	타입	변수설명	값설명
KEY	String(필수)	인증키	OpenAPI 에서 발급된 인증키
TYPE	String(필수)	요청파일타입	xml : xml, xml파일 : xmlf, 엑셀파일 : xls, json파일 : json
SERVICE	String(필수)	서비스명	realtimeStationArrival
START_INDEX	INTEGER(필수)	요청시작위치	정수 입력 (페이징 시작번호 입니다 : 데이터 행 시작번호)
END_INDEX	INTEGER(필수)	요청종료위치	정수 입력 (페이징 끝번호 입니다 : 데이터 행 끝번호)
statnNm	STRING(필수)	지하철역명	지하철역명
출력값
No	출력명	출력설명
공통	list_total_count	총 데이터 건수 (정상조회 시 출력됨)
공통	RESULT.CODE	요청결과 코드 (하단 메세지설명 참고)
공통	RESULT.MESSAGE	요청결과 메시지 (하단 메세지설명 참고)
1	subwayId	지하철호선ID
(1001:1호선, 1002:2호선, 1003:3호선, 1004:4호선, 1005:5호선 1006:6호선, 1007:7호선, 1008:8호선, 1009:9호선, 1061:중앙선1063:경의중앙선, 1065:공항철도, 1067:경춘선, 1075:수인분당선 1077:신분당선, 1092:우이신설선, 1093:서해선, 1081:경강선, 1032:GTX-A)
2	updnLine	상하행선구분
(상행/내선, 하행/외선)
3	trainLineNm	도착지방면
(성수행(목적지역) - 구로디지털단지방면(다음역))
5	statnFid	이전지하철역ID
6	statnTid	다음지하철역ID
7	statnId	지하철역ID
8	statnNm	지하철역명
9	trnsitCo	환승노선수
10	ordkey	도착예정열차순번
(상하행코드(1자리), 순번(첫번째, 두번째 열차 , 1자리), 첫번째 도착예정 정류장 - 현재 정류장(3자리), 목적지 정류장, 급행여부(1자리))
11	subwayList	연계호선ID
(1002, 1007 등 연계대상 호선ID)
12	statnList	연계지하철역ID
(1002000233, 1007000000)
13	btrainSttus	열차종류
(급행,ITX,일반,특급)
14	barvlDt	열차도착예정시간
(단위:초)
15	btrainNo	열차번호
(현재운행하고 있는 호선별 열차번호)
16	bstatnId	종착지하철역ID
17	bstatnNm	종착지하철역명
18	recptnDt	열차도착정보를 생성한 시각
19	arvlMsg2	첫번째도착메세지
(도착, 출발 , 진입 등)
20	arvlMsg3	두번째도착메세지
(종합운동장 도착, 12분 후 (광명사거리) 등)
21	arvlCd	도착코드
(0:진입, 1:도착, 2:출발, 3:전역출발, 4:전역진입, 5:전역도착, 99:운행중)
22	lstcarAt	막차여부
(1:막차, 0:아님)


---


해당 데이터를 HTTP REST API로 호출해서 Supabase(Postgres DB)에 입력하게 하려고 해.

적재하는데 필요한 정보가 무엇인지 알려주고, 데이터의 컬럼명도 직관적(e.g. updnLine -> updown_line)이고 해당 데이터로 할 수 있는 데이터분석 리스트와 각 리스트의 개별 목적에 맞게 자세하게 분석 프로젝트로 세우고 싶어. 데이터분석의 목적은 원할한 지하철 운행이 되는지 모니터링하고 싶어.

신규 내부 프로젝트로 폴더를 만들어서 구축해줘.