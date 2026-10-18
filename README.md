# Bridge and torch with crossing times 1, 2, ..., n: a closed formula for every bridge capacity

People 1, 2, ..., n cross a bridge at night; person i takes i minutes, at most c people
fit on the bridge, and one torch must go on every trip. T_c(n) is the least total time.

Thang Pang Ern and Sayson (J. Integer Seq. 29 (2026), arXiv:2608.05190) solved c = 3 and left
open whether a short closed formula or bounded-order recurrence exists for c >= 4.
This note proves one for every c >= 3. With n + 3 = g c + d, 0 <= d < c:

    T_c(n) = c g(g+1)/2 + (g+1) d - 10 + ceil( (3g + max(0, d-c+3)) / 2 )

for all n >= 5c - 5 (n >= 7 when c = 3). Equivalently T_c(n) = T_c(n-2c) + 2n - c + 9.

- Paper (readable PDF): `paper/main.pdf` (LaTeX source `paper/main.tex`)
- Code: `code/` (exact search `dij.c`, exact DP `model2.cpp`, LP/ILP checks, weight checks)

Status: draft, not peer reviewed.

Credits: Uchral Nyam-Osor proposed the research direction (find a recent paper's open
problem and solve it). Claude, an AI model by Anthropic, chose the problem, did the
mathematics and computations, and wrote the paper.

## Rerunning the checks

    cd code
    g++ -O2 -o model2 model2.cpp && gcc -O2 -o dij dij.c
    python3 ucheck.py        # formula vs exact DP (needs ./model2)
    python3 verify_dual.py   # lower-bound weights
    python3 qtable.py        # window inequalities up to c = 300
    python3 bags.py          # base schedules
