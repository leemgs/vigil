ACL 제출용 PDF 빌드 명령입니다.

### 기본 (익명 리뷰본 → `main.pdf`)
```bash
cd acl_submission
bash gen_pdf.sh
# 또는
bash gen_pdf.sh review
```

### 수동 빌드 (스크립트 없이)
```bash
cd acl_submission
pdflatex -interaction=nonstopmode -halt-on-error -jobname=main '\def\aclmode{review}\input{main.tex}'
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error -jobname=main '\def\aclmode{review}\input{main.tex}'
pdflatex -interaction=nonstopmode -halt-on-error -jobname=main '\def\aclmode{review}\input{main.tex}'
```

### 기타 모드
```bash
bash gen_pdf.sh preprint   # → main-preprint.pdf (camera_ready.tex 필요)
bash gen_pdf.sh final      # → main-final.pdf     (camera_ready.tex 필요)
```

### 필요 환경
- TeX Live (`pdflatex`, `bibtex`)
- 패키지: `algorithms` (`algorithm.sty`, `algorithmic`) 등 ACL 의존성  
  Debian/Ubuntu 예: `sudo apt-get install texlive-science texlive-latex-extra`

### Overleaf
- Main document를 `main.tex`으로 지정하면 기본이 review 모드입니다.