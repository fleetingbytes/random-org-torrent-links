# random-org-torrent-links

A script to output the torrent download links to the monthly archives from Random.org's Pregenerated File Archive - Binary Files.

## Usage

Run without arguments, it outputs links to all the monthly archives from the beginning of Random.org until the most current.

```sh
$ ./random-org-torrent-links
https://archive.random.org/download?file=2006-03-bin.torrent
https://archive.random.org/download?file=2006-04-bin.torrent
https://archive.random.org/download?file=2006-05-bin.torrent
...
```

If you are only interested in the most recent ones, pipe it to `tail` (where with `-n` you specify how many of the most recent ones you want)

```sh
$ ./random-org-torrent-links | tail -n 1
https://archive.random.org/download?file=2026-10-bin.torrent
```

You can also use a positional argument (in `%Y-%m` format) to start the listing from a specific date:

```sh
$ ./random-org-torrent-links 2024-12
https://archive.random.org/download?file=2024-12-bin.torrent
https://archive.random.org/download?file=2025-01-bin.torrent
https://archive.random.org/download?file=2025-02-bin.torrent
...
```
