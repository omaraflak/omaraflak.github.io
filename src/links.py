import os
import dataclasses
import dataclasses_json
import link_preview.link_preview


@dataclasses.dataclass
class Link(dataclasses_json.DataClassJsonMixin):
    url: str
    title: str
    description: str
    website: str


@dataclasses.dataclass
class Links(dataclasses_json.DataClassJsonMixin):
    links: dict[str, Link] = dataclasses.field(default_factory=dict)


class LinkPreview:
    def __init__(self, cache_path: str = ".cache/links.json"):
        self.cache_path = cache_path
        self.cache = Links()
        try:
            with open(cache_path, "r") as file:
                self.cache = Links.from_json(file.read())
        except:
            pass

    def get_link_preview(self, url: str) -> Link | None:
        if url in self.cache.links:
            return self.cache.links[url]

        try:
            preview = link_preview.link_preview.generate_dict(url)
            link = Link(
                url,
                preview["title"],
                preview["description"],
                preview["website"]
            )
            self._add_to_cache(link)
            return link
        except:
            return None

    def _add_to_cache(self, link: Link):
        try:
            self.cache.links[link.url] = link
            dir = os.path.dirname(self.cache_path)
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(self.cache_path, "w") as file:
                file.write(self.cache.to_json(indent=2))
        except:
            pass
