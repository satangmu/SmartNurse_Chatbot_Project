import os
import pandas as pd
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema import HumanMessage, AIMessage

# Azure OpenAI를 사용하는 객체 생성
chat = AzureChatOpenAI(
    deployment_name='배포이름',
    model_name='모델이름',
    temperature=0.5
)



# 기본 프롬프트 템플릿 생성
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
# 예시 데이터
examples = [
    {"input": "비효과적 호흡 양상 환자의 간호기록 NANDA 양식으로 작성해줘.", "output": "환자 정보:\n\n이름: 이해준\n나이: 34세\n성별: 남성\n\n진단: 비효과적 호흡 양상 (NANDA-I #00032)\n\n주요 증상 및 특성:\n\n*호흡수 증가 (분당 24회)\n*호흡곤란 증상 (얕고 빠른 호흡)\n*산소포화도 감소 (92%)\n*환자의 주관적 호흡 불편 표현\n\n단기 목표:\n\n*환자의 호흡수가 24시간 이내에 분당 12~20회로 정상 범위 내로 감소\n*산소포화도가 95% 이상으로 유지\n\n장기 목표:\n\n*환자가 호흡 곤란을 호소하지 않고, 산소포화도가 지속적으로 95% 이상 유지\n*환자가 호흡에 관련된 자가 관리 방법을 이해하고 실행\n\n간호 계획 및 중재:\n\n*호흡 상태 모니터링: 2시간마다 호흡수, 산소포화도 체크\n*산소 요법: 의사의 지시에 따라 산소 공급 (필요 시)\n*호흡 운동 교육: 깊고 천천히 숨쉬기, 복식호흡법 교육\n*안위 제공: 편안한 자세 유지, 스트레스 감소 방법 안내\n*교육 및 상담: 호흡곤란의 원인과 관리 방법 설명\n\n간호 평가:\n*호흡 상태: 호흡수 및 산소포화도 변화 모니터링\n*환자의 자가 관리 능력: 호흡 운동 실시 여부 및 효과 평가\n*교육 효과: 환자의 이해도 및 반응 관찰"},
    {'input': "비효과적 기도 청결 환자의 간호기록 NANDA 양식으로 작성해줘.", "output": "환자 정보:\n 이름: 이상진\n 나이: 45세\n 성별: 남성\n\n진단: 비효과적 기도 청결 (NANDA-I #00031)\n\n주요 증상 및 특성:\n\n*가래 증가 및 점도 높음\n*기침 효과 감소\n*호흡 시 천명음\n*환자 호흡 불편 호소\n\n단기 목표:\n\n*24시간 내 가래 제거 용이\n*호흡 시 청결한 기도 유지\n\n장기 목표:\n\n*기도 청결 상태 유지\n*호흡 곤란 또는 가래 문제 불평 없음\n*자가 관리 능력 향상\n\n간호 중재:\n\n*호흡 상태 및 가래 상태 모니터링: 매 4시간마다 폐 청진 및 가래 양, 성질 확인\n*가습 요법: 적절한 수분 섭취 및 환경 가습 유지\n*기도 청소 지원: 체위 배액, 가슴 타진, 효과적 기침 기술 교육 및 실습\n*흡인 준비: 필요 시 즉각적인 흡인 가능하도록 기구 준비\n*환자 및 보호자 교육: 기도 청결 유지 방법, 중요성 설명\n\n간호 평가:\n\n*호흡 상태 변화: 호흡수, 청진 소견, 가래 양 및 성질 추적\n*자가 관리 능력: 기도 청결 유지 기술 실천 여부 및 효과 평가\n*교육 이해도: 환자 및 보호자의 반응 및 피드백 확인"},
    {'input': "가스 교환 장애 환자의 간호기록 NANDA 양식으로 작성해줘.", "output":"환자 정보:\n 이름: 정호석\n 나이: 32세\n 성별: 남성\n\n진단: 가스 교환 장애 (NANDA-I #00030)\n\n주요 증상 및 특성:\n\n*동맥혈 가스 분석 상 산소 포화도 88%, 이산화탄소 농도 상승\n*호흡곤란, 얕고 빠른 호흡 (분당 30회)\n*시안증, 창백함 관찰\n*환자 호흡 불편 호소\n\n단기 목표:\n\n*24시간 내 산소포화도 94-98% 범위 내 유지\n*호흡곤란 증상 감소\n\n장기 목표:\n\n*호흡 곤란 없이 안정된 가스 교환 상태 유지\n*호흡 관리 자가 수행 능력 향상\n\n간호 중재:\n\n*호흡 상태 및 산소포화도 모니터링: 정기적으로 호흡수, 산소포화도 체크\n*산소 요법: 의사 지시에 따라 산소 공급 조정\n*호흡 운동 및 체위 교육: 깊고 천천히 숨쉬기, 복식호흡법 교육 및 실습\n*스트레스 관리: 안정 및 휴식 촉진, 환자 불안 감소 기법 안내\n*환자 및 보호자 교육: 가스 교환 장애 원인, 중요성 및 자가 관리 방법 설명\n\n간호 평가:\n\n*호흡 상태 변화: 호흡수, 산소포화도 추적\n*자가 관리 능력: 호흡 운동 수행 여부 및 효과 평가\n*교육 이해도: 환자 및 보호자 반응 및 피드백 확인"},
    {'input': "낙상 위험 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 이윤아\n 나이: 67세\n 성별: 여성\n\n진단: 낙상 위험 (NANDA-I #00155)\n\n주요 증상 및 특성:\n\n*보행 불안정\n*균형 장애\n*약물 부작용 영향 (예: 진정제 사용)\n*시각 장애\n*환경적 위험 요소 (예: 미끄러운 바닥)\n\n단기 목표:\n\n*24시간 내 환자 안전한 이동 및 활동 유지\n*환자 및 보호자 낙상 예방 조치 이해 및 준수\n\n장기 목표:\n\n*입원 기간 낙상 없이 안전 유지\n*자가 관리를 통한 낙상 위험 최소화\n\n간호 중재:\n\n*낙상 위험 평가: 정기적 낙상 위험 평가 수행\n*환경 조정: 낙상 위험 감소 환경 조성 (예: 미끄럼 방지 매트, 적절한 조명 설치)\n*보행 보조기구 사용: 필요 시 보행 보조기구 제공 및 사용법 교육\n*약물 관리: 낙상 위험 증가 약물 모니터링 및 조정\n*교육 및 상담: 낙상 예방 방법 및 환경 안전 유지 교육\n\n간호 평가:\n\n*이동 능력: 보행 안정성 및 균형 유지 능력 평가\n*환경 안전성: 환경 안전 지속적 확인\n*교육 효과: 낙상 예방 조치 이해도 및 실행 여부 평가"},
    {'input': "불안정한 혈압 위험 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 이정호\n 나이: 55세\n 성별: 남성\n\n진단: 불안정한 혈압 위험 (NANDA-I 관련 진단 없음, 일반적 위험 진단 적용)\n\n주요 증상 및 특성:\n\n*혈압 변동성 (최근 측정치: 150/90 mmHg)\n*고혈압 및 저혈압 에피소드\n*현기증, 두통 또는 피로감 호소\n*약물 부작용 또는 기타 의학적 상태 영향\n\n단기 목표:\n\n*24시간 내 혈압 안정화 (목표 범위: 수축기 혈압 120-130 mmHg, 이완기 혈압 80-85 mmHg)\n*현기증 및 기타 증상 감소\n\n장기 목표:\n\n*장기적 혈압 안정 유지\n*자가 관리 능력 및 약물 복용 순응도 향상\n\n간호 중재:\n\n*혈압 모니터링: 매 4시간마다 혈압 측정 및 기록\n*약물 관리: 혈압 조절 약물 복용 모니터링 및 조정\n*환자 교육: 혈압 관리 및 생활 습관 조정 교육 (예: 저염식, 규칙적 운동)\n*스트레스 관리 기법 교육: 이완 기법, 호흡 운동 교육 및 실습\n*부작용 모니터링: 혈압 조절 약물의 부작용 감시 및 대응\n\n간호 평가:\n\n*혈압 변동 추적: 측정된 혈압 값 추적 및 변동성 평가\n*약물 순응도: 약물 복용 정확성 및 규칙성 평가\n*교육 효과: 환자 및 보호자의 이해도 및 생활 습관 변화 실행 여부 평가"},
    {'input': "근육 긴장 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 이재흰\n 나이: 35세\n 성별: 남성\n\n진단: 근육 긴장 (NANDA-I 관련 진단 없음, 일반적 증상 기반 진단 적용)\n\n주요 증상 및 특성:\n\n*근육 경직 및 불편감\n*통증 수준 중등도 (통증 점수 5/10)\n*일상 활동에서의 제한성\n*스트레스 및 피로도 증가\n\n단기 목표:\n\n*24시간 내 통증 점수 3/10 이하로 감소\n*근육 긴장 완화 및 이완 능력 향상\n\n장기 목표:\n\n*일상 활동 수행 시 통증 및 긴장 불평 없음\n*자가 관리를 통한 근육 긴장 관리 능력 향상\n\n간호 중재:\n\n*통증 및 근육 긴장 평가: 매 4시간마다 통증 점수 및 근육 상태 확인\n*근육 이완 기법 교육: 진정 호흡, 복식호흡법 교육 및 실습\n*온열 요법 적용: 온찜질 및 온수욕 적용 지시\n*스트레스 관리 기법 교육: 이완 기법, 명상 및 요가 실습 권장\n*일상 활동 조절: 과도한 근육 사용 피하기, 적절한 휴식 시간 제공\n\n간호 평가:\n\n*통증 및 근육 긴장 변화: 통증 점수 및 근육 상태 추적\n*이완 기법 실행 여부: 환자의 이완 기법 수행 능력 및 효과 평가\n*생활 습관 변화 실행 여부: 일상 활동 조절 및 스트레스 관리 기법 적용 여부 평가"},
    {'input': "충수염으로 인한 복통 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 전시연\n 나이: 30세\n 성별: 여성\n\n진단: 충수염으로 인한 복통 (NANDA-I #00132: 급성통증)\n\n주요 증상 및 특성:\n\n*오른쪽 하복부 통증 (통증 점수 7/10)\n*복부 압통 및 경직\n*체온 38°C\n*메스꺼움 및 식욕 부진\n\n단기 목표:\n\n*24시간 내 통증 점수 7/10에서 3/10 이하로 감소\n*체온 정상 범위(36.5°C - 37.2°C)로 유지\n\n장기 목표:\n\n*완전한 회복 및 일상 활동 복귀\n*장기적 건강 상태 및 영양 상태 개선\n\n간호 중재:\n\n*통증 관리: 정기적 통증 평가 및 의사 지시에 따른 진통제 투여\n*체온 모니터링: 매 4시간마다 체온 측정 및 기록\n*수술 후 간호: 수술 부위 청결 유지, 합병증 예방 조치 적용\n*환자 및 보호자 교육: 수술 후 관리 및 회복 과정 안내\n*영양 및 수분 섭취 관리: 적절한 식이 조정 및 수분 섭취 권장\n\n간호 평가:\n\n*통증 상태: 통증 점수 및 감소 추이 평가\n*체온 관리: 체온 변화 및 정상 범위 유지 여부 평가\n*회복 과정: 수술 부위 상태 및 합병증 발생 여부 확인"},
    {'input': "외상성 지주막하 출혈 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 한혜주\n 나이: 32세\n 성별: 남성\n\n진단: 외상성 지주막하 출혈 (NANDA-I 관련 진단 없음, 일반적 위험 진단 적용)\n\n주요 증상 및 특성:\n\n*의식 수준 변화 (반응성 감소)\n*두통 및 혼란\n*신경학적 결손 (예: 한쪽 팔다리의 약화)\n*혈압 및 맥박 변동\n\n단기 목표:\n\n*24시간 이내 의식 수준 및 반응성 향상\n*두통 및 신경학적 증상 감소\n\n장기 목표:\n\n*완전한 신경학적 회복 및 기능적 상태 회복\n*장기적 합병증 예방\n\n간호 중재:\n\n*신경학적 상태 모니터링: 정기적 의식 수준, 동공 반응, 운동 기능 체크\n*혈압 및 맥박 관리: 지속적 혈압 및 맥박 모니터링, 조절\n*두통 관리: 의사 지시에 따른 진통제 투여, 편안한 환경 유지\n*합병증 예방: 체위 변경, 욕창 예방 조치 적용\n*환자 및 가족 교육: 상태, 예상 회복 과정 및 가능한 합병증에 대한 정보 제공\n\n간호 평가:\n\n*신경학적 상태 변화: 의식 수준, 운동 기능, 동공 반응 평가\n*합병증 발생 여부: 욕창, 폐렴 등 합병증 감시 및 대응\n*치료 반응: 혈압 및 맥박 조절 효과, 두통 관리 효과 평가"},
    {'input': "당뇨 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 박선호\n 나이: 50세\n 성별: 남성\n\n진단: 당뇨병 (NANDA-I #00179 - 혈당 불안정 위험)\n\n주요 증상 및 특성:\n\n*혈당 수치 변동성 (최근 측정: 공복 혈당 180 mg/dL)\n*증가된 갈증 및 빈뇨\n*체중 감소\n*피로감\n\n단기 목표:\n\n*24시간 내 혈당 수치 80-130 mg/dL 범위 내로 유지\n*탈수 증상 및 체중 감소 방지\n\n장기 목표:\n\n*장기적 혈당 조절 유지\n*당뇨병 관련 합병증 예방\n\n간호 중재:\n\n*혈당 모니터링: 정기적 혈당 측정 및 기록 (하루 4회)\n*식사 계획 및 교육: 균형 잡힌 식단, 식사 일정 교육\n*운동 계획: 규칙적인 운동 권장 및 환자의 운동 능력 평가\n*약물 관리: 당뇨병 약물 복용 지도 및 모니터링\n*환자 및 가족 교육: 혈당 관리, 당뇨병 합병증 예방 교육\n\n간호 평가:\n\n*혈당 수치 변화: 측정된 혈당 값 추적 및 변동성 평가\n*식이 및 운동 계획 준수 여부: 식사 및 운동 계획 실행 평가\n*약물 복용 순응도: 약물 복용 정확성 및 규칙성 평가"},
    {'input': "무릎관절증 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 이희주\n 나이: 60세\n 성별: 여성\n\n진단: 무릎관절증 (NANDA-I 관련 코드 없음, 일반적 증상 기반 진단 적용)\n\n주요 증상 및 특성:\n\n*무릎 관절 통증 및 부종\n*관절 운동 범위 제한\n*보행 시 불편감\n*일상 활동 중 통증 증가\n\n단기 목표:\n\n*24시간 내 통증 점수 7/10에서 4/10 이하로 감소\n*관절 운동 범위 개선\n\n장기 목표:\n\n*장기적 통증 관리 및 관절 기능 향상\n*일상 활동 시 통증 최소화\n\n간호 중재:\n\n*통증 평가: 정기적 통증 점수 평가 및 기록\n*냉찜질 및 온찜질 적용: 통증 및 부종 감소를 위한 냉/온찜질 적용\n*관절 보호 교육: 관절 보호 기법 및 적절한 체위 지도\n*가벼운 운동 교육: 관절 운동 범위 개선을 위한 가벼운 스트레칭 및 운동 교육\n*통증 관리 약물: 의사 지시에따른 진통제 투여\n\n간호 평가:\n\n*통증 수준 변화: 통증 점수 추적 및 감소 평가\n*관절 운동 범위: 운동 후 관절 운동 범위 개선 여부 평가\n*일상 활동 수행 능력: 통증 관리 후 일상 활동 수행 능력  평가"},
    {'input': "퇴행성 관절염 환자의 간호기록 NANDA 양식으로 작성해줘.","output":"환자 정보:\n 이름: 이희전\n 나이: 65세\n 성별: 남성\n\n진단: 퇴행성 관절염 (NANDA-I 관련 코드 없음, 일반적 증상 기반 진단 적용)\n\n주요 증상 및 특성:\n\n*지속적인 관절 통증 및 강직\n*일상 활동 중 불편감 및 기능 제한\n*부종 및 관절의 변형\n*운동 시 관절의 삐걱거림\n\n단기 목표:\n\n*24시간 내 통증 점수 7/10에서 4/10 이하로 감소\n*일상 활동 중 통증 관리 향상\n\n장기 목표:\n\n*장기적 관절 기능 유지 및 통증 관리\n*자가 관리 능력 및 생활 질 향상\n\n간호 중재:\n\n*통증 및 강직 평가: 정기적으로 통증 점수 및 강직 정도 평가\n*물리치료 협력: 물리치료사와 협력하여 관절 운동 프로그램 구성\n*교육 및 상담: 관절 보호 기법 및 적절한 운동 방법 교육\n*약물 관리: 의사 지시에 따른 항염증제 및 진통제 투여\n*생활 습관 조정: 체중 관리 및 균형 잡힌 식단 권장\n\n간호 평가:\n\n*통증 및 기능 상태: 통증 감소 및 일상 활동 수행 능력 평가\n*물리치료 효과: 물리치료 후 관절 운동 범위 및 강직 개선 평가\n*약물 복용 순응도 및 효과: 항염증제 및 진통제 복용 및 효과 평가"},
]



# FewShotChatMessagePromptTemplate 인스턴스 생성
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

# 추가 지침
instruction = """
You are a nurse working in a general hospital. Answer the question, adhering to the following guidelines:
1. Write in Korean
2. Utilize the information available in the prompt. If relevant information is not found there, then seek answers through other channels.
3. Use precise and concise language. Use endings like 음, 함, 임.
4. Fill out patient information in order
5. Necessary to include '주관적자료/객관적자료', '단기목표/장기목표', '간호계획' '간호중재', '간호평가'
6. Create a fictional patient's information.
7. Be as specific as possible.
8. Record precise measurements.
9. Use bullet points for the description instead of using numeric order.
10.Fill in the patient's name, age, and gender, but no other personal information.
11. Give it a different name ex) 김현중, 구진성, 홍선우, 조아라, 최승우, 남하늘, 신영태...
"""



# 최종 프롬프트 템플릿 생성
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instruction),
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)



# 체인 구성
chain = final_prompt | chat

# CSV 파일에서 데이터 불러오기
df = pd.read_csv("csv 파일 경로")

# 새로운 데이터셋
new_dataset = []

# 각 행 처리
for index, row in df.iterrows():
    user_question = row['disease name'], "환자의 간호기록 NANDA 양식으로 작성해줘."  # CSV 파일의 'input' 열에서 질문을 가져옴
    message = HumanMessage(content=user_question)
    response = chain.invoke({"input": user_question, "output": ""})
    new_dataset.append({'input': user_question, 'output': response.content})
    print(response)

# 새로운 데이터셋을 DataFrame으로 변환
new_df = pd.DataFrame(new_dataset)

# 새로운 데이터셋을 CSV 파일로 저장
new_df.to_csv("저장 경로", index=False, encoding='utf-8')
