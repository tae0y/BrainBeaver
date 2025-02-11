from expand.references.referencesservice import ReferencesService

class ReferencesHandler:
    """
    references 관련 요청을 처리한다.
    """
    def __init__(self):
        self.service = ReferencesService()
        # ...existing code...

    def reset_expand_keyconcpts(self):
        """
        expand_keyconcpts 테이블을 초기화한다.
        """
        self.service.reset_expand_keyconcpts()
        pass

    def expand_keyconcepts_with_websearch(self, options: dict):
        """
        주요개념 확장을 위해 웹검색을 수행하고 저장한다.
        """
        self.service.expand_keyconcepts_with_websearch(options)
        pass