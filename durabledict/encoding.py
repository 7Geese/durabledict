from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import json
import pickle


class EncoderError(ValueError):
    pass


class EncodingError(EncoderError):
    pass


class DecodingError(EncoderError):
    pass


class Encoder(object):
    encoding_exceptions = ()
    decoding_exceptions = ()

    @staticmethod
    def encoder(data):
        raise NotImplementedError()

    @staticmethod
    def decoder(data):
        raise NotImplementedError()

    @classmethod
    def encode(cls, *args, **kwargs):
        try:
            return cls.encoder(*args, **kwargs)
        except cls.encoding_exceptions as e:
            raise EncodingError(e)

    @classmethod
    def decode(cls, *args, **kwargs):
        try:
            return cls.decoder(*args, **kwargs)
        except cls.decoding_exceptions as e:
            raise DecodingError(e)


class NoOpEncoding(Encoder):
    encode = staticmethod(lambda d: d)
    decode = staticmethod(lambda d: d)


class PickleEncoding(Encoder):
    encoding_exceptions = (TypeError, pickle.PicklingError,)
    decoding_exceptions = (TypeError, pickle.UnpicklingError,)

    @staticmethod
    def encoder(data):
        # 2 is the highest protocol version in python 2. Let's use that for the migration.
        # Can switch this back to `pickle.HIGHEST_PROTOCOL` later
        pickled = pickle.dumps(data, protocol=2)
        return base64.b64encode(pickled)

    @staticmethod
    def decoder(data):
        pickled = base64.b64decode(data)
        return pickle.loads(pickled)


class JSONEncoding(Encoder):
    encoding_exceptions = (TypeError, ValueError,)
    decoding_exceptions = (TypeError, ValueError,)

    encoder = staticmethod(json.dumps)
    decoder = staticmethod(json.loads)


DefaultEncoding = PickleEncoding
