import requests
from datetime import datetime


def scrape_program_urls(page):
    url = f"https://bugcrowd.com/engagements.json?category=bug_bounty&page={page}&sort_by=promoted&sort_direction=desc"
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
            print(target)
            tech_used = []
            sub_domain = target['name']
            for tech in target['target']['tags']:
                tech_used.append(tech['name'])
            target_tech.append([sub_domain, tech_used, target_url[1]])
        
    return target_tech


def main():
    program_urls = []
    page = 1

    while True:
        programs = scrape_program_urls(page)['engagements']
        page += 1
        if len(programs) == 0:
            break

        for program in programs:
            prog = ""
            name = ""

            try:
                prog = program['briefUrl']
                name = program['name']
              
            except:
                continue

            program_urls.append([prog, name])

    target_urls = scrape_program_target_groups(program_urls)
    tech = scrape_program_target_tech(target_urls)
    
    # write content to markdown file
    with open("bugcrowd_tech.md", "w") as f:
        f.write("# BugCrowd Tech\n")
        f.write("## Info\n")

        dt = datetime.now()
        f.write(f"Updated {dt}\n\n")
        f.write("Filtered with: sort_by=promoted&sort_direction=desc\n\n")
        f.write("Note: Out of scope targets are not filtered out\n\n")

        current_site = tech[0][2]
        f.write(f"## {current_site}\n")

        for site in tech:
            if (site[2] != current_site):
                current_site = site[2]
                f.write(f"## {current_site}\n")

            f.write(f"### {site[0]}\n")
            for t in site[1]:
                f.write(f"- ```{t}```\n")
            f.write("\n\n")


if __name__ == '__main__':
    main()
