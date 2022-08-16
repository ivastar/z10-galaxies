# Iva's Fantastic List of z>=10 Galaxies

This is a list of interesting things in this case high-redshift galaxies. All `things` are found in `src/website/things` folder. New `things` can be added via pull request or commit.

## Webpage

The data from this list is displayed on a GitHub Pages [webpage](https://ivastar.github.io/z10-galaxies/). The page has sortable columns, table search and per-column search, export options.

The page is recreated every time the reporsitory master branch is updated. 

## Simple API

The data for each thing can be accessed via a simple API in the following format:

`https://ivastar.github.io/z10-galaxies/things/[default_ref]_[default_id].yml`

This will return a the yml file for this thing. For example the data for object GL-z11 from 2022arXiv220709434N is available at: 

[https://ivastar.github.io/z10-galaxies/things/2022arXiv220709434N_GL-z11.yml](https://ivastar.github.io/z10-galaxies/things/2022arXiv220709434N_GL-z11.yml)

## List Definition

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

`List` items (known as `Things`) are in the `src/website/things` folder and follow a format of one `Thing` per YAML file. `Thing` definition files can follow any naming convention. The filename for a `Thing` is not special but in this case we're using the filename to make it more straightforward to identify the galaxy we're describing with the arXiv number and galaxy ID (e.g. `2022arXiv220709434N_GL-z11.yaml`)

`Thing` YAML definitions may only contain properties that are already defined on the parent `List` in `list.yaml`:

```YAML
default_id:
  value: GL-z11
default_ra:
  value: 3.51191667
default_dec:
  value: -30.37186111
default_phot_z:
  value: 10.9
default_ref:
  value: 2022arXiv220709434N
```

The `src/website/things` folder also contains a `TEMPLATE` empty file should you want to use that to generate a new thing easier. 


## Data Validation

![This is an image](https://github.com/ivastar/z10-galaxies/actions/workflows/ci.yml/badge.svg)

This List repository knows how to validate itself by running the tests in `test_list.py`. Any modifications to the `Thing` YAML files or the `List` definition in `list.yaml` will be tested by GitHub Actions CI. All properties with `default` in the name must be set in order for the tests to pass. All properties must be included even of most of them are empty.

## To Do

- How to make your own list of thing
- How to connect to a Google spreadsheet (maybe https://github.com/epetenko/google-sheets-scraper)
