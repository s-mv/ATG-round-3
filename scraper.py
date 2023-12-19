
class TwitterUser():
    bio : str
    following, followers : int
    location : str
    website : str

    def __init__(self, bio, following, followers, location, website):
        self.bio = bio
        self.following = following
        self.followers = followers
        self.location = location
        self.website = website



def scrape_twitter_links(links: [str]) -> [TwitterUser]:
    # TODO
    return {}


def get_twitter_user_object(link: str) -> TwitterUser:
    # TODO: return real information
    return {}
