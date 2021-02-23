     __  __  _ __   ____  
    /\ \/\ \/\`'__\/',__\ 
    \ \ \_\ \ \ \//\__, `\
     \ \____/\ \_\\/\____/
      \/___/  \/_/ \/___/... Universal Reddit Scraper 

![GitHub top language](https://img.shields.io/github/languages/top/JosephLai241/URS?logo=Python)
[![PRAW Version](https://img.shields.io/badge/PRAW-7.1.4-red?logo=Reddit)][PRAW]
[![Build Status](https://img.shields.io/travis/JosephLai241/URS?logo=Travis)][Travis CI Build Status]
[![Codecov](https://img.shields.io/codecov/c/gh/JosephLai241/URS?logo=Codecov)][Codecov]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/JosephLai241/URS)][Releases]
![License](https://img.shields.io/github/license/JosephLai241/URS)

<p align="center"> 
    <img 
        alt="Full Demo"
        src="https://i.imgur.com/lEDB7wP.png">
</p>

# Table of Contents

* [Contact](#contact)
* [Introduction](#introduction)
* [URS Overview](#urs-overview)
    + [Export File Format](#export-file-format)
    + [Export Directory Structure](#export-directory-structure)
    + [Scrape Speeds](#scrape-speeds)
    + [Scraping Reddit via PRAW](#scraping-reddit-via-praw)
        * [Getting Started](#getting-started)
        * [Rate Limits](#rate-limits)
        * [Table of All Subreddit, Redditor, and Submission Comments Attributes](#a-table-of-all-subreddit-redditor-and-submission-comments-attributes)
        * [Subreddits](#subreddits)
        * [Redditors](#redditors)
        * [Submission Comments](#submission-comments)
    + [Analytical Tools](#analytical-tools)
        * [Target Fields](#target-fields)
        * [Generating Word Frequencies](#generating-word-frequencies)
        * [Generating Wordclouds](#generating-wordclouds)
    + [Exporting](#exporting)
* [Contributing](#contributing)
    + [Before Making Pull or Feature Requests](#before-making-pull-or-feature-requests)
    + [Building on Top of URS](#building-on-top-of-urs)
    + [Making Pull or Feature Requests](#making-pull-or-feature-requests)
* [Contributors](#contributors)
* [Derivative Projects](#derivative-projects)
* Supplemental Documents
    + [How to get Reddit API Credentials for PRAW][How to get Reddit API Credentials for PRAW]
    + [Error Messages and Rate Limit Information][Error Messages and Rate Limit Info]
    + [2-Factor Authentication][2-Factor Authentication]
    + [Releases/Changelog][Releases]
    + [Some Linux Tips][Some Linux Tips]

# Contact

Whether you are using URS for enterprise or personal use, I am very interested in hearing about your use case and how it has helped you achieve a goal. 

Additionally, please send me an email if you would like to [contribute](#contributing), have questions, or want to share something you have built on top of it. 

You can send me an email or leave a note by clicking on either of these badges. I look forward to hearing from you!

[![Email](https://img.shields.io/badge/Email-urs__project%40protonmail.com-informational?logo=ProtonMail)][URS Project Email]
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-blue)][Say Thanks!]

# Introduction

This is a comprehensive Reddit scraping tool that integrates multiple features:

* Scrape Reddit via [`PRAW`][PRAW] (the official Reddit API)
    + Scrape Subreddits
    + Scrape Redditors
    + Scrape submission comments
* Analytical tools for scraped data
    + Get frequencies for words that are found in submission titles, bodies, and/or comments
    + Generate a wordcloud from scrape results
    
Run `pip install -r requirements.txt` to get all project dependencies. 

You will need your own Reddit account and API credentials for PRAW. See the [Getting Started](#getting-started) section for more information. 

***NOTE:*** `PRAW` is currently supported on Python 3.6+.

# URS Overview

## Export File Format

**All files except for those generated by the wordcloud tool are exported to JSON by default**. Wordcloud files are exported to PNG by default. URS supports exporting to CSV as well, but JSON is the more versatile option. See the [Exporting](#exporting) section for more information.

## Export Directory Structure

All exported files are saved within the `scrapes` directory and stored in a sub-directory labeled with the date. Many more sub-directories may be created in the date directory. Sub-directories are only created when its respective tool is run.

The `subreddits`, `redditors`, or `comments` directories are created when you run each scraper.

The `analytics` directory is created when you run any of the analytical tools. Within it, the `frequencies` or `wordclouds` directories are created when you run each tool. See the [Analytical Tools](#analytical-tools) section for more information.

All of these directories are automatically created when you run URS and its respective scrapers. For example, if you only use the Subreddit scraper, only the `subreddits` directory is created.

This is the [samples][Samples]' directory structure generated by the [tree command][tree].

```
scrapes/
└── 02-22-2021
    ├── analytics
    │   ├── frequencies
    │   │   ├── askreddit-hot-100-results.csv
    │   │   └── askreddit-hot-100-results.json
    │   └── wordclouds
    │       ├── spez-5-results.png
    │       └── What do you think about adults that don’t eat ve---RAW.png
    ├── comments
    │   ├── What do you think about adults that don’t eat ve---50-results.json
    │   └── What do you think about adults that don’t eat ve---RAW.json
    ├── redditors
    │   └── spez-5-results.json
    ├── subreddits
    │   ├── askreddit-hot-100-results.csv
    │   ├── askreddit-hot-100-results.json
    │   └── wallstreetbets-search-'robinhood'-past-month-rules.json
    └── urs.log
```

## Scrape Speeds

Scrape speed is determined by a couple things:

* The number of results returned for Subreddit or Redditor scraping
* The submission's popularity (total number of comments) for submission comments scraping
* Your internet connection speed

## Scraping Reddit via PRAW

### Getting Started

It is very quick and easy to get Reddit API credentials. Refer to [my guide][How to get Reddit API Credentials for PRAW] to get your credentials, then update the `API` dictionary located in `Credentials.py`

### Rate Limits

Yes, PRAW has rate limits. These limits are proportional to how much karma you have accumulated - the higher the karma, the higher the rate limit. This has been implemented to mitigate spammers and bots that utilize PRAW.

Rate limit information for your account is displayed in a small table underneath the successful login message each time you run any of the PRAW scrapers. I have also added a `--check` flag if you want to quickly view this information.

URS will display an error message as well as the rate limit reset date if you have used all your available requests.

There are a couple ways to go about solving issues with rate limits:

* Scrape intermittently
* Use an account with high karma to get your PRAW credentials
* Scrape less results per run

Available requests are refilled if you use the PRAW scrapers intermittently, which might be a good solution to bypassing rate limit issues. This can be especially helpful if you have automated URS and are not looking at the output on each run.

---

### A Table of All Subreddit, Redditor, and Submission Comments Attributes

These attributes are included in each scrape. 

| Subreddits    | Redditors                      | Submission Comments |
|---------------|--------------------------------|---------------------|
| Title         | Name                           | Parent ID           |
| Flair         | Fullname                       | Comment ID          |
| Date Created  | ID                             | Author              |
| Upvotes       | Date Created                   | Date Created        |
| Upvote Ratio  | Comment Karma                  | Upvotes             |
| ID            | Link Karma                     | Text                |
| Is Locked?    | Is Employee?                   | Edited?             |
| NSFW?         | Is Friend?                     | Is Submitter?       |
| Is Spoiler?   | Is Mod?                        | Stickied?           |
| Stickied?     | Is Gold?                       |                     |
| URL           | \*Submissions                  |                     |
| Comment Count | \*Comments                     |                     |
| Text          | \*Hot                          |                     |
| &nbsp;        | \*New                          |                     |
| &nbsp;        | \*Controversial                |                     |
| &nbsp;        | \*Top                          |                     |
| &nbsp;        | \*Upvoted (may be forbidden)   |                     |
| &nbsp;        | \*Downvoted (may be forbidden) |                     |
| &nbsp;        | \*Gilded                       |                     |
| &nbsp;        | \*Gildings (may be forbidden)  |                     |
| &nbsp;        | \*Hidden (may be forbidden)    |                     |
| &nbsp;        | \*Saved (may be forbidden)     |                     |

\*Includes additional attributes; see [Redditors](#redditors) section for more information. 

---

### Subreddits

<img
    alt="Subreddit Demo GIF"
    src="https://i.imgur.com/ikAxcwe.gif">

\*This GIF is uncut.

**Usage:** `$ ./Urs.py -r SUBREDDIT [H|N|C|T|R|S] N_RESULTS_OR_KEYWORDS` 

**Supported export formats:** JSON and CSV. To export to CSV, include the `--csv` flag.

You can specify Subreddits, the submission category, and how many results are returned from each scrape. I have also added a search option where you can search for keywords within a Subreddit.

These are the submission categories:

* Hot
* New
* Controversial
* Top
* Rising
* Search

The file names for all categories except for Search will follow this format: 

`"[SUBREDDIT]-[POST_CATEGORY]-[N_RESULTS]-result(s).[FILE_FORMAT]"`

If you searched for keywords, file names will follow this format:

`"[SUBREDDIT]-Search-'[KEYWORDS]'.[FILE_FORMAT]"` 

### Time Filters

Time filters may be applied to some categories. Here is a table of the categories on which you can apply a time filter as well as the valid time filters.

| Categories    | Time Filters  | 
|---------------|---------------|
| Controversial | All (default) |
| Top           | Day           |
| Search        | Hour          |
| &nbsp;        | Month         | 
| &nbsp;        | Week          |
| &nbsp;        | Year          |

Specify the time filter after the number of results returned or keywords you want to search for.

**Usage:** `$ ./Urs.py -r SUBREDDIT [C|T|S] N_RESULTS_OR_KEYWORDS OPTIONAL_TIME_FILTER`

If no time filter is specified, the default time filter `all` is applied. The Subreddit settings table will display `None` for categories that do not offer the additional time filter option.

If you specified a time filter, `-past-[TIME_FILTER]` will be appended to the file name before the file format like so: 

`"[SUBREDDIT]-[POST_CATEGORY]-[N_RESULTS]-result(s)-past-[TIME_FILTER].[FILE_FORMAT]"` 

Or if you searched for keywords:

`"[SUBREDDIT]-Search-'[KEYWORDS]'-past-[TIME_FILTER].[FILE_FORMAT]"`

After submitting the arguments, URS will display a table of Subreddit scraping settings as a final check before executing. You can include the `-y` flag to bypass this check.

Exported files will be saved to the `subreddits` directory.

***NOTE:*** Up to 100 results are returned if you search for keywords within a Subreddit. You will not be able to specify how many results to keep.

---

### Redditors

<img
    alt="Redditor Demo GIF"
    src="https://i.imgur.com/QTZuztr.gif">

\*This GIF has been cut for demonstration purposes.

**Usage:** `$ ./Urs.py -u USER N_RESULTS` 

**Supported export formats:** JSON.

You can also scrape Redditor profiles and specify how many results are returned.

Some Redditor attributes are sorted differently. Here is a table of how each is sorted.

| Attribute Name | Sorted By/Time Filter                       |
|----------------|---------------------------------------------|
| Comments       | Sorted By: New                              |
| Controversial  | Time Filter: All                            |
| Gilded         | Sorted By: New                              |
| Hot            | Determined by other Redditors' interactions |
| New            | Sorted By: New                              |
| Submissions    | Sorted By: New                              |
| Top            | Time Filter: All                            |

Of these Redditor attributes, the following will include additional attributes:

| Submissions, Hot, New, Controversial, Top, Upvoted, Downvoted, Gilded, Gildings, Hidden, and Saved | Comments                                     |
|----------------------------------------------------------------------------------------------------|----------------------------------------------|
| Title                                                                                              | Date Created                                 |
| Date Created                                                                                       | Score                                        |
| Upvotes                                                                                            | Text                                         |
| Upvote Ratio                                                                                       | Parent ID                                    |
| ID                                                                                                 | Link ID                                      |
| NSFW?                                                                                              | Edited?                                      |
| Text                                                                                               | Stickied?                                    |
| &nbsp;                                                                                             | Replying to (title of submission or comment) |
| &nbsp;                                                                                             | In Subreddit (Subreddit name)                |

The file names will follow this format: 

`"[USERNAME]-[N_RESULTS]-result(s).[FILE_FORMAT]"` 

Exported files will be saved to the `redditors` directory.

***NOTE:*** If you are not allowed to access a Redditor's lists, PRAW will raise a 403 HTTP Forbidden exception and the program will just append a "FORBIDDEN" underneath that section in the exported file. 

***NOTE:*** The number of results returned are applied to all attributes. I have not implemented code to allow users to specify different number of results returned for individual attributes. 

---

### Submission Comments

<img
    alt="Structured Comments Demo GIF"
    src="https://i.imgur.com/CJJSfJI.gif">
<img
    alt="Raw Comments Demo GIF"
    src="https://i.imgur.com/sPSYDjZ.gif">

\*These GIFs have been cut for demonstration purposes.

**Usage:** `$ ./Urs.py -c URL N_RESULTS` 

**Supported export formats:** JSON.

You can also scrape comments from submissions and specify the number of results returned. 

Comments are sorted by "Best", which is the default sorting option when you visit a submission.

**There are two ways you can scrape comments: structured or raw.** This is determined by the number you pass into `N_RESULTS`:

| Scrape Type | N_RESULTS      |
|-------------|----------------|
| Structured  | N_RESULTS >= 1 |
| Raw         | N_RESULTS = 0  |

Structured scrapes resemble comment threads on Reddit and will include down to third-level comment replies. 

Raw scrapes do not resemble comment threads, but returns all comments on a submission in level order: all top-level comments are listed first, followed by all second-level comments, then third, etc.

Of all scrapers included in this program, this usually takes the longest to execute. PRAW returns submission comments in level order, which means scrape speeds are proportional to the submission's popularity.

The file names will follow this format: 

`"[POST_TITLE]-[N_RESULTS]-result(s).[FILE_FORMAT]"` 

Exported files will be saved to the `comments` directory.

***NOTE:*** You cannot specify the number of raw comments returned. The program with scrape all comments from the submission. 

## Analytical Tools

This suite of tools can be used *after* scraping data from Reddit. Both of these tools analyze the frequencies of words found in submission titles and bodies, or comments. 

***PRO TIP:*** Drag and drop the file into the terminal to quickly get the correct filepath.

Running either tool will create the `analytics` directory within the date directory. **This directory is located in the same directory in which the scrape data resides**. For example, if you run the frequencies generator on February 16th for scrape data that was captured on February 14th, `analytics` will be created in the February 14th directory. Command history will still be written in the February 16th `urs.log`.

A shortened export path is displayed once URS has completed exporting the data, informing you where the file is saved within the `scrapes` directory. You can open `urs.log` to view the full path. 

The sub-directories `frequencies` or `wordclouds` are created in `analytics` depending on which tool is run.

***NOTE:*** Do not move the `scrapes` directory elsewhere if you want to use these tools. URS uses a relative path to save the generated files.

---

### Target Fields

The data varies depending on the scraper, so these tools target different fields for each type of scrape data:

| Scrape Data         | Targets                 |
|---------------------|-------------------------|
| Subreddit           | "title", "text"         |
| Redditor            | "title", "body", "text" |
| Submission Comments | "text"                  |

For Subreddit scrapes, data is pulled from the "title" and "text" fields for each submission (submission title and body).

For Redditor scrapes, data is pulled from all three fields because both submission and comment data is returned. The "title" and "body" fields are targeted for submissions, and the "text" field is targeted for comments.

For submission comments scrapes, data is only pulled from the "text" field of each comment.

---

### Generating Word Frequencies

<img
    alt="Frequencies Demo GIF"
    src="https://i.imgur.com/mlQAInp.gif">

**Usage:** `$ ./Urs.py -f FILE_PATH` 

**Supported export formats:** JSON and CSV. To export to CSV, include the `--csv` flag.

You can generate a dictionary of word frequencies created from the words within the target fields. 

Frequencies export to JSON by default, but this tool also works well in CSV format.

Exported files will be saved to the `analytics/frequencies` directory.

---

### Generating Wordclouds

<img
    alt="Wordcloud Demo GIF"
    src="https://i.imgur.com/VyDxVV9.gif">

**Usage:** `$ ./Urs.py -wc FILE_PATH`

**Supported export formats:** .eps, .jpeg, .jpg, .pdf, .png (default), .ps, .rgba, .tif, .tiff.

Taking word frequencies to the next level, you can generate wordclouds based on word frequencies. This tool is independent of the frequencies generator - you do not need to run the frequencies generator before creating a wordcloud. 

PNG is the default format, but you can also export to any of the options listed above by including the format as the second flag argument.

**Usage:** `$ ./Urs.py -wc FILE_PATH OPTIONAL_EXPORT_FORMAT` 

Exported files will be saved to the `analytics/wordclouds` directory.

## Exporting

As stated before, URS supports exporting to either JSON or CSV. **JSON is the default format** - you will have to include the `--csv` flag to export to CSV.

I recommend only exporting to CSV when using:

+ The Subreddit scraper
+ The word frequencies generator

These tools are also suitable for CSV format and are optimized to do so if you want to use that format instead.

JSON is the more practical option for Redditor and submission comments scraping, which is why I have designed these scrapers to work best in this format. It is much easier to read the scrape results since Redditor scraping returns attributes that include additional submission or comment attributes. 

Comments scraping is especially easier to read in JSON format because structured exports look similar to threads on Reddit. You can process all the information pertaining to a comment much quicker compared to CSV. 

You can still export Redditor data and submission comments to CSV, but you will be disappointed with the results.

### See the [samples][Samples] for scrapes ran on February TBD, 2021.

# Contributing

**See the [Contact](#contact) section for ways to reach me.**

## Before Making Pull or Feature Requests

Consider the scope of this project before submitting a pull or feature request. URS stands for Universal Reddit Scraper. Two important aspects are listed in its name - *universal* and *scraper*.

I will not approve feature or pull requests that deviate from its sole purpose. This may include scraping a specific aspect of Reddit or [adding functionality that allows you to post a comment with URS][Commenting Feature Request]. Adding either of these requests will no longer allow URS to be universal or merely a scraper. However, I am more than happy to approve requests that enhance the current scraping capabilities of URS.

## Building on Top of URS

Although I will not approve requests that deviate from the project scope, feel free to reach out if you have built something on top of URS or have made modifications to scrape something specific on Reddit. I will add your project to the [Derivative Projects](#derivative-projects) section!

## Making Pull or Feature Requests

You can suggest new features or changes by going to the [Issues tab][Issues] and fill out the Feature Request template. If there is a good reason for a new feature, I will consider adding it.

You are also more than welcome to create a pull request - adding additional features, improving runtime, or refactoring existing code. If it is approved, I will merge the pull request into the master branch and credit you for contributing to this project.

# Contributors

| Date           | User                                                      | Contribution                                                                                                               |
|----------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| March 11, 2020 | [ThereGoesMySanity][ThereGoesMySanity] | Created a [pull request][ThereGoesMySanity Pull Request] adding 2FA information to README |
| October 6, 2020 | [LukeDSchenk][LukeDSchenk] | Created a [pull request][LukeDSchenk Pull Request] fixing "[Errno 36] File name too long" issue, making it impossible to save comment scrapes with long titles |
| October 10, 2020 | [IceBerge421][IceBerge421] | Created a [pull request][IceGerge421 Pull Request] fixing a cloning error occuring on Windows machines due to illegal filename characters, `"`, found in two scrape samples |

# Derivative Projects

This is a showcase for projects that are built on top of URS!

* [skiwheelr/URS][skiwheelr Project Link] 
    + Contains a bash script built on URS which counts ticker mentions in Subreddits, subsequently cURLs all the relevant links in parallel, and counts the mentions of those.
    + ![skiwheelr screenshot][skiwheelr screenshot]

<!-- BADGES: Links for the badges at the top of the README -->
[Codecov]: https://codecov.io/gh/JosephLai241/URS
[PRAW]: https://pypi.org/project/praw/
[Releases]: https://github.com/JosephLai241/URS/releases
[Say Thanks!]: https://saythanks.io/to/jlai24142%40gmail.com
[Travis CI Build Status]: https://travis-ci.com/github/JosephLai241/URS
[Github Actions - Pytest]: https://github.com/JosephLai241/URS/actions?query=workflow%3APytest 
<!-- [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/JosephLai241/URS/Pytest?logo=github)][Github Actions - Pytest] -->
[URS Project Email]: mailto:urs_project@protonmail.

<!-- DEMO GIFS: Links to demo GIFS -->
[Main Demo]: https://someimgurlink.com

[Subreddit Demo]: https://i.imgur.com/ikAxcwe.gif
[Redditor Demo]: https://i.imgur.com/QTZuztr.gif
[Structured Comments Demo]: https://i.imgur.com/CJJSfJI.gif
[Raw Comments Demo]: https://i.imgur.com/sPSYDjZ.gif

[Frequencies Demo]: https://i.imgur.com/mlQAInp.gif
[Wordcloud Demo]: https://i.imgur.com/VyDxVV9.gif

<!-- GITHUB LINKS: Links around the URS repo on GitHub -->
[Issues]: https://github.com/JosephLai241/URS/issues
[Commenting Feature Request]: https://github.com/JosephLai241/URS/issues/17

<!-- SEPARATE DOCS: Links to documents located in the docs/ directory -->
[2-Factor Authentication]: https://github.com/JosephLai241/URS/blob/master/docs/Two-Factor%20Authentication.md
[Error Messages and Rate Limit Info]: https://github.com/JosephLai241/URS/blob/master/docs/Error%20Messages.md
[How to get Reddit API Credentials for PRAW]: https://github.com/JosephLai241/URS/blob/master/docs/How%20to%20Get%20PRAW%20Credentials.md
[Releases]: https://github.com/JosephLai241/URS/blob/master/docs/Releases.md
[Some Linux Tips]: https://github.com/JosephLai241/URS/blob/master/docs/Some%20Linux%20Tips.md

<!-- SAMPLES: Links to the samples directory -->
[Samples]: https://github.com/JosephLai241/URS/tree/master/samples/scrapes/02-05-2021

<!-- ThereGoesMySanity: Links for user ThereGoesMySanity and pull request -->
[ThereGoesMySanity]: https://github.com/ThereGoesMySanity
[ThereGoesMySanity Pull Request]: https://github.com/JosephLai241/URS/pull/9

<!-- LukeDSchenk: Links for user LukeDSchenk and pull request -->
[LukeDSchenk]: https://github.com/LukeDSchenk
[LukeDSchenk Pull Request]: https://github.com/JosephLai241/URS/pull/19

<!-- IceBerge421: Links for user IceBerge421 and pull request -->
[IceBerge421]: https://github.com/IceBerge421
[IceGerge421 Pull Request]: https://github.com/JosephLai241/URS/pull/20

<!-- DERIVATIVE PROJECTS LINKS: Links to projects that were built on top of URS -->
[skiwheelr Project Link]: https://github.com/skiwheelr/URS
[skiwheelr screenshot]: https://i.imgur.com/ChHdAZv.png

<!-- ADDITIONAL LINKS: A space for useful links -->
[tree]: http://mama.indstate.edu/users/ice/tree
