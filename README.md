A simple Python script for parsing a large number of pages from rutracker.me forum topics
===========

> [!WARNING]
> <b>You have opened a branch that is no longer supported!</b> (read: <a href="https://github.com/Dimoka113/Parser-ru-trackers?tab=readme-ov-file#a-simple-python-script-for-parsing-a-large-number-of-pages-from-rutrackerme-forum-topics">Reason</a>)<br>
> You can still use it, but please read this:

<b>Warning</b>
===========
I recommend setting a long delay between receiving torrents so that the ru-tracker doesn't get too angry.<br>

> [!NOTE]
> If you wish, it is best to check with one of the forum moderators to find out how many requests per second YOU can make to the forum.


<b>ATTENTION</b>
===========

> [!CAUTION]
> IF YOU GET BANNED WHILE USING THIS SCRIPT, IT IS ENTIRELY YOUR RESPONSIBILITY.<br>
> I am not responsible in any way, and I am not the admin/moderator of this forum.

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