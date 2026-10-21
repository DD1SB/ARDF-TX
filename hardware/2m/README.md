# RF2M — M5B-E6R2 controlled evaluation candidate

Open [RF2M.kicad_pro](RF2M.kicad_pro). The current, independently reviewed
M5B-E6R2 evaluation candidate is a 150×110 mm, two-layer project. It implements
carrier-keyed A2A Architecture C and one supported SK81 100 SA cooler
for Q501/Q401/Q402. The 20-pin controller contract and critical RF routing are
preserved. Controller M6-L2 and RF80 are unchanged.

Read the [review decision](../../docs/M5B_E6R2_REVIEW_DECISION.md),
[implementation](../../docs/M5B_E6R2_IMPLEMENTATION.md),
[mechanical assembly](../../docs/M5B_E6R2_MECHANICAL_ASSEMBLY.md),
[manufacturing](../../docs/M5B_E6R2_MANUFACTURING.md) and
[first-article plan](../../docs/M5B_E6R2_FIRST_ARTICLE_TEST.md).
The [review package](review/M5B-E6R2/README.md) contains fresh native/CAD evidence,
Gerbers,separate drills,full top stencil,3D views,STEP assembly and all populations.

Independent review found no concrete blocker for **five bare evaluation PCBs**.
Physical RF, thermal and operational qualification remains **NOT_RUN**, and
target firmware integration remains incomplete. No board or stencil has been
ordered and no hardware energized. See the [final reproduction/publication record](../../docs/M5B_E6R2_FINAL_PUBLICATION.md).

- [Five-board fabrication ZIP](review/M5B-E6R2/fabrication/RF2M-M5B-E6R2_JLCPCB_5boards.zip).
- [Full top stencil](review/M5B-E6R2/fabrication/RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip).
- [Mechanical STEP assembly](review/M5B-E6R2/mechanical/complete-mechanical-stack.step).

[E5 review/manufacturing](review/M5B-E5/README.md),[E6](review/M5B-E6/README.md)
and[E6R1](review/M5B-E6R1/README.md) remain immutable. A starting E5native snapshot
is additionally preserved in the E6R2 review package. Use the current
[reproduction procedure](review/M5B-E6R2/REPRODUCE.md),not old CAD-generation
commands against this updated native project.
