# -*- coding: utf-8 -*-

# !opt/local/bin/pytho
from reader import ForArticle


def test_hacker_news():
    story = ForArticle()
    story.request_from_firebaseio()
    assert len(story.storage) == 10
    for value in story.storage:
        assert len(value['title']) >= 50
