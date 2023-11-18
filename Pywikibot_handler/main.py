import pywikibot

site = pywikibot.Site('147.231.55.155:en')
repo = site.data_repository()  # the Wikibase repository for given site
page = repo.page_from_repository('Q1')  # create a local page for the given item
item = pywikibot.ItemPage(repo, 'Q1')  # a repository item
data = item.get()  # get all item data from repository for this item