#!/usr/bin/env python
"""Leet code problem chooser"""

from enum import Enum
from random import choice, sample
from typing import List, Dict, Any

import click
import requests


class Level(Enum):
    """simple enum for difficulty"""

    easy = 1
    medium = 2
    hard = 3


class LeetProblems:
    """Leet code class interface"""

    def __init__(self, paid: bool = False) -> None:
        url: str = "https://leetcode.com/api/problems/all/"
        self.request: requests.Response = requests.get(url)
        self.problems: List[Dict[str, Any]] = self.request.json()["stat_status_pairs"]
        clean_dict: Dict[int, List[Dict[str, Any]]] = dict(
            zip([i for i in range(1, 4)], [[] for _ in range(1, 4)])
        )
        for problem in self.problems:
            if paid is False and problem["paid_only"] is True:
                pass
            else:
                clean_dict[problem["difficulty"]["level"]].append(
                    {
                        "question_title": problem["stat"]["question__title"],
                        "question_title_slug": problem["stat"]["question__title_slug"],
                        "question_url": f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}",
                        "question_id": problem["stat"]["frontend_question_id"],
                        "paid_only": problem["paid_only"],
                    }
                )

        self.data = clean_dict

    def get_items(self, level: int, num: int) -> List[Dict[str, Any]]:
        """get multiple items"""
        return sample(self[level], k=num)

    def __repr__(self) -> str:
        return str(self.data)

    def __str__(self) -> str:
        return (
            f"Easy: {len(self[1])}\n"
            + f"Medium: {len(self[2])}\n"
            + f"Hard: {len(self[3])}"
        )

    def __getitem__(self, item: int) -> List[Dict[str, Any]]:
        return self.data[item]

    def __delitem__(self, key: int) -> None:
        del self[key]

    def __len__(self) -> int:
        return len(self[1]) + len(self[2]) + len(self[3])


@click.command()
@click.option("--num", prompt="How many problems", help="The total number of problems")
@click.option("--easy", default=0, help="number of easy problems")
@click.option("--medium", default=0, help="number of medium problems")
@click.option("--hard", default=0, help="number of hard problems")
@click.option("--paid", default=False, help="Do you want paid challenges?")
def get_problems(
    num: int, paid: bool, easy: int = 0, medium: int = 0, hard: int = 0
) -> None:
    """Display a leet code problem"""
    leet_problems = LeetProblems(paid)
    levels: Dict[str, Dict[str, int]] = {
        "easy": {"count": easy, "number": 1},
        "medium": {"count": medium, "number": 2},
        "hard": {"count": hard, "number": 3},
    }
    num_rem: int = int(num)
    chosen_problems: Dict[str, List[Dict[str, Any]]] = dict(
        zip("easy medium hard".split(), [[] for _ in range(3)])
    )
    for k, v in list(levels.items()):
        if v["count"] > 0:
            chosen_problems[k] = leet_problems.get_items(v["number"], v["count"])
            num_rem -= v["count"]
            del levels[k]
    level_rem = len(list(levels.keys()))
    if num_rem > 0 and level_rem > 0:
        i = 1
        for k, v in levels.items():
            if i == level_rem:
                chosen_problems[k] = leet_problems.get_items(v["number"], num_rem)
            else:
                rand = choice(range(num_rem))
                chosen_problems[k] = leet_problems.get_items(v["number"], rand)
                num_rem -= rand
                i += 1
    click.echo()
    for level, problems in chosen_problems.items():
        colors = {"easy": "green", "medium": "yellow", "hard": "red"}
        level_print = click.style(level, fg=colors[level])
        for problem in problems:
            click.echo(
                f"\t[{level_print + ']':30}"
                + click.style(f"({problem['question_id']:4}) ", dim=True)
                + click.style(f"{problem['question_title'] + ':':60}", bold=True)
                + click.style(f"{problem['question_url']}", fg="blue")
            )
    click.echo()


if __name__ == "__main__":
    get_problems()
