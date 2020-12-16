#
# Copyright 2020 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"Tabular data loaders."

import os
from typing import Dict, Union

import pandas as pd  # type: ignore

from .. import _typing
from ..schema import SchemaDict
from ._base import Loader


class CSVPandasLoader(Loader):

    def load(self, path: Union[_typing.PathLike, Dict[str, str]], options: SchemaDict) -> str:
        """The type hint says Dict, because this loader will be handling those situations in the future, perhaps via a
        ``IteratingLoader`` class.

        :param path: The path to the CSV file.
        :param options:
               - ``columns`` key specifies the data type of each column. Each data type corresponds to a Pandas'
                 supported dtype. If unspecified, then it is default.
               - ``delimiter`` key specifies the delimiter of the input CSV file.
               - ``no_header`` key specifies if the first row of the CSV file contains the headers. Defaults to False.
                 If the value is set to anything "truthy" in Python, the first row of the CSV will be read as data.
               - ``encoding`` key specifies the encoding of the CSV file. Defaults to UTF-8.
        :raises TypeError: ``path`` is not a path object.
        """

        if not isinstance(path, (str, os.PathLike)):
            # In Python 3.8, this can be done with isinstance(path, typing.get_args(_typing.PathLike))
            raise TypeError(f'Unsupported path type "{type(path)}".')

        parse_dates = []
        dtypes = {}
        for column, type_ in options.get('columns', {}).items():
            if type_ == 'datetime':
                # pandas has this unusual handling of date datatype. Instead of specifying as a data type of a column,
                # we have to pass in `parse_dates`.
                parse_dates.append(column)
            else:
                dtypes[column] = type_

        names = None
        header = None
        if options.get('no_header'):
            # If no header use the columns provided in schema
            names = [*options.get('columns', {})]
        else:
            header = 'infer'

        return pd.read_csv(path, dtype=dtypes,
                           # The following line after "if" is for circumventing
                           # https://github.com/pandas-dev/pandas/issues/38489
                           parse_dates=parse_dates if len(parse_dates) > 0 else False,
                           header=header, names=names,
                           encoding=options.get('encoding', 'utf-8'),
                           delimiter=options.get('delimiter', ','))
