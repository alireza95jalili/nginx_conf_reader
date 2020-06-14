import json


class nginx:
    def __init__(self):
        pass

    def conf_reader2(self):
        with open("nginx-config-2.txt") as f:
            lines = f.readlines()
            begining_of_server = list()
            ending_of_server = list()
            begining_of_upstream = list()
            ending_of_upstream = list()

            for n, line in enumerate(lines, 1):
                line = line.strip()

                if line == "#begining_of_server":
                    begining_of_server.append(n)
                if line == "#ending_of_server":
                    ending_of_server.append(n)
                if line == "#begining_of_upstream":
                    begining_of_upstream.append(n)
                if line == "#ending_of_upstream":
                    ending_of_upstream.append(n)

            server_blocks = list(zip(begining_of_server, ending_of_server))
            upstream_blocks = list(zip(begining_of_upstream, ending_of_upstream))
            del (
                begining_of_server,
                ending_of_server,
                begining_of_upstream,
                ending_of_upstream,
            )

            print(server_blocks)
            print(upstream_blocks)


test = nginx()
test.conf_reader2()

# serverBlock  = []

# serverBlock[(0,0), (1,25)]
