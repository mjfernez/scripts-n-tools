import sys
import json
import unittest
import subprocess
sys.path.append('..')
import fhash

class TestFhash(unittest.TestCase):
    # these files were teseted with openssl
    HASHES = json.load(open('hashes.json'))
    FHASH = "../fhash.py"
    DIR = "files/"


    def test_shattered(self):
        """Just for fun, two files that have the same hash, breaking sha1"""
        SHATTERED = '38762cf7f55934b34d179ae6a4c80cadccbb7f0a'
        cmd = [self.FHASH, 'sha1', '-i', self.DIR + 'shattered-1.pdf']
        shat1 = subprocess.check_output(cmd).strip().decode()
        cmd[3] = self.DIR + 'shattered-2.pdf'
        shat2 = subprocess.check_output(cmd).strip().decode()
        self.assertTrue(shat1 == shat2 == SHATTERED)


    def test_file_types(self):
        """Tests that hashes for different file types are correct.
        Uses sha1"""
        for k in self.HASHES.keys():
            cmd = [self.FHASH, 'sha1', '-i', self.DIR + k]
            fh = subprocess.check_output(cmd).strip().decode()
            ssl = self.HASHES[k]['sha1']
            self.assertFalse(ssl != fh, 
                    f"{k}:{fh} did not match the correct hash: {ssl}"
                )

    def test_algos(self):
        """Tests that hashes for different algorithms and sizes are correct.
        """

        for k in self.HASHES.keys():
            for alg in fhash.ALGOS:
                if alg == 'md5' or alg == 'sha1':

                    cmd = [self.FHASH, alg, '-i', self.DIR + k]
                    fh = subprocess.check_output(cmd).strip().decode()
                    ssl = self.HASHES[k][alg]
                    self.assertFalse(ssl != fh, 
                            f"{k}:{fh} did not match the correct hash: {ssl}"
                        )
                else:
                    for s in fhash.SIZES:
                        cmd = [self.FHASH, alg, '-i', self.DIR + k, '-s',
                                str(s)]
                        fh = subprocess.check_output(cmd).strip().decode()
                        ssl = self.HASHES[k][alg + '-' + str(s)]
                        self.assertFalse(ssl != fh, 
                                f"{k}:{fhash} did not match the correct hash: {ssl}"
                            )


if __name__ == '__main__':
    unittest.main()
