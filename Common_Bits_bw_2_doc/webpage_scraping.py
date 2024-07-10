import requests

def title(url):
    dummy_text = url.text
    start = dummy_text.find('<title>') + len("<title>")
    end = dummy_text.find("</title>")
    return (dummy_text[start:end])

def body_content(url):
    dummy_text = url.text    
    content = " "
    start = False
    start = dummy_text.find("<script")
    end = dummy_text.find("</script>")
    
    while start!=-1:
        dummy_text = dummy_text[:start] + dummy_text[end+8:]
        start = dummy_text.find("<script")
        end = dummy_text.find("</script>")    
        
    for line in dummy_text:
        
        if line == "<":
            start = False
        elif line == ">":
            start = True
        elif start:
            content += line

    content = content.split("\n")
    modified = ""
    for line in content:
        if line.strip()=="":
            modified += line.strip()
        else:
            modified += "\n"+line.strip()
        
    return (modified)

def script_style_rmv(dummy_text):
    script_S = dummy_text.find("<script")
    script_E = dummy_text.find("</script>")
    
    while script_S!=-1:
        dummy_text = dummy_text[:script_S] + dummy_text[script_E+8:]
        script_S = dummy_text.find("<script")
        script_E = dummy_text.find("</script>") 

    style_S = dummy_text.find("<style")
    style_E = dummy_text.find("</style>")
    
    while style_S!=-1:
        dummy_text = dummy_text[:style_S] + dummy_text[style_E+7:]
        style_S = dummy_text.find("<style")
        style_E = dummy_text.find("</style>")     

    while "&#" in dummy_text:
        start = dummy_text.find("&#")
        end = dummy_text.find(";", start)
        if start != -1 and end != -1:
            dummy_text = dummy_text[:start] + dummy_text[end + 1:]
        else:
            break

    return dummy_text 



def body_link(url):
    dummy_text = url.text
    text_list = dummy_text.split("\n")  
    lst = []
    for line in text_list:
        if "https" in line:
            start = line.find("https")
            end = line[start:].find('"')
            link = line[start:start + end]
            lst.append(link)
    
    for i in lst:
        print(i)
    



def main(url):
    
    page_title = title(url)
    Page_body = body_content(url)
    # print("Title:", page_title)
    print("\nBody of the page : ", Page_body)
    # print("\nLinks availabe on webpage: ", body_link(url))


# if __name__=="__main__":
    # site = input("Enter url : ") 
# url = requests.get("https://en.wikipedia.org/wiki/Machine_learning")
# url = "https://sitare.org/"
# print(body_content(url))



