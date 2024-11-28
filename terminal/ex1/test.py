import unittest
from pathlib import Path
import zipfile
import os
from main import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_zip = "test_fs.zip"
        with zipfile.ZipFile(cls.test_zip, "w") as zf:
            zf.writestr("file1.txt", "content1")
            zf.writestr("dir1/file2.txt", "content2")
            zf.writestr("dir1/file3.txt", "content3")

        cls.test_yaml = "test_config.yaml"
        with open(cls.test_yaml, "w") as yaml_file:
            yaml_file.write(f"""
                            username: test_user
                            hostname: test_host
                            fs_path: {cls.test_zip}
                            """)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_zip)
        os.remove(cls.test_yaml)

    def setUp(self):
        self.emulator = ShellEmulator(self.test_yaml)

    def test_ls_root(self):
        result = self.emulator.ls()
        self.assertIn("file1.txt", result)
        self.assertIn("dir1", result)

    def test_cd_valid(self):
        result = self.emulator.cd(["dir1"])
        self.assertEqual(result, "")
        self.assertEqual(self.emulator.current_path, Path("/dir1"))

    def test_cd_invalid(self):
        result = self.emulator.cd(["nonexistent"])
        self.assertIn("Ошибка", result)


    def test_uniq(self):
        result = self.emulator.uniq(["file1.txt"])
        self.assertEqual(result, "content1")

    def test_whoami(self):
        result = self.emulator.run_command("whoami")
        self.assertEqual(result, "test_user")


if __name__ == "__main__":
    unittest.main()
