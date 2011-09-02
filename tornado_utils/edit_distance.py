class EditDistance(object):
    def __init__(self, against, alphabet=u'abcdefghijklmnopqrstuvwxyz'):
        self.against = against
        self.alphabet = alphabet

    def match(self, word):
        return list(self._match(word))

    def _match(self, word):
        for w in self._edits1(word):
            if w in self.against:
                yield w

    def _edits1(self, word):
        n = len(word)
        return set(# deletion
                   [word[0:i]+word[i+1:] for i in range(n)] +
                   # transposition
                   [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] +
                   # alteration
                   [word[0:i]+c+word[i+1:] for i in range(n) for c in self.alphabet] +
                   # insertion
                   [word[0:i]+c+word[i:] for i in range(n+1) for c in self.alphabet])

if __name__ == '__main__':
    against = ('peter',)
    ed = EditDistance(against)
    assert ed.match('peter') == ['peter']
    assert ed.match('petter') == ['peter']
    assert ed.match('peffeer') == []

    against = ('peter','petter')
    ed = EditDistance(against)
    assert ed.match('pettere') == ['petter']
