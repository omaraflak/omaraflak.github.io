import metadata
import templates
import datetime


def _format_date(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")


def make_sitemap_entry(meta: metadata.Metadata, filename: str) -> str:
    date = meta.updated_date or meta.date
    xml = templates.SITEMAP_ENTRY
    xml = xml.replace("{{date}}", _format_date(date))
    xml = xml.replace("{{filename}}", filename)
    return xml


def make_sitemap(entries: str) -> str:
    xml = templates.SITEMAP
    xml = xml.replace("{{entries}}", entries)
    return xml
