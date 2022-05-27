# 생물정보학 및 실습 1 Project
***
본 Repository는 서울대학교 생명과학부에서 수강한 **고급생물정보학 및 실습 1**의 과제물이다.   
본 Repository는 [Cell. 2012 Nov 9;151(4):765-777](https://doi.org/10.1016/j.cell.2012.10.019)의 분석을 재현하는 것을 기본으로, 3주 간의 공통 분석, 그 이후의 자유 분석에 대한 결과물이다.   
아래의 문서는 자유 분석에 관한 Introduction이다.   
***

## 1. 목적

**Lin28a의 Binding Motif들을 transcriptome-wide하게 파악해보기**
+ Binding Motif 찾기 (Fig S3C 재현)
+ Lin28a Binding Motif Predictor 만들기   

(혹시 같이 processing 할만하다고 판단된다면,)
+ Human LIN28A와 Binding Motif 비교하기 (외부 데이터 탐색)
+ Mouse Lin28b와 Binding Motif 비교하기 (외부 데이터 탐색)

## 2. Project 개요

### 2.1. Binding Motif 찾기
+ 이전 분석에서 사용한 BAM file 이용
+ Transcriptome에서 error가 많이 나오는 부분들 주변 서열을 모아서 문맥을 파악
+ WebLogo 등을 이용하여 시각화

### 2.2. Lin28a Binding Motif Predictor 만들기
+ **2.1. Binding Motif 찾기**에서 모은 Lin28a-bound Sequence들을 이용
+ 적합한 Machine Learning Model 탐색 (CNN, Random Rofest, KNN 등)
+ 모델 평가 (민감도, 특이도 등 평가)

### 2.3. (추가 분석) 외부 데이터셋 이용
**CLIP density / binding motif 등 비교**

본 논문 외의 Publicly Available CLIP Data를 탐색하여
+ Human LIN28A in [RNA. 2013 May; 19(5): 613–626.](https://doi.org/10.1261%2Frna.036491.112) (PAR-CLIP)
+ Mouse Lin28b in [RNA Biol. 2013 Jul 1; 10(7): 1146–1159.](https://doi.org/10.4161%2Frna.25194) (PAR-CLIP)
+ Human LIN28B in [RNA. 2013 May; 19(5): 613–626.](https://doi.org/10.1261%2Frna.036491.112) (PAR-CLIP) 또는 ENCODE eCLIP

등과 비교해보고자 함. (구체적인 데이터셋은 분석 중 변동될 수도 있음)