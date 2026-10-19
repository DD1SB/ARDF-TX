# Contributing to ARDF-TX

Start with the [current hardware table](README.md#hardware-architecture) and
[documentation index](docs/README.md). Report the commit, population, toolchain
and reproduction commands. Separate CAD/model results from measurements. A
proposed ADR is not an accepted decision.

## Source and checks

Use a normal branch and pull request. Keep changes focused and retain all
third-party notices. Original contributions default to [MIT](LICENSE);
identify material under other terms explicitly.

```sh
python3 tools/m7_publication.py verify
python3 -m unittest discover -s firmware/controller_hw -p 'test_*.py' -v
cc -std=c11 -Wall -Wextra -Werror firmware/controller_hw/contract.c firmware/controller_hw/test_contract.c -lm -o /tmp/ardf-controller-contract
/tmp/ardf-controller-contract
```

Electrical changes need pad assertions, connector contracts, fail-off and
population checks. Layout changes need actual KiCad ERC/DRC, native-geometry
DFM and affected RF/power/thermal checks. Disclose warnings, excluded categories,
assumptions and remaining physical gates.

## Engineering artifact reproduction

The recorded environment uses KiCad 10.0.6, standard libraries and matching
`pcbnew` bindings, Python 3 and a C11 compiler. Additional geometry/render
dependencies are documented in each revision's instructions. There is no
universal package-install or `make` target.

Use a disposable worktree:

```sh
git worktree add --detach /tmp/ardf-reproduction HEAD
```

Follow the preserved commands for [controller](hardware/controller/review/M6-L1/REPRODUCE.md),
[RF80](hardware/80m/production/review/M4A-V1R1/REPRODUCE.md) or
[RF2M](hardware/2m/review/M5B-E5/REPRODUCE.md).
Historical checks can bind exact historical inputs: use the pinned commit when
replaying that milestone. Old generators can replace an entire schematic or
board; they are not routine verification commands.

Do not overwrite old review directories or fabrication ZIPs with a new revision.
Provide a new package with native hashes, tool versions, ERC/DRC, net/pad and DFM
results and SHA-256 manifest. A changed source invalidates its old bound manifest;
do not edit old checksums to conceal a design change.

CAD review, supplier quotation, purchase, assembly, energizing and RF operation
are separate stages. A pull request or passing simulation authorizes none of
those physical actions. Current physical qualification remains pending.
