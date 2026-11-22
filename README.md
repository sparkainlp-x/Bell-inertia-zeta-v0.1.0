# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
# Bell + inertia + zeta

**SYNTHETIC classical emulation only. No claim about physical reality.
No headline claim is emitted.**

Three measured scientific outcomes, each measured in this laboratory
from its own first principles, not quoted. From three posts Jean
shared: John Bell's 1964 EPR paper, the moment of inertia of a solid
sphere by disk slicing, and Riemann's zeta function.

## Bell (1964): the EPR paradox, measured

Bell showed no local hidden-variable theory can reproduce the quantum
predictions for the singlet state. The CHSH form (Clauser, Horne,
Shimony, Holt, 1969) is the testable version: S = E(a,b) - E(a,b') +
E(a',b) + E(a',b'), with |S| <= 2 for any local hidden-variable theory
and 2 sqrt(2) for quantum mechanics at a = 0, a' = pi/2, b = pi/4,
b' = 3 pi/4.

- The quantum side is the singlet correlation E(a,b) = -cos(a - b).
- The classical side is a local hidden-variable model: each pair
  carries lambda uniform on [0, 2 pi); Alice's outcome is
  sign(cos(lambda - a)), Bob's is -sign(cos(lambda - b)). It gives the
  triangle-wave correlation E(a,b) = 2|a - b|/pi - 1.
- The EPR point is also measured: at equal settings the outcomes are
  perfectly anticorrelated, E(a,a) = -1, so the result is predetermined
  by lambda.

## Inertia: a solid sphere, by slicing into disks

Slice the sphere into thin disks at height z (disk radius y,
y^2 = R^2 - z^2, dI = (1/2) y^2 dm): I = (1/2) rho pi int y^4 dz =
(8/15) rho pi R^5, and with rho = M/(4/3 pi R^3), I = (2/5) M R^2. A
thin spherical shell of the same M and R has I = (2/3) M R^2, so the
solid sphere carries 3/5 of the shell's inertia: its mass sits closer
to the axis. The disk-slice integral is done numerically (Simpson's
rule) and compared with the analytic value.

## Zeta: Riemann's zeros on the critical line

Riemann (1859): zeta(s) = sum 1/n^s, with the hypothesis that every
nontrivial zero lies on the critical line Re(s) = 1/2. Here zeta(s) is
computed from scratch by Euler-Maclaurin summation (N = 100, K = 6).
The zeros are found by scanning |zeta(1/2 + i t)| for local minima and
refining each by golden-section search. The count below t = 50 is
compared with the Riemann-von Mangoldt formula N(T) ~ (T/2 pi)
log(T/2 pi) - T/2 pi + 7/8.

## Measured claims (v0.1.0)

Bars frozen before evaluation. Frozen seeds {42, 7, 1234, 2026, 2718}
drive the Monte Carlo Bell measurements (1,000,000 samples per
correlation). 23/23 tests pass. **7/7 claims pass.**

- (i) bell-lhv: **PASS** -- max |S| 2.0000 (bar <= 2.01). The local
  hidden-variable model saturates the bound and never exceeds it.
- (ii) bell-quantum: **PASS** -- |S| 2.828427, expected 2 sqrt(2)
  (rel err 1.57e-16, bar 1e-9).
- (iii) bell-epr: **PASS** -- worst |E(a,a) + 1| 0.00 (bar 0.01).
  Perfect anticorrelation at equal settings.
- (iv) inertia-sphere: **PASS** -- numerical disk-slice integral gives
  (2/5) M R^2 (worst rel err 1.39e-16, bar 1e-6).
- (v) inertia-ratio: **PASS** -- I_sphere/I_shell = 0.6 (worst rel err
  3.70e-16, bar 1e-6).
- (vi) zeta-zeros: **PASS** -- 10 zeros found, worst |t - known|
  4.78e-07 (bar 1e-3). The computed zeros land on the established
  values (14.134725, 21.022040, 25.010858, ...).
- (vii) zeta-count: **PASS** -- count 10, Riemann-von Mangoldt
  estimate 9.42 (diff 0.58, bar 1.0).

Reading: locality has a ceiling (2) that quantum mechanics breaks
(2.828); a sphere's inertia is exactly the disk-slice sum (2/5); and
Riemann's zeros, computed from scratch, sit where the tables say they
do -- ten of them below t = 50.

## Run it

```sh
make test   # pytest
make run    # the measured claims
```

## Licence

Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP).
SPDX-License-Identifier: AGPL-3.0-only. See LICENSE.
