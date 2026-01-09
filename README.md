A simple Python script for parsing a large number of pages from rutracker.me forum topics
===========

How to install
------
* ..It is assumed that you already have an account on rutracker.me.
* Download Python 3.11 (newer or older versions may be supported, but this has not been tested).
* Download the latest version or clone the repository
* Rename `example.api.py` to `api.py`, specify your “bb_session” and “bb_data” in it. (You can use any plugin to get cookies from your browser)

How to use
------
<b>* - optional</b>

In the config.py file, configure:<br>
`limit` - How many files to download per run.<br>
`SEEDS_LIMIT` - How many seeds there should be (<SEEDS_LIMIT) <br>
*`MAX_PAGES`  - Number of pages to check<br>

In the main.py file:<br>
If you already have some downloaded .torrent files, you can specify check=True, which will tell the script to go through the “torrents” directory and do nothing else.<br>

Select the topic number you want to parse and specify it in FORUM_ID or specify 0 if you want to go through the tracker's “red book”.<br>

Enjoy!

Using the code
------
> [!NOTE]
> Although there is a license for this, I want to duplicate it here.<br>
> If you use my code or the code, please consider adding links to the original authors.<br>
> And please read the license.<br>
> Thank you! 