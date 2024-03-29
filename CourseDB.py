from Timeblock import *
import Course

class CourseDB():
    def __init__(self, path=""):
        self.course_list = [] # 여기에 강의 저장
        self.load_path = "Data/lecture.txt" # 강의 파일 저장 장소
        if path:
            self.load_path = path
        self.load_courses(self.load_path)

    def add(self, lecture):
        self.course_list.append(lecture)

    # 인자로 준 변수 기준 정렬.  ex) sort("course_id")
    def sort(self, option):
        self.course_list.sort(key=lambda x: getattr(x, option))
    
    # id로 강의검색 (테스트용으로 쓰임)
    def search_by_id(self, id):
        for c in self.course_list:
            if c.course_id == id:
                return c
    
    # 파일 읽어서 Course객체로 파싱 & 저장
    def load_courses(self, path=""):
        if path:
            _path = path
        else:
            _path = self.load_path
        with open('Data/lecture.txt', 'r', encoding='utf-8') as f:
            lecture_data = f.readlines()
            # 파일을 한 줄씩 읽어서 Course 객체한테 넘겨줌 -> Course 객체 안에서 파싱
            for i in range(len(lecture_data)):
                course = Course.Course(lecture_data[i].strip().split("$"))
                self.add(course)


    def search(self, condition):
        # 검색 버튼 누르면 호출되는 메서드
        #   condition : gui에서 사용자가 설정한 검색조건
        #   condition[0] : 대학명
        college = condition[0]
        #   condition[1] : 학과명
        dept_name = condition[1]
        #   condition[2] : 강의명
        title = condition[2]
        #   condition[3] : 요일 "일" ~ "월"
        day = condition[3]
        #   condition[4] : 교시
        period = condition[4]
        
        # 검색 방식
        # 일단 모든 강의를 담아두고,
        # condition[0]부터 condition[4]까지 차례차례 필터링한다 (일치하는 것만 거른다)

        # result : 리턴할 강의목록. 일단 모든 강의를 담아두고 시작함
        result = self.course_list[:]

        # 필터 함수 : 함수에 적힌 대로 강의 필터링 진행
        def checkCollege(course): # 대학 필터 : 강의와 전체 일치하면 True
            return course.college == college
        
        def checkDepartment(course): # 학과명 필터 : 강의와 전체 일치하면 True
            return course.department == dept_name
        
        def checkTitle(course): # 강의명 필터 : 강의명과 일부만 일치하면 True
            return title in course.title

        def checkDay(course): # 요일 필터 : 해당 요일이 강의 요일과 하나라도 일치하면 True
            for t in course.time:
                if t.day == day:
                    return True
            return False
        
        def checkPeriod(course): # 교시 필터 : 해당 교시가 course의 강의시간에 껴있으면 True
            period_to_min = (int(period) + 8) * 60
            for t in course.time:
                if t.startmin <= period_to_min < t.endmin:
                    # 해당 교시가 강의시간에 낀 경우
                    if (not day) or (day and t.day == day):
                        # 요일이 설정된 경우, 교시+요일 둘 다 겹치면 True
                        return True
            return False
        
        # 대학 검색 (ex. 대학(전체), 소프트웨어대학)
        if condition[0]:
            result = list(filter(checkCollege, result))

        # 학과명 검색 (ex. 소프트웨어학부)
        if condition[1]:
            result = list(filter(checkDepartment, result))

        # 요일 (ex. '월', '화')
        if condition[3]:
            result = list(filter(checkDay, result))

        # 교시 (ex. 1, 2)
        if condition[4]:
            result = list(filter(checkPeriod, result))

        # 강의명 (ex. ACT, AC, A) -> 연산 젤 많을 거 같아서 뒤로 뺐음
        if condition[2]:
            result = list(filter(checkTitle, result))

        return result

#pyinstaller 성능 이슈로 구문 주석 처리
'''
if __name__ == "__main__":
    # DB 테스트 코드
    db = CourseDB()
    # DB 로드
    with open('Data/lecture.txt', 'r', encoding='utf-8') as f:
        lecture_data = f.readlines()
        for i in range(len(lecture_data)):
        #for i in range(600, 900):
            course = Course.Course(lecture_data[i].strip().split("$"))
            db.add(course)
    # 검색 수행
    # 대학 학과명 강의명 요일 교시
    condition = ["", "", "AC", "월", "3"]
    results = db.search(condition)
    for r in results:
        print(r)
    print(len(db.course_list), len(results))
    pass
'''