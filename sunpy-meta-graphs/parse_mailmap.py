import git
from pathlib import Path


def get_author_transform_mapping(repo):
    """
    Read the mailmap into a `dict` to be used to transform authors.

    Parameters
    ----------

    repo : `git.Repo`

    """

    mailmap_file = Path(repo.working_tree_dir) / ".mailmap"

    if not mailmap_file.exists():
        raise ValueError("This repo does not have a mailmap")

    with open(mailmap_file) as fd:
        mailmap_lines = fd.readlines()

    for i, line in enumerate(mailmap_lines):
        line = line.strip().lower()
        split = line.find("> ") + 1
        mailmap_lines[i] = (line[:split].strip(), line[split+1:].strip())[::-1]

    return dict(mailmap_lines)
