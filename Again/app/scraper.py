import datetime
from requests_html import HTMLSession
from app.database import SessionLocal
from app.crud import create_news
from app.schemas import NewsCreate
from app.schemas import News
import sys
import os

# Ensure UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')


def single_news_scraper(url: str):
    session = HTMLSession()
    try:
        response = session.get(url)
        # response.html.render()  # This will download Chromium if not found

        #publisher_website = url.split('/')[2]
        #publisher = publisher_website.split('.')[-2]
        title_element = response.html.find('h2', first=True)
        title = title_element.text if title_element else "Title not found"
        reporter = response.html.find('.contributor-name', first=True).text
        datetime_element = response.html.find('time', first=True)
        news_datetime = datetime_element.attrs['datetime']
        category_element = response.html.find('div', first=True)
        category = category_element.find('a', first=True).text if category_element else "Category not found"
        reporter_element = response.html.find('.contributor-name', first=True)
        reporter = reporter_element.text if reporter_element else "Reporter not found"

        content = '\n'.join([p.text for p in response.html.find('p')])
        img_tags = response.html.find('img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]
        news_datetime = datetime.datetime.now()
        news_body_elements = response.html.find('p')
        body = "\n".join([p.text for p in news_body_elements]) if news_body_elements else "News body not found"

        print(f"Scraped news from {url}")
        print(f"Title: {title}")
        print(f"Reporter: {reporter}")
        print(f"Date: {news_datetime}")
        print(f"Category: {category}")
        print(f"Images: {images}")


        return NewsCreate(
            #publisher_website=publisher_website,
            #news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=content,
            images=images,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def scrape_and_store_news(url: str, db: SessionLocal):
    db = SessionLocal()
    news_data = single_news_scraper(url)
    print(news_data)
    inserted_news = ""
    if news_data:
        # print(news_data)
        inserted_news = create_news(db=db, news=news_data)
    db.close()

    return inserted_news