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

If you are only interested in a few recent ones, use the positional argument start_date. The script will output the links
from the corresponding month's archive onward until the most recent one:

```sh
$ ./random-org-torrent-links 2024-12
https://archive.random.org/download?file=2024-12-bin.torrent
https://archive.random.org/download?file=2025-01-bin.torrent
https://archive.random.org/download?file=2025-02-bin.torrent
...
```
