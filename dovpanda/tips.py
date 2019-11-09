import pathlib
import random
import re


class Tip:
    def __init__(self, html=None, ref_url=None, ref_name=None):
        self.html = html
        self.ref_url = ref_url
        self.ref_name = ref_name

    @staticmethod
    def parse_meta(meta):
        meta = meta.split('\n')
        meta = [kv.split(': ') for kv in meta]
        meta = {k: v for k, v in meta}
        return meta

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as f:
            html = f.read()  # .split('\n')
            try:
                meta, content = re.split(r'\n-{3,}\n', html, maxsplit=1)
            except (IndexError, ValueError):
                return cls('parse error', '', '')
        meta = cls.parse_meta(meta)
        return cls(content, **meta)

    def __repr__(self):
        return self.html

    def _repr_html_(self):
        return self.nice_output()

    def nice_output(self):
        html = f'''
        <div class="alert alert-warning" role="alert">
          {self.html}

          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
                  <p>
            Source: <a href="{self.ref_url}" target="_blank">{self.ref_name}</a>
          </p>
        '''
        return html


def random_tip():
    tip_list = pathlib.Path(__file__).parent / 'tip_files'
    tip_list = list(tip_list.iterdir())
    tip_file = random.choice(tip_list)
    tip = Tip.from_file(tip_file)
    return tip


if __name__ == '__main__':
    random_tip()
