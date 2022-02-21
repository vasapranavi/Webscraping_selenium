from jobs_web_scrapping import start_driver, get_html, get_links
import validators
import time


def read_inputs():
    field = input('Please enter field:')
    location = input('Please enter location in UK:')
    return field, location


def get_query(field, location):
    field = '+'.join(field.split())
    location = '+'.join(location.split())
    return 'https://www.google.com/search?q=' + field + '+jobs+in+' + location


def write_to_file(final_url):
    with open('urls.txt', 'w') as f:
        for url in final_url:
            f.write(url)
            f.write('\n')


def main():
    start_time = time.time()
    field, location = read_inputs()
    query = get_query(field, location)
    driver = start_driver()
    html = get_html(driver, query)
    links = get_links(html)
    links_from_google = []
    for link in links:
        x = str(link.get("href"))
        if validators.url(x) and ('google.com' not in x):
            links_from_google.append(x)
    indeed_links = []
    for link in links_from_google:
        if str(link).find('https://uk.indeed.com/') == 0:
            indeed_links.append(link)
    indeed_a_ele = []
    for link in indeed_links:
        indeed_a_ele.append(get_links(get_html(driver, link)))
    job_ids = []
    for element in indeed_a_ele:
        for ele in element:
            try:
                if ele.get("data-jk") is not None:
                    job_ids.append(ele.get("data-jk"))
            finally:
                continue
    job_pages_links = []
    for job_id in job_ids:
        query_part = 'https://uk.indeed.com/viewjob?jk='+job_id
        job_pages_links.append(get_links(get_html(driver, query_part)))
    company_sites = []
    for job_page in job_pages_links:
        try:
            for a_ele in job_page:
                try:
                    if a_ele.text.strip().find('Apply on company site') != -1:
                        company_sites.append(a_ele.get("href"))
                finally:
                    continue
        finally:
            continue
    final_url = []
    for company_site in company_sites:
        driver.get(company_site)
        final_url.append(driver.current_url)
    write_to_file(final_url)
    print('Time taken to fetch urls:', time.time()-start_time)


if __name__ == '__main__':
    main()
