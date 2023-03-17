import requests
import time
from datetime import datetime

def scrape_program_urls(page):
    url = f"https://bugcrowd.com/programs.json?sort[]=promoted-desc&vdp[]=false&page[]={page}"
    r = requests.get(url)

    return r.json()


def scrape_program_target_groups(program_url):
    target_urls = []
    targets = ""

    for prog_url in program_url:
        url = f"https://bugcrowd.com{prog_url[0]}/target_groups"
        r = requests.get(url)

        try:
            targets = r.json()['groups']
        except:
            continue 

        for target in targets:
            target_urls.append([target['targets_url'], prog_url[1]])
        
    return target_urls


def scrape_program_target_tech(target_urls):
    target_tech = []
    targets = ""

    for target_url in target_urls:
        url = f"https://bugcrowd.com{target_url[0]}"
        r = requests.get(url)

        try:
            targets = r.json()['targets']
        except:
            continue

        for target in targets:
            tech_used = []
            sub_domain = target['name']
            for tech in target['target']['tags']:
                tech_used.append(tech['name'])
            target_tech.append([sub_domain, tech_used, target_url[1]])
        
    return target_tech


def main():
    total_pages = scrape_program_urls(1)['meta']['totalPages']
    program_urls = []

    for page in range(1,total_pages+1):
        programs = scrape_program_urls(page)['programs']

        for program in programs:
            prog = ""
            name = ""

            try:
                prog = program['program_url']
                name = program['name']
              
            except:
                continue

            program_urls.append([prog, name])

    target_urls = scrape_program_target_groups(program_urls)
    tech = scrape_program_target_tech(target_urls)
    
    # write content to md
    with open("bugcrowd_tech.md", "w") as f:
        f.write("# BugCrowd Tech\n")
        f.write("## Info\n")

        dt = datetime.now()
        f.write(f"Updated {dt}\n\n")
        f.write("Filtered with: sort[]=promoted-desc&vdp[]=false\n\n")
        f.write("Note: Out of scope targets are not filtered out\n\n")

        curr_site = tech[0][2]
        f.write(f"## {curr_site}\n")

        for site in tech:
            if (site[2] != curr_site):
                curr_site = site[2]
                f.write(f"## {curr_site}\n")

            f.write(f"### {site[0]}\n")
            for t in site[1]:
                f.write(f"- ```{t}```\n")
            f.write("\n\n")

if __name__ == '__main__':
    main()
