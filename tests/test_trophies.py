import struct
import sys
import tempfile
import unittest
from pathlib import Path

from paths import ROOT
sys.path.insert(0, str(ROOT / 'launcher'))
import trophies  # noqa: E402


def fake_trp(files):
    """A trophy package with the given {name: bytes}, laid out like sce_sys/trophy/trophy00.trp."""
    element = 0x40
    data_start = 0x60 + element * len(files)
    entries, blobs = b'', b''
    for name, blob in files.items():
        entries += name.encode().ljust(0x20, b'\0') + struct.pack('>QQ', data_start + len(blobs), len(blob))
        entries += b'\0' * (element - 0x30)
        blobs += blob
    header = b'\xdc\xa2\x4d\x00'.ljust(0x10, b'\0') + struct.pack('>II', len(files), element)
    return header.ljust(0x60, b'\0') + entries + blobs


class Trophies(unittest.TestCase):
    def test_the_list_has_every_trophy_once(self):
        self.assertEqual(trophies.TROPHY_COUNT, 39)
        self.assertEqual(trophies.tier(0), 'platinum')
        self.assertEqual([trophies.tier(i) for i in range(1, 39)].count('gold'), 3)
        self.assertEqual(len({name for name, _d, _t in trophies.TEXTS}), 39)
        texts = [row[:2] for row in trophies.TEXTS] + [row for rows in trophies.TRANSLATED.values() for row in rows]
        for name, description in texts:  # the runtime's 127- and 319-byte buffers
            self.assertTrue(name and description and '|' not in name + description and '\n' not in name + description)
            self.assertLess(len(name.encode()), 128)
            self.assertLess(len(description.encode()), 320)
        self.assertEqual(trophies.text(39), ('', ''))

    def test_translations(self):
        for language, rows in trophies.TRANSLATED.items():
            self.assertEqual(len(rows), trophies.TROPHY_COUNT, language)
            self.assertEqual(len({name for name, _d in rows}), trophies.TROPHY_COUNT, language)
        self.assertEqual(trophies.text(22, 'it'), ('Il pollo è la risposta', 'Lancia 42 cosce di pollo.'))
        self.assertEqual(trophies.text(17, 'ru')[0], 'Сэр Толстосум')
        self.assertEqual(trophies.text(22, 'ko'), trophies.text(22))  # no official text: English

    def test_texts_file(self):
        with tempfile.TemporaryDirectory() as folder:
            trophies.write_texts(Path(folder) / 'user', (('notice', 'TROFEO  SBLOCCATO'),), 'it')
            lines = (Path(folder) / 'user' / 'trophy_texts.txt').read_text(encoding='utf-8').splitlines()
        self.assertIn('@notice=TROFEO SBLOCCATO', lines)
        self.assertIn('2=Morten sarebbe orgoglioso | Sblocca tutte le voci del Tomo di Gallowmere.', lines)
        self.assertEqual(sum(line[:1].isdigit() for line in lines), 39)

    def test_icons_are_read_by_id(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'trophy00.trp'
            path.write_bytes(fake_trp({'TROPCONF.ESFM': b'x', 'TROP000.PNG': b'zero', 'TROP012.PNG': b'twelve'}))
            self.assertEqual(trophies.read_trp_icons(path), {0: b'zero', 12: b'twelve'})
            path.write_bytes(b'not a package')
            self.assertEqual(trophies.read_trp_icons(path), {})
        self.assertEqual(trophies.read_trp_icons(Path(folder) / 'missing.trp'), {})

    def test_unlocked_bits_and_reset(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'trophies.dat'
            self.assertEqual(trophies.read_unlocked(path), set())
            self.assertEqual(trophies.reset(path), 0)
            path.write_bytes(struct.pack('<4I', 1 | 1 << 5, 1 << 6, 0, 0))
            self.assertEqual(trophies.read_unlocked(path), {0, 5, 38})
            self.assertEqual(trophies.reset(path), 3)
            self.assertFalse(path.exists())
            self.assertEqual(trophies.read_unlocked(path.with_name('trophies.dat.bak')), {0, 5, 38})


if __name__ == '__main__':
    unittest.main()
