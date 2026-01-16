A simple Python script for parsing a large number of pages from rutracker.me forum topics
===========

> [!IMPORTANT]
> ## <b>There are two branches in this repository:</b><br>
> <b>Synchronous</b> (<a href="https://github.com/Dimoka113/Parser-ru-trackers/tree/main">current</a>)<br>
> <b>Asynchronous</b> (<a href="https://github.com/Dimoka113/Parser-ru-trackers/tree/async-download">async-download</a>) (No longer supported)<br><br>
> ## <b>Why are they separated?</b>
> I want to support this project, but I don't want to harm the forum.<br>
> Therefore, it was decided to abandon a large number of requests to the forum.<br>
> Therefore, the "asynchronous" version remains for memory.<br>
> You can still use it, but before you do, read the section below:<br>


<b>Warning</b>
===========
I recommend setting a long delay between receiving torrents so that the ru-tracker doesn't get too angry.<br>

> [!NOTE]
> If you wish, it is best to check with one of the forum moderators to find out how many requests per second YOU can make to the forum.

<b>ATTENTION</b>
===========

> [!WARNING]
> IF YOU GET BANNED WHILE USING THIS SCRIPT, IT IS ENTIRELY YOUR RESPONSIBILITY.<br>
> I am not responsible in any way, and I am not the creator/moderator of this forum.

------

How to install
===========

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