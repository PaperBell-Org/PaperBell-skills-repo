# Spatial analysis pre-review checklist · 空间分析审稿前检查清单

Twelve topics that reviewers of geospatial papers raise again and again. Each
item has four parts:

- **Problem** — what can go wrong.
- **Why reviewers ask** — the objection you will receive if it is not handled.
- **How to check** — concrete checks, each of which leaves evidence (a table,
  a figure, a sentence in Methods, a sensitivity run).
- **References** — classic literature to cite.

Examples use fictional projects: *urban green-space accessibility* (city
grid cells, park polygons, population rasters), *nighttime lights and the
economy* (satellite radiance vs. county GDP), *air-pollution exposure from
mobile-phone traces*, and *land-cover classification with machine learning*.

About the references: every entry with a DOI was checked against Crossref
(title, journal, volume, issue, pages). Entries that could not be confirmed
were left out rather than guessed. Before citing, still open the source and
confirm it says what you cite it for.

Verdicts used when the checklist is applied (see `SKILL.md`): **通过 / Pass**,
**有风险 / At risk**, **不适用 / Not applicable** — always with evidence or a
one-line reason.

---

## 1. MAUP — modifiable areal unit problem · 可塑面积单元问题

### 1a. Scale effect · 尺度效应

**Problem.** The same data aggregated to 1 km cells, 10 km cells, districts or
cities gives different correlations and regression coefficients — sometimes
with opposite signs.

**Why reviewers ask.** A result that holds at one scale only may be produced by
the aggregation rather than by the phenomenon. Expect: "Why this scale? Does
the result hold at another one?"

**How to check**
- State why this scale was chosen (native data resolution, policy unit, prior
  work), and fix that reason before looking at results.
- Re-run the main model at least one finer and one coarser scale; plot the
  coefficients and intervals side by side.
- When an input is coarse (e.g. a 0.25° reanalysis or a 500 m night-light
  product), finer analysis units add no information. Report the *effective*
  resolution; do not present interpolation or resampling as refinement.

**References**
- Fotheringham, A. S. & Wong, D. W. S. (1991). The modifiable areal unit problem in multivariate statistical analysis. *Environment and Planning A* 23(7):1025–1044. doi:10.1068/a231025
- Jelinski, D. E. & Wu, J. (1996). The modifiable areal unit problem and implications for landscape ecology. *Landscape Ecology* 11(3):129–140. doi:10.1007/BF02447512

**Example.** Green-space accessibility shows no gap between income groups on a
10 km grid. That "no gap" may be the grid averaging away within-city
differences; report results on 1, 2 and 4 km grids together and say which
scale the conclusion depends on.

### 1b. Zoning effect · 分区效应

**Problem.** Same scale, different boundaries (administrative units vs. equal
grid; grid shifted by half a cell) — different results.

**Why reviewers ask.** Administrative boundaries correlate with population,
income and environment. Part of a pattern found on administrative units may
come from how the boundaries were drawn.

**How to check**
- Main analysis on administrative units → add an equal-area grid version.
  Main analysis on a grid → shift the grid origin by half a cell and re-run.
- Units that straddle two zones (a city crossing two climate or economic
  regions): write the assignment rule and run a sensitivity with the
  alternative assignment.
- If two boundary datasets exist (official vs. open-source), choose one as
  primary, run the other as a sensitivity and report both.

**References**
- Fotheringham & Wong (1991), above.

**Example.** Night-light vs. GDP regressions on counties; re-run on a 10 km
grid with GDP downscaled by a published method, and on a half-cell shifted
grid.

---

## 2. UGCoP and NEAP · 不确定地理背景问题与邻里效应平均化问题

**Problem.**
- *UGCoP*: the environment people actually experience differs from the
  "context unit" the researcher assigns (usually the home neighbourhood).
  Using the home area as exposure introduces measurement error.
- *NEAP*: people move between places during the day, so exposures are
  averaged. Someone living in a polluted area may spend the day in a cleaner
  one and vice versa; mobility-based exposure gaps can be smaller (or larger)
  than residence-based ones.

**Why reviewers ask.** Reviewers working on mobility and environmental
exposure almost always ask: is exposure measured at home or along activity
locations, and how different are the two?

**How to check**
- Report residence-based and mobility-based exposure, and their difference.
- For mobility-based exposure, state the weighting: one record one vote,
  equal weight per day, or dwell-time weighting; whether home locations are
  included.
- Averaging mechanically shrinks variance. Add a null model (e.g. shuffle
  activity locations across people) to show how much of the observed
  difference exceeds mechanical averaging.

**References**
- Kwan, M.-P. (2012). The uncertain geographic context problem. *Annals of the Association of American Geographers* 102(5):958–968. doi:10.1080/00045608.2012.687349
- Kwan, M.-P. (2018). The neighborhood effect averaging problem (NEAP): an elusive confounder of the neighborhood effect. *International Journal of Environmental Research and Public Health* 15(9):1841. doi:10.3390/ijerph15091841
- Kwan, M.-P. (2018). The limits of the neighborhood effect: contextual uncertainties in geographic, environmental health, and social science research. *Annals of the American Association of Geographers* 108(6):1482–1490. doi:10.1080/24694452.2018.1453777

**Example.** Air-pollution exposure from phone traces: inequality across
income groups falls by a third when moving from home-based to mobility-based
exposure. Before calling this a finding, shuffle activity locations to see how
much of the drop is pure averaging. Conversely, if exposure is a city-day
value that everyone in the city receives, say clearly that it measures "how
polluted the city was that day", not individual dose.

---

## 3. Spatial autocorrelation · 空间自相关

**Problem.** Residuals of neighbouring units are similar; observations are
not independent. Ordinary standard errors are too small and significance is
overstated.

**Why reviewers ask.** City, grid and neighbourhood data are almost always
spatially autocorrelated. Reporting p-values without handling it is one of
the most common comments from spatial reviewers.

**How to check**
- Compute global Moran's I on the main model's residuals; state the spatial
  weights (distance band, k-nearest neighbours, contiguity). Use a LISA map to
  locate residual clusters if needed.
- Fixing inference (the coefficient keeps its meaning, only the standard
  errors change) — choose or report several: cluster at a larger spatial unit
  (e.g. province / state); Conley spatial HAC with the distance cutoff stated
  and 2–3 cutoffs as sensitivity; or a spatial error model, which puts the
  dependence in the error term.
- A spatial lag model (SAR, or Durbin with lagged covariates) is different:
  it changes the estimand. With a lagged outcome, the coefficient is no longer
  the marginal effect; report direct, indirect (spillover) and total effects
  instead (LeSage & Pace 2009). Use it only when spillovers are part of the
  question.
- To choose between lag and error specifications, run the Lagrange multiplier
  tests (LM-lag, LM-error and their robust versions) on the OLS residuals
  (Anselin et al. 1996), and state which one the data favour.
- Panels: handle temporal correlation too — two-way clustering by space and
  time, or the spatio-temporal Conley variant.
- Few clusters (e.g. ~30 regions): use a wild cluster bootstrap.
- Be aware that spatially smooth noise alone can yield "significant" results
  (Conley & Kelly 2025).

**References**
- Moran, P. A. P. (1950). Notes on continuous stochastic phenomena. *Biometrika* 37(1–2):17–23. doi:10.1093/biomet/37.1-2.17
- Anselin, L. (1995). Local indicators of spatial association—LISA. *Geographical Analysis* 27(2):93–115. doi:10.1111/j.1538-4632.1995.tb00338.x
- Anselin, L. (1988). *Spatial Econometrics: Methods and Models*. Dordrecht: Kluwer. doi:10.1007/978-94-015-7799-1
- Anselin, L., Bera, A. K., Florax, R. & Yoon, M. J. (1996). Simple diagnostic tests for spatial dependence. *Regional Science and Urban Economics* 26(1):77–104. doi:10.1016/0166-0462(95)02111-6
- LeSage, J. & Pace, R. K. (2009). *Introduction to Spatial Econometrics*. Boca Raton: Chapman and Hall/CRC. doi:10.1201/9781420064254
- Conley, T. G. (1999). GMM estimation with cross sectional dependence. *Journal of Econometrics* 92(1):1–45. doi:10.1016/S0304-4076(98)00084-0
- Dormann, C. F. et al. (2007). Methods to account for spatial autocorrelation in the analysis of species distributional data: a review. *Ecography* 30(5):609–628. doi:10.1111/j.2007.0906-7590.05171.x
- Conley, T. G. & Kelly, M. (2025). The standard errors of persistence. *Journal of International Economics* 153:104027. doi:10.1016/j.jinteco.2024.104027

**Example.** Green-space accessibility regressed on income across 1 km cells:
neighbouring cells are strongly correlated. Report residual Moran's I and
compare with a spatial error model or Conley SEs at three cutoffs.

---

## 4. Ecological fallacy · 生态谬误

**Problem.** A relationship observed for groups (cities, grid cells) cannot be
transferred to individuals. "Counties with brighter night lights have higher
GDP per capita" does not mean "each household near a bright pixel is richer".

**Why reviewers ask.** Reviewers at high-impact journals care about the level
of inference. One individual-level sentence in the abstract or discussion will
be caught.

**How to check**
- For each claim, write down the unit of analysis and compare it with the
  wording: a city × day result speaks only about city-level composition.
- With individual data, add an individual fixed-effects model and check the
  direction; if it differs, discuss composition change (who is observed) vs.
  behaviour change (the same people acting differently).
- Avoid individual-psychology phrasing ("people choose…", "residents tend
  to…") without individual-level evidence.
- State the construct boundary: what the outcome measures and what it does
  not.

**References**
- Robinson, W. S. (1950). Ecological correlations and the behavior of individuals. *American Sociological Review* 15(3):351–357. doi:10.2307/2087176

**Example.** A park-visit study using aggregated phone pings per cell should
say "visits to parks in lower-income cells were fewer", not "low-income
residents visit parks less".

---

## 5. Coordinate reference systems and distance · 坐标系与距离计算

**Problem.** Euclidean distance or area computed on longitude/latitude is
distorted with latitude. Layers from different sources may use different
CRSs; in China, WGS84, GCJ-02 and BD-09 coexist and misalign by hundreds of
metres when overlaid.

**Why reviewers ask.** Buffers, nearest distances, accessibility and kernel
densities change directly with CRS errors. Reviewers familiar with Chinese
data will ask how coordinates were unified.

**How to check**
- For every layer, record the original CRS and every transformation (in the
  dataset card and in Methods).
- Distances: use a projection with small distortion over the study area
  (e.g. the local UTM zone, a transverse Mercator and therefore conformal
  projection) or compute geodesic distances on the ellipsoid. Areas: use an
  equal-area projection (e.g. Albers equal-area, Lambert azimuthal
  equal-area). Do not use a single UTM zone for a national extent.
- For POIs from Chinese web-map providers, confirm GCJ-02 vs. BD-09 before
  converting; then check a few dozen known landmarks against imagery. (No
  formal academic source for these offsets was confirmed; cite the provider's
  documentation.)
- Before raster–vector overlay, check pixel registration (centre vs. corner).

**References**
- Snyder, J. P. (1987). *Map Projections—A Working Manual*. U.S. Geological Survey Professional Paper 1395. doi:10.3133/pp1395
- Vincenty, T. (1975). Direct and inverse solutions of geodesics on the ellipsoid with application of nested equations. *Survey Review* 23(176):88–93. doi:10.1179/sre.1975.23.176.88
- Karney, C. F. F. (2013). Algorithms for geodesics. *Journal of Geodesy* 87(1):43–55. doi:10.1007/s00190-012-0578-z

**Example.** Park-access distances computed in EPSG:4326 degrees and then
multiplied by 111 km: wrong east–west at mid-latitudes. Reproject cells and
parks to the local UTM zone, or compute geodesic distances.

---

## 6. Positional error · 定位误差

**Problem.** Many "point" data are not precise positions: social-media
check-ins carry the representative point of the chosen place (one point for a
whole park or "city"), geocoded addresses snap to street or district
centroids, phone records locate to the serving cell tower.

**Why reviewers ask.** Treating such points as exact when extracting raster
values or drawing buffers brings error into the exposure, and the error may
differ systematically by place type.

**How to check**
- State what a coordinate means (place representative point, address
  centroid, tower location, GPS fix) and the share of records with only
  coarse (e.g. city-level) locations.
- Use coordinates only where the error is much smaller than the analysis unit:
  city-level analysis may be fine; 100 m overlays usually are not.
- Stratify by place type (large parks, scenic areas, malls, residential
  compounds); flag or drop "giant" places whose single point stands for a
  large area.
- When extracting raster values, use a buffer mean as a sensitivity to see
  whether conclusions hinge on a single pixel.

**References**
- Zandbergen, P. A. (2009). Accuracy of iPhone locations: a comparison of assisted GPS, WiFi and cellular positioning. *Transactions in GIS* 13(s1):5–25. doi:10.1111/j.1467-9671.2009.01152.x
- Kwan (2012), above — positional error as one source of UGCoP.

**Example.** Check-ins at a 2 km² park all share one coordinate; a 100 m
buffer around that point says nothing about where visitors were.

---

## 7. Information leakage in spatial cross-validation · 空间交叉验证的信息泄漏

**Problem.** With random train/test splits, neighbouring points land on both
sides. The model scores well by "remembering neighbours" and fails in new
regions. Time series behave the same way.

**Why reviewers ask.** In GeoAI and machine-learning papers, random k-fold
accuracy is often inflated. Reviewers will ask for spatial blocks or
region hold-outs.

**How to check**
- Split by spatial blocks (larger than the residual autocorrelation range),
  by city or region, or by time period. Size blocks from the residual
  variogram or correlation range.
- Report both random k-fold and spatial k-fold. A large gap shows that the
  result depends on spatial autocorrelation and needs explaining; it also
  reflects the difference between interpolation and extrapolation (see
  Wadoux et al. 2021).
- Remove features that leak the label (e.g. a city statistic computed from the
  same records as the target).
- When predicting into new regions or future scenarios, state whether
  predictions lie inside or outside the training data's domain (area of
  applicability).
- Present both sides: when map accuracy is assessed with a probability
  sample, random splits can be appropriate (Wadoux et al. 2021).

**References**
- Roberts, D. R. et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40(8):913–929. doi:10.1111/ecog.02881
- Ploton, P. et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications* 11:4540. doi:10.1038/s41467-020-18321-y
- Meyer, H. et al. (2018). Improving performance of spatio-temporal machine learning models using forward feature selection and target-oriented validation. *Environmental Modelling & Software* 101:1–9. doi:10.1016/j.envsoft.2017.12.001
- Valavi, R. et al. (2019). blockCV: an R package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models. *Methods in Ecology and Evolution* 10(2):225–232. doi:10.1111/2041-210X.13107
- Meyer, H. & Pebesma, E. (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Methods in Ecology and Evolution* 12(9):1620–1633. doi:10.1111/2041-210X.13650
- Wadoux, A. M. J.-C. et al. (2021). Spatial cross-validation is not the right way to evaluate map accuracy. *Ecological Modelling* 457:109692. doi:10.1016/j.ecolmodel.2021.109692

**Example.** A land-cover classifier reaches 95 % with random 10-fold CV and
78 % when whole tiles are held out. Report both; provided the held-out tiles
are representative of the target region, the 78 % is closer to what a new
region will see. Also make sure the same place (or the same place under two spellings)
is not in both the development and the test set.

---

## 8. Temporal alignment · 时间对齐

**Problem.** Reanalysis and satellite products are usually in UTC; behavioural
records are in local time. Which day boundary defines "daily maximum"?
Does an accumulated variable's timestamp refer to the previous or the next
hour? Responses may lag. Any misalignment shifts exposure by hours to a day.

**Why reviewers ask.** Misalignment blurs or shifts effects and is invisible in
the results. For diurnal-rhythm papers reviewers will ask about time zones and
day boundaries.

**How to check**
- For every source, state the time base (UTC / local standard time / local
  solar time) and the conversion.
- Compute daily statistics on the local day boundary and spot-check against an
  official daily product.
- Confirm the meaning of timestamps on accumulated variables (precipitation,
  radiation) in the provider's documentation.
- Run lag sensitivity (same day, previous day, 0–3 day distributed lag).
- For regions spanning many longitudes under one clock time, consider a solar
  time sensitivity.
- Mark collection gaps (hours, days) explicitly; never treat them as zero.

**References**
- Hersbach, H. et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society* 146(730):1999–2049. doi:10.1002/qj.3803
- Muñoz-Sabater, J. et al. (2021). ERA5-Land: a state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data* 13(9):4349–4383. doi:10.5194/essd-13-4349-2021
- Gasparrini, A., Armstrong, B. & Kenward, M. G. (2010). Distributed lag non-linear models. *Statistics in Medicine* 29(21):2224–2234. doi:10.1002/sim.3940

**Example.** Hourly pollution in UTC joined to phone records in UTC+8 without
conversion puts the morning peak at midnight. Convert first, then aggregate on
the local day.

---

## 9. Edge effects · 边缘效应

**Problem.** Units near the study-area boundary have part of their neighbours
or reachable facilities outside it, so statistics are biased. Kernel
densities, K functions, accessibility and spatial lag terms are all affected.
Coarse rasters also mix water and land in coastal and lakeshore cells.

**Why reviewers ask.** Reviewers of accessibility and point-pattern work will
ask whether facilities and population beyond the boundary were included and
whether results near the edge look odd.

**How to check**
- Extend facility and population data beyond the study area by a buffer of at
  least the maximum search radius; compute with them, report only units inside
  the study area.
- Plot results against distance to the boundary to see whether edge units are
  systematically lower or higher.
- Use edge-corrected estimators for point-pattern statistics.
- Coastal cells: report the population share in mixed land/water cells and run
  a land-cells-only sensitivity.

**References**
- Haase, P. (1995). Spatial pattern analysis in ecology based on Ripley's K-function: introduction and methods of edge correction. *Journal of Vegetation Science* 6(4):575–582. doi:10.2307/3236356

**Example.** A city borders three others. Residents near the border use parks
across it; counting only parks inside the city understates their access.
Add neighbouring parks within the search radius, or at least run the
distance-to-boundary diagnostic.

---

## 10. Sample representativeness · 样本代表性

**Problem.** Social-media, app and phone users skew young, urban and
educated; posting is not the same as being present; collection intensity
changes over time and across places. A change in record counts may reflect
platform or collection changes, not behaviour.

**Why reviewers ask.** This is the most frequent question for big-data papers:
to whom do the results generalise? Are the most vulnerable groups (older
people, rural residents, outdoor workers) exactly the ones missing?

**How to check**
- Compare the sample with census data on age, sex and urban/rural share where
  fields exist.
- Use shares rather than absolute counts as outcomes, with unit and time
  fixed effects, or unit × period fixed effects at a level coarser than the
  exposure (e.g. city × month when exposure varies by day), to absorb
  collection intensity. Unit × time fixed effects at the exposure's own level
  absorb all of the exposure's variation, leaving nothing to identify the
  effect.
- Look for collection breaks; stratify by collection period; run
  leave-out sensitivity for the largest cities.
- Test a positive control with a known direction (e.g. fewer outdoor records
  on rainy days) to show the data can detect a real behavioural signal.
- In Limitations, state the bias and whether it would push the effect up or
  down.

**References**
- Mislove, A. et al. (2011). Understanding the demographics of Twitter users. *Proceedings of the International AAAI Conference on Web and Social Media (ICWSM)* 5(1):554–557. doi:10.1609/icwsm.v5i1.14168
- Hecht, B. & Stephens, M. (2014). A tale of cities: urban biases in volunteered geographic information. *Proceedings of the International AAAI Conference on Web and Social Media (ICWSM)* 8(1):197–205. doi:10.1609/icwsm.v8i1.14554
- Longley, P. A., Adnan, M. & Lansley, G. (2015). The geotemporal demographics of Twitter usage. *Environment and Planning A* 47(2):465–484. doi:10.1068/a130122p

**Example.** Park check-ins drop 60 % from one year to the next in every city at
once, and weekends stop differing from weekdays. That is a collection change,
not behaviour; cross-year level comparisons are off, and analysis must be
stratified by collection period.

---

## 11. Multiple testing · 多重检验

**Problem.** Splitting by region, city, place type, time slot and population
group produces many tests; some will be "significant". Local spatial
statistics (LISA, local GWR coefficients) are one test per unit.

**Why reviewers ask.** Heterogeneity analyses and surprising findings often
come from multiple comparisons. Reviewers will ask how many tests were run,
whether they were corrected, and whether the main hypothesis was fixed in
advance.

**How to check**
- Separate primary tests (fixed in advance, one or a few) from exploratory
  analyses, and write them separately.
- Correct exploratory families with FDR (Benjamini–Hochberg) or Romano–Wolf;
  report corrected results.
- LISA cluster maps: use FDR- or Bonferroni-adjusted significance. Adjust
  local GWR coefficient significance too.
- For "no difference" conclusions, use equivalence tests (TOST) instead of
  "not significant".

**References**
- Benjamini, Y. & Hochberg, Y. (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society Series B* 57(1):289–300. doi:10.1111/j.2517-6161.1995.tb02031.x
- Romano, J. P. & Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica* 73(4):1237–1282. doi:10.1111/j.1468-0262.2005.00615.x
- Caldas de Castro, M. & Singer, B. H. (2006). Controlling the false discovery rate: a new application to account for multiple and dependent tests in local statistics of spatial association. *Geographical Analysis* 38(2):180–208. doi:10.1111/j.0016-7363.2006.00682.x
- da Silva, A. R. & Fotheringham, A. S. (2016). The multiple testing issue in geographically weighted regression. *Geographical Analysis* 48(3):233–247. doi:10.1111/gean.12084
- Lakens, D. (2017). Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. *Social Psychological and Personality Science* 8(4):355–362. doi:10.1177/1948550617697177

**Example.** Night-light elasticity estimated separately for 31 provinces;
three are significant at 5 %. Without correction that is roughly what chance
gives.

---

## 12. Spatial heterogeneity (limits of GWR / MGWR) · 空间异质性

**Problem.** Effects differ across places. GWR and MGWR give local
coefficients, but those coefficients are correlated, sensitive to bandwidth,
affected by collinearity, and their local "significance" is a multiple-testing
problem.

**Why reviewers ask.** A pretty map of local coefficients invites
over-interpretation. Expect: how was the bandwidth chosen? Is the variation
larger than random fluctuation? Was local collinearity checked?

**How to check**
- Decide what the question is. To test "the effect differs between type-A and
  type-B regions", an interaction term or split-sample regression is more
  direct; GWR / MGWR is for exploration, not causal claims.
- With MGWR, report each variable's bandwidth and its interval; a bandwidth
  close to the full extent means no clear spatial variation.
- Check local collinearity (local VIF or condition number).
- Correct the significance of local coefficients for multiple testing
  (da Silva & Fotheringham 2016).
- With fixed-effects panels GWR is usually unsuitable; model heterogeneity with
  group × exposure interactions.

**References**
- Brunsdon, C., Fotheringham, A. S. & Charlton, M. E. (1996). Geographically weighted regression: a method for exploring spatial nonstationarity. *Geographical Analysis* 28(4):281–298. doi:10.1111/j.1538-4632.1996.tb00936.x
- Fotheringham, A. S., Yang, W. & Kang, W. (2017). Multiscale geographically weighted regression (MGWR). *Annals of the American Association of Geographers* 107(6):1247–1265. doi:10.1080/24694452.2017.1352480
- Wheeler, D. & Tiefelsdorf, M. (2005). Multicollinearity and correlation among local regression coefficients in geographically weighted regression. *Journal of Geographical Systems* 7(2):161–187. doi:10.1007/s10109-005-0155-6
- Oshan, T. M. et al. (2019). mgwr: a Python implementation of multiscale geographically weighted regression for investigating process spatial heterogeneity and scale. *ISPRS International Journal of Geo-Information* 8(6):269. doi:10.3390/ijgi8060269
- da Silva & Fotheringham (2016), above.

**Example.** An MGWR of green-space access on income gives a local-coefficient
map; the income bandwidth spans 90 % of cells. Report that as "little spatial
variation", not as a regional pattern.
