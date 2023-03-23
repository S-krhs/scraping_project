import json
import traceback
import functions as fn

def main(request):
    # Scraping with Exception Handling
    try: 
        print(request)
        page = request.get_json()
        
        # Get result
        res = fn.scrape(page)

    except Exception as e:
        print("Error occurred:", e)
        print("StackTrace:", traceback.format_exc())
        return {}

    return res