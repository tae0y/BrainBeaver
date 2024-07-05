from llm.llmroute import query_with_context
from concurrent.futures import ThreadPoolExecutor
from common.file import get_plaintext_from_filepath

def split_file_into_keyconcept(file_list: list) -> list[dict]:
    keyconcept_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(extract_keyconcept, file_list)
        for result in results:
            keyconcept_list.extend(result)

    #print('> split_file_into_keyconcept :: '+str(keyconcept_list))
    return keyconcept_list


def extract_keyconcept(file_path):
    try:
        #너무다 다양한 인코딩이 존재함 : None, ascii, windows-1254, windows-1253, euc-kr, utf-8 등
        file_content = get_plaintext_from_filepath(file_path)

        #print('------------------------------------------------------------------')
        print(f"{file_path} (len:{len(file_content)})")

        role = """[ROLE]
        당신은 탁월한 문서 요약 전문가입니다.
        """
        query = """[SYSTEM]
        다음 제시된 문서는 개인적으로 학습한 내용을 정리한 것입니다.
        회고를 돕고 새로운 아이디어를 얻을 수 있도록, 주요내용을 요약하려고 합니다.
        첫째, 핵심되는 내용들을 한 문단으로 작성하세요.
        둘째, 반드시!! 다음 제시된 문서의 내용만을 기준으로 작성하세요.

        다음 응답포맷에 따라 JSON 형식으로 답변하세요.
        {
            "title"    : "명사형으로 끝나는 한 줄 이내의 제목",
            "keywords" : "key1,key2,key3 등 문서에서 추출한 키워드",
            "category" : "정보,감상,질문,착안 중에서 카테고리 선택",
            "summary"  : "기억해둘만한 주요 내용을 한 문단 이내 작성",
        }

        [DOCUMENT]
        """
        context = file_content #TIP: 맥락정보를 유지하기 위해 파일경로(분류) 및 제목 포함
        response_list = query_with_context(role + query, file_path, context) #파일경로(분류), 파일제목, 파일내용
        for response in response_list:
            response['filepath'] = file_path
            response['plaintext'] = file_content
        #print('> extract_keyconcept :: '+str(response_list))

    except Exception as e:
        print(f"extract_keyconcept error: file_path - {e}")
        response_list = []

    return response_list