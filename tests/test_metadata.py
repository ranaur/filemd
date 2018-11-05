from pprint import pprint
import unittest
from metadata import metadata

import hashlib
def md5(fname):
    return hash(fname, hashlib.md5())

def hash(fname, algorithm):
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            algorithm.update(chunk)
    return algorithm.hexdigest()

import os
import datetime

class TestMetadata(unittest.TestCase):
    testfile = 'test_metadata.py'

    def removeRemoraFile(self):
        try:
            os.remove(self.testfile + '.metadata')
        except:
            pass

    def test_metadata(self):
        print("M0")
        with metadata(self.testfile) as m0:
            m0.clear()

        print("M1")
        with metadata(self.testfile) as m:
            m.setMeta('test key', 'test value')
            self.assertTrue(m.getMeta('test key') == 'test value')
            self.assertFalse(m.getMeta('test key') == 'testNOTvalue')

            m.setMeta('test key2', 'test value2')
            self.assertTrue(m.getMeta('test key2') == 'test value2')
            self.assertFalse(m.getMeta('test key2') == 'testNOTvalue')

            self.assertTrue(m.getMeta('test key NON EXIST', "DEFAULT") == "DEFAULT")
            self.assertTrue(m.getMeta('test key NON EXIST') is None)

            m.remove('test key2')
            self.assertTrue(m.getMeta('test key2') is None)

        with metadata(self.testfile) as m2:
            self.assertTrue(m2.getMeta('test key') == 'test value')
            self.assertFalse(m2.getMeta('test key') == 'testNOTvalue')
            self.assertFalse(m2.getMeta('test key2') == 'test value2')

        with metadata(self.testfile) as m3:
            m3.clear()


    def test_stat(self):
        s = os.stat(self.testfile)
        with metadata(self.testfile) as m:
            m.setMeta('stat.st_mode', s.st_mode)
            m.setMeta('stat.ist_ino', s.st_ino)
            m.setMeta('stat.st_dev', s.st_dev)
            m.setMeta('stat.st_nlink', s.st_nlink)
            m.setMeta('stat.st_uid', s.st_uid)
            m.setMeta('stat.st_gid', s.st_gid)
            m.setMeta('stat.st_size', s.st_size)
            m.setMeta('stat.st_atime', datetime.datetime.fromtimestamp(s.st_atime))
            m.setMeta('stat.st_mtime', datetime.datetime.fromtimestamp(s.st_mtime))
            m.setMeta('stat.st_ctime', datetime.datetime.fromtimestamp(s.st_ctime))

            m.setMeta("path.filename", self.testfile)
            m.setMeta("path.absolute", os.path.abspath(self.testfile))
            m.setMeta("path.base", os.path.basename(self.testfile))
            m.setMeta("path.prefix", os.path.splitext(self.testfile)[0])
            m.setMeta("path.extension", os.path.splitext(self.testfile)[1])

            m.setMeta("hash.md5", hash(self.testfile, hashlib.md5()))
            m.setMeta("hash.sha1", hash(self.testfile, hashlib.sha1()))
            m.setMeta("hash.sha224", hash(self.testfile, hashlib.sha224()))
            m.setMeta("hash.sha256", hash(self.testfile, hashlib.sha256()))
            m.setMeta("hash.sha384", hash(self.testfile, hashlib.sha384()))
            m.setMeta("hash.sha512", hash(self.testfile, hashlib.sha512()))

    def test_tags(self):
        m = metadata(self.testfile)
        m.setTag("tags", "tag1")
        m.setTag("tags", "tag2")
        m.setTag("tags", "tag3")
        m.setTag("tags", "tag4")
        m.setTag("set", "tag5")
        m.setTag("set", "tag6")
        m.setTag("set", "tag7")
        m.setTag("set", "tag8")
        #m.save()
if __name__ == '__main__':
    unittest.main()
