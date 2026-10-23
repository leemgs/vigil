# ARR Responsible NLP Research Checklist — VIGIL (ACL 2027)

작성일: 2026-10-23. 이 파일은 논문 빌드에 포함되지 않습니다.
ARR 제출 폼에 그대로 옮겨 적을 수 있도록, 항목별 답·근거 위치·영문 서술 초안을 정리했습니다.
질문 목록은 공식 페이지(aclrollingreview.org/responsibleNLPresearch)에서 가져왔습니다.

**왜 중요한가:** ARR은 관련 질문에 **근거 섹션이나 사유를 체계적으로 제시하지 않은 제출물을 desk reject**합니다.
"No"라고 답해도 되지만, 반드시 사유를 적어야 합니다. "No" 자체는 거절 사유가 아닙니다.

섹션 번호는 현재 빌드(`main.aux`) 기준입니다. Limitations와 Ethical Considerations는 번호 없는 섹션입니다.
본문 §1–§8, 부록은 다음과 같습니다.
A 트리아지·보고서 평가 / B 엣지 추출 / C P2 / D 오류 전파 / E ablation / F 이론·보정·backbone / G 하이퍼파라미터·모델 / H P1

`[AUTHORS: …]`는 원고에 근거가 없어 저자가 채워야 하는 부분입니다. 임의로 채우지 않았습니다.

---

## A. 모든 제출물

| 항목 | 답 | 근거 위치 | 비고 |
|---|---|---|---|
| A1 한계 서술 | Yes | Limitations | |
| A2 위험 논의 | Yes | Ethical Considerations ("Risks of misuse and over-reliance", "Decision-support boundary") | |

## B. 과학적 산출물(artifact)

| 항목 | 답 | 근거 위치 | 비고 |
|---|---|---|---|
| B1 출처 인용 | Yes | §3.2, §3.4, §5.1, §6, App. G, H | CourtListener, CAP, CONAN, LegalBERT, bge, Llama-3.1, BM25 |
| B2 라이선스·이용 조건 | Yes (부분) | Ethical Considerations ("Data governance") | **보완 필요:** P1 파일럿이 쓴 CAP와 CONAN의 이용 조건이 원고에 없습니다. |
| B3 의도된 용도 | Yes | Ethical Considerations ("Data governance": research use, not automated legal decisions; P2 citator under institutional subscription) | |
| B4 개인정보·불쾌 콘텐츠 | Yes (부분) | Ethical Considerations ("Data governance": party/counsel names from public filings, no other personal information) | 불쾌 콘텐츠 점검 여부는 서술 없음 → 아래 초안 |
| B5 산출물 문서화 | Yes | §4.1, Table 2, Limitations ("Extractor quality…": U.S.-federal, large-defendant skew) | |
| B6 통계·분할 | Yes | §4.1, Table 2, §5.1 | |

**B2 보완 초안:** `[AUTHORS: state the terms of use of the Caselaw Access Project data and of the Constitution Annotated table used in the P1 pilot (App. H), and confirm the pilot complies with them.]`

**B4 초안 (불쾌 콘텐츠):** "Records are public U.S. federal court filings; we did not filter offensive content because the released data consist of docket metadata and machine-generated summaries. `[AUTHORS: confirm, or describe any screening performed.]`"

## C. 계산 실험

| 항목 | 답 | 근거 위치 | 비고 |
|---|---|---|---|
| C1 파라미터 수·총 연산량·인프라 | **No (부분)** | App. G ("Models, compute, and software") | 총 연산량이 원고에 없음 |
| C2 실험 설정·하이퍼파라미터 | Yes | §5.1, App. G (Table: hyperparameters; "Runs and seeds") | 임계값은 validation으로 튜닝, `w(·)`는 고정 schedule |
| C3 기술통계(오차 막대 등) | Yes (부분) | Limitations ("Statistical uncertainty"), App. F (mean ± std over five runs), App. E | 주요 비교는 점추정이며 CI 없음. P0 실험 후 갱신 |
| C4 사용 패키지·설정 | Yes (부분) | App. G | 패키지 버전은 공개 코드의 의존성 파일에만 있음 |

**C1 사유 초안:** "Parameter counts are reported for open models (Llama-3.1-70B; App. G). GPT-4o and the OpenAI embedding model are accessed through an API, and their parameter counts are not public. `[AUTHORS: total API calls or tokens, and GPU type and hours for the Llama-3.1-70B run.]`"

**C3 사유 초안:** "Main comparisons are point estimates without confidence intervals (Limitations, 'Statistical uncertainty'); run-level mean ± std over five seeds are reported in App. E–F."
→ P0 bootstrap CI를 넣으면 "Yes"로 바꿉니다.

**C4 보완 권장:** BM25 구현, re-ranker 모델, conformal 보정 코드의 이름과 버전을 App. G에 한 줄로 적습니다. `[AUTHORS: package names/versions]`

## D. 사람 주석자

| 항목 | 답 | 근거 위치 | 비고 |
|---|---|---|---|
| D1 지시문 전문 | **No** | §4.2, Ethical Considerations ("Annotators and raters") | 가이드라인은 데이터셋과 함께 공개하며, 논문에는 싣지 않음 |
| D2 모집·보상 | Yes | Ethical Considerations ("Annotators and raters": institutional staff within regular paid duties) | |
| D3 동의 | Yes | Ethical Considerations ("Annotators and raters": written task description, verbal consent recorded) | |
| D4 윤리 심의 | Yes | Ethical Considerations ("Annotators and raters": determined not to be human-subjects research under institutional policy) | |
| D5 주석자 인구통계 | **No** | — | 서술 없음 |

**D1 사유 초안:** "The full annotation guidelines, including the task description given to annotators, are released with the dataset in the supplementary material."

**D5 사유 초안:** `[AUTHORS: either report basic characteristics (e.g., legal-research specialists in <country>, years of experience), or justify omission, e.g., the group is small (three annotators, two raters) and reporting demographics could identify them.]`

## E. AI 도구 사용

| 항목 | 답 | 근거 위치 |
|---|---|---|
| E1 AI 도구 사용 공개 | Yes | Ethical Considerations ("Use of AI assistants") |

---

## 제출 전 저자 할 일 요약

1. **C1:** 총 연산량(API 호출·토큰, GPU 종류·시간)을 기재합니다.
2. **B2:** CAP·CONAN 이용 조건을 확인하고 Ethics에 한 문장을 추가합니다.
3. **D5:** 주석자 특성을 보고하거나 생략 사유를 적습니다.
4. **C4:** 패키지 이름과 버전을 App. G에 넣습니다(권장).
5. **C3:** P0 bootstrap CI를 마치면 답을 "Yes"로 갱신합니다.
