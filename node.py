# -*- coding:utf-8 -*-

class Node:

    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __str__(self):
        return 'id : {}, name : {}'.format(self._id, self._name)


class Combination:

    def __init__(self, id):
        self._id = id
        self._container = set()
        self._draw_down = None
        self._growth = None

    @property
    def id(self):
        return self._id

    @property
    def length(self):
        return len(self._container)

    @property
    def weight(self):
        return len(self._container)

    @property
    def draw_down(self):
        return self._draw_down

    @draw_down.setter
    def draw_down(self, v):
        self._draw_down = v

    @property
    def growth(self):
        return self._growth

    @growth.setter
    def growth(self, v):
        self._growth = v

    def add_node(self, node_id):
        self._container.add(node_id)

    @property
    def combination(self):
        return ','.join(sorted(list(map(str, self._container))))

    @property
    def detail(self):
        return self._container

    def describe_node_details(self, signals={}):
        if len(signals) == 0:
            return ''

        desc = '('
        desc += ','.join(sorted([signals[id].name if id in signals else '' for id in self._container]))
        desc += ')'
        return desc

    def __str__(self):
        return self.combination
