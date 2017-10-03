import re


def platform_check(s, ua):
    platform = ua.platform
    agent_string = ua.string
    if (platform == 'android' or platform == 'iphone') or (re.search('iPad', agent_string)) or (
            platform == 'windows' and re.search('Windows Phone OS', agent_string)):
        s['mobile'] = True
    else:
        s['mobile'] = False
    return s


if __name__ == '__main__':
    pass
