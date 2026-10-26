# Trophies

The game calls the PlayStation trophy library (`sceNpTrophy*`). The port answers those calls, keeps
the unlocked trophies on disk and shows them: a notice when a trophy is unlocked, a list inside the
game and a **Trophies** page in the launcher. The same system as the God of War III port
([gow3_pc](https://github.com/FelipePrado0/gow3_pc), `docs/TROPHIES.md`).

The icons and the number of trophies are read from the player's game folder
(`sce_sys/trophy/trophy00.trp`, 39 trophies); no game data is part of the port.

## What the player sees

| Where | What |
|-------|------|
| In the game, when a trophy unlocks | A card at the top-right (below the FPS counter when it is on) with the trophy's icon, name and description. It slides in, stays 5 seconds and fades. |
| In the game, **F8** or **R3+R2** | A list of all trophies: icon, name, description and state (unlocked in colour, locked dimmed), the count, and a filter (all / unlocked / locked). |
| Launcher, **Trophies** page | The same list, with the grade (platinum, gold, silver, bronze), a filter and **Reset trophies**. |

Keys of the in-game list: Up/Down, W/S, PageUp/PageDown, Home/End, mouse wheel or D-pad scroll;
Left/Right, A/D or L1/R1 change the filter; F8, Esc, Backspace, Enter, Circle/Cross or R3+R2 close it.
While it is open the game gets no input (like the Insert menu).

The platinum (id 0) is unlocked with the last other trophy, as on the PlayStation.

## Texts

The names and descriptions are the official PlayStation texts, in `launcher/trophies.py`: English and
the translations of Russian, French, Italian, Spanish, German, Portuguese (Brazil), Polish and
Japanese, copied from trophy sites (the source of each is named there). The localized texts inside
the `.trp` are encrypted and are not read. Chinese, Korean, Turkish and Arabic show English names:
no verified source was found for them (the Chinese PSN text describes an older version of the list).
The labels of the notice and of the list follow the launcher's language, except Arabic, which stays
English in the game (the overlay cannot join Arabic letters or write right to left).

The game's font has no Chinese, Japanese or Korean characters: when the texts need them, the game
adds a system font (Windows: Yu Gothic, Meiryo, Malgun Gothic or Microsoft YaHei; Linux: Noto Sans
CJK, package `google-noto-sans-cjk-fonts` or `fonts-noto-cjk`). `GOW3_CJK_FONT=<path to a .ttf, .otf
or .ttc>` chooses another. Without one those characters are not shown.

The launcher writes `trophy_texts.txt` in the saves folder every time it starts the game. Without
the launcher, put the same file there by hand (or `trophy_names.txt`, used when there is no
`trophy_texts.txt`):

```
# comment
@heading=Trophies
@notice=TROPHY UNLOCKED
@unlocked=UNLOCKED
@locked=LOCKED
@all=All trophies
@only_unlocked=Unlocked
@only_locked=Locked
@counter={} of {} unlocked
@hint=Up/Down: scroll   Left/Right: filter   F8 / R3+R2 / Esc: close
0=Savior of Gallowmere | Unlock all trophies.
1=Quest Complete-est | Complete all levels in the game.
```

`ID=Name | Description` (the description is optional), UTF-8, one trophy per line. The ID is the
trophy's number in the game's trophy list (0 is the platinum). A name takes up to 127 bytes and a
description up to 319. A trophy without a line is shown as `Trophy ID N`. Missing `@` lines use the
English labels.

## Saved state

`trophies.dat` in the saves folder: four little-endian 32-bit words, bit `id % 32` of word `id / 32`
set for an unlocked trophy. The game reads it at start and reports it back when it asks which
trophies are unlocked, so a trophy is noticed once. **Reset trophies** in the launcher moves it to
`trophies.dat.bak` (close the game first: it keeps the trophies in memory while it runs).

Only trophies unlocked with the port are known; the ones earned on a PlayStation are not.
