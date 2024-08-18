"""Implementation of TagRule."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ansiblelint.constants import LINE_NUMBER_KEY
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule, TransformMixin

if TYPE_CHECKING:
    from ansiblelint.errors import MatchError
    from ansiblelint.utils import Task


class TagRule(AnsibleLintRule, TransformMixin):
    """Rule for checking task tags."""

    id = "tag"
    description = (
        "All task tags should have distinct names"
        "and templates in tags should be avoided."
    )
    severity = "MEDIUM"
    tags = ["idiom"]
    _re_templated = re.compile(r"^.*\{\{.*\}\}.*$")
    _ids = {
        "tag[no-duplicate]": "Tasks should not duplicate tags.",
        "tag[no-template]": "Tasks should not use Jinja templates in tags.",
    }

    def matchtask(
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> list[MatchError]:
        results: list[MatchError] = []
        if file and file.failed():
            return results
        tags = task.get("tags")
        if tags:
            if len(tags) != len(set(tags)):
                results.append(
                    self.create_matcherror(
                        message="Tasks should not duplicate tags.",
                        lineno=task[LINE_NUMBER_KEY],
                        tag="tag[no-duplicate]",
                        filename=file,
                    ),
                )
            for tag in tags:
                if self._re_templated.match(tag):
                    results.append(
                        self.create_matcherror(
                            message="Tasks should not use Jinja templates in tags.",
                            lineno=task[LINE_NUMBER_KEY],
                            tag="tag[no-template]",
                            filename=file,
                        ),
                    )
                    break
        return results
