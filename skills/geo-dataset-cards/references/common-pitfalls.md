# Common pitfalls of geospatial data

Use this list as a prompt when reading a dataset's documentation and when
running the checks in `SKILL.md`. Write a pitfall into a card only when the
dataset's own documentation, a paper or a recorded check supports it, and cite
that source. The examples are generic illustrations, not statements about any
specific product.

## 1. Point coordinates are not always where people were

**Example.** A social-media check-in dataset gives a latitude and longitude for
each post. For many platforms that pair is the representative point of a
tagged place (a POI), not a GPS fix of the user. Consequences: many posts share
one coordinate, positions snap to venue centroids, and a large park or campus
is a single point. Do not use such points for sub-POI distances, trajectories
at metre scale or exposure at the user's true position. Treat them as "place
visited".

**Check.** Count distinct coordinate pairs against rows; look at the top
repeated coordinates.

## 2. China coordinate offsets (WGS-84 / GCJ-02 / BD-09)

Maps and POI services in mainland China commonly publish GCJ-02 (an offset
system) or BD-09 (a further offset on top of GCJ-02); satellite products and
GNSS use WGS-84. Mixing them shifts features by tens to hundreds of metres,
which breaks grid-cell assignment and point-in-polygon joins. Several versions
of the same dataset can coexist (raw, converted, re-converted); a card must say
which one a file is, and a conversion must never be applied twice.

**Check.** Plot a few well-known landmarks or road intersections against a
WGS-84 basemap; compare the offset direction and size with the known
GCJ-02 / BD-09 behaviour. Only inside China do these offsets apply.

## 3. Collection breaks make levels non-comparable across years

A data platform may change what it collects (a source dropped, a coverage
threshold changed, an indexing rule updated). The number of records or users
then jumps at a date for reasons unrelated to the phenomenon. Year-to-year
level comparisons across the break are invalid; within-segment comparisons or
share-based measures may still work.

**Check.** Plot records per month and per region over the whole period; look
for step changes, not for trends. Record the break dates on the card.

## 4. Raster cell versus point (and cell area)

A raster cell is an area, a point is a location. Sampling a coarse cell at a
point assigns the cell mean to a place that may differ from it. Cells in a
geographic (lat/lon) grid shrink in area toward the poles, so sums or
densities need area weighting; a cell value labelled "per cell" is not "per
km2". When aggregating to administrative units, say whether the method is
centroid-in-polygon, area-weighted or zonal statistics, and whether cells that
straddle a boundary are split.

**Check.** Read the units in the metadata (per cell, per km2, count, mean);
compute the cell area at the study latitude.

## 5. Reanalysis accumulated variables and time stamps

Reanalysis products often store precipitation, radiation and similar fluxes as
accumulations over a window that resets at fixed hours or from a forecast
start. The stamp can refer to the end of the accumulation window, and the
value is a running total, not an instantaneous rate. Taking differences
incorrectly, mixing UTC with local time, or reading an end-of-window stamp as
the start shifts results by hours and can produce negative or doubled values.
Instantaneous variables (e.g. 2 m temperature) do not have this problem.
Period maxima and minima (e.g. ERA5's `mx2t` / `mn2t`, maximum / minimum 2 m
temperature since the previous post-processing) are statistics over the
preceding period, so they carry the same time-stamp issue: the value stamped
00 UTC describes the hour before it, which belongs to the previous day.

**Check.** Read the variable's documentation (accumulation period, stamp
convention, units); verify on one day that de-accumulated values are
non-negative and sum to the daily total.

## 6. Population grid versions differ

Gridded population products are released in versions that change the base
census, the redistribution model, the constraint to built-up areas and the
reference year. Values for the same cell and year can differ materially
between versions, and some are "unconstrained" (modelled everywhere) versus
"constrained" (only where buildings are detected). Do not mix versions within
one analysis, do not compare totals across versions, and record version, year,
constrained flag and resolution on the card.

**Check.** Sum the grid over a unit with a known official total and compare;
record the ratio.

## 7. Other recurring traps

- **Time zone and day boundary.** Daily aggregates cut at UTC midnight differ
  from local calendar days; say which one was used.
- **Boundary vintage.** Administrative boundaries change (merges, renamings,
  code reassignments). A boundary file's year must match the statistics' year.
- **Missing values coded as numbers.** `-9999`, `0` or `65535` used as fill;
  check the documented fill value before computing statistics.
- **Scale factors and offsets.** Integer-stored rasters need `scale_factor`
  and `add_offset` applied exactly once.
- **Mirror and version drift.** Two download mirrors of the "same" product can
  differ in version or processing date; compare checksums or a statistical
  fingerprint.
- **Projection and distance.** Distances and areas computed in lat/lon
  degrees are wrong; use a suitable projected CRS.
- **Ecological and scale effects.** Results at one spatial unit (MAUP) do not
  transfer to another; record the unit on the card.
