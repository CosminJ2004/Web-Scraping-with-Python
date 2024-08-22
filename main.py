from bs4 import BeautifulSoup
import requests
import time
def find_jobs():
    html_text=requests.get('https://www.bestjobs.eu/ro/locuri-de-munca/inginer').text
    soup =BeautifulSoup(html_text, 'lxml')
    print("Write a minimum salary expectation: ")
    sum_input = input('>').strip()
    try:
        sum_input = int(sum_input)
    except ValueError:
        print("Please enter a valid number for the salary.")
        exit()

    print(f'Filtering out all jobs under {sum_input}')

    jobs= soup.find_all('div', class_="col mb-5 js-card-item card-item job-card")
    for index, job in enumerate(jobs):
        company_name = job.find('div', class_="h6 text-muted text-truncate py-2").get_text(strip=True)
        company_name = company_name.replace('Angajeaza Premium Talent', '').replace('Raspunde rapid', '').strip()
        # Extract the link from the "card-body p-4" class
        more_info_div = job.find('div', class_="card-body p-4")
        more_info_link = more_info_div.find('a')['href'] if more_info_div and more_info_div.find('a') else "No link available"
        # Clean location by removing extra spaces and newlines
        location = job.find('div', class_="d-flex min-width-3").get_text(strip=True)
    # Safely check for the salary div
        salary_div = job.find('div', class_="text-nowrap")
        if salary_div:
            salary = salary_div.text.strip()
            salary= salary.split(' - ')
            min_salary=int(salary[0])
            if min_salary>=sum_input:
                with open(f'posts/{index}.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Company: {company_name}\n")
                    f.write(f"Location: {location}\n")
                    f.write(f"Salary: {salary}\n")
                    f.write(f'More info link:{more_info_link}\n')
                    f.write("-" * 30)
                print(f'File saved: {index}')

            
        else:
            salary = "Not specified"
            with open(f'posts/{index}.txt', 'w', encoding='utf-8') as f:
                f.write(f"Company: {company_name}\n")
                f.write(f"Location: {location}\n")
                f.write(f"Salary: {salary}\n")
                f.write(f'More info link:{more_info_link}\n')
                f.write("-" * 30)
            print(f'File saved: {index}')
        print('')
        

if __name__=='__main__':
    while True:
        find_jobs()
        time_wait=10
        print(f'Waiting {time_wait} minutes')
        time.sleep(time_wait*60)


        
    
    