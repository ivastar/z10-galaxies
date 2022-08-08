# Iva's Fantastic List of z>=10 Galaxies

This repository contains a `List` definition, `list.yaml` which defines the properties of the List, together with the available properties for `Things` in the `List`:

```YAML
name: "A Fantastic List of z>10 Galaxies"
description: "Iva's list of z>10 galaxies, mostly discovered by JWST. Collected from the arXiv from July 13, 2022 up to now."
properties:
- name: ID
  kind: string
  units: ""
  required: True
  group: Default
  key: default_id
```

`List` items (known as `Things`) are in the `things` folder and follow a format of one `Thing` per YAML file. `Thing` definition files can follow any naming convention. The filename for a `Thing` is not special but in this case we're using the filename to make it more straightforward to identify the galaxy we're describing with the arXiv number and galaxy ID (e.g. `2022arXiv220709434N_GL-z11.yaml`)

`Thing` YAML definitions may only contain properties that are already defined on the parent `List` in `list.yaml`:

```YAML
default_id:
  origin: ''
  value: GL-z11
default_ra:
  origin: ''
  value: 3.51191667
default_dec:
  origin: ''
  value: -30.37186111
default_phot_z:
  origin: ''
  value: 10.9
default_ref:
  origin: ''
  value: 2022arXiv220709434N
  origin: ""
```

## Data Validation

https://github.com/ivastar/z10-galaxies/actions/workflows/ci.yml/badge.svg

This List repository knows how to validate itself by running the tests in `test_list.py`. Any modifications to the `Thing` YAML files or the `List` definition in `list.yaml` will be tested by GitHub Actions CI.
