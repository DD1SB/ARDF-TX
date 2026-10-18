# Assembly artwork overlays

These project-local copies of 33 used KiCad/custom footprints move small body art and reference text from silkscreen to fabrication layers. Copper, holes, pad numbers, courtyards and model references remain the audited original geometries, except the six explicitly revised standard-PTH landings in `ARDF_TX.pretty`.

The overlays keep component IDs stable and make library/PCB comparison meaningful. They do not disable DRC or add decorative courtyards. Their purpose is a readable standard white legend; essential marks are board-level text at least 1.0 mm high with 0.15 mm strokes.

Credit: KiCad library contributors; CC-BY-SA-4.0 WITH KiCad-libraries-exception. See [licence and source attribution](../LICENSES.md). Standard source copies came from the installed KiCad 10 libraries. Original manufacturer package assertions remain in the electrical verification; these are artwork variants, not replacement components.
