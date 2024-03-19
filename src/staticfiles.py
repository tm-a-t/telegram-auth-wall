import os
import typing

from fastapi.staticfiles import StaticFiles


class HTMLStaticFiles(StaticFiles):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, html=True)

    def lookup_path(
            self, path: str
    ) -> typing.Tuple[str, typing.Optional[os.stat_result]]:
        if not path.endswith('.html'):
            full_path, stat_result = super().lookup_path(path + '.html')
            if stat_result:
                return full_path, stat_result

        return super().lookup_path(path)
