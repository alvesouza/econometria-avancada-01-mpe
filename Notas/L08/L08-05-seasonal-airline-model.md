---
tags: [notes, lecture-08, time-series, seasonality, seasonal-differencing, airline-model, sarima, airpassengers, forecasting]
date: 2026-10-25
status: taught
source: "seasonal.pdf slides 1–28 (seasonal adjustment, seasonal differencing, airline model and its ACF, multiplicative vs non-multiplicative, SARIMA, ARIMA(1,1,1)x(1,1,1)12 expansion, J&J and Decile 1 examples, forecast package, AirPassengers data, fits, RMSE(h) study, two best models); airpassengers-seasonalmodels.html (log transform, trend + dummies, BIC over 16 models, 108/36 split); Tsay AFTS 3e §2.8 pp. 81–90 (eqs. 2.41–2.42, Example 2.3 J&J, Example 2.4 Decile 1); Wooldridge 6e §10.5e pp. 336–338 (seasonal dummies)"
---

# §2.8 · Seasonal models — difference twice, model the remainder with two MA terms, and know when the seasonality is deterministic

> **Claim.** **The airline model $(1-B^s)(1-B)x_t=(1-\theta B)(1-\Theta B^s)a_t$ removes trend and seasonality by regular and seasonal differencing and describes what is left with two MA parameters.** Its differenced series has nonzero autocorrelations only at lags $1$, $s-1$, $s$, $s+1$, and the two side lags are the *product* $\rho_1\rho_s$: the regular and seasonal dynamics are orthogonal. It is the ARIMA$(0,1,1)\times(0,1,1)_s$ special case of Box–Jenkins SARIMA. **When the fitted seasonal MA coefficient reaches 1 it cancels the seasonal difference and the seasonality is deterministic**: dummies then do the same job (Decile 1's January effect). For the AirPassengers series, BIC picks the airline model, statsmodels reproduces the deck's estimates, and out of sample it forecasts 1958–60 with RMSE 36.6 against 63.3 for a trend-plus-dummies regression.
> Prev: [[L08-04-long-memory-arfima]] · Next: [[L08-06-arch-garch]] · Map: [[L08-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $x_t$ | the (usually log) series | |
| $s$ | periodicity: 4 quarterly, 12 monthly | $s\ge3$ in §3 |
| $\Delta=1-B$, $\Delta_s=1-B^s$ | regular and seasonal difference | |
| $w_t=(1-B^s)(1-B)x_t$ | the doubly differenced series | |
| $\theta$, $\Theta$ | regular and seasonal MA coefficients (Tsay's sign: $1-\theta B$) | $|\theta|,|\Theta|<1$ |
| $a_t$ | white noise, variance $\sigma_a^2$ | |
| $\gamma_\ell$, $\rho_\ell$ | autocovariance and ACF of $w_t$ | |
| $\phi(B),\theta(B)$; $\Phi_P(B^s),\Theta_Q(B^s)$ | regular and seasonal AR and MA polynomials | |

**Sign convention.** R's `arima`/`Arima` and statsmodels print MA coefficients with a plus sign, $1+\theta B$. A printed `ma1 = -0.3864` is Tsay's $\theta=0.3864$. AR coefficients print with the same sign in all three.

---

## 1 · C — seasonal series and seasonal adjustment (slides 3–4; T §2.8, pp. 81–82; W §10.5e, pp. 336–337)

A seasonal series repeats a pattern every $s$ periods: Tsay's Figure 2.13 shows the quarterly earnings per share of Johnson & Johnson, 1960–1980, growing exponentially with a strong period-4 pattern and rising variability. **Seasonal adjustment** removes the seasonal component before inference; most US government series (GDP growth, unemployment) are published adjusted (T p. 82; W p. 336). "In other applications such as forecasting, seasonality is as important as other characteristics of the data and must be handled accordingly" (slide 4): the course models it.

**Logs first** (T pp. 82–83). The log turns exponential growth into a linear trend and stabilises the variance: the widening seasonal swings of the J&J earnings (and of AirPassengers, §6) become swings of constant amplitude. In R this is `lambda = 0` (Box–Cox with $\lambda=0$).

---

## 2 · C — seasonal differencing (slide 5; T §2.8.1, pp. 83–84)

With $x_t$ the log earnings, the ACF of $x_t$ decays slowly (trend), and the ACF of $\Delta x_t$ spikes at multiples of 4 (seasonality). Following Box, Jenkins and Reinsel, take both differences:

$$\Delta_s y_t=(1-B^s)y_t=y_t-y_{t-s},\tag{1}$$

$$\Delta_s\Delta x_t=(1-B^s)(1-B)x_t.\tag{2}$$

Multiply the operators in (2), $(1-B^s)(1-B)=1-B-B^s+B^{s+1}$, and apply to $x_t$:

$$\Delta_s\Delta x_t=x_t-x_{t-1}-x_{t-s}+x_{t-s-1}.\tag{3}$$

For quarterly data, $\Delta_4\Delta x_t=x_t-x_{t-1}-x_{t-4}+x_{t-5}$ (T p. 83): this year's quarterly change minus last year's change in the same quarter. Its ACF for J&J has "a significant negative ACF at lag 1 and a marginal negative correlation at lag 4" (T p. 84), the pattern the next model is built for.

---

## 3 · C — the airline model and its ACF (slides 6–8; T §2.8.2, eq. 2.41, pp. 84–85)

$$(1-B^s)(1-B)x_t=(1-\theta B)(1-\Theta B^s)a_t,\qquad|\theta|<1,\ |\Theta|<1.\tag{4}$$

The AR side is just the two differences; all the modelling is in the MA side. Expanding the right-hand side, with $w_t$ as in the notation:

$$w_t=(1-\theta B-\Theta B^s+\theta\Theta B^{s+1})a_t=a_t-\theta a_{t-1}-\Theta a_{t-s}+\theta\Theta a_{t-s-1}.\tag{5}$$

$w_t$ is an MA($s+1$) with only four nonzero weights, so $E(w_t)=0$.

**Variance.** The four shocks in (5) are uncorrelated:

$$\gamma_0=\sigma_a^2\big(1+\theta^2+\Theta^2+\theta^2\Theta^2\big)=(1+\theta^2)(1+\Theta^2)\,\sigma_a^2.\tag{6}$$

**Autocovariances.** For each lag write $w_{t-\ell}$ from (5) and keep only the shocks it shares with $w_t$ (assume $s\ge3$, so that lags $1$, $s-1$, $s$, $s+1$ are distinct).

Lag 1: $w_{t-1}=a_{t-1}-\theta a_{t-2}-\Theta a_{t-s-1}+\theta\Theta a_{t-s-2}$. Shared shocks: $a_{t-1}$ (weights $-\theta$ in $w_t$, $1$ in $w_{t-1}$) and $a_{t-s-1}$ (weights $\theta\Theta$ and $-\Theta$):

$$\gamma_1=\sigma_a^2\big[(-\theta)(1)+(\theta\Theta)(-\Theta)\big]=-\theta(1+\Theta^2)\,\sigma_a^2.\tag{7}$$

Lag $s-1$: $w_{t-s+1}=a_{t-s+1}-\theta a_{t-s}-\Theta a_{t-2s+1}+\theta\Theta a_{t-2s}$. Shared: $a_{t-s}$ (weights $-\Theta$ and $-\theta$):

$$\gamma_{s-1}=\sigma_a^2(-\Theta)(-\theta)=\theta\Theta\,\sigma_a^2.\tag{8}$$

Lag $s$: $w_{t-s}=a_{t-s}-\theta a_{t-s-1}-\Theta a_{t-2s}+\theta\Theta a_{t-2s-1}$. Shared: $a_{t-s}$ (weights $-\Theta$ and $1$) and $a_{t-s-1}$ (weights $\theta\Theta$ and $-\theta$):

$$\gamma_s=\sigma_a^2\big[(-\Theta)(1)+(\theta\Theta)(-\theta)\big]=-\Theta(1+\theta^2)\,\sigma_a^2.\tag{9}$$

Lag $s+1$: $w_{t-s-1}=a_{t-s-1}-\theta a_{t-s-2}-\dots$. Shared: $a_{t-s-1}$ (weights $\theta\Theta$ and $1$):

$$\gamma_{s+1}=\theta\Theta\,\sigma_a^2.\tag{10}$$

Every other lag shares no shock: $\gamma_\ell=0$ for $\ell>0$, $\ell\notin\{1,s-1,s,s+1\}$.

**ACF.** Divide (7)–(10) by (6):

$$\rho_1=\frac{-\theta(1+\Theta^2)}{(1+\theta^2)(1+\Theta^2)}=\frac{-\theta}{1+\theta^2},\qquad\rho_s=\frac{-\Theta}{1+\Theta^2},\tag{11}$$

$$\rho_{s-1}=\rho_{s+1}=\frac{\theta\Theta}{(1+\theta^2)(1+\Theta^2)}=\rho_1\rho_s.\tag{12}$$

**Why "multiplicative"** (T p. 85). The MA(1) $y_t=(1-\theta B)a_t$ has $\rho_1(y)=-\theta/(1+\theta^2)$ and nothing else; the MA($s$) $z_t=(1-\Theta B^s)a_t$ has $\rho_s(z)=-\Theta/(1+\Theta^2)$ and nothing else. By (11)–(12), $\rho_1=\rho_1(y)$, $\rho_s=\rho_s(z)$ and $\rho_{s\pm1}=\rho_1(y)\rho_s(z)$: the side lags are the interaction of the regular and seasonal dependence. "A multiplicative seasonal model says that the dynamics of the regular and seasonal components of the series are approximately orthogonal" (slide 8).

**Non-multiplicative alternative** (T eq. 2.42, p. 85):

$$w_t=(1-\theta B-\Theta B^s)a_t=a_t-\theta a_{t-1}-\Theta a_{t-s}.\tag{13}$$

Repeat the bookkeeping: $w_{t-s+1}$ contains $-\theta a_{t-s}$, which meets $-\Theta a_{t-s}$ in $w_t$, so $\gamma_{s-1}=\theta\Theta\sigma_a^2\ne0$; but $w_{t-s-1}=a_{t-s-1}-\theta a_{t-s-2}-\Theta a_{t-2s-1}$ shares no shock with $w_t$, so

$$\rho_{s+1}=0\quad\text{in (13)}.\tag{14}$$

Both models have two parameters; the multiplicative one has more nonzero autocorrelations (lags $1,s-1,s,s+1$ against $1,s-1,s$), hence it is the more parsimonious description of a symmetric pattern around lag $s$ (T p. 85).

### 3.1 · Worked — the two fitted airline models

**Johnson & Johnson (T Example 2.3, p. 85; slide 11).** Exact likelihood on the log earnings:

$$(1-B)(1-B^4)x_t=(1-0.678B)(1-0.314B^4)a_t,\qquad\hat\sigma_a=0.089,$$

standard errors 0.080 and 0.101; residual $Q(12)=10.0$, p 0.44: adequate. By (11)–(12), with $1+\theta^2=1+0.678^2=1.4597$ and $1+\Theta^2=1+0.314^2=1.0986$:

$$\rho_1=\frac{-0.678}{1.4597}=-0.4645,\qquad\rho_4=\frac{-0.314}{1.0986}=-0.2858,\qquad\rho_3=\rho_5=(-0.4645)(-0.2858)=0.1328,$$

and by (6) $\gamma_0=1.4597\times1.0986\times0.089^2=1.6036\times0.007921=0.0127$.

**AirPassengers (§6, page fit on 1949–1957, $s=12$).** $\theta=0.3864$, $\Theta=0.5885$: $1+\theta^2=1.1493$, $1+\Theta^2=1.3463$,

$$\rho_1=\frac{-0.3864}{1.1493}=-0.3362,\qquad\rho_{12}=\frac{-0.5885}{1.3463}=-0.4371,\qquad\rho_{11}=\rho_{13}=(-0.3362)(-0.4371)=0.1470.$$

With $\hat\sigma_a^2=0.001416$, (6) gives $\gamma_0=1.5473\times0.001416=0.00219$.

![Two bar charts of the exact autocorrelation of the doubly differenced series. Left, Johnson and Johnson with s = 4: bars only at lag 1 (-0.464), lag 3 (0.133), lag 4 (-0.286) and lag 5 (0.133). Right, AirPassengers with s = 12: bars only at lag 1 (-0.336), lags 11 and 13 (0.147 each) and lag 12 (-0.437); all other lags up to 30 are exactly zero](figures/L08-airline-acf.png)
*Figure — exact ACF (11)–(12) of $w_t$ for the two fitted airline models: J&J $(\theta,\Theta)=(0.678,0.314)$, $s=4$ (T p. 85); AirPassengers $(0.3864,0.5885)$, $s=12$ (`airpassengers-seasonalmodels.html`).*

The theoretical ACF has exactly four spikes. The two negative ones, at lags 1 and $s$, are the regular and seasonal MA(1) effects; the two small positive ones flank lag $s$ with equal height $\rho_1\rho_s$. Reading a sample ACF of $\Delta_s\Delta x_t$: spikes at $1$ and $s$ with small symmetric shoulders at $s\pm1$ point to the airline model; a shoulder only at $s-1$ points to (13).

---

## 4 · C — SARIMA, and how constrained it is (slides 9–10)

The airline model is the special case of the seasonal ARIMA of Box and Jenkins (1970):

$$\Phi_P(B^s)\,\phi(B)\,(1-B^s)^D(1-B)^d\,x_t=\delta+\Theta_Q(B^s)\,\theta(B)\,a_t,\tag{15}$$

written ARIMA$(p,d,q)\times(P,D,Q)_s$, with $\phi,\theta$ of degrees $p,q$ in $B$ and $\Phi_P,\Theta_Q$ of degrees $P,Q$ in $B^s$. **The airline model is ARIMA$(0,1,1)\times(0,1,1)_s$.**

### 4.1 · Worked — ARIMA$(1,1,1)\times(1,1,1)_{12}$ is a constrained ARMA(26,13)

$$(1-\phi L)(1-\Phi L^{12})\,\Delta\Delta_{12}\,y_t=(1-\theta L)(1-\Theta L^{12})\,\epsilon_t.\tag{16}$$

Multiply the four AR factors in pairs. Regular pair: $(1-\phi L)(1-L)=1-(1+\phi)L+\phi L^2$. Seasonal pair: $(1-\Phi L^{12})(1-L^{12})=1-(1+\Phi)L^{12}+\Phi L^{24}$. Their product, term by term:

$$\big[1-(1+\phi)L+\phi L^2\big]\big[1-(1+\Phi)L^{12}+\Phi L^{24}\big]$$

$$=1-(1+\phi)L+\phi L^2-(1+\Phi)L^{12}+(1+\phi)(1+\Phi)L^{13}-\phi(1+\Phi)L^{14}+\Phi L^{24}-(1+\phi)\Phi L^{25}+\phi\Phi L^{26}.\tag{17}$$

The MA side is $(1-\theta L)(1-\Theta L^{12})=1-\theta L-\Theta L^{12}+\theta\Theta L^{13}$. Moving every lagged $y$ to the right:

$$\begin{aligned}y_t={}&(1+\phi)y_{t-1}-\phi y_{t-2}+(1+\Phi)y_{t-12}\\&-(1+\phi)(1+\Phi)y_{t-13}+(1+\Phi)\phi y_{t-14}\\&-\Phi y_{t-24}+(1+\phi)\Phi y_{t-25}-\phi\Phi y_{t-26}\\&+\epsilon_t-\theta\epsilon_{t-1}-\Theta\epsilon_{t-12}+\theta\Theta\epsilon_{t-13}.\end{aligned}\tag{18}$$

An ARMA(26,13) whose 26 AR and 13 MA coefficients are functions of four parameters, "with severe parameter constraints" (slide 10). **Slide typos:** the slide prints the $y_{t-12}$ coefficient as $(1-\phi+\Phi)$ and the $y_{t-13}$ coefficient as $-(1+\phi\Phi+\Phi)$; (17) gives $(1+\Phi)$ and $-(1+\phi)(1+\Phi)=-(1+\phi+\Phi+\phi\Phi)$. Check: setting $L=1$ in (17) must give 0 (the polynomial contains $(1-L)$), and $1-(1+\phi)+\phi-(1+\Phi)+(1+\phi)(1+\Phi)-\phi(1+\Phi)+\Phi-(1+\phi)\Phi+\phi\Phi=0$ ✓. The other coefficients on the slide agree with (18).

---

## 5 · C — deterministic seasonality: when $\Theta\to1$ (slides 12–14; T pp. 86–90; W §10.5e)

**Why $\Theta=1$ means deterministic** (T p. 86). With $\Theta=1$, (4) is $(1-B^s)(1-B)x_t=(1-\theta B)(1-B^s)a_t$. Move everything to one side and factor $(1-B^s)$:

$$(1-B^s)\big[(1-B)x_t-(1-\theta B)a_t\big]=0.$$

The bracket $S_t$ satisfies $S_t-S_{t-s}=0$, i.e. it is a fixed period-$s$ pattern set by the initial conditions:

$$(1-B)x_t=(1-\theta B)a_t+S_t,\qquad S_t=S_{t-s}.\tag{19}$$

A fixed seasonal pattern is exactly what seasonal dummies estimate, so "the same forecasts are obtained by using either dummy variables or a multiplicative seasonal model when the seasonal pattern is deterministic. Yet use of dummy variables can lead to inferior forecasts if the seasonal pattern is not deterministic" (T p. 86). Tsay recommends the **exact** likelihood, which can reach $\Theta$ near 1 where the conditional likelihood cannot.

**Worked — CRSP Decile 1 monthly returns, 1970–2008, 468 months (T Example 2.4, pp. 86–90; slides 12–14).** The time plot shows no seasonality but the ACF is significant at lags 1, 12, 24, 36. The model $(1-\phi_1B)(1-\phi_{12}B^{12})R_t=(1-\theta_{12}B^{12})a_t$ gives:

| Method | $\hat\phi_1$ | $\hat\phi_{12}$ (seasonal AR) | $\hat\theta_{12}$ (seasonal MA) | $\tilde\sigma_a$ |
|---|---|---|---|---|
| conditional likelihood | 0.18 | 0.87 | 0.74 | 0.069 |
| exact likelihood | 0.188 | **0.951** | **0.997** | 0.063 |

With the exact method the seasonal AR and MA factors nearly cancel, $(1-0.951B^{12})\approx(1-0.997B^{12})$, and $\hat\theta_{12}\approx1$: by (19) the seasonality looks deterministic. (R's exact `arima` gives `ar1` 0.1787, `sar1` 0.9886, `sma1` $-0.9127$, i.e. $\theta_{12}=0.9127$; "slightly differ from those of SCA", T p. 89.) The confirming regression on a January dummy (T p. 88):

$$\hat R_t=0.0029+0.1253\,Jan_t,\qquad\text{s.e. }0.0033\ \text{and}\ 0.0115,\qquad R^2=0.2016.$$

The January slope has $t=0.1253/0.0115=10.9$ (R prints 10.848): the average January return is $0.0029+0.1253=0.1282$, about 12.8%, against 0.29% in other months. The residual ACF loses its lags 12, 24, 36. **The seasonality of Decile 1 is the January effect**, and one dummy captures it.

**Seasonal dummies in regression (W §10.5e, pp. 336–338).** With monthly data, include eleven month dummies (one month as base) in the regression, alone or with a trend and other regressors; the dummy coefficients are the average seasonal differences from the base month. This is the "deterministic trend + cycle" model of the AirPassengers page.

---

## 6 · C — the AirPassengers study (slides 15–28; `airpassengers-seasonalmodels.html`)

**Data** (slide 16; Box, Jenkins and Reinsel's Series G): monthly international airline passengers in thousands, 1949–1960, $n=144$, from 112 in Jan 1949 to 432 in Dec 1960 (sum 40,363). Seasonal swings grow with the level, so the analysis is on $\log y_t$ (`lambda = 0`); the page plots $y_t-y_{t-1}$, $y_t-y_{t-12}$ and $y_t-y_{t-1}-y_{t-12}+y_{t-13}$, which is (3), before and after the log.

**Design (page).** Training 1949.1–1957.12 ($n_1=108$, nine years), testing 1958.1–1960.12 ($n_2=36$). Two competitors:

1. *Deterministic trend + cycle*: OLS of $\log y_t$ (and of $y_t$) on an intercept, $t$, and 11 month dummies (W §10.5e).
2. *Seasonal ARIMA*: all sixteen ARIMA$(i,1,j)\times(k,1,l)_{12}$ with $i,j,k,l\in\{0,1\}$, chosen by BIC.

**BIC choice.** The page's loop returns `0 1 0 1 -336.9304`: **ARIMA$(0,1,1)\times(0,1,1)_{12}$, the airline model, BIC $-336.93$**. Fitted (page):

$$(1-B)(1-B^{12})\log y_t=(1-0.3864B)(1-0.5885B^{12})a_t,\qquad\text{s.e. }0.1097,\ 0.0927,\quad\hat\sigma_a^2=0.001416,$$

log-likelihood 175.3, AIC $-344.59$, BIC $-336.93$. The printed `ma1 = -0.3864`, `sma1 = -0.5885` are $-\theta$, $-\Theta$.

**Reproduction in Python** (statsmodels `SARIMAX` on the logs, exact likelihood; our computation, in [[L08-12-python]]):

| Sample | Deck / page (ma1, sma1) | statsmodels | log-lik, AIC, BIC (statsmodels) |
|---|---|---|---|
| to 1956.12 ($n=96$, slide 19) | $-0.3941$, $-0.6129$; BIC $-284.27$ | $-0.3944$, $-0.6133$ | 148.76, $-291.52$, $-284.26$ |
| to 1957.12 ($n=108$, page) | $-0.3864$, $-0.5885$; BIC $-336.93$ | $-0.3876$, $-0.5886$ | 175.29, $-344.59$, $-336.92$ |
| full ($n=144$, slide 26) | $-0.4018$, $-0.5569$; AIC $-483.4$ | $-0.4017$, $-0.5571$ | 244.70, $-483.39$, $-474.77$ |

The log-likelihoods and criteria agree to the printed precision; the coefficients to about 0.001, the difference between R's and statsmodels' optimisers. In statsmodels the BIC-best of the sixteen on $n=108$ is also (0,1,1)(0,1,1), with (1,1,0)(0,1,1) second at $-335.85$.

**Forecasts (slides 20–21).** `forecast(air.model, h=48)` from the 1956 fit, and refits ending 1953–1956 with forecasts to 1960: the airline forecasts reproduce the growing seasonal pattern, with 80% and 95% bands that widen with the horizon (the two unit roots, [[L08-03-unit-roots-dickey-fuller]] (6)).

**RMSE($h$) study (slides 22–24, 27).** For every origin $t=48,\dots,n-12$, refit fifteen models (the sixteen minus $(1,1,1)\times(1,1,1)$) on observations $1,\dots,t$ and forecast $y_t(h)$, $h=1,\dots,12$:

$$\text{RMSE}(h)=\sqrt{\frac{1}{n-11-t_0}\sum_{t=t_0}^{n-12}\big(y_{t+h}-y_t(h)\big)^2},\qquad t_0=48,\tag{20}$$

plotted in levels and relative to model 6, the airline model ($100(\text{RMSE}_i/\text{RMSE}_6-1)$). The models without a regular or seasonal MA term do clearly worse at all horizons. **The full-sample fits of the leading models (slide 26):**

| Model | Coefficients (R sign) | $\hat\sigma^2$ | log-lik | AIC | BIC |
|---|---|---|---|---|---|
| (0,1,1)(0,1,1) | ma1 $-0.4018$ (0.0896), sma1 $-0.5569$ (0.0731) | 0.001371 | 244.70 | $-483.40$ | $-474.77$ |
| (0,1,1)(1,1,1) | ma1 $-0.4143$, sar1 $-0.1116$ (0.1547), sma1 $-0.4817$ | 0.001375 | 244.96 | $-481.91$ | $-470.41$ |
| (1,1,0)(1,1,1) | ar1 $-0.3451$, sar1 $-0.0760$ (0.1548), sma1 $-0.5108$ | 0.001399 | 243.86 | $-479.73$ | $-468.23$ |
| (1,1,0)(0,1,1) | ar1 $-0.3395$ (0.0822), sma1 $-0.5619$ (0.0748) | 0.001391 | 243.74 | $-481.49$ | $-472.86$ |

The seasonal AR terms are insignificant ($t=-0.72$ and $-0.49$), and the extra parameter only lowers the BIC. The "two best models" plotted on slide 28 are (0,1,1)(0,1,1) and (1,1,0)(0,1,1): an MA(1) or an AR(1) for the regular part, both with the seasonal MA. A regular MA(1) with $\theta=0.40$ and an AR(1) with $\phi=-0.34$ have close ACFs at lag 1 ($-0.35$ and $-0.34$), which is why they forecast alike.

**Out of sample, 1958–1960 (our computation).** Fitting on $n_1=108$ and forecasting 36 months by exponentiating the log forecasts: RMSE **36.6** thousand passengers for the airline model against **63.3** for the log trend + 11 dummies regression. The deterministic model forces the same seasonal shape and trend slope estimated on 1949–57 onto 1958–60; the airline model lets both drift, which is (19) read in reverse.

> **Seasonality is stochastic until the data say otherwise.** Use the exact likelihood; if $\hat\Theta\to1$ (or a seasonal AR and MA cancel), switch to dummies.

---

## Links

- Neighbours: [[L08-04-long-memory-arfima]] · [[L08-06-arch-garch]].
- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] (the SARIMAX reproduction, the RMSE comparison, the Decile 1 January regression) · [[L08-02-forecasting-ma-arma]] (MA ACF, forecasts) · [[L08-03-unit-roots-dickey-fuller]] (differencing, ARIMA).
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] (ACF of a linear process from its $\psi$ weights, L01-07 (4)).
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]].
- **Practice (number and printed page only):** T 2.6 (p. 105). Worked solutions: `Listas/lista-L08-book-exercises.pdf`.
