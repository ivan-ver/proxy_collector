import os


class Util:
    @staticmethod
    def read_lua_script():
        with open(os.getcwd() + "/proxy_collector_scrapy/execute.lua") as file:
            r = file.read()
            print()
            return r
