# VIGIL — ACL 리뷰어 관점 점검 및 Accept용 TODO

작성일: 2026-10-18 · 대상: `paper/` (main.tex, 본문 8쪽 + 부록)

이 문서는 논문 빌드에 포함되지 않습니다. 여기 적힌 수치는 모두 원고 본문,
또는 저장소 이력의 이전 원고(`paper_old/088_appendix.tex`, `065_evaluation.tex`;
커밋 `128228c`)에 저자가 이미 보고한 값입니다. 새로 만든 수치는 없습니다.

---

## 1. 예상 심사 결과

- **현재 예상:** Borderline / Weak Reject (Soundness 2.5–3, Excitement 3).
- **강점:**
  - 과제 정의가 새롭습니다(제품 속성 → 법적 위험 이론, 시점 조건부 근거).
  - "날짜 필터로는 안 되는 이유"(판례 효력 종료일 e_v는 이후 판결이 정함)가 명확합니다.
  - 상용 citator와 대조 검증(P2)했고, 부정적 결과인 P1 파일럿까지 정직하게 보고했습니다.
- **예상 거절 사유(심각도 순):**
  1. **통계적 근거 부재:** 핵심 비교(PLRE F1 0.78 vs 0.72, 372쌍)와 severity(0.79 vs 0.75,
     n=82)에 신뢰구간도 유의성 검정도 없습니다.
  2. **순환성 의심:** PLRE 쌍의 19.7%가 "효력 상실 판례" 오답 후보(stale distractor)이고,
     게이트는 바로 그것을 제거하도록 설계되었습니다. 이 후보들을 뺀 subset의 결과가 없습니다.
  3. **PLRE에서 핵심 비교군 누락:** 날짜 필터, 반복 횟수를 맞춘 self-refinement(B5),
     시간 인식 re-ranker가 PLRE에서 돌지 않았습니다. 개념적 논증만으로는 리뷰어를 설득하기 어렵습니다.
  4. **데이터 누수:** 분할이 분쟁 단위가 아니어서 같은 분쟁의 docket이 train/test에 걸칠 수 있습니다.
     제품 유형(archetype)도 5개뿐이라 일반화 검증이 약합니다.
  5. **사람 검증 규모가 작음:** 사람이 판정한 severity 테스트가 82건, 보고서 평가가 15건뿐이고,
     평가자는 모두 저자 기관 소속입니다.
  6. **재현성 의존:** 핵심 실험이 GPT-4o 특정 snapshot에 의존하고, P2는 비공개 상용 citator가 필요합니다.

---

## 2. 이번에 직접 수정한 항목 (커밋에 포함)

| 구분 | 수정 내용 |
|---|---|
| 근거 없는 주장 제거 | "instance-level 예측을 보관·공개하여 누구나 bootstrap CI 계산 가능"이라는 문장(Discussion, Limitations)을 삭제했습니다. 이전 원고에는 반대로 "보관하지 않았다(not retained)"고 적혀 있었고, 재실험 툴킷은 바로 그 예측을 다시 만들기 위한 것입니다. → **§4-1 확인 필요** |
| 근거 없는 주장 제거 | "Public AI-copyright trackers typically list a few hundred disputes"(출처 없음)를 삭제했습니다. |
| 검증 불가 사실 제거 | "gpt-4o-2024-08-06이 Azure OpenAI에서 retired"를 삭제했습니다(OpenAI API를 썼다는 서술과도 충돌). |
| 잘못된 논리 수정 | "open-weights 실행이 학습데이터 오염(contamination)을 부분 점검한다"를 "오염 confound를 제거하지 못한다"로 바꿨습니다. Llama도 같은 공개 판례로 학습되었을 수 있습니다. |
| 오해 소지 수정 | RQ2 "Evidence Sufficiency에서 VIGIL 최고"는 다른 시스템보다 우수하다는 뜻으로 읽힙니다. VIGIL 자체 점수 4.3/4.1/4.2/4.4/3.9(그중 최고가 Evidence Sufficiency)로 바꾸고, 쌍별 우위는 주장하지 않는다고 명시했습니다. |
| 서술 불일치 해소 | non-distractor 분석을 RQ4는 "스크립트로 제공", Limitations는 "향후 과제"라고 서로 다르게 적고 있었습니다. "이번 버전은 미보고"로 통일했습니다. |
| 서술 불일치 해소 | 데이터셋 범위를 한 곳은 "copyright/IP 소송", 다른 곳은 "privacy·publicity·product-liability 포함"이라고 적고 있었습니다. "U.S. AI-related litigation"으로 통일했습니다(§4-3 확인 필요). |
| 표기 충돌 | 판례 그래프 `P_t`가 제품 사양 `P`와 겹쳐 `\mathcal{P}_t`로 바꿨습니다. 완화책 `\mathcal{G}^*`가 목표 술어 `\mathcal{G}`와 겹쳐 `M^*`로 바꿨습니다. 정의되지 않은 기호 `C`가 들어 있던 `RiskScore(d_i,P,C)`는 서술형으로 바꿨습니다. |
| 해석 보강 | 게이트를 적용해도 stale 인용이 남는 이유(precedent chaining으로 문맥에 유입, 경계 사례에서 주석자 판단 불일치)를 저자 원고 그대로 RQ3에 넣었습니다. |
| 비교 조건 명시 | B1이 pre-labeler 행렬에서 composite bonus를 뺀 것이라는 점, B5가 토큰이 아니라 반복 횟수로 맞췄다는 점, Llama 실행에서는 baseline을 재실행하지 않았다는 점을 명시했습니다. |
| 분할 명시 | case 분할 70/10/20(분쟁 단위 아님), PLRE 분할은 "archetype으로 층화, 모든 split에 모든 archetype 포함"이라고 적었습니다. 원문의 "partitioned by archetype"은 unseen archetype 분할로 오해될 수 있었습니다. |
| 과장 완화 | 초록에 n=82가 "small"임을 표시했습니다. RQ1에 4점 차이를 확립된 차이로 보지 않는다고 적었습니다. P1은 사전 기준을 통과하지 못했다고 명시했습니다. |
| 중복 제거 | Related Work에서 Introduction과 같은 소송 사례 문장을 삭제했습니다. |
| 부록 복원 | "supplementary material"로만 미뤄 두었던 근거를 PDF 부록 A–G에 복원했습니다. 모두 저자가 보고한 값이며 현재 본문 수치와 전부 일치함을 확인했습니다. 관계별 edge 정확도, keyword heuristic(F1 0.52), P2 설계와 결과 표 2개, edge-error 전파 표, loop·retriever ablation, Observation 1 증명과 CRC 보정, backbone 표, 하이퍼파라미터, P1 파일럿 표가 들어 있습니다. |
| 참고문헌 | P1이 인용하는 `conan2022`를 다시 추가했습니다. 원래 항목의 "Centennial Edition"은 2013년판 명칭이라 틀렸고, govinfo에서 2022년판 제목과 부록 표 존재를 확인한 뒤 바로잡았습니다. 인용 49 → 50편. |
| 표 폭 | 부록 표 5개가 원래 크기로는 열 폭을 넘어 축소되고 있었습니다. 라벨을 줄이고 간격을 조정해 축소 없이 들어가게 했습니다. |

결과: 본문은 8쪽 이내(8쪽 초반에 종료), 전체 15쪽입니다. Overfull·미정의 참조·`??`·bibtex 경고·Type 3 폰트 모두 0건이고, 초록은 183단어입니다.

---

## 3. Accept를 위한 필수 TODO (추가 실험·검증 필요 — 직접 수행 불가)

저장소 이력 `backup/plre_reexperiment.zip`(커밋 `128228c`)에 아래 P0 1–3과 P1 4를
재실행하는 툴킷이 이미 있습니다(`run_plre_infer.py`, `compute_metrics.py`,
`run_b5_plre.py`, `regex_gate_passages.py`). 실행에는 **실제 PLRE test 372쌍 데이터**와
API 키가 필요합니다. 저장소에 있는 `plre_test_shells_372.jsonl`은 내용이 비어 있는 틀이고,
`plre_test_synthetic`은 조작된 합성 데이터라 **논문 결과에 절대 사용하면 안 됩니다**.

### P0 — 없으면 reject 가능성이 높음
1. **Paired bootstrap 95% CI:** VIGIL Full vs w/o gating(PLRE F1, stale-cite %, 372쌍,
   10,000 resamples), 그리고 severity VIGIL vs B5(n=82). Table 4·5·3에 CI 열을 추가하고 초록·결론에 반영합니다.
2. **Non-distractor subset F1:** 오답 후보(19.7% 비율이면 약 73쌍으로 추정)를 제외하고 gate vs no-gate를 비교합니다.
   이득이 대부분 사라지면 주장 범위를 "stale 근거 거부"로 좁혀야 합니다.
3. **PLRE 날짜 필터 baseline:** 문서 날짜 ≤ t_q만 남기는 필터입니다. 개념적 논증을 수치로
   뒷받침하는 가장 싼 실험이며, regex-gate도 함께 돌립니다.
4. **Table 4의 이상치 설명:** stale 인용은 "이미 닫힌 판례 인용"으로 정의되고, 닫힌 판례는
   indicator가 이미 제거합니다. 그런데 `w(·)`만 제거해도 stale이 4.1 → 7.8%로 늘어납니다.
   경로별 분해(chaining으로 들어온 것 vs 추출기가 놓친 closure)로 설명하지 않으면 리뷰어가 측정 오류를 의심합니다.

### P1 — 점수를 크게 올림
5. **B5(self-refinement)를 PLRE에서 실행:** "추가 연산 때문이 아니다"라는 주장을 직접 뒷받침합니다.
6. **분쟁 단위 재분할(dispute-blocked) 재평가**와 **leave-one-archetype-out** 평가.
7. **Severity의 사람 판정 test 확대:** 82건 → 200건 이상. 가능하면 외부(비소속) 주석자로 일부를 재판정합니다.
8. **RQ2 baseline별 평균 점수 표와 Wilcoxon 결과 공개:** 하지 않을 거라면 RQ2를 부록으로 내립니다.
9. **κ 산출 방식 명시:** 5점 척도에는 weighted κ나 Krippendorff's α가 표준입니다.

### P2 — 마무리 품질
10. P1 전체(COLIEE slice, extractor-treatment 변형) 실행 또는 범위 축소.
11. 보완할 관련 연구 후보: 시간 인식 RAG(TempRALM 등), 법률 인용 처리 분류 연구.
    추가 전에 반드시 실존 여부를 검증합니다.
12. 비용·연산량(LLM 호출 수, 토큰, GPU 시간) 보고. ARR Responsible NLP checklist 항목입니다.

---

## 4. 저자 확인이 필요한 사실관계 (임의로 정하지 않음)

1. **Instance-level 예측 보관 여부:** 보관했다면 P0-1을 바로 계산할 수 있습니다. 보관하지 않았다면
   재실행해야 하고, 이전 원고처럼 "not retained"라고 명시해야 합니다.
2. **부록에 복원한 수치:** 이전 원고(2026-10 초)의 값입니다. 현재 본문 수치와 겹치는 부분은 모두
   일치했지만, 최종 실험 로그와 다시 대조해 주세요.
3. **데이터셋 범위:** 이전 원고의 검색어와 연도별 표는 copyright/DMCA/trade secret/other 중심입니다.
   현재 본문은 privacy·publicity·product-liability 포함을 주장합니다. 실제 수집 기준을 확인해 주세요.
4. **Product archetype 5종의 명칭:** 이전 원고(API distribution, multimodal scraping 포함)와
   test 틀 파일(deployment/product liability, privacy/publicity 포함)이 서로 다릅니다.
5. **수치의 개연성:** "약 980개 고유 분쟁"과 "고유 피고 43명"의 조합이 타당한지 확인해 주세요.
   리뷰어가 데이터 규모를 의심할 수 있으니 분쟁·피고 분포 표를 부록에 추가하는 것을 권장합니다.
6. **B1 순환성:** B1은 pre-labeler와 거의 같은 규칙입니다. 그런데 "Full" 열에는 pre-label 847건이
   포함되어, B1이 자기 출력과 비교되는 셈입니다. 해석에 주의하고, 필요하면 "Full" 열을 부록으로 옮기세요.
7. **실험 시점:** 이전 원고는 "primary evaluation runs: June 2025", 현재 원고는
   "December 2025 이후 실행"이라고 적고 있습니다. 데이터가 2025년 12월까지 포함되므로 현재 서술이 맞다면 그대로 두면 됩니다.

---

## 5. 2차 점검 (2026-10-18, 같은 날 재요청)

**수치 내부 일관성 검산.** 본문과 부록의 모든 P/R/F1 값을 조화평균으로 다시 계산했고, 전부 반올림 범위 안에서 일치했습니다(표 1, 5, 6, 7, keyword heuristic). 함께 확인한 값은 다음과 같습니다.
- P2 집계: 129/156 = 0.83, 129/162 = 0.80, 누락 33/162 = 20.4%, 오작동 7/156 = 4.5%. 관계별 TP 45 + 37 + 47 = 129, 예측 52 + 45 + 59 = 156.
- 마스킹 비율에 따른 실효 누락률 31%, 41%, 46%.

**이번에 직접 수정한 항목**
- `w(·)`의 "cautionary"(0.75)가 무엇을 가리키는지 정의가 없었습니다. 엣지 분류에는 cautionary 관계가 없기 때문입니다. 저자 이전 원고의 정의("\textsc{Distinguishes}, 또는 interval을 닫지 않는 약한 부정 처리")를 §3.4에 복원했습니다.
- Ethics에 ARR 체크리스트 항목을 보강했습니다.
  - 공개 기록에 당사자·변호인 이름이 포함되고, 그 외 개인정보는 수집하지 않는다는 점(이전 원고 문장).
  - 연구용이며 자동 법률 판단용이 아니라는 용도 제한(이전 원고 문장).
  - 오남용·과의존 위험 문단(신규 서술, 결과 주장 없음).

**추가로 확인이 필요한 항목**
1. PLRE 라벨 κ = 0.71을 몇 쌍, 몇 명의 주석자로 산출했는지 본문에 없습니다.
2. §2의 controller 행동(Search/Analyze/Summarize/Map/Verify/Report)과 §3.3의 4개 에이전트(Planner/Retriever/Analyzer/Reporter)가 어떻게 대응하는지 설명이 없습니다. 리뷰어가 같은 루프의 두 가지 서술로 혼동할 수 있습니다.
3. 부록 하이퍼파라미터의 "Mapping threshold 0.72 (bi-encoder)"는 본문 PLRE 절차(검증셋 threshold)에서 어디에 쓰이는지 언급되지 않습니다.

예상 심사 결과는 바뀌지 않습니다. §3 P0 실험(bootstrap CI, non-distractor subset, 날짜 필터 baseline, Table 4 이상치 설명) 없이는 Borderline / Weak Reject로 예상합니다.

---

## 6. 3차 점검 (2026-10-18)

미해결 항목을 저자의 이전 원고(`paper_old/`, 커밋 `128228c`)에서 다시 찾아 확인했습니다.

**이번에 해결한 항목**
- **§4-6 B1 순환성:** 이전 원고에 저자가 직접 쓴 설명이 있었습니다. B1은 additive 점수만 쓰고, retained pre-label은 composite bonus를 썼기 때문에 B1이 자기 출력과 비교되지 않는다는 것입니다. 이 문장을 Limitations에 복원하고, Table 3의 Full 열은 규모 참고용이라고 명시했습니다. 질문 자체는 해결되었고, Full 열을 부록으로 옮길지는 선택 사항입니다.
- **PLRE 카드 출처:** "legal-research annotators가 공개 제품 문서와 소장(complaint) 주장으로부터 고정 가이드라인에 따라 작성"이라는 이전 원고 문장을 §3.5에 복원했습니다. 리뷰어가 흔히 묻는 "라벨 입력은 누가 무엇으로 만들었나"에 대한 답입니다.

**검증으로 확인한 사실**
- 이전 원고의 "Azure OpenAI가 2026-02-27에 `gpt-4o-2024-08-06`을 retire"는 **사실과 다릅니다.** 2026-02-27은 초기 공지의 "그 이전에는 retire하지 않음(no earlier than)" 날짜였습니다. 최신 Microsoft Foundry 일정에서는 Deprecated 상태이고, retire 예정일은 2027-04-14입니다. 따라서 이 문장을 되살리면 안 되고, 현재 서술("hosted snapshot은 retire될 수 있다")을 유지합니다.

**여전히 저자 확인이 필요한 항목** (이전 원고에서도 찾지 못함)
1. PLRE κ = 0.71의 산출 표본(쌍 수, 주석자 수).
2. Controller 행동 6개와 에이전트 4개의 대응 관계.
3. 부록 "Mapping threshold 0.72 (bi-encoder)"가 PLRE 절차의 어디에 쓰이는지.
4. §4의 1–5, 7번 (예측값 보관 여부, 부록 수치 대조, 데이터셋 범위, archetype 명칭, 980 분쟁/43 피고, 실험 시점).

예상 심사 결과는 그대로입니다. §3 P0 실험 없이는 Borderline / Weak Reject로 예상합니다.

---

## 7. 4차 점검 (2026-10-18): 과장 표현 정리

원고 변경이 없어서, 이번에는 신뢰구간 없는 점추정이 뒷받침하지 못하는 강한 표현을 전수 검색했습니다. 검색어는 confirm, systematically, demonstrate, significant, robust, establish, "not explained", "the component that" 등입니다. 4곳을 근거 수준에 맞게 고쳤습니다.

| 위치 | 이전 | 수정 |
|---|---|---|
| RQ3 | "Flat retrieval **systematically** promotes … closed authorities" | "Without the gate, retrieval admits more … closed authorities" (근거는 집계 stale 비율 하나뿐) |
| RQ4 | "the gate **is the component that** improves PLRE" | "in this ablation, the PLRE gain comes with the gate" |
| Discussion | "gains are **not explained by** extra test-time compute" | "suggests that extra compute alone does not explain the gain (compute-matched B5 on PLRE remains to be run)" |
| Conclusion | 이득을 단정적으로 서술 | 점추정임을 밝히고, CI·non-distractor·날짜 필터 비교가 다음 단계라고 명시 |

남은 TODO와 확인 항목은 §3, §4, §6과 같습니다.

---

## 8. 5차 점검 (2026-10-19): 관련 연구 보강

원고 변경이 없어서, 이번에는 리뷰어가 "가장 가까운 선행 연구가 빠졌다"고 지적할 만한 부분을 봤습니다. Related Work의 시간 관련 문단에 시간 인식 RAG 방법이 없었습니다. 실존과 서지 정보를 확인한 2편을 추가했습니다.
- Gade & Jetcheva (2024), "It's About Time: Incorporating Temporality in Retrieval Augmented Language Models" (TempRALM). arXiv 2401.13222에서 제목·저자·날짜를 확인했습니다.
- Qian et al. (2024), "TimeR$^4$: Time-aware Retrieval-Augmented LLMs for Temporal KGQA". EMNLP 2024, pp. 6942–6952. ACL Anthology 공식 BibTeX으로 확인했습니다.

추가한 서술은 "이 방법들도 시간을 사실·문서·질의의 속성으로 다룬다"는 한 문장입니다. 본 논문이 내세우는 차별점(이후 판결이 이전 판례의 효력을 바꾸는 supersession)과 대비시키는 역할입니다. 인용은 50편에서 52편이 되었고, 본문은 여전히 8쪽 안에 들어갑니다.

---

## 9. 투고처 확정: ACL 2027 (ARR 경유) — 2026-10-19

**공식 CFP에서 확인한 사항** (2027.aclweb.org/calls/main)
- ARR 제출 마감은 **2027-01-04 23:59 AoE**입니다. ARR 2027 1월 사이클이 마지막 기회이고, commitment 마감은 아직 미정입니다.
- 학회는 2027-08-17~22 일본 교토에서 열립니다(본 학회 8/20–22).
- 분량은 long 8쪽이며, 채택 후 camera-ready에서 9쪽까지 늘릴 수 있습니다. Limitations 섹션은 필수이고 부록은 허용됩니다. 심사는 이중맹검입니다.
- Responsible NLP Research Checklist, ACL 윤리·공개 정책, ACL AI writing assistance 정책이 적용됩니다.

**이번에 반영한 것**
- **제목 변경:** "VIGIL: Validity-Gated Retrieval for Product–Litigation Risk Entailment"에서 **"VIGIL: Validity-Interval Gating of Legal Precedent for Product–Litigation Risk Entailment"**로 바꿨습니다. 이유는 두 가지입니다.
  - 본문의 약어 풀이(Validity-Interval Gating in Litigation)와 맞춥니다.
  - 핵심 기제(validity interval)와 대상(legal precedent)을 제목에 드러냅니다.
- **스타일 파일:** `acl.sty`와 `acl_natbib.bst`가 공식 저장소(acl-org/acl-style-files) 최신본과 바이트 단위로 같음을 확인했습니다.
- **main.tex 머리 주석:** 투고처를 ACL 2027 (ARR)로 명시했습니다.

**제출 절차상 TODO (원고 밖)**
1. ARR 제출 폼에서 Responsible NLP Checklist를 작성합니다. 해당 섹션 번호를 기재하는데, 참고 위치는 Limitations, Ethics, §4.2(주석자), 부록 G(하이퍼파라미터·시드; 부록 A 신설 후 문자 변경)입니다. 연산량(compute) 항목은 원고에 없으므로 §3 P2-12를 먼저 처리해야 합니다.
2. AI 사용 공개는 Ethics "Use of AI assistants"에 이미 있습니다. ACL 정책에 맞는지 최종 확인합니다.
3. ARR sustainable reviewing 정책(2026년 10월부터 적용)에 따라 저자 중 심사 의무를 질 사람을 지정합니다.
4. commitment 시점에는 저자 목록을 바꿀 수 없으므로, 제출 전에 저자 목록을 확정합니다.
5. 채택되면 발표자 등록이 필수입니다(조기 등록 마감까지 등록하지 않으면 채택이 취소될 수 있음).
6. supplementary(코드·데이터 zip)는 익명화한 상태로 준비합니다. 개인 GitHub 링크와 저자명이 들어가면 안 됩니다.

**일정 권장:** §3 P0 실험(bootstrap CI, non-distractor subset, 날짜 필터 baseline, Table 4 이상치 설명)을 **2026년 12월 중순까지** 끝내야 결과를 본문에 반영하고 다시 점검할 시간이 남습니다. camera-ready의 추가 1쪽은 채택 후에만 쓸 수 있으므로, 제출본은 8쪽 안에 P0 결과를 넣어야 합니다. 현재 8쪽 하단에 약 0.4쪽의 여유가 있습니다.

---

## 10. 서사 집중 재구성 (2026-10-20, 저자 선택 반영)

리뷰 예상 약점 W7("시스템 논문인지 과제·방법 논문인지 모호")에 대해 저자가 **RQ1·RQ2 부록 이동**을 선택해, 그대로 반영했습니다.

- **본문 RQ를 3개로 재편했습니다. 모두 유효성 게이트 중심입니다.**
  - RQ1: PLRE (구 RQ4)
  - RQ2: 게이트 ablation과 edge 오류 전파 (구 RQ3)
  - RQ3: 증거 커버리지 위험 통제 (구 RQ5)
- **부록 A "Severity Triage and Report Quality"를 신설했습니다.** 구 RQ1(severity, n=82)과 구 RQ2(보고서 평가, n=15), B1–B5 정의, backbone 비교를 수치 변경 없이 옮겼습니다.
- **초록:** n=82 severity 문장을 삭제했습니다(183 → 164단어).
- **§2, Discussion, Limitations:** 새 RQ 번호와 부록 A를 가리키도록 교차참조를 고쳤습니다.
- **분량 변화:** 본문이 8쪽 초반이 아니라 **7쪽 오른쪽 단에서 끝납니다.** 8쪽 제한까지 **약 1쪽**이 남아, P0 실험 결과(CI 열, non-distractor 표, 날짜 필터 행)를 제출본에 넣을 수 있습니다.
- 표 축소 없음, 정의되지 않은 참조 0건, `??` 0건, bibtex 경고 0건입니다.

이로써 §3의 P1 "서사 집중" 항목을 완료했습니다. 남은 핵심은 §3 P0 실험입니다.

---

## 11. 기여 목록 정리와 사후 검증 비교 명시 (2026-10-20)

- **W6 반영(저자 선택):** 기여를 4개에서 3개로 줄였습니다. 남은 기여는 (1) treatment layer와 유효성 게이트, (2) PLRE 벤치마크, (3) VIGIL-Dataset과 SCOTUS testbed입니다.
  - goal-conditioned 에이전트 루프는 "게이트를 담는 시스템 구성요소"로 낮췄습니다. 그 근거(게이트 없이는 PLRE를 개선하지 않음, 증거 누락 위험 보장은 교환가능성 가정에서만 성립하고 시간 분할에서는 깨짐)를 서론에 명시했습니다.
- **W5 명시:** 사후 인용 필터링(생성 후 같은 유효기간으로 인용을 걸러내고 재생성)을 PLRE에서 비교하지 않았다는 점을 Limitations에 적었습니다. "생성 전에 거르는 것"의 이점이 측정되지 않았다는 점도 함께 적었고, Future work에도 추가했습니다.
- **새 TODO (P1):** 사후 필터링 baseline 실험. 이미 보유한 유효기간과 생성 출력만으로 구현할 수 있어, P0 실험과 함께 돌리기 좋습니다.
- **제목:** 게이트 중심 구성과 맞으므로 변경하지 않았습니다.

---

## 12. 제출 규약·표 폭·참고문헌 재점검 (2026-10-20)

재구성(부록 A 신설, 기여 조정, 참고문헌 3편 추가) 이후 최종 빌드로 다시 점검했습니다.

- **Desk reject 요소: 없음.**
  - 본문은 7쪽에서 끝나며, ACL 2027 long paper 제한은 8쪽입니다.
  - A4 용지이고, 1쪽부터 줄 번호가 찍혀 있습니다.
  - PDF 메타데이터의 Title·Author가 비어 있습니다.
  - 익명성을 해치는 흔적, 여백·간격을 조작한 흔적, 작성 중 표식(TODO 등)이 없습니다.
  - 초록은 164단어입니다.
  - Type 3 폰트와 임베드되지 않은 폰트가 없습니다.
  - 정의되지 않은 참조, `??`, 중복 label이 모두 0건입니다.
- **표·그림 폭:** Overfull 0건입니다. `adjustbox`를 제거한 원래 크기로도 0건이라, 모든 표가 축소 없이 열 폭 안에 들어갑니다. 본문과 부록에 그림은 없습니다.
- **참고문헌: 인용 52편 = bib 52편.** 빠진 항목도, 인용되지 않은 항목도 없습니다.
  - Crossref로 26편이 일치했습니다. 나머지는 원 출처(arXiv, ACL Anthology, NeurIPS·ICLR·PMLR·JMLR, 출판사, govinfo)로 확인한 결과를 유지합니다(§5–§8).
  - **수정:** `gade2024tempralm`은 arXiv 프리프린트로 적혀 있었지만, 실제로는 **2025 IEEE CAI, pp. 75–82에 출판**되었습니다(저자 3인: Gade, Jetcheva, Trivedi; DOI 10.1109/CAI64502.2025.00019). 출판본으로 바꾸고 키를 `gade2025tempralm`으로 변경했습니다.
  - Robertson & Zaragoza(2009)는 Crossref 기록만 페이지가 다르며, 출판사 기준 3(4):333–389가 맞습니다.

---

## 13. Responsible NLP 체크리스트 대응: 모델·연산·소프트웨어 (2026-10-23)

ARR 체크리스트의 실험 항목(모델 크기, 연산 규모, 소프트웨어)에 답할 원고 내용이 없었습니다. 저자 이전 원고의 "Models, compute, and software" 문단을 부록 G(하이퍼파라미터·모델)에 복원했습니다.
- 담긴 내용: GPT-4o snapshot과 온도, 임베딩 모델, Llama-3.1-70B(70B 파라미터)와 bge-large, RECAP으로 미세조정한 LegalBERT, 사례당 평균 2.4회 반복(최대 5회), 5회 실행, 패키지 버전 고정.
- 이전 원고의 "primary evaluation runs: June 2025"는 넣지 않았습니다. 데이터가 2025년 12월까지 포함된다는 현재 서술과 충돌하기 때문입니다(§4-7 확인 필요).
- **여전히 빠진 것 (저자 확인 필요):** 총 연산량(API 호출 수 또는 토큰 수, Llama 실행의 GPU 종류와 시간). 체크리스트 C1에 기재해야 하며, 원고 어디에도 근거 수치가 없어 만들지 않았습니다.

---

## 14. ARR Responsible NLP Checklist 대응표 (2026-10-23)

`paper/ARR_CHECKLIST.md`를 만들었습니다. 공식 질문 A1–E1마다 답(Yes/No), 근거 섹션, 제출 폼에 붙여 넣을 영문 사유 초안을 정리했습니다.
- ARR은 근거나 사유를 체계적으로 빠뜨린 제출물을 desk reject합니다. 이 대응표가 그 위험을 막습니다.
- 원고에 근거가 없는 5개 항목은 `[AUTHORS: …]`로 비워 두었습니다: C1 총 연산량, B2 CAP·CONAN 이용 조건, D5 주석자 특성, C4 패키지 버전, C3 신뢰구간.
- **정정:** 부록 A 신설 후 하이퍼파라미터·모델 부록의 문자가 F에서 **G**로 바뀌었습니다. §9와 §13의 "부록 F" 표기를 바로잡았습니다.
