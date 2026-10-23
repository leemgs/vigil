# PLRE re-experiment toolkit (P0 experiments for ACL 2027)

이 툴킷은 리뷰 대응에 필요한 P0·P1 실험을 실제 데이터로 돌리기 위한 것입니다(`paper/REVIEW_TODO.md` §3, §11).
저장소 이력의 `backup/plre_reexperiment.zip`(커밋 `128228c`)을 복원하고, 아래 결함을 고쳤습니다.
**이 저장소에는 실제 데이터와 결과가 없습니다.** 결과는 실제 372쌍으로 실행해야만 나옵니다.

## 무엇을 측정하나

| 논문 TODO | 시스템 / 출력 |
|---|---|
| P0-1 gate 유무의 신뢰구간 | `vigil_full` vs `vigil_no_gate`: paired bootstrap 95% CI (F1, stale) |
| P0-2 오답 후보 제외 subset | 모든 지표를 `is_stale_distractor == false` subset에서도 출력 |
| P0-3 날짜 필터 baseline과 B5 | `date_filter`, `b5`(iteration-matched; `PLRE_B5_MAX_TOKENS`로 token-matched) |
| P0-4 Table 4 분해 (일부) | `gate_only`는 닫힌 판례만 제거하고 나머지 라벨은 숨김. "− treatment weighting"에 해당 |
| P1 사후 검증 baseline | `posthoc_filter`: 게이트 없이 생성 → 닫힌 판례를 인용했으면 제거하고 1회 재생성 |

## 원본(backup) 대비 수정한 결함

1. **"no gate"가 실제로는 gate였습니다.** 원본 `vigil_no_gate`는 passage마다 `validity=closed`를 보여 주고, "closed는 근거로 쓰지 말라"는 프롬프트를 썼습니다. 그러면 gate 유무 차이가 과소 추정됩니다.
   이제 ungated 조건(`vigil_no_gate`, `date_filter`, `posthoc_filter` 1차, `b5`)은 유효성 라벨도, 관련 지시도 보지 않습니다.
2. **stale 인용이 모델의 자기 보고였습니다.** 원본은 모델이 반환한 `stale_cited`를 그대로 썼습니다.
   이제 모든 조건이 `supporting_doc_ids`를 반환하고, `compute_metrics.py`가 입력 데이터의 `validity_status == "closed"`와 대조해 측정합니다. 측정값은 두 가지입니다: 쌍 단위 `stale_pair`, 인용 단위 `stale_cite`.
3. **B5가 인용 문서를 반환하지 않았습니다.** 그래서 stale을 측정할 수 없었는데, 이제 반환합니다.
4. **CI 범위를 넓혔습니다.** 원본은 F1 차이만 계산했습니다. 이제 F1과 stale 차이 모두에 대해, 전체 쌍과 non-distractor subset 각각, 기준 시스템 대 모든 시스템의 CI를 계산합니다. 두 시스템의 gold가 다르면 오류로 멈춥니다.
5. **검증되지 않은 사본을 제거했습니다.** 원본의 `plre_reexperiment_all_in_one.py`는 모듈과 중복되는 비검증 사본이라 복원하지 않았습니다. 의존성에서 scikit-learn도 뺐습니다(F1은 직접 계산).

## 해석상 주의: 결과를 논문에 넣는 방법

- **이 하네스는 쌍마다 LLM을 한 번 호출합니다.** 논문 Table 4·5의 "VIGIL Full"(에이전트 루프, 판례 연쇄 확장 포함)과 같은 시스템이 아닙니다.
  - 따라서 여기 나온 수치로 **기존 표의 값을 바꾸면 안 됩니다.** 모든 조건을 같은 하네스에서 다시 돌린 **별도의 통제 실험**으로 보고해야 합니다(예: "single-call controlled re-run", 새 표 1개).
  - 기존 표와 수치가 다른 것은 정상입니다.
- 이 하네스의 `vigil_full`은 닫힌 판례를 아예 보여 주지 않습니다. 그래서 stale 인용은 모델이 보여 주지 않은 doc_id를 지어낸 경우에만 생깁니다. 이 경우는 `unknown_cited`로 따로 집계합니다.
  - 따라서 논문의 잔여 stale 4.1%(판례 연쇄 확장으로 문맥에 유입)는 이 하네스로 재현할 수 없습니다.
- **P0-4(Table 4 이상치)의 경로별 분해는 이 툴킷만으로는 불가능합니다.** 실제 VIGIL 파이프라인 로그에 stale 인용마다 다음 정보가 있어야 합니다.
  - 그 문서가 문맥에 들어온 경로: 게이트 통과 검색 / precedent chaining / 기타
  - 추출기가 해당 closure를 놓쳤는지
  - 같은 쌍에서 `w(·)` 제거 전후의 순위 변화
- `seed`는 디코딩(temperature 0.2)과 예시 순서만 바꿉니다. 여러 seed의 mean ± std는 신뢰구간이 아닙니다. CI는 한 seed 안에서 쌍 단위 bootstrap으로 계산합니다.

## 데이터

- `data/plre_test.jsonl`에 실제 held-out 372쌍을 넣습니다. 형식은 `data/SCHEMA.md`와 `data/README_DATA.md`를 따릅니다. `validity_status`는 treatment graph의 값입니다.
- `data/plre_test.example.jsonl`은 형식을 보여 주기 위한 예시 3쌍이며, 사건명과 내용은 가상입니다.
- 저장소 이력의 `plre_test_synthetic`(조작된 합성 데이터)은 **논문 결과에 절대 사용하지 마십시오.**

## 실행

```bash
cd experiments/plre_reexperiment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q tests          # 오프라인 검증(모의 LLM, API 호출 없음)

export OPENAI_API_KEY=...          # 또는 AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT (+ AZURE_OPENAI_DEPLOYMENT)
export PLRE_MODEL=gpt-4o-2024-08-06
cd scripts
python run_plre_infer.py --input ../data/plre_test.jsonl --systems vigil_full,vigil_no_gate --limit 2   # 스모크 테스트
./run_all.sh ../data/plre_test.jsonl   # 전체: 6개 조건 × 5 seed, 이후 metrics
```

결과는 `outputs/`에 저장되며, git에는 올라가지 않습니다(`.gitignore`). 요약은 `outputs/metrics_seed0.txt`입니다.

## 비용 감각

조건 5개 × seed 5개 × 372쌍이면 약 9,300회 호출입니다. 여기에 `posthoc_filter` 재생성분과 B5(반복 횟수만큼)가 추가됩니다.
CI 자체는 seed 하나로 계산하므로, 예산이 부족하면 `PLRE_SEEDS=0`으로 먼저 돌려도 P0 판단에는 충분합니다.
