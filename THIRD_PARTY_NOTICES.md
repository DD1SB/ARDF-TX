# Third-party notices and licensing scope

The root [MIT License](LICENSE) applies to original material the ARDF-TX
contributors have rights to license. It does not override these notices,
including those retained in historical commits and archived native packages.

| Material | Attribution and terms |
| --- | --- |
| OpenARDF SignalSlinger/FlexFox80 reference renderings, BOM extracts and reused RF-core principles | OpenARDF; MIT notices retained in [reference assets](docs/assets/80m-reference/LICENSES.md), [RF80 attribution](hardware/80m/LICENSES.md) and [OpenARDF license](hardware/80m/LICENSE-OpenARDF.txt). |
| KiCad-derived symbols, footprints and standard-library artwork in local libraries, assembly overlays and historical archives | KiCad library contributors; **CC-BY-SA-4.0 with the KiCad libraries exception**, not MIT. Retained notices: [RF80](hardware/80m/LICENSES.md), [RF80 production](hardware/80m/production/LICENSES.md), [RF2M](hardware/2m/LICENSE-KICAD-SYMBOLS.md), [controller](hardware/controller/LICENSE-KICAD-LIBRARIES.md). Modifications are described there and in the revision reports. |
| [tools/m5b_e2_sliver.py](tools/m5b_e2_sliver.py) | Algorithm adapted from KiCad 10.0.6 `drc_test_provider_sliver_checker.cpp`; copyright The KiCad Developers, adaptation ARDF-TX contributors, 2026. **GPL-2.0-or-later**; full [GPL v2 text](LICENSES/GPL-2.0-or-later.txt). Source is supplied. MIT does not remove GPL obligations for this helper or combinations distributed under them. Use of the tool does not relicense the hardware. |
| Historical M5A-R3 DL3BBX-derived circuit, schematic and exports | Siegfried Pomplun, DL3BBX, CQ-DL 5/1992 pp.289–292. [Retained restriction](hardware/2m/LICENSE-REFERENCE-DL3BBX.md): attributed copying/printing and private construction permitted; commercial use requires written permission. No commercial permission is claimed. R3 is excluded from the general MIT grant to the extent of those third-party rights. |
| Manufacturer documents and commercial observations | Respective manufacturers/publishers. Official documents are linked, not supplied as a vendor-document collection. Transcribed facts, original calculations and design reports grant no rights to underlying vendor artwork or documents. |

The [official KiCad license](https://www.kicad.org/libraries/license/) explains
that the design/generated-file exception does not relicense redistributed library
collections. The [CC-BY-SA-4.0 legal code](https://creativecommons.org/licenses/by-sa/4.0/legalcode)
is also supplied [locally](LICENSES/CC-BY-SA-4.0.txt) and applies to library material
with that exception. Keep notices with copies,
including local assembly artwork overlays.

The [DL3BBX article](https://www.robkalmeijer.nl/techniek/electronica/radiotechniek/hambladen/cq-dl/1992/page289/index.html)
states its copying/private-construction conditions. Its original article and
illustrations are not republished here. Later R4 and subsequent modern RF2M
work have their own documented manufacturer-reference provenance; they do not
remove R3's restrictions.

FreeRouting, KiCad and other installed verification/rendering programs remain
external tools under their own licenses; their binaries are not supplied here.
No claim is made to relicense external firmware, distributor catalogs or
manufacturer CAD models not supplied in this repository.

FoxPro2 compatibility in M6-L2 is independently written project code. Nick Roethe / DF1FO's original [FOXPRO2.asm](https://df1fo.darc.de/ASM/FOXPRO2.asm), [FJTX.asm](https://df1fo.darc.de/ASM/FJTX.asm) and [Zeitsteuerung2G.doc](https://df1fo.darc.de/DOC/Zeitsteuerung2G.doc) are external technical references, retain their original rights, and are not claimed to be MIT-licensed. Their complete contents and the manufacturer ESP32 STEP model are not redistributed here. The revision source register records reference URLs and retrieved hashes.
