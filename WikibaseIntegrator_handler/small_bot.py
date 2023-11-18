from wikibaseintegrator import wbi_core, wbi_login, wbi_datatype
from wikibase_config import configure_wb

configure_wb()
#The new password to log in with Admin@small_bot is 2c7r9a81orn77qfa3mtuke6thpta4ekc. Please record this for future reference.
#(For old bots which require the login name to be the same as the eventual username, you can also use Admin as username and small_bot@2c7r9a81orn77qfa3mtuke6thpta4ekc as password.) 

# login object
login_instance = wbi_login.Login(user='Admin@small_bot', pwd='2c7r9a81orn77qfa3mtuke6thpta4ekc')

# data type object, e.g. for a NCBI gene entrez ID
entrez_gene_id = wbi_datatype.String(value='Q3', prop_nr='P1')

# data goes into a list, because many data objects can be provided to
data = [entrez_gene_id]

# Search for and then edit/create new item
wd_item = wbi_core.ItemEngine(data=data)
wd_item.write(login_instance)