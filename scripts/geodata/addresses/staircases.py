import random
import six

from geodata.addresses.config import address_config
from geodata.addresses.numbering import NumberedComponent
from geodata.encoding import safe_decode

from geodata.configs.utils import nested_get
from geodata.addresses.directions import RelativeDirection
from geodata.addresses.floors import Floor
from geodata.addresses.numbering import NumberedComponent, sample_alphabet, latin_alphabet
from geodata.encoding import safe_decode
from geodata.math.sampling import weighted_choice, zipfian_distribution, cdf


class Staircase(NumberedComponent):
    max_staircases = 10

    staircase_range = range(1, max_staircases + 1)
    staircase_range_probs = zipfian_distribution(len(staircase_range), 2.0)
    staircase_range_cdf = cdf(staircase_range_probs)

    @classmethod
    def random(cls, language, country=None):
        num_type, num_type_props = cls.choose_alphanumeric_type('staircases.alphanumeric', language, country=country)

        if num_type == cls.NUMERIC:
            number = weighted_choice(cls.staircase_range, cls.staircase_range_cdf)
            return safe_decode(number)
        else:
            alphabet = address_config.get_property('alphabet', language, country=country, default=latin_alphabet)
            letter = sample_alphabet(alphabet, 2.0)
            if num_type == cls.ALPHA:
                return safe_decode(letter)
            else:
                number = weighted_choice(cls.staircase_range, cls.staircase_range_cdf)

                whitespace_probability = float(num_type_props.get('whitespace_probability', 0.0))
                whitespace_phrase = six.u(' ') if whitespace_probability and random.random() < whitespace_probability else six.u('')

                if num_type == cls.ALPHA_PLUS_NUMERIC:
                    return six.u('{}{}{}').format(letter, whitespace_phrase, number)
                elif num_type == cls.NUMERIC_PLUS_ALPHA:
                    return six.u('{}{}{}').format(number, whitespace_phrase, letter)

    @classmethod
    def phrase(cls, staircase, language, country=None):
        if staircase is None:
            return None
        return cls.numeric_phrase('staircases.alphanumeric', staircase, language,
                                  dictionaries=['staircases'], country=country)