from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r'[\w]+')

class MRWordCount(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   reducer=self.reducer_sum_words),
            MRStep(mapper=self.mapper_get_keys,
                   reducer=self.reducer_find_most_common_word)
        ]

    def mapper_get_words(self, _, line):
        words = WORD_RE.findall(line)
        for word in words:
            yield word.lower(), 1

    def reducer_sum_words(self, word, counts):
        yield word, sum(counts)

    def mapper_get_keys(self, key, value):
        yield None, (value, key)

    def reducer_find_most_common_word(self, key, values):
        yield max(values)


if __name__ == '__main__':

    MRWordCount.run()
