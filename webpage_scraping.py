import requests

def title(url):
    dummy_text = url.text
    start = dummy_text.find('<title>') + len("<title>")
    end = dummy_text.find("</title>")
    print(dummy_text[start:end])



def body_content(url):
    dummy_text = url.text    
    content = " "
    start = False
    space = True
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
    prev = ""
    for line in content:
        if line.strip()=="":
            modified += line.strip()
        else:
            modified += "\n"+line.strip()
        prev = line
        
    print(modified)


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
    Links = body_link(url)
    print("Title:", page_title)
    print("\nBody of the page : ", Page_body)
    print("\nLinks availabe on webpage: ", Links)
    

if __name__=="__main__":
    site = input("Enter url : ")
    url = requests.get(site)
    main(url)