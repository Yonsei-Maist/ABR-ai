from ip2geotools.databases.noncommercial import DbIpCity


class IPLocation:
    @staticmethod
    def get_region(ip):
        if ip == "127.0.0.1":
            return "local"
        response = DbIpCity.get(ip, api_key='free')

        return "{}, {}, {}".format(response.city, response.region, response.country)
