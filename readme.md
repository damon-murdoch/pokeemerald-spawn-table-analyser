# Wild Encounter Analyzer
## PokeEmerald Wild Encounter Analyzer
### Created by Damon Murdoch ([@SirScrubbington](https://twitter.com/SirScrubbington))

## About

This script has been developed for the purpose of reporting
which species have encounters in your PokeEmerald project,
which is useful for projects where you are trying to have
as many different encounters as possible. 

It can be used as a source of truth for tracking which 
Pokemon are and are not able to be encountered in your
rom hack directly, or can be used as a data source for
another script / program to be analysed with greater 
detail. 

The goal of this script is to prevent the need for having 
a seperate, manually updated document or spreadsheet 
outlining which species currently do and do not have
encounters available.

### Usage

The command-line usage of this tool is as follows:

```bash
python analyser.py [path-to-wild-encounters.json]
```

It is advised to use Python 3.x for this project.

### Input

- `path-to-wild-encounters.json`: The path to the JSON file containing wild Pokémon encounter data.

### Output

The script generates a CSV report file named `encounter-report.csv` in the same folder as the input file. The report includes the following columns:

- `Species`: Pokémon species identifier.
- `Encounters`: Number of encounters for each species.
- `Routes`: List of routes where each species can be encountered (pipe-separated).

### Example

Please see below for a sample output for the script.

```csv
Species,Encounters,Routes
SPECIES_BULBASAUR,1,gRoute102
SPECIES_IVYSAUR,0,
SPECIES_VENUSAUR,0,
SPECIES_CHARMANDER,0,
SPECIES_CHARMELEON,0,
...
SPECIES_CATERPIE,1,gRoute102
SPECIES_METAPOD,0,
SPECIES_BUTTERFREE,0,
SPECIES_WEEDLE,0,
SPECIES_KAKUNA,0,
SPECIES_BEEDRILL,0,
SPECIES_PIDGEY,1,gRoute102
SPECIES_PIDGEOTTO,0,
SPECIES_PIDGEOT,0,
SPECIES_RATTATA,1,gRoute102
...
SPECIES_URSHIFU_SINGLE_STRIKE_STYLE_GIGANTAMAX,0,
SPECIES_URSHIFU_RAPID_STRIKE_STYLE_GIGANTAMAX,0,
```

### Limitations

Please note, this script currently only references
the first member of the `wild_encounter_groups` array
in the `wild-encounters.json` file, as (at least in 
vanilla) the other two do not allow for you to catch 
any Pokemon. Because of this, if you encounter groups
have been reorganised for whatever reason, this script
will not work for you without either modifying your
project structure or the script itself.
