import pandas as pd
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Azure OpenAI를 사용하는 객체 생성
chat = AzureChatOpenAI(
    deployment_name='배포 이름',
    model_name='모델 이름',
)

# 한국어 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            
            """ 당신은 간호기록 작성지를 작성해주는 전문가입니다. 다음의 의료기록을 분석하고 중간에 끊긴 문장이 있거나 오탈자가 있으면 알맞게 수정하고 NANDA 형식으로 출력하세요.
            한글로 작성하세요.
            """,
        ),
        ("human", "{medical_record}"),
    ]
)

# 프롬프트와 채팅 모델 결합
chain = prompt | chat  

# CSV 파일에서 데이터 불러오기
pd.read_csv("각 전처리한 파일 경로")

# 새로운 데이터셋
new_dataset = []

# 각 행 처리
for index, row in df.iterrows():
    response = chain.invoke({"medical_record": row['input']})
    new_dataset.append({'input': row['input'], 'output': response})
    print(response)
    

# 새로운 데이터셋을 DataFrame으로 변환
new_df = pd.DataFrame(new_dataset)

# 새로운 데이터셋을 CSV 파일로 저장
new_df.to_csv("저장하고 싶은 경로\\이름.csv", index=False, encoding='utf-8')
