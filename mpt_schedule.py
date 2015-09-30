#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# version: 0.1 Beta Public
# Copyright 2015 Anton Karasev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from urllib import urlopen
from bs4 import BeautifulSoup

buildings = [u'Нахимовский', u'Бирюлёво']


class Schedule(object):
    def __init__(self, bs):
        self.bs = bs
        self.lines = bs.findAll('tr', {'height': '20'})
        self.days = map(Day, zip(*([iter(self.lines)]*14)))


class Day(object):
    def __init__(self, lines):
        self.lines = lines
        if len(self.lines) == 14:
            field = self.lines[0].find('td', {'rowspan': '2'})
            if field and (field.get_text() == u'ТЕКСТИЛЬЩИКИ'):
                self.building = buildings[1]
            else:
                self.building = buildings[0]
            self.day =\
                self.lines[0].find('td', {'rowspan': '14'}).get_text().replace('\r\n', '').replace(' ', '').capitalize()

            self.pairs = map(Pair, zip(*([iter(self.lines)]*2))[1:])
        else:
            raise IOError


class Pair(object):
    def __init__(self, lines):
        self.lines = lines
        first_line =\
            self.lines[0].find('td', {'style': 'border-top:none;border-left:none'})
        second_line = self.lines[1].find('td', {'style': 'border-top:none;border-left:none'}.get_text())
        # TODO: fisrt line is working, second not doing this. check this fuckup
        if first_line:
            self.subject = list()
        else:
            self.subject = None

        if self.subject:
            first_line = first_line.get_text()
            if first_line.count('.'): # если пары делятся на числитель\знаменатель
                self.subject.append(self.split_pair_and_teacher(first_line.split('\r\n'))) ### TODO: перенести все
                self.subject.append(self.split_pair_and_teacher(second_line.split('\r\n')))
                # на выходе [['История', 'Л.А. Чернышова'], ['Обществознание'. 'С.А. Абрамов']]
            else: # если не делятся
                self.subject = list()
                self.subject[0].append(self.replace_double_spaces(first_line.replace('\r\n', '')))
                self.subject[0].append(self.replace_double_spaces(second_line.replace('\r\n', '')))
                # на выходе [['История', 'Л.А. Чернышова'], []]

    def replace_double_spaces(self, line):
        while line.count('  '):
            line.replace('  ', '')
        return line


    def split_pair_and_teacher(self, line): ##### TODO: refactor this shit
        response = list()
        response.append(self.replace_double_spaces(''.join(line[:-1]).strip()))
        response.append(self.replace_double_spaces(''.join(line[-1]).strip()))
        return response


#Schedule(BeautifulSoup(urlopen('http://mpt.ru/education/allocation/alloc_1_e2-13.htm')))