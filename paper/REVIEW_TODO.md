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
