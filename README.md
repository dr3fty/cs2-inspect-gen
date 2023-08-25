## cs-inspect-gen

A Proof of Concept script to generate inspect links from broskins' gen codes.

### Usage
First, install the latest protobuf package: `pip install protobuf`

Then run the script by executing `python convert-gen.py <command> <args>`

#### Commands
- `gengl <def id> <paint index> <paint seed> <paint wear>`
- `gen <def id> <paint index> <paint seed> <paint wear> (<sticker id> <sticker wear>)`
- `genrarity <rarity id> <... same arguments as !gen>`

By default, all inspect links generated for weapons don't have their rarities set, you can set the rarity manually by using a `genrarity` command

#### Possible Rarities

(I was too lazy to implement items_game parsing, so instead you have to set the rarity manually)

| ID | Name             | Color      |
|----|------------------|------------|
| 0  | Stock            | Gray       |
| 1  | Consumer Grade   | Gray       |
| 2  | Industrial Grade | Light Blue |
| 3  | Mil-Spec Grade   | Blue       |
| 4  | Restricted       | Purple     |
| 5  | Classified       | Pink       |
| 6  | Covert           | Red        |
| 7  | Contraband       | Gold       |
| 99 |                  | Gold       |