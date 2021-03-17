## 무비판

추천시스템에 기본이라고 할 수 있는 영화데이터를 가지고 Django framework 영화 추천 웹서비스 구현

URL = http://alswhddh.pythonanywhere.com/

![메인페이지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FckME4K%2Fbtq0nO6v6dA%2FOxFrqUCiAC125mGTmcEyvk%2Fimg.png)

<br><br>
### 1. 프로젝트 목표
 - 영화 월드컵을 통한 컨텐츠 기반 추천 시스템 구현
 - 영화 평점을 통한 사용자/아이템 기반 협업 필터링 구현

<br><br>
### 2. 데이터 소개
 - 데이터 출처 : 무비렌즈 ( https://grouplens.org/datasets/movielens/ )
 - 포스터 링크 및 한국어 소개 : 네이버 영화 API 사용
 
 총 영화: 7239 개 <br>
 평가 유저 : 610명 <br>
 평가 수 : 66,000개의 평가 데이터를 활용 <br>
 
 <아쉬운 점><br>
 원본 데이터는 9천개의 영화데이터가 있었으나 영어였음,<br>
 네이버 API를 사용해서 한국어로 전부 merge 하는 과정에서 약 2천개의 영화가 날라감<br>
 그에 따른 평가 수도 10만개에서 6만개로 줄어듬 <br>

<br><br>
### 3. 회원 가입
 - 개인화된 추천 시스템 협업필터링을 사용하기 위해서 회원가입 구현
 - 기존에 있던 610명의 유저/평점데이터 를 보존하기 위해 더미로 610명의 회원 가입

<br><br>
### 4. 이상형 월드컵
 ![이상형 월드컵](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FUxYhf%2Fbtq0nOrThdD%2FKuegK1xOunv85V7evTP840%2Fimg.png)
 
 - 영화 월드컵에서 우승을 많이한 영화
 
 ![우승 많이한 영화](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F9juTS%2Fbtq0ehpfz8T%2FNPNKbdXGl9sPgOganrCd4K%2Fimg.png)

 영화 월드컵이 끝날 때마다 우승 횟수를 카운트 해줘서 우승 횟수가 많은 순으로 보여준다.
 
<br><br>
### 5. 콘텐츠 기반 추천

 - 영화 월드컵에서 우승한 영화와 비슷한 장르 추천
 
  ![비슷한 장르](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fc2eChK%2Fbtq0iXi45QC%2FngZQs1BdBBuf0sYMpKNGF0%2Fimg.png)
 
 - 같은 감독 작품 추천
  ![같은 감독](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FsvBao%2Fbtq0g0OgqS4%2FU31ylywWeCxIV4iYtGeYr0%2Fimg.png)
 
 - 같은 배우 추천
  ![같은 배우](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbWumiN%2Fbtq0kEJ8HKz%2FCOcwkklNNVXYay3mVsTODk%2Fimg.png)

<br><br> 
### 6. 영화 평가하기
![평가하기](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FwCLXf%2Fbtq0jMVRWjj%2F3hkXDB3kdtL92o18LFZMb1%2Fimg.png)

 0.5 ~ 5 점 까지 평점을 매길 수 있다.
 
 참고 : 왓차피디아 평가하기
 
<br><br>
### 7. 협업 필터링 

 - 영화 월드컵에서 우승한 영화와 가장 비슷한 영화 중 영화 평점기반 순위
  ![우승영화기반](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbneNBo%2Fbtq0fldUSWm%2F8jJntFD5rba3FzfRm4Zi3k%2Fimg.png)
  
 - 아이템 기반 협업 필터링 ( 예상 평점 기반 순위 )
 
  ![아이템기반](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb5gpav%2Fbtq0g0AyXbp%2FWNsSt6131nvlJ1bWRCAOyk%2Fimg.png)
  
 - 유저 기반 협업 필터링 ( 예상 평점 기반 순위 )
 
 ![유저기반](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbn7RM9%2Fbtq0fjHawBZ%2FxgDuHSbPrBWbeJipqozrTK%2Fimg.png)
 
<br><br>
### 8 . 결론 느낀 점

python 에서만 구혔했던 추천시스템을 웹으로 구현할 수 있다.<br>
가벼운 유사도 기반 알고리즘만 사용했지만 다른 추천 시스템도 충분히 웹으로 구현이 가능할 것 같다.<br>
 
정답이 없는 추천 시스템 <br>
추천 시스템은 정답이 없기 때문에 어느 정도 납득이 되는 지로 평가를 하게 되는 데 <br>
테스트를 많이 해보았지만 납득이 되는 추천도 있었고 납득이 되지 않는 추천도 있었다.

cold start 문제 <br>
내가 사용한 영화는 7천개 이다. 7천개 중 비주류 영화가 대부분이고 비주류 영화를 추천하면 사람들은 보지 않을 것이다.<br>
그렇다고 인기 영화만 추천하면 매번 비슷비슷한 추천이 나올 것 이다. <br>
그래서 난 1995년 이상 영화만 추천해주도록 제한을 두었다. 이 방법이 옳은 방법은 아니지만 일단 이 것으로 대체했다.<br>
추천시스템에서 역시 cold start 는 어려운 문제인 것 같다.<br>