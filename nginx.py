try:
    import json
    import time
    import subprocess
    import crossplane
    import os

except ImportError:
    print("One of required Package is not installed")


class conf_manipulator:
    def __init__(self):
        # self.nginx_config_file_address = nginx_config_file_address
        self.start_time = time.time()

    def writer(self, conf, name="nginx-config.json"):
        # try:
        #     os.remove("nginx-config.json")
        # except:
        #     print("SSSSSS")

        try:
            with open(name, "w+") as outfile:
                json.dump(conf, outfile)
        except Exception as e:
           
            print(e)
            return False
        else:
            return True

    def conf2json(self, nginx_config, output_name="nginx-config.json"):
        """
        this function will read a nginx Config and Parse it and save it as a Json Format
        INPUT:
            nginx_config = address of Nginx config file
            output_name = if You Want Desire Name, Defult is 'site-config.json'
        OUTPUT:
            Json file that will save to the current directory
        """
        try:
            subprocess.call(
                ["crossplane", "parse", "--no-catch","--include-comments","--single-file", "-o", output_name, nginx_config,]
            )
        except Exception as error:
            for e in error:
                print(e)
            return False
        else:
            return True

    def json2conf(self, jsonfile="site-config.json", dir=None):
        """
        this function will build a Nginx json file and build it as a nginx config
        INPUT:
            jsonfile = Nginx Json File the was build by 'conf2json' function
            dir = the base directory to build in
        OUTPUT:
            nginx config file that will save in current dir or in desire dir (if you passed)
        """
        try:
            subprocess.call(["crossplane", "build", "-t", "-f", "-d", "dir", jsonfile])
        except Exception as error:
            print("EEEEEEEEEERRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRR")
            print(error)
            return False
        else:
            return True

    def change_conf(
        self,
        block: str,
        prev_value: str,
        new_value: str,
        directive=None,
        attribute=None,
        jsonfile=None,
    ):


        """
        INPUT:
            block:str -> this is directive name.
            prev_value:str -> previus value that we want to change
            new_value:str -> new value for that argument
            directive -> is just For 'server' block.
            attribute -> is just For 'server' block. and is secound parametr of directive

        OUTPUT:
            a modified json file that will send to the 
        """
        with open(jsonfile,'r') as f:
            config = json.load(f)

            if block == "upstream":
                for elem in config["config"][0]["parsed"][0]["block"]:
                    if elem["directive"] == "upstream":
                        for each in elem["block"]:
                            # print(each["args"])
                            if each["args"].__contains__(prev_value):
                                each["args"].remove(prev_value)
                                each["args"].append(new_value)

            elif block == "server":
                # config.parsed.block[].server.block.block
                for elem in config["config"][0]["parsed"][0]["block"]:
                    if elem["directive"] == block:
                        for each in elem["block"]:
                            if "block" in each:
                                for elem in each["block"]:
                                    if (
                                        elem["directive"] == directive
                                        and elem["args"][0] == attribute
                                    ):
                                        elem["args"].remove(prev_value)
                                        elem["args"].append(new_value)
        
 
        if self.writer(conf=config, name=f"{jsonfile}"):

            # print(
            #     "Total Execution Time: {:.4f} Secounds".format(
            #         time.time() - self.start_time
            #     )
            # )

            return True
        else:
            return False


    def add_subdomain(self, domain: str, sub_name, ip, ssl: bool):
        with open("nginx-config.json") as f:
            config = json.load(f)
        catchdir = domain.replace(".", "").upper()
        sub_domain_with_ssl = [
            {
                "directive": "upstream",
                "line": 7,
                "args": [f"{sub_name}_{domain}"],
                "block": [{"directive": "server", "line": 8, "args": [f"{ip}"],}],
            },
            {
                "directive": "server",
                "line": 12,
                "args": [],
                "block": [
                    {
                        "directive": "server_name",
                        "line": 13,
                        "args": [f"{sub_name}_{domain}"],
                    },
                    {
                        "directive": "location",
                        "line": 14,
                        "args": ["/"],
                        "block": [
                            {
                                "directive": "proxy_pass",
                                "line": 15,
                                "args": [f"{sub_name}_{domain}"],
                            },
                            {
                                "directive": "proxy_next_upstream",
                                "line": 16,
                                "args": [
                                    "error",
                                    "timeout",
                                    "invalid_header",
                                    "http_500",
                                    "http_502",
                                    "http_503",
                                    "http_504",
                                ],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 17,
                                "args": ["Accept-Encoding", ""],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 18,
                                "args": ["Host", "$host"],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 19,
                                "args": ["X-Real-IP", "$remote_addr"],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 20,
                                "args": [
                                    "X-Forwarded-For",
                                    "$proxy_add_x_forwarded_for",
                                ],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 21,
                                "args": ["X-Forwarded-Proto", "$scheme",],
                            },
                            {
                                "directive": "add_header",
                                "line": 22,
                                "args": ["Front-End-Https", "on"],
                            },
                            {
                                "directive": "proxy_redirect",
                                "line": 23,
                                "args": ["off"],
                            },
                            {
                                "directive": "proxy_buffering",
                                "line": 24,
                                "args": ["on"],
                            },
                            {
                                "directive": "proxy_cache",
                                "line": 25,
                                "args": [f"{catchdir}"],
                            },
                            {
                                "directive": "proxy_cache_valid",
                                "line": 26,
                                "args": ["200", "4h"],
                            },
                            {
                                "directive": "proxy_cache_use_stale",
                                "line": 27,
                                "args": [
                                    "error",
                                    "timeout",
                                    "invalid_header",
                                    "updating",
                                    "http_500",
                                    "http_502",
                                    "http_503",
                                    "http_504",
                                ],
                            },
                        ],
                    },
                ],
            },
        ]

        sub_domain = [
            {
                "directive": "upstream",
                "line": 7,
                "args": [f"{sub_name}_{domain}"],
                "block": [{"directive": "server", "line": 8, "args": [f"{ip}"],}],
            },
            {
                "directive": "server",
                "line": 12,
                "args": [],
                "block": [
                    {
                        "directive": "server_name",
                        "line": 13,
                        "args": [f"{sub_name}_{domain}"],
                    },
                    {
                        "directive": "location",
                        "line": 14,
                        "args": ["/"],
                        "block": [
                            {
                                "directive": "proxy_pass",
                                "line": 15,
                                "args": [f"{sub_name}_{domain}"],
                            },
                            {
                                "directive": "proxy_next_upstream",
                                "line": 16,
                                "args": [
                                    "error",
                                    "timeout",
                                    "invalid_header",
                                    "http_500",
                                    "http_502",
                                    "http_503",
                                    "http_504",
                                ],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 17,
                                "args": ["Accept-Encoding", ""],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 18,
                                "args": ["Host", "$host"],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 19,
                                "args": ["X-Real-IP", "$remote_addr"],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 20,
                                "args": [
                                    "X-Forwarded-For",
                                    "$proxy_add_x_forwarded_for",
                                ],
                            },
                            {
                                "directive": "proxy_set_header",
                                "line": 21,
                                "args": ["X-Forwarded-Proto", "$scheme",],
                            },
                            {
                                "directive": "add_header",
                                "line": 22,
                                "args": ["Front-End-Https", "on"],
                            },
                            {
                                "directive": "proxy_redirect",
                                "line": 23,
                                "args": ["off"],
                            },
                            {
                                "directive": "proxy_buffering",
                                "line": 24,
                                "args": ["on"],
                            },
                            {
                                "directive": "proxy_cache",
                                "line": 25,
                                "args": [f"{catchdir}"],
                            },
                            {
                                "directive": "proxy_cache_valid",
                                "line": 26,
                                "args": ["200", "4h"],
                            },
                            {
                                "directive": "proxy_cache_use_stale",
                                "line": 27,
                                "args": [
                                    "error",
                                    "timeout",
                                    "invalid_header",
                                    "updating",
                                    "http_500",
                                    "http_502",
                                    "http_503",
                                    "http_504",
                                ],
                            },
                        ],
                    },
                    {"directive": "listen", "line": 29, "args": ["443", "ssl"],},
                    {
                        "directive": "ssl_certificate",
                        "line": 30,
                        "args": ["fullchain.pem"],
                    },
                    {
                        "directive": "ssl_certificate_key",
                        "line": 31,
                        "args": ["privkey.pem"],
                    },
                    {
                        "directive": "include",
                        "line": 32,
                        "args": ["options-ssl-nginx.conf"],
                        "includes": [1],
                    },
                    {
                        "directive": "ssl_dhparam",
                        "line": 33,
                        "args": ["ssl-dhparams.pem"],
                    },
                    {
                        "directive": "server",
                        "line": 36,
                        "args": [],
                        "block": [
                            {
                                "directive": "if",
                                "line": 37,
                                "args": ["$host", "=", f"{sub_name}.{domain}"],
                                "block": [
                                    {
                                        "directive": "return",
                                        "line": 38,
                                        "args": ["301", "https://$host$request_uri",],
                                    }
                                ],
                            },
                            {
                                "directive": "server_name",
                                "line": 41,
                                "args": [f"{sub_name}_{domain}"],
                            },
                            {"directive": "listen", "line": 42, "args": ["80"]},
                            {"directive": "return", "line": 43, "args": ["404"],},
                        ],
                    },
                ],
            },
        ]

        try:
            if ssl:
                for each in sub_domain_with_ssl:
                    config["config"][0]["parsed"][0]["block"].append(each)
            else:
                for each in sub_domain:
                    config["config"][0]["parsed"][0]["block"].append(each)
        except:
            return False
        else:
            self.writer(conf=config, name="new-nginx-config.json")
            return True

    def add_ssl(self):

        pass
        # with open('ssss.py', 'w') as f:
        #     f.write(config)

    def dev_mod(self, jsonfile: json, status: bool):
        with open(jsonfile) as f:
            config = json.load(f)
            for elem in config["config"][0]["parsed"][0]["block"]:
                if elem["directive"] == "server":
                    for directive in elem["block"]:
                        if "block" in directive:
                            for elem in directive["block"]:
                                if elem["directive"] == "proxy_cache":
                                    elem["args"] = "off"
            return config
