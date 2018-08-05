"""
play_by_ear.py

Copyright (c) 2018 Weipeng He <weipeng.he@idiap.ch>
"""

import random

import mingus.core.notes as notes
import mingus.core.keys as keys
from mingus.containers import Note
from mingus.midi import fluidsynth

fluidsynth.init('/usr/share/soundfonts/default.sf2', 'alsa')


class DefaultLogger:
    def __init__(self):
        # TODO
        pass

    def new_session(self):
        # TODO
        pass

    def log(self, question, answers):
        # TODO
        pass


class CLI:
    def __init__(self):
        # TODO
        pass

    def display(self, qid, n_answered, n_correct):
        print '#%d (Correct: %d/%d)' % (qid, n_correct, n_answered)

    def show_correct(self):
        print 'Correct!'

    def show_wrong(self):
        print 'Wrong!'

    def show_answer(self, answer):
        print 'Answer: %s' % answer

    def get_answer(self):
        a = raw_input('answer : ').upper()
        while not notes.is_valid_note(a) and not a.startswith('R'):
            print 'Invalid input'
            a = raw_input('answer : ').upper()
        return a if not a.startswith('R') else None


class PlayByEar:
    def __init__(self, interface, logger=DefaultLogger()):
        self.interface = interface
        self.logger = logger

    def run(self):
        self.logger.new_session()
        n_answered = 0
        n_correct = 0
        for qid in xrange(10):
            self.interface.display(qid, n_answered, n_correct)
            q = self.get_question()
            correct = False
            aseq = []
            while not correct:
                q.play()
                a = self.interface.get_answer()
                while a is None:
                    q.play()
                    a = self.interface.get_answer()
                aseq.append(a)
                correct = q.is_correct(a)
                if correct:
                    self.interface.show_correct()
                    if len(aseq) == 1:
                        n_answered += 1
                        n_correct += 1
                else:
                    self.interface.show_wrong()
                    if len(aseq) == 1:
                        n_answered += 1
                self.interface.display(qid, n_answered, n_correct)
            self.logger.log(q, aseq)
            self.interface.show_answer(q.get_answer())

    def get_question(self):
        return SingleNote(random.choice(keys.get_notes('C')))


class SingleNote:
    def __init__(self, note):
        self.note = note.upper()

    def play(self):
        fluidsynth.play_Note(Note(self.note))

    def get_answer(self):
        return self.note

    def is_correct(self, answer):
        return answer.upper() == self.note

# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
