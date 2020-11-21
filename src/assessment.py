import csv

def generate_description(description_text):
    if description_text.strip() == "":
        return ""
    else:
        return f"""\n\t\t<h1>Description</h1>
        \t<span>{description_text}</span>\n
        """.rstrip()

def generate_ul_contents(domains):
    ul_contents = ""
    for d in domains:
        if d.strip() != "":
            ul_contents += f"\n\t\t\t\t<li>{d}</li>"
    return ul_contents
        
def generate_html_content(title, description, ul_contents):

    content = f"""
    <html>
    \t<head>
        \t<title>{title}</title>
    \t</head>
    \t<body>{description}
        \t<h1>Domains</h1>
        \t\t<ul>{ul_contents}
        \t\t</ul>
    \t</body>\n</html>
    """

    return content

def parse_csv():
    with open("../data/output_assessment.csv", "w") as f:
        f.write("assessment_id,html\n")

    with open("../data/assessment.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = row[0]
            title = row[1]
            description_text = row[2]
            description = generate_description(description_text)
            domains = [row[3], row[4], row[5]]

            ul_contents = generate_ul_contents(domains)
            content = generate_html_content(title, description, ul_contents)
            # print(content)
            # print("="*23)
            with open("../data/output_assessment.csv", "a+") as f:
	            f.write(",".join([id, f"\"{content.strip()}\"\n"]))


parse_csv()
