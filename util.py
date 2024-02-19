import csv
from io import StringIO
from selenium.webdriver.common.by import By

def get_page_elements_table(driver):
    body_element = driver.find_element(By.XPATH,"//body")
    elements_in_body = body_element.find_elements(By.XPATH,".//*")
    rows = []
    headers = ['INDEX','TAG' ,'INPUT TYPE', 'ID','NAME','TEXT REFERENCE TO BODY TEXT START INDEX']
    global_class_names = set()
    # class_names_set = {class_name for index, element in enumerate(elements_in_body) for class_name in element.get_attribute("class").split()}
    body_text = body_element.text
    for index, element in enumerate(elements_in_body):
        col = []
        tag_name = element.tag_name
        if tag_name not in ["button","input","form","a"]:
            continue 
        col.append(index)  # Index
        col.append(tag_name)  # Type
        col.append(element.get_attribute('type'))
        col.append(element.get_attribute("id")) 
        # Id
        #col.append(element.get_attribute("class"))  # Class
        
        # Data
        attributes = element.get_property("attributes")
        data = ''
        for attr in attributes:
            attr_name = attr['name']
            attr_value = attr['value']
            if attr_name.startswith('data'):
                data += f"{attr_name[4:]}:{attr_value} "  # Append data attribute
        #col.append(data.strip())  # Append data string
        
        col.append(element.get_attribute("name"))  # Name
        col.append(body_text.find(element.text))  # Value
        
        rows.append(col)
    
    # Write table data to CSV-formatted string
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    
    return body_text, output.getvalue()

def get_page_elements_v2(driver):
    rows = []
    index = 0
    def visit_children(node):
        nonlocal index
        # Get the child elements of the current node
        child_elements = node.find_elements(By.XPATH,"./*")
        indexed_elements = []
        # Process each child element
        for element in child_elements:
            col = []
            is_text_node = element.get_attribute('nodeType') == "3"
            tag_name = element.tag_name

            if is_text_node:
                col.append(index)  # Index
                col.append('text_node')  # Type
                col.append('')
                col.append('') 
                col.append(element.text)
                index += 1
                indexed_elements.append(element)
                continue
            
            if tag_name  in ["script","svg","img"]:
                continue 
            # Do something with the child element (e.g., print its tag name)
            col.append(index)  # Index
            col.append(tag_name if not is_text_node else 'text_node')  # Type
            col.append(element.get_attribute('type'))
            col.append(element.get_attribute("id")) 
            col.append(element.text)
            rows.append(col)
            
            index += 1
            indexed_elements.append(element)
            # Recursively visit the children of the child element
            visit_children(element)
    
    body_element = driver.find_element(By.XPATH,"//body")
    visit_children(body_element)
    return rows

# Get the body element of the DOM tree

def get_all_class_names_unique(driver):
    body_element = driver.find_element(By.XPATH,"//body")
    elements_in_body = body_element.find_elements(By.XPATH,".//*")
    return  {class_name for index, element in enumerate(elements_in_body) for class_name in element.get_attribute("class").split()}
