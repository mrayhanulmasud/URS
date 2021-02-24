"""
Tools
=====
Running all tools that URS has to offer.
"""


import logging

from urs.analytics.Frequencies import GenerateFrequencies
from urs.analytics.Wordcloud import GenerateWordcloud

from urs.praw_scrapers.Basic import RunBasic
from urs.praw_scrapers.Comments import RunComments
from urs.praw_scrapers.Redditor import RunRedditor
from urs.praw_scrapers.Subreddit import RunSubreddit
from urs.praw_scrapers.utils.Validation import Validation

from urs.utils.Cli import (
    CheckCli,
    Parser
)
from urs.utils.Global import s_t
from urs.utils.Titles import MainTitle

class Run():
    """
    Methods to call CLI and all tools.
    """

    def __init__(self, reddit):
        """
        Initialize variables used in instance methods:

            self._reddit: Reddit instance
            self._args: argparse Namespace object
            self._parser: argparse ArgumentParser object

        Returns
        -------
        None
        """

        self._reddit = reddit
        self._args, self._parser = self._introduce_then_args()
        
    def _introduce_then_args(self):
        """
        Print title, then run checks for CLI args and PRAW credentials.

        Parameters
        ----------
        None

        Returns
        -------
        args: Namespace
            argparse Namespace object
        parser: ArgumentParser
            argparse ArgumentParser object
        """

        MainTitle.title()

        args, parser = Parser().parse_args()
        CheckCli().check_args(args, parser)

        return args, parser

    def run_urs(self):
        """
        Switch for running all URS tools.
        """

        if self._args.check:
            """
            Run rate limit check.
            """

            logging.info("RUNNING API CREDENTIALS CHECK.")
            logging.info("")

            Validation.validate_user(self._parser, self._reddit)

        elif self._args.subreddit or self._args.redditor or self._args.comments or self._args.basic:
            """
            Run PRAW scrapers.
            """
            
            Validation.validate_user(self._parser, self._reddit)

            if self._args.subreddit:
                RunSubreddit.run(self._args, self._parser, self._reddit, s_t)
            if self._args.redditor:
                RunRedditor.run(self._args, self._parser, self._reddit)
            if self._args.comments:
                RunComments.run(self._args, self._parser, self._reddit)
            elif self._args.basic:
                RunBasic.run(self._args, self._parser, self._reddit)
        
        elif self._args.frequencies or self._args.wordcloud:
            """
            Run analytical tools.
            """

            if self._args.frequencies:
                GenerateFrequencies().generate(self._args)
            if self._args.wordcloud:
                GenerateWordcloud().generate(self._args)
        