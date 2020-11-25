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

import os
import pathlib
from typing import Dict, Optional, Union

from .. import _typing
from ..schema import SchemaDict
from ._base import Loader


class PlainTextLoader(Loader):

    def load(self, path: Union[_typing.PathLike, Dict[str, str]], options: Optional[SchemaDict]) -> str:
        """The type hint says Dict, because this loader will be handling those situations in the future.

        :param path: The path to the plain text file.
        :param options: Unused.
        """

        if not isinstance(path, (str, os.PathLike)):
            # In Python 3.8, this can be done with isinstance(path, typing.get_args(_typing.PathLike))
            raise TypeError(f'Unsupported path type "{type(path)}".')
        return pathlib.Path(path).read_text()
