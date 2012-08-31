##the form the index will take
indexForm = r'<%d,%d,%d,%d>';

#site_limit = 2000;
site_limit = 1;

reset_site = 'http://localhost:8080/LiRa/';
#reset_site = 'http://localhost:8080/';

#development_status = "development";
development_status = "test";
#development_status = "production";

### LOGGING ###
logging_template = "C:\UUMMUU_Code\Logs\%s";

ThreadLimit = 10;

sql_commands = {'getDomainCountByUrl':"SELECT url, pages_crawled from sites_domains where url = '%s';",
                        'getDomainCount': "SELECT url, pages_crawled FROM sites_domains order by pages_crawled limit 1;",
                        };
