# Coal-mining disasters, 1851–1962: verified series (2026-10-19)

- Site R page `Aula/class-01/materials/class1-poisson.html` has only 1851–1891 (41 values, mean 3.097561).
- Full 112-year series = Jarrett (1979, Biometrika 66, 191–193), as in Carlin, Gelfand & Smith (1992):
  `4,5,4,1,0,4,3,4,0,6,3,3,4,0,2,6,3,3,5,4,5,3,1,4,4,1,5,5,3,4,2,5,2,2,3,4,2,1,3,2,2,1,1,1,1,3,0,0,1,0,1,1,0,0,3,1,0,3,2,2,0,1,1,1,0,1,0,1,0,0,0,2,1,0,0,0,1,1,0,2,3,3,1,1,2,1,1,1,1,2,4,2,0,0,0,1,4,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1`
- Checked against `poisson-with-breakpoint.pdf`: n = 112, s = 191; first 40 sum 125, first 41 sum 127; s² = 2.714 (full), 2.574 (1851–1890), 1.063 (1891–1962); every row of the cut-point table (slide 18) reproduced to 3 dp; LR vs single λ at τ = 1891 = 69.99.
- Cut point τ = last year of the high-rate regime (τ = 1891 → n1 = 41).
