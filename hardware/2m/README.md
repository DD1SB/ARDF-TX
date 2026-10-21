# RF2M — M5B-E6R2 controlled evaluation candidate

Open [RF2M.kicad_pro](RF2M.kicad_pro). This native150×110mm,2layer project
implements carrier-keyed A2A ArchitectureC and one supported SK81100SA cooler
for Q501/Q401/Q402. The20pin controller contract and critical RF routing are
preserved. Controller M6-L2 and RF80 are unchanged.

Read the [review decision](../../docs/M5B_E6R2_REVIEW_DECISION.md),
[implementation](../../docs/M5B_E6R2_IMPLEMENTATION.md),
[mechanical assembly](../../docs/M5B_E6R2_MECHANICAL_ASSEMBLY.md),
[manufacturing](../../docs/M5B_E6R2_MANUFACTURING.md) and
[first-article plan](../../docs/M5B_E6R2_FIRST_ARTICLE_TEST.md).
The [review package](review/M5B-E6R2/README.md) contains fresh native/CAD evidence,
Gerbers,separate drills,full top stencil,3D views,STEP assembly and all populations.

Engineering disposition concerns five bare evaluation boards only. Physical
RF/AM/thermal qualification and target firmware integration remain incomplete.
No order,powered operation,acceptance tag,production release or push is implied.

[E5 review/manufacturing](review/M5B-E5/README.md),[E6](review/M5B-E6/README.md)
and[E6R1](review/M5B-E6R1/README.md) remain immutable. A starting E5native snapshot
is additionally preserved in the E6R2 review package. Use the current
[reproduction procedure](review/M5B-E6R2/REPRODUCE.md),not old CAD-generation
commands against this updated native project.
