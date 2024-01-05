# this is a separate module because of circular imports

class TwitterUser:
    link: str  # for reference
    bio: str
    following: int
    followers: int
    location: str
    website: str

    def __init__(self, link, bio, following, followers, location, website):
        self.link = link
        self.bio = bio
        self.following = following
        self.followers = followers
        self.location = location
        self.website = website
