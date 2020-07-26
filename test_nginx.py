import unittest
import nginx
import os
from time import sleep


class TestNginx(unittest.TestCase):
    def setUp(self):
        self.cn = nginx.conf_manipulator()

    def test_config2json(self):
        self.assertTrue(self.cn.conf2json(nginx_config="alirezajalili.ir.conf", output_name="alirezajalili.ir.config.json"))

    def test_change_conf1(self):

        self.assertTrue(
            self.cn.change_conf(
                block="upstream",
                prev_value="weight=1",
                new_value="weight=333",
                jsonfile="alirezajalili.ir.config.json",
            )
        )

    # def test_change_conf2(self):
    #     self.assertTrue(
    #         self.cn.change_conf(
    #             block="server",
    #             prev_value="$remote_addr",
    #             new_value="$remote_addrrrrr",
    #             directive="proxy_set_header",
    #             attribute="X-Real-IP",
    #             jsonfile="site-config.json",
    #         )
    #     )

    # def test_json2config(self):
    #     self.assertTrue(self.cn.json2conf(jsonfile="new-nginx-config.json"))

    # def test_add_subdomain(self):
    #     self.assertTrue(
    #         self.cn.add_subdomain(domain="prodevops.ir",sub_name="blog", ip='127.0.0.1', ssl=True)
    #     )
    # def test_json2config(self):
    #     self.assertTrue(self.cn.json2conf(jsonfile="new-nginx-config.json"))
    
    # def test_dev_mod(self):
    #     self.assertIsInstance(self.cn.dev_mod("alirezajalili.ir.json", status=False),dict)

if __name__ == "__main__":
    unittest.main()
