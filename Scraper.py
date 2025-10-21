from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Chrome
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://coinmarketcap.com/")

# Wait for table body
tbody = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "tbody"))
)

rows = tbody.find_elements(By.TAG_NAME, "tr")
data = []

for row in rows[:10]:  # Top 10 coins
    tds = row.find_elements(By.TAG_NAME, "td")
    try:
        name = tds[2].find_element(By.TAG_NAME, "p").text
        symbol = tds[2].find_elements(By.TAG_NAME, "p")[1].text
        price = tds[3].text
        change_24h = tds[6].text
        market_cap = tds[7].text
        logo_url = tds[2].find_element(By.TAG_NAME, "img").get_attribute("src")

        data.append([name, symbol, price, change_24h, market_cap, logo_url])
    except Exception as e:
        print("Error in row:", e)

driver.quit()

df = pd.DataFrame(data, columns=['Name', 'Symbol', 'Price', '24h Change', 'Market Cap', 'Logo URL'])
df.to_csv('Top10_Crypto.csv', index=False)
df.to_excel('Top10_Crypto.xlsx', index=False)


print(df)
print("Top 10 crypto data saved to CSV & Excel")