# -*- coding: utf-8 -*-

# !opt/local/bin/python
import os
import json
import requests
import pickle
from newspaper import Article
import string
from reader_window import Curses
from constant import *


class ForArticle(object):
    def __init__(self):
        self.storage = []
        self.news_id = None
        self.another_id = None
        self.top_list = []

    def request_from_firebaseio(self):
        self.top_list = requests.get(STORY_URL).json()[:10]
        for value in self.top_list:
            request = requests.get(ITEM_URL % value)
            self.storage.append(request.json())

    def check_top_list(self):
        if not self.read_top_list():
            self.request_from_firebaseio()
            self.cache_top_list(self.top_list)
            self.cache_dict_content()
            self.display_on_console()
        else:
            self.check_equality()

    def cache_dict_content(self):
        dict_content = {}
        self.cache_top_dict(dict_content)
        i = 0
        for value in self.top_list:
            if value == self.storage[i]['id']:
                try:
                    dict_content[value] = self.storage[i]["title"], self.storage[i]["url"]
                except KeyError:
                    dict_content[value] = self.storage[i]["title"], ["HN_URL" % value]
            i += 1
        self.cache_top_dict(dict_content)

    def check_equality(self):
        self.request_from_firebaseio()
        cached_top_list = self.read_top_list()
        if set(cached_top_list) == set(self.top_list):
            print "Both are equal..!"
            self.display_on_console()
        else:
            self.check_non_equality(cached_top_list)

    def check_non_equality(self, cached_top_list):
        print "Both are not eqaula..!"
        a = []  # the list contains different values from cached_top_list
        for value in self.top_list:
            if not value in cached_top_list:
                a.append(value)
        rest_list = cached_top_list[:-len(a)]
        rest_list.extend(a)
        self.cache_top_list(rest_list)
        self.cache_temporary_dict(cached_top_list, a)
        self.display_on_console()

    def cache_temporary_dict(self, cached_top_list, a):
        temporary_dict = self.read_top_dict()
        b = cached_top_list[
            len(cached_top_list) - len(a):]  # the list contains deleted dict according to changes in top_list
        for value in b:
            temporary_dict.pop(value)
        i = 0
        for value in a:
            if value == self.storage[i]['id']:
                temporary_dict[value] = self.storage[i]["title"], self.storage[i]["url"]
            i += 1
        self.cache_top_dict(temporary_dict)

    def cache_top_list(self, top_list):
        pickle.dump(top_list, open("list.p", "wb"))

    def cache_top_dict(self, top_dict):
        pickle.dump(top_dict, open("dictionary.p", "wb"))

    def read_top_dict(self):
        content = pickle.load(open("dictionary.p", 'rb'))
        return content

    def read_top_list(self):
        try:
            content = pickle.load(open("list.p", 'r'))
            return content
        except (EOFError, IOError):
            return None

    def display_on_console(self):
        i = 0
        for value in self.storage:
            try:
                print i + 1, " ", value["title"], value["url"]
            except IndexError:
                pass
            i += 1
        self.condition()

    def text_article(self, news_id):
        news_id -= 1
        news_url = self.storage[news_id]["url"]
        article = Article(url=news_url)
        article.download()
        article.parse()
        return article.title + "\n" + "===============================================" + "\n" + article.text

    def range_article(self, news_id):
        if news_id in string.ascii_letters + string.punctuation + string.whitespace:
            Curses().popup()

        else:
            if int(news_id) in range(1, 11):
                self.another_id = int(news_id)

                print self.text_article(int(news_id))
            else:
                Curses().popup()

    def condition(self):
        while True:
            news_id = self.input_from_user()
            if news_id == "0":
                self.display_on_console()
            elif news_id == "*":
                if self.another_id:
                    self.another_id -= 1
                    print self.text_article(self.another_id)
                else:
                    Curses().popup()
            elif news_id == "-":
                if self.another_id:
                    self.another_id += 1
                    print self.text_article(self.another_id)
                else:
                    Curses().popup()
            elif news_id == "q":
                quit()
            elif news_id == "?":
                Curses().popup()
            else:
                self.range_article(news_id)

    def input_from_user(self):
        return raw_input("Please,enter a character:")


if __name__ == "__main__":
    ForArticle().check_top_list()
else:
    print "!!!!!!!!!!!"
