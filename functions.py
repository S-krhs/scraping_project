import asyncio
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# ---SubFunctions---

# --soup source shaper--
# soup to soup array, find_all method
def s2sArray_find_all(soup,style):
    if style["IdentifyMethod"]=="Class":
        res = soup.find_all(class_=style["Class"])
    elif style["IdentifyMethod"]=="Tag":
        res = soup.find_all(style["Tag"])
    elif style["IdentifyMethod"]=="Id":
        res = soup.find_all(id=style["Id"])
    elif style["IdentifyMethod"] in style:
        res = soup.find_all(style["Tag"], {style["IdentifyMethod"]:style[style["IdentifyMethod"]]})
    else:
        raise NameError("Unexpected IdentifyMethod Value")
    return res
    
# --soup source shaper end--


# --str data shaper--
def rank_shaper_001(param,j):
    res = j+1
    return res

def int_shaper_001(param,j):
    res=param.replace(",","")
    return res
# --str data shaper end--


# Function Selection Map
function_map={
    "rank-shaper-001":rank_shaper_001,
    "int-shaper-001":int_shaper_001
}

# ---SubFunctions end---


# Select renderer and Get HTML
async def getHTML(URL):
    asession = AsyncHTMLSession()
    res = await asession.get(URL)
    if res is None:
        raise ValueError("RendererError occurred")
    return res

# Shaping HTML data
def shaping(page_data,format):
    # BeautifulSoup
    soup = BeautifulSoup(page_data.html.html,"lxml")
    if soup is None:
        raise ValueError("Soup is None")
    
    # Extract main containts
    style_main = format["Main"]
    soup_main = s2sArray_find_all(soup,style_main)[style_main["Num"]]
    if soup_main is None:
        raise ValueError("Main containts is None. Please check IdentifyMethod and Class value in Format-Main.")
    
    # Extract containts per anime title
    style_item = format["Items"]
    soup_items_array = s2sArray_find_all(soup_main,style_item)
    if soup_items_array is None:
        raise ValueError("Animes containts is None. Please check IdentifyMethod and Class value in Format-Animes.")
    
    # Create dataframe
    columns=["Date","Datetime"]
    for feature in format["Features"]:
        columns.append(feature["FeatureName"])
    df = pd.DataFrame(columns=columns)
    
    # Date and Datetime in Asia/Tokyo
    DIFF_JST_FROM_UTC = 9
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    today = now.date()

    # Imput data into dataframe
    for i,soup_item in enumerate(soup_items_array):
        # Inisialize add_list
        add_list=[[today,now]]
    
        # Shaping data
        for style_feature in format["Features"]:
            
            soup_param=s2sArray_find_all(soup_item, style_feature)[style_feature["Num"]]
            if soup_param is None:
                print(feature["FeatureName"]," containts is None. Please check IdentifyMethod and Class value in Format-Feature.")
                add_list[0].append("")
                continue
            
            # Extract text
            param = soup_param.text
            # Shaping if extra processes are needed
            if feature["ShapingFunction"] in ["","default"]:
                pass
            else:
                param = function_map[feature["ShapingFunction"]](param,i)
            if param is None:
                raise ValueError(feature["FeatureName"]," containts is None. Please check IdentifyMethod, Class, ShapingFunction value in Format-Feature.")
                
            add_list[0].append(param)

        # Merge add_list to dataframe
        df_add = pd.DataFrame(data=add_list,columns=columns)
        df = pd.concat([df, df_add], ignore_index=True, axis=0)
    
    return df


# Main function
def scrape(page):
    # Start Scraping
    print(page)
    format = page["Format"]
    
    # Get HTML
    print("HTML request started...")
    loop = asyncio.new_event_loop()
    page_data = loop.run_until_complete(getHTML(format["URL"]))
    page_data.raise_for_status()
    print("HTML data retrieved successfully.")
            
    # Create DataFrame and Input Data"
    df = shaping(page_data, format)
    print(df)
    print("Data shaping completed successfully.")
    
    # Output Data
    res = df.to_json(orient='records')
    print("Data exported successfully.\n")

    return res

