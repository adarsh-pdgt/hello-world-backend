# Standard Library
import os.path

from six import text_type

# Third Party Stuff
from settings.exceptions import InvalidGitRepository


def fetch_git_sha(path, head=None):
    """
    fetch_git_sha(os.path.dirname(__file__))
    """
    if not head:
        head_path = os.path.join(path, ".git", "HEAD")
        if not os.path.exists(head_path):
            raise InvalidGitRepository(
                "Cannot identify HEAD for git repository at %s" % (path,)
            )

        with open(head_path, "r") as fp:
            head = text_type(fp.read()).strip()

        if head.startswith("ref: "):
            head = head[5:]
            revision_file = os.path.join(path, ".git", *head.split("/"))
        else:
            return head
    else:
        revision_file = os.path.join(path, ".git", "refs", "heads", head)

    if not os.path.exists(revision_file):
        if not os.path.exists(os.path.join(path, ".git")):
            raise InvalidGitRepository(
                "%s does not seem to be the root of a git repository" % (path,)
            )

        # Check for our .git/packed-refs' file since a `git gc` may have run
        # https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
        packed_file = os.path.join(path, ".git", "packed-refs")
        if os.path.exists(packed_file):
            with open(packed_file) as fh:
                for line in fh:
                    line = line.rstrip()
                    if line and line[:1] not in ("#", "^"):
                        try:
                            revision, ref = line.split(" ", 1)
                        except ValueError:
                            continue
                        if ref == head:
                            return text_type(revision)

        raise InvalidGitRepository(
            'Unable to find ref to head "%s" in repository' % (head,)
        )

    with open(revision_file) as fh:
        return text_type(fh.read()).strip()


def get_release():
    import os
    
    import hello_world

    release = hello_world.__version__
    try:
        git_hash = fetch_git_sha(os.path.dirname(os.pardir))[:7]
        release = "{}-{}".format(release, git_hash)
    except InvalidGitRepository:
        pass
    return release
